import ibm_db
class Storage():
    cnt = ibm_db.connect(
        "DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSl;SSL=true;UID=mzz66103;PWD=EIjmVVQ9CytfCyNc", "", "")

    def check(self, Mobile):
        sql = "SELECT MOBILE FROM USERDETAILS"
        cur = ibm_db.exec_immediate(self.cnt, sql)
        res=ibm_db.fetch_tuple(cur)
        while res!=False:
            if res[0]==Mobile:
                return 1
            res=ibm_db.fetch_tuple(cur)
        return 0
    def store(self,uname,mobile,email,psw):
        ob2=Storage()
        if ob2.check(mobile)==0:
            sql="INSERT INTO USERDETAILS (SNAME,MOBILE,EMAIL,PSW) VALUES('{}','{}','{}','{}')".format(uname,mobile,email,psw)
            cur=ibm_db.exec_immediate(self.cnt,sql)
            print("Success")
            return 1
        else:
            return 1