#!/bin/bash

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
dir=""
text="$(pbpaste)"
dir=""
if [[ $(echo "$text" | wc -l) -gt 1 ]];then
    case_desc="$(echo "$text" | gsed -n '1p')"
    case_num="$(echo "$text" | gsed -n '2p' | perl -pe 's/.*?([0-9]+).*?/$1/g')"
    if [[ ! $case_num =~ ^[0-9]+$ ]];then
        exit
    fi
    combined="${case_num} ${case_desc}"
    cleaned=$(echo "$combined" | gsed 's/[#\/:]//g')
    dir="${HOME}/Downloads/${cleaned}"
    if [[ ! -d $dir ]] && [[ $case_num =~ ^[0-9]+$ ]];then
        mkdir -p "$dir"
    fi
else
    case_num=$(echo "$text" | gsed -n '1p' | perl -pe 's/.*?([0-9]+).*?/$1/g')
    if [[ ! $case_num =~ ^[0-9]+$ ]];then
        exit
    fi
    dir=$(ls -d "${HOME}/Downloads/${case_num}"*)
fi
if [[ -n "$dir" ]];then
    echo "cd '$dir'" | pbcopy
    open "$dir"
fi
exit
