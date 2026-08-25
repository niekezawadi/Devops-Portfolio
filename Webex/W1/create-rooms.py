import requests

access_token = 'YzljNmM2NWEtYjc5Ni00OTAwLWI2YjItMzMyM2I2YWRmNDNhMDk0MTkwMjgtZjA3_PE93_c8b056ff-2097-4f20-987c-5bdaeff74d03'
url = 'https://webexapis.com/v1/rooms'
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {'title': 'DevOps Examen Nieke'}
res = requests.post(url, headers=headers, json=params)
print(res.json())# Fill in this file with the code to create a new room from the Webex Teams exercise
