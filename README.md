# pyBill - fetch IBM Cloud billing and usage information

The script expects you to be logged in to IBM Cloud using the CLI. It reads your currently set account and resource group from the config file (assuming `~/.bluemix/config.json`). Next, it fetches the usage data for the current month and dumps the JSON response.