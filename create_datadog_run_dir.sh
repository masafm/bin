#!/bin/bash

export PATH="/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH"

# /var/run/datadog ディレクトリを作成
mkdir -p /var/run/datadog

# mkashi ユーザーの所有に設定
chown mkashi:staff /var/run/datadog

# パーミッションを適切に設定
chmod 755 /var/run/datadog
