#!/bin/sh
zip -r -j deploy.zip ../lambda_func/*
aws lambda update-function-code \
    --function-name tuomasTestFunction \
    --zip-file fileb://deploy.zip
rm deploy.zip
