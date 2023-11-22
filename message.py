import db
import other


class Message:
    def __init__(self,from_user,to_user="",content="",status=1):
        self.from_user=from_user
        self.to_user=to_user
        self.content=content
        self.status=status
        self.datetime=other.get_datetime()

    # 新增消息
    def insert_message(self):
        mongo = db.conn_mongodb()
        if mongo:
            coll = mongo["im"]["messages"]
            data = {
                "fromUser":self.from_user,
                "toUser":self.to_user,
                "content":self.content,
                "status":self.status,
                "datetime":self.datetime
            }
            coll.insert_one(data)
            mess = other.message(1,"新增成功")
            mongo.close()
        else:
            mess = other.message(2,"连接数据失败")
        return mess


    # 查询最后n条聊天数据
    def find_message_many(self,data={},number=50):
        mongo = db.conn_mongodb()
        if mongo:
            coll = mongo["im"]["messages"]
            data = coll.find(data).sort("_id",-1).limit(number) if number > 0 else coll.find(data)
            mess_list = []
            for item in data:
                mess = {
                    "fromUser":item["fromUser"],
                    "toUser":item["toUser"],
                    "content":item["content"],
                    "status":item["status"],
                    "datetime":item["datetime"]
                    }
                mess_list.append(mess)
            mess = other.message(1,mess_list)
            mongo.close()
            return mess
        else:
            mess = other.message(2,"连接数据库失败")
        return mess




if __name__=="__main__":
    pass
    # messobj = Message("wujiang")
    # data = messobj.find_message_many({"toUser":""},50)
    # print(data)
    # for i in data:
    #     print(i)

