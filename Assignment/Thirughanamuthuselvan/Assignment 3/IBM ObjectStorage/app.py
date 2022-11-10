from flask import Flask, render_template, redirect, request
from databasecloud import Storage
from objectstorage import cloudstorage
app = Flask(__name__)
@app.route("/")
def welcome():
    return render_template("base.html")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        mobile = request.form["umobile"]
        ob1 = Storage()
        ans = ob1.check(mobile)
        if ans == 1:
            return redirect("/next")
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


@app.route("/next")
def next():
    ob1=cloudstorage()
    files=ob1.get_bucket_contents("flaskstorage")
    return render_template("next.html",files=files)

@app.route("/upload",methods=["POST","GET"])
def upload():
    if request.method=="POST":
        bucket=request.form["bucket"]
        fname=request.form["filename"]
        f=request.files["file"]
        ob1=cloudstorage()
        ob1.multi_part_upload(bucket,fname,f.filename)
        return render_template("upload1.html",tag=0)
    return render_template("upload.html",tag=1)

@app.route("/delete",methods=["POST","GET"])
def delete():
    if request.method=="POST":
        bucket=request.form["bucket"]
        fname=request.form["filename"]
        ob1=cloudstorage()
        ob1.delete_item(bucket,fname)
        return render_template("delete1.html",tag=0)
    return render_template("delete.html",tag=1)



if __name__ == "__main__":
    app.run(port="8050", debug=True)
  