# pyBill - fetch IBM Cloud billing and usage information

The script expects you to be logged in to IBM Cloud using the CLI and takes the access token from there. It also reads your currently set account and resource group from the config file (assuming `~/.bluemix/config.json`). Next, it fetches the usage data for the current month and dumps the JSON response.

Print the resource instance usage for 09/2018:
```
./pyBill.py -riu -print -m 2018-09
```

Print the resource instance usage for 08/2018 as CSV (CSV only supported for "riu"):
```
./pyBill.py -riu -csv -m 2018-08
```

Print the resource group usage (currently set group) for 05/2018:
```
./pyBill.py -rgu -print -m 2018-05
```


## Contribution
Pull requests welcome...