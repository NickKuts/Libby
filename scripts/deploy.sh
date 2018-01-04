#!/bin/sh
cd ../lambda_func
zip -r ../deploy.zip .
cd ..
aws lambda update-function-code \
    --function-name tuomasTestFunction \
    --zip-file fileb://deploy.zip
rm deploy.zip
