#!/usr/bin/env python3
import os
import time
import requests
import urllib.parse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from ddtrace import tracer
import logging

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

    # Get current IP address
    pip = requests.get("https://checkip.amazonaws.com").text.strip()

    # Post data to Datadog API
    dd_api_key = os.getenv("DD_API_KEY")
    dd_app_key = os.getenv("DD_APP_KEY")
    office_ip = "pip:154.18.30.1* OR pip:209.249.214.17*"

    data = {
        "series": [
            {
             "metric": "work",
             "type": 1,
             "points": [
                 {
                  "timestamp": cur_timestamp,
                  "value": 1
                  }
                  ],
             "tags": [
                 f"pip:{pip}"
                 ]
                 }
                 ]
                 }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": dd_api_key
        }

    response = requests.post("https://api.datadoghq.com/api/v2/series", headers=headers, json=data)

    try:
        # Calculate the start and end timestamps for the current month
        first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        from_timestamp = int(first_day_of_month.timestamp())
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        to_timestamp = int(last_day_of_month.timestamp())
        log.debug(f"from: {from_timestamp}")
        log.debug(f"to: {to_timestamp}")

        # Define queries
        query_office = "count_not_null(sum:work{"+office_ip+"}.as_count().rollup(daily, 'Asia/Tokyo'))"
        query_home = "count_not_null(cutoff_min(sum:work{NOT ("+office_ip+")}.as_count().rollup(daily, 'Asia/Tokyo'), 20))"

        encoded_query_office = urllib.parse.quote(query_office)
        encoded_query_home = urllib.parse.quote(query_home)

        # Query Datadog API for office days
        response_office = requests.get(
            f"https://api.datadoghq.com/api/v1/query?from={from_timestamp}&to={to_timestamp}&query={encoded_query_office}",
            headers={
                "Accept": "application/json",
                "DD-API-KEY": dd_api_key,
                "DD-APPLICATION-KEY": dd_app_key
                }
                ).json()
        log.debug("response_office: "+str(response_office))

        # Query Datadog API for home days
        response_home = requests.get(
            f"https://api.datadoghq.com/api/v1/query?from={from_timestamp}&to={to_timestamp}&query={encoded_query_home}",
            headers={
                "Accept": "application/json",
                "DD-API-KEY": dd_api_key,
                "DD-APPLICATION-KEY": dd_app_key
                }
                ).json()
        log.debug("response_home: "+str(response_home))

        days_home = 0
        days_office = 0

        # Calculate office days
        for office_point in response_office['series'][0]['pointlist']:
            office_timestamp = office_point[0]
            office_value = office_point[1]

            for home_point in response_home['series'][0]['pointlist']:
                home_timestamp = home_point[0]
                home_value = home_point[1]

                if office_timestamp == home_timestamp:
                    if office_value > 0 and home_value > 0:
                        days_home -= 1
                        log.debug(f"{home_timestamp}: --")
                    break

            if office_value > 0:
                days_office += 1

        # Calculate home days
        for home_point in response_home['series'][0]['pointlist']:
            home_value = home_point[1]

            if home_value > 0:
                days_home += 1

        log.debug(f"Days office: {days_office}")
        log.debug(f"Days home (adjusted): {days_home}")

        # Calculate ratio
        if (days_home + days_office) == 0:
            ratio = 100
        else:
            ratio = round(days_office / (days_home + days_office) * 100, 1)
            log.debug(f"Ratio: {ratio}")

            # Post ratio data to Datadog API
            data = {
                "series": [
                    {
                     "metric": "office_percent",
                     "type": 3,
                     "points": [
                         {
                          "timestamp": cur_timestamp,
                          "value": ratio
                          }
                          ]
                          }
                          ]
                          }

            response = requests.post("https://api.datadoghq.com/api/v2/series", headers=headers, json=data)
    except Exception as e:
        log.info(f"Exception: {e}")

main()
