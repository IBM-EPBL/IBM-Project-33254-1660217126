
from multiprocessing import connection
from multiprocessing.sharedctypes import Value
from flask import Flask,render_template,redirect,request
import sqlite3

app = Flask(__name__)

@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/signin")
def signin():
  return render_template("signin.html")

@app.route("/signup")
def signup():
  return render_template("signup.html")


con=sqlite3.connect('students.db')
cur = con.cursor()

@app.route("/getvalue",methods=['post'])
def getvalue():
  con=sqlite3.connect('students.db')
  cur = con.cursor()
  name=request.form['name']
  email=request.form['email']
  password=request.form['pass']
  cur.execute("insert into details values(?,?,?)",(name,email,password))
  con.commit()
  print("Created")
  return render_template("welcome.html")

@app.route("/slist")
def slist():
  con=sqlite3.connect('students.db')
  cur = con.cursor()
  cur.execute("select * from details")
  data=cur.fetchall()
  return render_template("slist.html",value=data)

@app.route("/checkvalue",methods=['post'])
def checkvalue():
  con=sqlite3.connect('students.db')
  cur = con.cursor()
  name=request.form['name']
  email=request.form['email']
  password=request.form['pass']
  a=cur.execute("select PName from details")
  
  
  lis=[]
  for i in a:
    lis.append(i[0])
  
  print(lis)
  if name in lis:
    return render_template("frontpage.html")
  else:
    return render_template("signup.html")


if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8081,debug=True)
