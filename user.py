import db
import other

class User:
    def __init__(self,uname="",upass="",petname="",usay="",head_img=""):
        self.uname=uname
        self.upass=upass
        self.petname=petname
        self.usay=usay if usay!="" else "这人很懒，没有留下任何足迹。"
        self.headImg=head_img if head_img !="" else "/static/images/default.jp"

    # 新增一个用户
    def insert_user(self):
        mongo = db.conn_mongodb()
        code_number = 0
        if mongo:
            coll = mongo["im"]["user"]
            user_info = {
                "name":self.uname,
                "password":self.upass,
                "petname":self.petname,
                "say":self.usay,
                "headImg":self.headImg
            }
            coll.insert_one(user_info)
            mess = other.message(1,"新增成功")
            mongo.close()
        else:
            mess = other.message(2,"连接数据失败")
        return mess



    # 检查用户登录
    def find_user_login(self,user_info):
        mongo = db.conn_mongodb()
        if mongo:
            coll = mongo["im"]["user"]
            data = coll.find_one(user_info)
            if data:
                mess = other.message(1,"注册用户")
            else:
                mess = other.message(0,"用户名或密码错误")
            mongo.close()
        else:
            mess = other.message(2,"连接数据库失败")
        return mess


    # 查询一个用户信息
    def find_user_one(self,user_info):
        mongo = db.conn_mongodb()
        if mongo:
            coll = mongo["im"]["user"]
            data = coll.find_one(user_info)
            if data:
                user = {
                    "name":data["name"],
                    "password":data["password"],
                    "petname":data["petname"],
                    "say":data["say"],
                    "headImg":data["headImg"]
                }
                mess = other.message(1,user)
            else:
                mess = other.message(0,"没有数据")
            mongo.close()
        else:
            mess = other.message(2,"连接数据库失败")
        return mess
    

    # 查询所有用户信息(除登录用户)
    def find_user_many(self,loginUser):
        mongo = db.conn_mongodb()
        if mongo:
            coll = mongo["im"]["user"]
            data = coll.find()
            if data:
                userList=[]
                for item in data:
                    if item["name"]!=loginUser:
                        user = {
                            "name":item["name"],
                            "password":item["password"],
                            "petname":item["petname"],
                            "say":item["say"],
                            "headImg":item["headImg"]
                        }
                        userList.append(user)
                mess = other.message(1,userList)
            else:
                mess = other.message(0,"没有数据")
            mongo.close()
        else:
            mess = other.message(2,"连接数据库失败")
        return mess

    # 更新用户信息
    def update_user(self,userName,userPass,petName):
        mongo = db.conn_mongodb()
        if mongo:
            coll = mongo['im']['user']
            user = self.find_user_one({"name":userName})
            if user['status'] == 1:
                if user['result']['petname']==petName:
                    # data = {"$set":{"name":userName,"password":userPass,"petname":petName,"say":user['result']['say'],"headImg":user['result']['headImg']}}
                    data = {"$set":{"password":userPass}}
                    rel = coll.update_one({"name":userName},data)
                    mess = other.message(1,"更新成功")
                    mongo.close()
                else:
                    mess = other.message(0,"密保错误")
            else:
                mess = other.message(0,"没有此用户")
        else:
            mess = other.message(2,"连接数据失败")
        return mess



if __name__=="__main__":
    pass

