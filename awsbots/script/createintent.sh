#!/bin/bash


intentName=$1
accountID="2638-9361-4267"
fileName=$2
lambdaName=$3

aws lex-models put-intent \
   --region eu-west-1 \
   --name $intentName \
   --cli-input-json file://$fileName


aws lambda add-permission \
    --region eu-west-1 \
    --function-name $lambdaName \
    --statement-id LibbyStarted \
    --action lambda:InvokeFunction \
    --principal lex.amazonaws.com \
    --source-arn "arn:aws:lex:eu-west-1:$accountID:intent:$intentName:*"


