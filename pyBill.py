# Quick hack to dump billing information for the
# currently set account and resource group
#
# (C) 2018, Henrik Loeser, hloeser@de.ibm.com


import json
from os.path import expanduser
import requests

# Get the path for current user
homedir = expanduser("~")

# open the IBM Cloud config file
# Assumption: user is logged in and resource group is set
with open(homedir+'/.bluemix/config.json') as data_file:
    credentials = json.load(data_file)
iam_token = credentials.get('IAMToken')
api_endpoint = credentials.get('APIEndpoint')
account_id=credentials.get('Account').get('GUID')
resourceGroupID=credentials.get('ResourceGroup').get('GUID')


METERING_HOST="https://metering-reporting.ng.bluemix.net"
METERING_URL="/v4/accounts/"+account_id+"/resource_groups/"+resourceGroupID+"/usage/2018-09"

url=METERING_HOST+METERING_URL
headers = {
    "Authorization": "{}".format(iam_token),
    "Accept": "application/json",
    "Content-Type": "application/json"
}
response=requests.get(url, headers=headers)
print json.dumps(response.json())
