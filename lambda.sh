aws lambda create-function \
    --region eu-west-1 \
    --function-name OSMToolsTest \
    --code S3Bucket=libby-lambda-configuration,S3Key=project-dir.zip \
    --role arn:aws:iam::263893614267:role/service-role/jerryTriviaIrelandRole \
    --handler test.handler \
    --runtime python3.6 \
    --profile cookie \
    --timeout 10 \
    --memory-size 1024

