
from multiprocessing import connection
from multiprocessing.sharedctypes import Value
from flask import Flask,render_template,redirect,request

import ibm_db

app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb ; HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zks34476;PWD=QBQGQSBtToeE4TVg;", '', '')

print("connected successfully")

@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/signin")
def signin():
  return render_template("signin.html")

@app.route("/signup")
def signup():
  return render_template("signup.html")




@app.route("/getvalue",methods=['post'])
def getvalue():
 
  name=request.form['name']
  email=request.form['email']
  password=request.form['pass']
  
  sql="INSERT INTO details values(?,?,?)"
  stmt=ibm_db.prepare(conn,sql)
  ibm_db.bind_param(stmt,1,name)
  ibm_db.bind_param(stmt,2,email)
  ibm_db.bind_param(stmt,3,password)
  ibm_db.execute(stmt)

  print("Created")
  return render_template("welcome.html",msg="Account is Created")


@app.route("/checkvalue",methods=['post'])
def checkvalue():
  
  name=request.form['name']
  email=request.form['email']
  password=request.form['pass']
  
  sql="SELECT Pass from details WHERE PName=? and Email=?"
  stmt=ibm_db.prepare(conn,sql)
  ibm_db.bind_param(stmt,1,name)
  ibm_db.bind_param(stmt,2,email)
  ibm_db.execute(stmt)

  lis=ibm_db.fetch_assoc(stmt)
  
  a=lis.get('PASS')

  if a!=password:
    return render_template("welcome.html",msg="Your Name and Password is Wrong")
  else:
    return render_template("frontpage.html")

@app.route("/slist")
def slist():
    sql="SELECT * from details"
    stmt=ibm_db.exec_immediate(conn,sql)

    dict=ibm_db.fetch_assoc(stmt)

    lis=[]
    while dict!=False:
        b=[]
        for i,j in dict.items():
            b.append(j)
        a=tuple(b)
        lis.append(a)
        dict=ibm_db.fetch_assoc(stmt)

    print(lis)

    return render_template("slist.html",value=lis)




if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8081,debug=True)
