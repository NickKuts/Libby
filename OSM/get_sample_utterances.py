#!/usr/bin/env python

import os
import sys
import json


### Note: this script will overwrite any file named 'sample-utterances.json'
###       in the directory of this script
json_name = 'sample_utterances.json'

# Get absolute path to the directory where this file is
ABS_PATH = os.path.dirname(os.path.abspath(__file__))

# Get possible arguments from user
argums = sys.argv

# If user has defined the intent through arguments, use that
# else ask for one
if len(argums) > 1:
    intent = argums[1]
else: intent = input('intent> ')

# Now do the query, the result will be a string so we 
# have to change it later on
res_str = os.popen("aws lex-models get-intent --name "
                   "{} --intent-version \$LATEST".format(intent)).read()

# Check if errors occurred
if 'error occurred' in res_str:
    print('An error occurred, result was:\n{}'.format(res_str))
    sys.exit(1)

# Load the string to JSON
in_json = json.loads(res_str)
# And extract the sampleUtterances
in_json = in_json['sampleUtterances']

# Check if the user defined an indentation for the JSON file
# if not, do not indent (i.e. pretty-print or not)
try:
    indent = int(argums[2])
except (ValueError, IndexError): 
    indent = None

# Maybe check if the file already exists?

# And finally write the JSON file depending on the indentation
with open(ABS_PATH + '/' + json_name, 'w+') as fp:
    if indent:
        json.dump(in_json, fp, indent=indent)
    else: json.dump(in_json, fp)

