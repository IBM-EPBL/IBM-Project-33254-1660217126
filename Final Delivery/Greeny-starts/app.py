from flask import Flask,render_template,redirect,request,url_for

import ibm_db

import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID="8ir_OK_kdjY8SXvQXnvcYD34CrCrX7TIELEbWpzBQCFH"
COS_INSTANCE_CRN="crn:v1:bluemix:public:cloud-object-storage:global:a/cac77355b8e64285ab5824053ea1e90d:66b5a2a3-b654-458e-b4af-b3c551fc5b0f::"


cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/checkuserExistence",methods=['post'])
def checkuserExistence():
    conn = ibm_db.connect("DATABASE=bludb ; HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mzz66103;PWD=EIjmVVQ9CytfCyNc;", '', '')
    print("Cloud Connected Successfully!!")
    
    mail=request.form['mail']

    sql = "select *from green_starts WHERE mail=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1,mail )
    ibm_db.execute(stmt)
    user_checkIn = ibm_db.fetch_assoc(stmt)

    
    image="/static/images/image2.gif"
    msg1="Ooops!"
    msg2="This E-Mail is Already Exist!!"

    if user_checkIn:
        return render_template("notification.html",image=image,msg1=msg1,msg2=msg2)
    else:
        return render_template("signup.html",usermail=mail)


@app.route("/getdetails",methods=['post','get'])
def getdetails():
    conn = ibm_db.connect("DATABASE=bludb ; HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mzz66103;PWD=EIjmVVQ9CytfCyNc;", '', '')
    print("Cloud Connected Successfully!!")


    name=request.form['name']
    fname=request.form['fname']
    mail=request.form['email']
    mobile=request.form['mbno']
    password=request.form['pass']
    dob=request.form['dob']
    country=request.form['country']
    gender=request.form['gender']

    sql="INSERT INTO green_starts values(?,?,?,?,?,?,?,?)"
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.bind_param(stmt,2,fname)
    ibm_db.bind_param(stmt,3,mail)
    ibm_db.bind_param(stmt,4,mobile)
    ibm_db.bind_param(stmt,5,password)
    ibm_db.bind_param(stmt,6,dob)
    ibm_db.bind_param(stmt,7,country)
    ibm_db.bind_param(stmt,8,gender)
    ibm_db.execute(stmt)
    
    print("Account is Created !!")
    print(name+" "+fname+" "+mail+" "+mobile+" "+password+" "+dob+" "+country+" "+gender)

    image="/static/images/tick1.gif"
    msg1="Congratulation!"
    msg2="Your Account has been Successfully Created!!"
    return render_template("notification.html",image=image,msg1=msg1,msg2=msg2)

@app.route("/checkuser",methods=['post'])
def checkuser():
    conn = ibm_db.connect("DATABASE=bludb ; HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mzz66103;PWD=EIjmVVQ9CytfCyNc;", '', '')
    print("Cloud Connected Successfully!!")

    mail=request.form['email']
    password=request.form['pass']

    if mail=="Admin@gmail.com" and password=="Admin":
        print("Admin Login")
        return redirect("admin")

    print(mail+" "+password)

    sql = "select *from green_starts WHERE mail=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1,mail )
    ibm_db.execute(stmt)
    lis = ibm_db.fetch_assoc(stmt)

    
    image="/static/images/image2.gif"
    msg1="Ooops!"
    msg2="This E-Mail Doesn't Exist!!"

    if lis:
        sql="SELECT password from green_starts WHERE mail=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,mail)
        ibm_db.execute(stmt)

        lis=ibm_db.fetch_assoc(stmt)

        
        e=lis.get('PASSWORD')


        if e==password:
            print("Logged in successfully!!")
            return  redirect(url_for('.user1',mail=mail))
            
        else:
            print("****Error****")
            return render_template("notification.html",image=image,msg1=msg1,msg2="You Have Entered Wrong Password!!")

    else:
        return render_template("notification.html",image=image,msg1=msg1,msg2=msg2)
    

    
#                          ***********    Object Storage        ***********

def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

@app.route('/user1',methods=['post','get'])
def user1():
    mail=request.args['mail']

    conn = ibm_db.connect("DATABASE=bludb ; HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mzz66103;PWD=EIjmVVQ9CytfCyNc;", '', '')
    print("Cloud Connected Successfully!!")
   
    sql="SELECT * from green_starts WHERE mail=?"
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,mail)
    ibm_db.execute(stmt)

    lis=ibm_db.fetch_assoc(stmt)

    a=lis.get('UNAME')
    b=lis.get('FNAME')
    c=lis.get('MAIL')
    d=lis.get('MOBILE')
    e=lis.get('PASSWORD')
    f=lis.get('DOB')
    g=lis.get('COUNTRY')
    h=lis.get('GENDER')
    
    files = get_bucket_contents('green-starts')
    return render_template('user1.html', files = files,mail=mail,username=a,fname=b,usermail=c,mobile=d,country=g,gender=h)

                # ---------Admin Control----------------
                
                
                
def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))


@app.route('/upload', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
       bucket="green-starts"
       name_file=request.form['filename']
       f = request.files['file']
       print(f.filename)
       multi_part_upload(bucket,name_file,f.filename)
       
       print("File is Uploaded!!!!")
       return redirect("/admin")
   
@app.route('/admin')
def admin():
    files = get_bucket_contents('green-starts')
    return render_template('admin.html', files = files)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
   if request.method == 'POST':
       bucket="green-starts"
       name_file=request.form['filename']
       
       delete_item(bucket,name_file)
       return redirect("/admin")
    
   
   
def delete_item(bucket_name, object_name):
    try:
        cos.Object(bucket_name, object_name).delete()
        print("Item: {0} deleted!\n".format(object_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete object: {0}".format(e))

if __name__=="__main__":
    app.run(host="0.0.0.0",port="8020",debug=True)