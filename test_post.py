import json
import requests

def test(request_filename, url, reply_filename):
    with open(request_filename) as infile:
        data = json.load(infile)
        reply = requests.post(url, json=data)
        with open(reply_filename, 'w') as outfile:
            json.dump(reply.json(), outfile, indent=2)

if __name__ == '__main__':
    test('test.json', 'http://api.ruckig.com/calculate', 'test_result.json')
