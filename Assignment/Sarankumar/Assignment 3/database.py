import sqlite3
class storage:
    
    cnt=sqlite3.connect("mydb.db")
    print("Connected")

    def check(self, mobile):
        cur = self.cnt.cursor()
        cur.execute("SELECT mobile FROM Student;")
        res = cur.fetchall()
        for i in res:
            if i[0] == mobile:
                cur.close()
                return 0
        return 1

    def store(self, name, mobile, eail, psw):
        ob1 = storage()
        res = ob1.check(mobile)
        if res == 1:
            print("Should be created")
            sql = '''INSERT INTO Student (sname, mobile,email,spassword) VALUES ("{}","{}","{}","{}")'''.format(name,mobile,eail,psw)
            print(sql)
            cur = self.cnt.cursor()
            cur.execute(sql)
            self.cnt.commit()
            # self.cnt.close()
            return 1
        else:
            print("already")
            return 0
if __name__=="__main__":
    ob1=storage()
    print(ob1.check("9344879541"))
    print(ob1.store("suganya","8300851869","suganya@gmail.com","Sugan123$"))


