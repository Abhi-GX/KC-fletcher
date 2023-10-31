from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import csv
import pandas as pd
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kc.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class kc(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String)
    Name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    clas = db.Column(db.String(100), default="Not updated")
    sex = db.Column(db.String(50), nullable=False)
    pno = db.Column(db.String)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.Name}"

def initialize_database():
    global c,cv
    c = pd.read_csv("C:\\Users\\abhig\OneDrive\Desktop\YOUNOUS SIR.csv")
    cv = c.values

    with app.app_context():
        db.create_all()

        for j in range(833):
            pf = kc(id=str(cv[j][1]), Name=cv[j][7], dob=str(cv[j][9]), sex=cv[j][14], pno=str(cv[j][13]))
            db.session.add(pf)
            db.session.commit()
@app.route("/")
def home1():
    return render_template("HOME1.html")
@app.route("/search",methods=["GET","POST"])
def home():
    if request.method=="POST":
        n=request.form["key"]
        global hj
        if n.isdigit():
            n = int(n)
        else:
            n = n.upper()
        N = 0
        if n in cv:
            for i in cv:
                if n in i:
                    D = N
                N = N + 1
            hj = cv[D]
            payload1 = {
                "rollno": hj[1]
            }
        else:
           hj=["0"]*20
           payload1 = {
               "rollno": n}
        global response1
        response1 = json.loads((requests.post("https://kmitastra.vercel.app/api/rollno", data=payload1)).text)
        payload2 = {
            "method": "32",
            "rollno": str(response1['rollno'])
        }
        global response2
        response2 = json.loads((requests.post("http://teleuniv.in/netra/api.php", data=json.dumps(payload2))).text)

        return render_template("HOME.html",hj=hj,DL=response2)
@app.route("/details")
def home2():
    payload3 = {
        "method": "314",
        "rollno": str(response1['rollno'])
    }
    response3 = json.loads((requests.post("http://teleuniv.in/netra/api.php", data=json.dumps(payload3))).text)
    td = [str(response3["attandance"]["dayobjects"][0]["sessions"][i]) for i in response3["attandance"]["dayobjects"][0]["sessions"]]
    td1 = [response3["attandance"]["dayobjects"][1]["sessions"][i] for i in
           response3["attandance"]["dayobjects"][1]["sessions"]]
    td2 = [response3["attandance"]["dayobjects"][2]["sessions"][i] for i in
           response3["attandance"]["dayobjects"][2]["sessions"]]
    dd = [response3["attandance"]["dayobjects"][0]["day"], response3["attandance"]["dayobjects"][1]["date"],
          response3["attandance"]["dayobjects"][2]["date"]]
    ttd = [response3["attandance"]["twoweeksessions"][i] for i in response3["attandance"]["twoweeksessions"]]
    ov = response3['overallattperformance']['totalpercentage']
    ovc = response3['overallattperformance']['colorcode']
    sub = [response3['overallattperformance']['overall'][i]['subjectname'] for i in range(len(response3['overallattperformance']['overall']))]
    subp = [response3['overallattperformance']['overall'][i]['percentage'] for i in range(len(response3['overallattperformance']['overall']))]
    subc = [response3['overallattperformance']['overall'][i]['colorcode1'] for i in range(len(response3['overallattperformance']['overall']))]
    ddd = {
        "0": '''<svg aria-hidden="true" class="svg-inline--fa far-circle-xmark" color="red" data-icon="circle-xmark" data-prefix="far" focusable="false" role="img" viewbox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M175 175C184.4 165.7 199.6 165.7 208.1 175L255.1 222.1L303 175C312.4 165.7 327.6 165.7 336.1 175C346.3 184.4 346.3 199.6 336.1 208.1L289.9 255.1L336.1 303C346.3 312.4 346.3 327.6 336.1 336.1C327.6 346.3 312.4 346.3 303 336.1L255.1 289.9L208.1 336.1C199.6 346.3 184.4 346.3 175 336.1C165.7 327.6 165.7 312.4 175 303L222.1 255.1L175 208.1C165.7 199.6 165.7 184.4 175 175V175zM512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z" fill="currentColor"></path></svg>''',
        "2": '''<svg aria-hidden="true" class="svg-inline--fa far-circle" data-icon="circle" data-prefix="far" focusable="false" role="img" viewbox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z" fill="currentColor"></path></svg>''',
        "1": '''<svg aria-hidden="true" class="svg-inline--fa far-circle-check" color="green" data-icon="circle-check" data-prefix="far" focusable="false" role="img" viewbox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M243.8 339.8C232.9 350.7 215.1 350.7 204.2 339.8L140.2 275.8C129.3 264.9 129.3 247.1 140.2 236.2C151.1 225.3 168.9 225.3 179.8 236.2L224 280.4L332.2 172.2C343.1 161.3 360.9 161.3 371.8 172.2C382.7 183.1 382.7 200.9 371.8 211.8L243.8 339.8zM512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z" fill="currentColor"></path></svg>'''
    }
    tda = [ddd[i] for i in td]
    td1a = [ddd[i] for i in td1]
    td2a = [ddd[i] for i in td2]
    print(sub,subp,subc)
    return render_template("details.html",DL=response2,td=tda,td1=td1a,td2=td2a,dd=dd,ov=ov,sub=sub,subp=subp,subc=subc,ttd=ttd,ovc=ovc)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)