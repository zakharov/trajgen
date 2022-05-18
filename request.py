import json
import requests


# Sending request to the Ruckig online,
#   request_filename - path to a file with parameters of the trajectory
#   url - URL of the Ruckig service
#   Returns reply in a json format
def request(request_filename, url):
    with open(request_filename) as infile:
        data = json.load(infile)
        reply = requests.post(url, json=data)
        return reply.json()
    return None
