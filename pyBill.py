#!/usr/bin/env python
# Quick hack to dump billing information for the
# currently set account and resource group
#
# (C) 2018, Henrik Loeser, hloeser@de.ibm.com


import json
from os.path import expanduser
import requests
import datetime
import argparse


# Define parameters that we want to catch and some basic command help
def getParameters(args=None):
    parser = argparse.ArgumentParser(description='Some billing and usage data',
                                     prog='pyBill.py',
                                     usage='%(prog)s [-h | -rgu | -riu] [options]')
    parser.add_argument("-rgu",dest='resourceGroupUsage', action='store_true', help='resource group usage')
    parser.add_argument("-riu",dest='resourceInstanceUsage', action='store_true', help='resource instance usage')
    parser.add_argument("-print",dest='printJSON', action='store_true', help='print JSON data')
    parser.add_argument("-csv",dest='csv', action='store_true', help='print as csv')
    parser.add_argument("-m",dest='billMonth', help='billing month YYYY-MM')
    parms = parser.parse_args()
    return parms



def processResourceGroupUsage(account_id, resourceGroupID, billMonth):
    METERING_HOST="https://metering-reporting.ng.bluemix.net"
    METERING_URL="/v4/accounts/"+account_id+"/resource_groups/"+resourceGroupID+"/usage/"+billMonth+"?_names=true"
    url=METERING_HOST+METERING_URL
    headers = {
        "Authorization": "{}".format(iam_token),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response=requests.get(url, headers=headers)
    #print ("Usage for current resource group")
    return response.json()

def processResourceInstanceUsage(account_id, billMonth):
    METERING_HOST="https://metering-reporting.ng.bluemix.net"
    USAGE_URL="/v4/accounts/"+account_id+"/resource_instances/usage/"+billMonth+"?_limit=100&_names=true"

    url=METERING_HOST+USAGE_URL
    headers = {
        "Authorization": "{}".format(iam_token),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response=requests.get(url, headers=headers)
    #print ("\n\nResource instance usage for first 100 items")
    return response.json()


#
# Main program, for now just detect what function to call and invoke it
#
if __name__ == '__main__':
    # To get the current month
    now = datetime.datetime.now()

    # Get the path for current user
    homedir = expanduser("~")

    data=None

    # open the IBM Cloud config file
    # Assumption: user is logged in and resource group is set
    with open(homedir+'/.bluemix/config.json') as data_file:
        credentials = json.load(data_file)
    iam_token = credentials.get('IAMToken')
    api_endpoint = credentials.get('APIEndpoint')
    account_id=credentials.get('Account').get('GUID')
    resourceGroupID=credentials.get('ResourceGroup').get('GUID')

    parms = getParameters()
    if (parms.billMonth is None):
        billMonth=str(now.year)+"-"+str(now.month)
    else:
        billMonth=parms.billMonth
    # enable next line to print parameters
    # print parms
    if (parms.resourceGroupUsage):
        data=processResourceGroupUsage(account_id,resourceGroupID, billMonth)
    elif (parms.resourceInstanceUsage):
        data=processResourceInstanceUsage(account_id, billMonth)
    else:
        print ("Use -h for help.")

    #print ("Account: "+account_id)
    
    if data is not None:
        if (parms.printJSON):
            print (json.dumps(data, indent=4, sort_keys=True))
        elif (parms.csv):
            tags=['resource_instance_name', 'usage', 'resource_name', 'billable']
            #resources= [{x['resource_instance_name'], x['usage']} for x in data['resources'] ]
            #resources= [{restxt:x[restxt], usgtxt:x[usgtxt]} for x in data['resources'] ]
            resources= [{i:x[i] for i in tags } for x in data['resources']  ]
            #print (json.dumps(resources, indent=4))
            print ("resource, billable, metric, cost")
            for i in resources:
                for j in i['usage']:
                    print (i['resource_name']+","+str(i['billable'])+","+j['metric']+","+str(j['cost'])) 
        else:
            print ("No other option")