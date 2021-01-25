#!/usr/bin/env python

import os
import sys
import time
from zapv2 import ZAPv2
from pprint import pprint

if len(sys.argv) != 2:
    print(f'USAGE: python3 {os.path.basename(__file__)} <target_url>')
    sys.exit(1)

# The URL of the application to be tested
target = sys.argv[1]

# Change to match the API key set in ZAP, or use None if the API key is disabled
try:
    with open('token', 'r') as f: # Add API Key to file named 'token'!
        apiKey = ''.join(f.read().split())
except FileNotFoundError:
    print('Add API Key to file named \'token\'!')
    sys.exit(1)


# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apiKey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
# zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

print('Spidering target {}'.format(target))

# The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target)

print("scanID = " + scanID)

while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(5)

print('Spider has completed!')
# Prints the URLs the spider has crawled

results = open("spider_results.txt", "w")
results.write('\n'.join(map(str, zap.spider.results(scanID))))
results.close()

#print('\n'.join(map(str, zap.spider.results(scanID))))
# If required post process the spider results

# ajax
print('Ajax Spider target {}'.format(target))
scanID = zap.ajaxSpider.scan(target)

timeout = time.time() + 60*1   # 1 minutes from now
# Loop until the ajax spider has finished or the timeout has exceeded
while zap.ajaxSpider.status == 'running':
    if time.time() > timeout:
        break
    print('Ajax Spider status: ' + zap.ajaxSpider.status)
    time.sleep(10)

print('Ajax Spider completed')

ajaxResults = zap.ajaxSpider.results(start=0, count=10)
# salvar em arquivo?

# scanning

scanID = zap.ascan.scan(target)
while int(zap.ascan.status(scanID)) < 100:
    # Loop until the scanner has finished
    print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
    time.sleep(5)

print('Scan complete!')

# Print vulnerabilities found by the scanning

with open("vulns.json", "w") as f:
    f.write('Hosts: {}'.format(', '.join(zap.core.hosts)))
    f.write('Alerts: ')
    pprint(zap.core.alerts(baseurl=target), stream = f)

print('Done!')


