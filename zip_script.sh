#!/bin/bash

# Save save name the directory to be created
dir_name=$1

# If no name has been given, create name based on the current date and time
if [ -z "${dir_name}" ]; then
    timestamp=`date "+%Y/%m/%d-%H:%M:%S"`
    dir_name="zip${timestamp}"
fi

# Save the name of the zip-file to be created
zip_name="${dir_name}.zip"

# Make the directory
mkdir ${dir_name}
#cp -r venv/lib/python3.6/site-packages/* ${dir_name}/

# Copy all files from lambda_func to this directory
cp -r lambda_func/* ${dir_name}/

# Now create the actual zip-file
#zip -r ${zip_name} lambda_func/*

cd ${dir_name}
zip -r ${zip_name} *
mv ${zip_name} ..
cd ..
rm -rf ${dir_name}/

#aws s3 cp ${dir_name}.zip s3://libby-lambda-configuration/ --profile $2

echo ""
echo "New zip-file created: ${zip_name}"

