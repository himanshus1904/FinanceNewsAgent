__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import subprocess
import json


# Define the data to be sent in the POST request
def func():
    data = {
        "query": "Todays news on indian financial market",
        "type": "neural",
        "useAutoprompt": True,
        "numResults": 2,
        "contents": {
            "text": True
        }
    }

    json_data = json.dumps(data)
    curl_command = [
        'curl',
        '-X', 'POST', 'https://api.exa.ai/search',
        '--header', 'accept: application/json',
        '--header', 'content-type: application/json',
        '--header', 'x-api-key: 475aa0b2-827d-40fd-8f76-5cd8b3311935',
        '--data', json_data
    ]
    result = subprocess.run(curl_command, capture_output=True, text=True)
    output_data = json.loads(result.stdout)

    # Write the output data to a JSON file
    with open('output_results.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)


if __name__ == '__main__':
    func()
