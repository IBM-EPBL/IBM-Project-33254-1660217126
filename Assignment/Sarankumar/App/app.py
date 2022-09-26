
from flask import Flask,render_template,request,redirect
from data import storage, to_dbms
app=Flask(__name__)
@app.route("/")
def welcome():
    return render_template("base.html")
@app.route("/signin")
def signin():
    return render_template("index.html")


@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        details=request.form
        name=details["uname"]
        mobile=details["umobile"]
        email=details["uemail"]
        psw=details["psw"]
        ob1=to_dbms()
        ob1.get(name,mobile,email,psw)
        print(storage.database)
        return redirect("/sigin")
    return render_template("signup.html")
if __name__=="__main__":
    app.run(port="8050",debug=True)
