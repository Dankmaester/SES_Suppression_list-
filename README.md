# SES_Suppression_list-
This python script pulls emails from the Amazon web Services suppression list and exports them into a CSV file.

Make sure you have downloaded Python.

You need to first configure your AWS profile to use the CLI


aws configure --profile <profilename>
Grab your access key ID and secret access key ID for IAM

select ap-southeast-2 as region and json as output file 

your config and credentials will be stored in .aws folder in your computer.

Note: configure your Aws production environment.

You need boto3 library, click and ypy_boto3_sesv2.client to be installed before we proceed

 


pip install boto3

pip install -U click

python -m pip install 'boto3-stubs[sesv2]'
