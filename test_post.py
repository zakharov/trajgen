from request import request
import json


def test(request_filename, url, reply_filename):
    traj_json = request(request_filename, url)
    print(traj_json)
    with open(reply_filename, 'w') as outfile:
        json.dump(traj_json, outfile, indent=2)


if __name__ == '__main__':
    test('test1.json', 'http://api.ruckig.com/calculate', 'test_result.json')
