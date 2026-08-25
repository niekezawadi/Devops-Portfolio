import requests
import json

access_token = 'YzljNmM2NWEtYjc5Ni00OTAwLWI2YjItMzMyM2I2YWRmNDNhMDk0MTkwMjgtZjA3_PE93_c8b056ff-2097-4f20-987c-5bdaeff74d03'
url = 'https://webexapis.com/v1/people'
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {
    'email': 'nieke.karhambazawadi@student.odisee.be'
}
res = requests.get(url, headers=headers, params=params)
print(json.dumps(res.json(), indent=4))# Fill in this file with the people listing code from the Webex Teams exercise
