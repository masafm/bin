#!/bin/bash
text="$(cat)"
dir=""
if [[ $(echo "$text" | wc -l) -gt 1 ]];then
    case_desc="$(echo "$text" | /opt/homebrew/bin/gsed -n '1p')"
    case_num="$(echo "$text" | /opt/homebrew/bin/gsed -n '2p' | perl -pe 's/.*?([0-9]+).*?/$1/g')"
    if [[ ! $case_num =~ ^[0-9]+$ ]];then
        exit
    fi
    combined="${case_num} ${case_desc}"
    cleaned=$(echo "$combined" | /opt/homebrew/bin/gsed 's/[#\/:]//g')
    dir="${HOME}/Downloads/${cleaned}"
    if [[ ! -d $dir ]] && [[ $case_num =~ ^[0-9]+$ ]];then
        mkdir -p "$dir"
    fi
else
    case_num=$(echo "$text" | /opt/homebrew/bin/gsed -n '1p' | perl -pe 's/.*?([0-9]+).*?/$1/g')
    if [[ ! $case_num =~ ^[0-9]+$ ]];then
        exit
    fi
    dir=$(ls -d "${HOME}/Downloads/${case_num}"*)
fi
if [[ -n "$dir" ]];then
    echo "cd '$dir'" | /opt/homebrew/bin/gsed -z -e "s/\n//" | pbcopy
    open "$dir"
fi
exit
