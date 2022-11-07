import ibm_db
class Storage():
    cnt = ibm_db.connect(
        "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSl;SSL=true;UID=rvw93977;PWD=9BPkh4sg41jEiivY", "", "")

    def check(self, Mobile):
        sql = "SELECT MOBILE FROM USER"
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
            sql="INSERT INTO USER (SNAME,MOBILE,EMAIL,PASS) VALUES('{}','{}','{}','{}')".format(uname,mobile,email,psw)
            cur=ibm_db.exec_immediate(self.cnt,sql)
            print("Success")
            return 1
        else:
            return 1