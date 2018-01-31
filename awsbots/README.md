#Exceptions

BadRequestException:
- When creating a new bot, if you specify a checksum then this error will
  thrown. Example:
botocore.errorfactory.BadRequestException: An error occurred (BadRequestException) when calling the PutBot operation: checksum must be specified in PUT API, when the resource already exists

botocore.errorfactory.BadRequestException: An error occurred
(BadRequestException) when calling the PutBot operation: RelativeId does not
match Lex ARN format: bot:LibbyFromPython2:$LATEST
- The name should not contain numbers.
