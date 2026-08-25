import requests

access_token = 'YzljNmM2NWEtYjc5Ni00OTAwLWI2YjItMzMyM2I2YWRmNDNhMDk0MTkwMjgtZjA3_PE93_c8b056ff-2097-4f20-987c-5bdaeff74d03'
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vYTRhNDE4YjAtYTBkMi0xMWYxLWFmMzItNzFiOTU2Y2I3ZDM3'
url = 'https://webexapis.com/v1/rooms/{}/meetingInfo'.format(room_id)
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
res = requests.get(url, headers=headers)
print(res.json())# Fill in this file with the code to get room details from the Webex Teams exercise
