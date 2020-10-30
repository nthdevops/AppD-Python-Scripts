import http.client as httpc
import datetime, sys, jwt, json
from time import time
from flask import Flask, request

app = Flask(__name__)

# create a function to generate a token using the pyjwt library
def generateToken():
	token = jwt.encode({'iss':"JltcEu_yTUqRhiM6KaLbeQ", "exp": time() + 300}, "kz3cRy7fEdQdqFOzBhcTPxI2wyEa6wDK5fS0", algorithm='HS256').decode('utf-8')
	return token

#Headers
conn = httpc.HTTPSConnection("api.zoom.us")
headers = {'authorization': 'Bearer %s' % generateToken(), 'content-type': 'application/json'}

def mkRequest(method,url,bodyIn,headersIn):
	conn.request(method, url, body=bodyIn, headers=headersIn)
	res = conn.getresponse()
	data = res.read()
	return data.decode('utf-8')

@app.route('/', methods=['POST'])
def createMeeting():
  content = request.json
  #Emails
  emails = []
  #Adding emails from request
  emails.append(content["result"]["emailatendente"])
  emails.append(content["result"]["cliente"])

  #Names
  names = []
  for email in emails:
    names.append(email.split("@")[0])

  #Meeting creating config
  meetingName = "Virtual Techbar Supporting "+emails[1]
  date = datetime.datetime.now()
  jsonBodyCreate = {
    "topic": meetingName,
    "type": 2,
    "start_time": "{:%Y-%m-%dT%H:%M:%SZ}".format(date),
    "duration": 60,
    "timezone": "America/Sao_Paulo",
    "agenda": meetingName,
    "settings": {
      "approval_type": 0,
      "registrants_email_notification": "true",
      "meeting_authentication" : "false",
      "use_pmi": "false"
    }
  }
  urlCreate = "https://api.zoom.us/v2/users/L0rjFIgoSDWjZ74S4U9bag/meetings"

  #Meeting creation
  retCreation = json.loads(mkRequest("POST", urlCreate, json.dumps(jsonBodyCreate), headers))

  #Inviting Users
  urlInvite = "https://api.zoom.us/v2/meetings/MEETINGID/registrants".replace("MEETINGID", str(retCreation["id"]))

  for i in range(2):
    jsonBodyInvite = {"email": "", "first_name": ""}
    email = emails[i]
    name = names[i]
    jsonBodyInvite["email"] = email
    jsonBodyInvite["first_name"] = name
    mkRequest("POST", urlInvite, json.dumps(jsonBodyInvite), headers)
  
  return {'result':'Ok'}

app.run(host='0.0.0.0', port=9090)