import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt

ae = "Readings"
cnt1 = "Current_rpm"
cnt2 = "Session_id"
headers = {
    'X-M2M-Origin' : 'admin:admin',

    'Content-type' : 'application/json'
}
resp1 = requests.get(f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt1}/?rcn=4', headers=headers)
resp2 = requests.get(f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt2}/?rcn=4', headers=headers)
result1 = json.loads(resp1.text)
result2 = json.loads(resp2.text)
x_coordinates = []
y_coordinates = []
session_id = int(input("Enter session id: "))
val =0
for i in range(len(result1['m2m:cnt']['m2m:cin'])):
    if ((int)(result2['m2m:cnt']['m2m:cin'][i]['con']) == session_id):
        val+=1
        y_coordinates.append((float)(result1['m2m:cnt']['m2m:cin'][i]['con']))
        x_coordinates.append(datetime.strptime(result1['m2m:cnt']['m2m:cin'][i]['ct'], '%Y%m%dT%H%M%S'))
print(val, "entities")
plt.xlabel('Time')
plt.ylabel('Cadence')
plt.title('Session {}'.format(session_id))
plt.plot(x_coordinates, y_coordinates)
plt.show()