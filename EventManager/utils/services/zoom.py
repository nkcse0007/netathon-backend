
import jwt
import requests
import json
from time import time
 
API_KEY = 'e7ONq_qlSR2zvZ7Kf9SXfA'
API_SEC = 'jOCdVKqf84zxA8sYF6rZSFQKU2coa0zewiWk'
 
def generateToken():
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time() + 5000},
        API_SEC,
        algorithm='HS256'
    )
    return token
  
 
def createMeeting(meetingdetails):
    headers = {'authorization': 'Bearer ' + generateToken(),
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
    return join_URL, meetingPassword
