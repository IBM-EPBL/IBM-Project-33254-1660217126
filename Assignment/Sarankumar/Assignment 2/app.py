
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("base.html")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        details = request.form
        uname = details["uname"]
        umobile = details["umobile"]
        psw = details["psw"]
        cnt=sqlite3.connect("mydb.db")
        print("Connected")
        cur = cnt.cursor()
        cur.execute("SELECT mobile FROM Student;")
        res = cur.fetchall()
        ans=1
        for i in res:
            if i[0] == umobile:
                cur.close()
                ans= 0
                break
        if ans == 1:
            return redirect("/signup")
        
        return redirect("/next1")
    return render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        details = request.form
        name = details["uname"]
        mobile = details["umobile"]
        email = details["uemail"]
        psw = details["psw"]
        cnt=sqlite3.connect("mydb.db")
        print("Connected")
        cur = cnt.cursor()
        cur.execute("SELECT mobile FROM Student;")
        res = cur.fetchall()
        ans=1
        for i in res:
            if i[0] == mobile:
                cur.close()
                ans= 0
                break
        if ans == 1:
            print("Should be created")
            sql = '''INSERT INTO Student (sname, mobile,email,spassword) VALUES ("{}","{}","{}","{}")'''.format(name,mobile,email,psw)
            print(sql)
            cur = cnt.cursor()
            cur.execute(sql)
            cnt.commit()
            # self.cnt.close()
            return redirect("/signin")
        else:
            return redirect("/signin")
    return render_template("signup.html")

@app.route("/next1")
def next1():
    return render_template("next1.html")


if __name__ == "__main__":
    app.run(port="8050", debug=True)
