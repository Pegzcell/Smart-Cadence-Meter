from onem2m import *
from flask import Flask, render_template, redirect, url_for, jsonify
uri_cse = "http://127.0.0.1:8080/~/in-cse/in-name"
ae = "Readings"
cnt1 = "Current_rpm"
cnt2 = "Average_rpm"
cnt3 = "Session_time"
cnt4 = "Distance"
cnt5 = "Start_flag"
cnt6 = "Session_id"
uri_ae = uri_cse+"/"+ae
uri_cnt1 = uri_ae + "/" + cnt1
uri_cnt2 = uri_ae + "/" + cnt2
uri_cnt3 = uri_ae + "/" + cnt3
uri_cnt4 = uri_ae + "/" + cnt4
uri_cnt5 = uri_ae + "/" + cnt5
uri_cnt6 = uri_ae + "/" + cnt6

headers = {
    'X-M2M-Origin': 'admin:admin',
    'Content-type': 'application/json'
}

app =Flask(__name__)
#update rpm
@app.route('/_stuff', methods= ['GET'])
def stuff():
    resp = requests.get(
        f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt5}/la', headers=headers)
    result = json.loads(resp.text)
    start_flag = result['m2m:cin']['con']
    if start_flag == "1":
        resp = requests.get(
            f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt1}/la', headers=headers)
        result = json.loads(resp.text)
        current_rpm = result['m2m:cin']['con']
        return jsonify(content=current_rpm)
    else:
        return redirect(url_for("end"))
    

@app.route("/")
def home():
    resp = requests.get(
        f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt5}/la', headers=headers)
    result = json.loads(resp.text)
    start_flag = result['m2m:cin']['con']
    if start_flag == "1":
        resp = requests.get(
            f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt1}/la', headers=headers)
        result = json.loads(resp.text)
        current_rpm = result['m2m:cin']['con']
        return render_template("ui.html", content=float(current_rpm))
    else:
        return redirect(url_for("end"))

@app.route("/end")
def end():
    resp = requests.get(
        f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt5}/la', headers=headers)
    result = json.loads(resp.text)
    start_flag = result['m2m:cin']['con']
    if start_flag != "1":
        resp = requests.get(
            f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt6}/la', headers=headers)
        result = json.loads(resp.text)
        session_id = result['m2m:cin']['con']

        resp = requests.get(
            f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt2}/la', headers=headers)
        result = json.loads(resp.text)
        average_rpm = result['m2m:cin']['con']

        resp = requests.get(
            f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt3}/la', headers=headers)
        result = json.loads(resp.text)
        session_time = result['m2m:cin']['con']

        resp = requests.get(
            f'http://127.0.0.1:8080/~/in-cse/in-name/{ae}/{cnt4}/la', headers=headers)
        result = json.loads(resp.text)
        distance = result['m2m:cin']['con']
        return render_template("result.html", p1=session_id, p2=session_time, p3=average_rpm, p4=distance)
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()




