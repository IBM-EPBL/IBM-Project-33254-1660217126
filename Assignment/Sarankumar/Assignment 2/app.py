

from flask import Flask, render_template, redirect, request

from databasecloud import Storage
app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("base.html")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        user = request.form["uname"]
        mobile = request.form["umobile"]
        psw = request.form["psw"]
        ob1 = Storage()
        ans = ob1.check(mobile)
        if ans == 1:
            return redirect("/next1")
        else:
            return redirect("/signup")
    return render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        uname = request.form["uname"]
        mobile = request.form["umobile"]
        email = request.form["uemail"]
        psw = request.form["psw"]
        ob1 = Storage()
        ans = ob1.store(uname, mobile, email, psw)
        if ans==1:
            return redirect("/signin")
        
    return render_template("signup.html")


@app.route("/next1")
def next1():
    return render_template("next1.html")


if __name__ == "__main__":
    app.run(port="8050", debug=True)
