#!/bin/bash -x

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title zd
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🤖

# Documentation:
# @raycast.description Open Zendesk Directory
# @raycast.author Masafumi Kashiwagi

# クリップボードの内容を読み込む
text="$(pbpaste)"
if [[ $(echo "$text" | wc -l) -gt 1 ]];then
    line1="$(echo "$text" | gsed -n '1p')"
    line2="$(echo "$text" | gsed -n '2p')"
    combined="$line2 $line1"
    cleaned=$(echo "$combined" | gsed 's/[[:punct:]]//g')
    dir="${HOME}/Downloads/${cleaned}"
    if [[ ! -d $dir ]];then
        mkdir -p "$dir"
    fi
    echo "cd '$dir'" | pbcopy
    open "${HOME}/Downloads/${line1}"*
else
    line1=$(echo "$text" | gsed -n '1p' | perl -pe 's/.*?([0-9]+).*?/$1/g')
    open https://datadog.zendesk.com/agent/tickets/${line1}
    open "${HOME}/Downloads/${line1}"*
    #cd "${HOME}/Downloads/${line1}"* && code .
fi
