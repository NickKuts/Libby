#Exceptions

BadRequestException:
- When creating a new bot, if you specify a checksum then this error will
  thrown. Example:
botocore.errorfactory.BadRequestException: An error occurred (BadRequestException) when calling the PutBot operation: checksum must be specified in PUT API, when the resource already exists

botocore.errorfactory.BadRequestException: An error occurred
(BadRequestException) when calling the PutBot operation: RelativeId does not
match Lex ARN format: bot:LibbyFromPython2:$LATEST
- The name of bots, intents or slots cannot contain numbers.




# How to add a new intent
1. Create a placeholder intent that does not use anything related to lambda
   functions. The intent cannot be created if the lambda function that it uses
   does not have permissions to use, so we first need to create a dumb intent and
   fill it in after giving permissions to the lambda functions.
2. Add permissions for lambda function to use that intent.
3. Fill the intent so that it uses the lambda function.

Here is a sample json file that can be used to generate dummy intents.

```
{
	"name": "IntentName",
	"slots": [],
	"sampleUtterances": ["How you doin?"],
	"fulfillmentActivity": {
		"type": "ReturnIntent"
	}
}
```
