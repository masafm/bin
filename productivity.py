#!/usr/bin/env python3
import os
import requests
import time
import subprocess
import logging
from ddtrace import tracer

def get_logger():
    # Define a custom formatter that uses UTC
    class UTCFormatter(logging.Formatter):
        converter = time.gmtime  # Set the time conversion to UTC

    FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
              '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
              '- %(message)s')

    # Apply the custom formatter to the logging configuration
    logging.basicConfig(format=FORMAT)
    logging.getLogger().handlers[0].setFormatter(UTCFormatter(FORMAT))

    log = logging.getLogger(__name__)
    log.level = logging.DEBUG
    return log

log = get_logger()

@tracer.wrap(resource="source_script")
def source_script(script_path):
    # ファイルの存在を確認
    expanded_path = os.path.expanduser(script_path)
    if os.path.exists(expanded_path):
        # シェルスクリプトをサブシェルで実行し、環境変数をキャプチャ
        command = f"source {expanded_path} && env"
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, executable='/bin/zsh')
        for line in proc.stdout:
            # 各行を分割して環境変数を取得
            (key, _, value) = line.decode('utf-8').partition("=")
            os.environ[key] = value.strip()
        proc.communicate()
        log.info(f"Environment variables sourced from {script_path}")

@tracer.wrap(resource="main")
def main():    
    # Check if the profile script exists and source it
    source_script('~/src/masa-tools/profile-dd.sh')

    # Get current timestamp
    cur_timestamp = int(time.time())

    url = os.getenv("METABASE_URL")

    # 環境変数からクッキーを取得
    cookie = os.getenv("METABASE_COOKIE")
    
    headers = {
        "accept": "application/json",
        "accept-language": "ja,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "cookie": cookie,
        "pragma": "no-cache",
        }

    data = {
        "parameters": "[]"
    }

    response = requests.post(url, headers=headers, data=data)
    json_data=response.json()
    log.debug("metabase_response: "+str(json_data))
    
    # Post data to Datadog API
    dd_api_key = os.getenv("DD_API_KEY")
    dd_app_key = os.getenv("DD_APP_KEY")

    data = {"series": []}
    for person_data in json_data:
        name = person_data["Name"]
        zendesk_id = person_data["Zendesk ID"]
        productivity = person_data.get("Productivity")
        productivity_weighted = person_data.get("Weighted Productivity")

        # ProductivityがNoneの場合はスキップ
        if productivity is None:
            continue
    
        # Datadogに送信するデータの作成
        data["series"].append(
            {
             "metric": "productivity",
             "type": 3,
             "points": [
                 {
                  "timestamp": cur_timestamp,
                  "value": float(productivity)
                  },
                  ],
             "tags": [f"name:{name}",f"zendesk_id:{zendesk_id}"]
             }
        )
        data["series"].append(
            {
             "metric": "productivity.weighted",
             "type": 3,
             "points": [
                 {
                  "timestamp": cur_timestamp,
                  "value": float(productivity_weighted)
                  },
                  ],
             "tags": [f"name:{name}",f"zendesk_id:{zendesk_id}"]
             }
        )
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": dd_api_key
        }

    # DatadogにPOSTリクエストを送信
    response = requests.post("https://api.datadoghq.com/api/v2/series", headers=headers, json=data)

    # レスポンスを確認
    if response.status_code == 202:
        log.info(f"Successfully sent metrics")
    else:
        log.error(f"Failed to send metrics. Response: {response.text}")

main()
