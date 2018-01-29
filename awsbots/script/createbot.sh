#!/bin/bash

if [ $# -ne 1 ]; then
    echo $0: usage: createbot name filename
    exit 1
fi

name=$1
file=$2

aws lex-models put-bot \
    --region eu-west-1 \
    --name $name \
    --cli-input-json file://$file
