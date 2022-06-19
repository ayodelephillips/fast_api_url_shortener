import argparse
import os
import sys
import requests
from main import localhost_url

description = 'Provide input to the url shortener. The url AND the type of url is the only inputs to be entered.' \
              'Entering the long url returns its shortened url; entering a short url redirects to the long url'
help = 'Specify whether entered url "long_url", or "short_url"'
long_url, short_url = "long_url", "short_url"
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--url', metavar='url', type=str, help='input a valid url', required=True)
parser.add_argument('--urltype', metavar='urltype', type=str, help=help, required=True)

args = parser.parse_args()

if args.urltype not in (long_url, short_url):
    print(help)
else:
    if args.urltype == long_url:
        response = requests.post(f"{localhost_url}/shorten_url/", data={"url": args.url})
    else:
        response = requests.get(f"{localhost_url}/{args.url}/")
    print(f"The response got is {response.status_code}")
