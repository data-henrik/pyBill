# Quick hack to dump billing information for the
# currently set account and resource group
#
# (C) 2018, Henrik Loeser, hloeser@de.ibm.com


import json
from os.path import expanduser
import requests
import datetime

# To get the current month
now = datetime.datetime.now()

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
METERING_URL="/v4/accounts/"+account_id+"/resource_groups/"+resourceGroupID+"/usage/"+str(now.year)+"-"+str(now.month)

USAGE_URL="/v4/accounts/"+account_id+"/resource_instances/usage/"+str(now.year)+"-"+str(now.month)+"?_limit=100&_names=true"

url=METERING_HOST+METERING_URL
headers = {
    "Authorization": "{}".format(iam_token),
    "Accept": "application/json",
    "Content-Type": "application/json"
}
response=requests.get(url, headers=headers)
print "Usage for current resource group"
print json.dumps(response.json())

url=METERING_HOST+USAGE_URL
headers = {
    "Authorization": "{}".format(iam_token),
    "Accept": "application/json",
    "Content-Type": "application/json"
}
response=requests.get(url, headers=headers)
print "\n\nResource instance usage for first 100 items"
print json.dumps(response.json())


