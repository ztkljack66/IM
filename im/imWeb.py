from flask import Flask,request,make_response,Response,session
from flask import render_template
from flask import jsonify
from flask_cors import CORS
from io import BytesIO
from user import User
from message import Message
import other


app=Flask(__name__)
app.secret_key=other.SECRET_KEY
CORS(app,supports_credentials=True)

@app.route("/",methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/index",methods=["GET"])
def index():
    return render_template("index.html")

# 登录检查
@app.route("/login",methods=["POST"])
def login_check():
    if request.method == "POST":
        user_info = request.get_json()
        user_name = user_info.get("userName")
        user_pass = user_info.get("userPass")
        data = {"name":user_name,"password":user_pass}
        userObj = User(user_name,user_pass,"","","")
        result = userObj.find_user_login(data)
        return jsonify(result)
    else:
        return jsonify({"status":0,"result":"请求错误"})

# 注册
@app.route("/reg",methods=["POST"])
def register():
    base_code = str(session.get("imageCode"))
    if request.method == "POST":
        user_info = request.get_json()
        userName = user_info.get("userName")
        userPass = user_info.get("userPass")
        code = user_info.get("code")
        petName = user_info.get("petName")
        userObj = User(userName,userPass,petName)
        if code.lower() == base_code.lower():
            user = userObj.find_user_one({"name":userName})
            if user["status"] == 0:
                result = userObj.insert_user()
                return jsonify(result)
            else:
                return jsonify(user)
        else:
            return jsonify({"status":0,"result":"验证码错误"})
    else:
        return jsonify({"status":0,"result":"请求错误"})

# 获得验证码图片
@app.route("/getImg",methods=["GET"])
def getImg():
     image, code = other.create_image()
     buf = BytesIO()    # 图片以二进制形式写入
     image.save(buf,format='jpeg')
     buf_str = buf.getvalue()
     response = make_response(buf_str)   # 把buf_str作为response返回前端，并设置首部字段
     response.headers['Content-Type'] ='image/gif'
     session['imageCode'] = code   # 将验证码字符串储存在session中
     return response

# 重置密码
@app.route("/reset",methods=["POST"])
def reset_pass():
    if request.method == "POST":
        user_info = request.get_json()
        userName = user_info.get("userName")
        userPass = user_info.get("userPass")
        petName = user_info.get("petName")
        userObj = User(userName)
        rel = userObj.update_user(userName,userPass,petName)
        return jsonify(rel)
    else:
        return jsonify({"status":0,"result":"请求错误"})
    

# 查询一个用户信息
@app.route("/getUser",methods=["POST"])
def get_user():
    if request.method == "POST":
        user_info = request.get_json()
        userName = user_info["name"]
        userObj = User(userName,"","","","")
        userInfo = userObj.find_user_one({"name":userName})
        return jsonify(userInfo)
    else:
        return jsonify({"status":2,"result":"请求错误"})

# 查询多个用户信息
@app.route("/ulist",methods=["POST"])
def user_list():
    if request.method == "POST":
        user_info = request.get_json()
        userName = user_info["fromUser"]
        userObj = User("","","","","")
        data = userObj.find_user_many(userName)
        return jsonify(data)
    else:
        return jsonify({"status":2,"result":"请求错误"})


# 发送群聊消息
@app.route("/sendPubMess",methods=["POST"])
def sendPubMess():
    if request.method=='POST':
        mess_info =request.get_json()
        userName = mess_info.get("fromUser")
        message = mess_info.get("message")
        if userName != "":
            messObj = Message(from_user=userName,content=message)
            result = messObj.insert_message()
            return jsonify(result)
        else:
            return jsonify({"status":0,"result":"relogin"})
    else:
        return jsonify({"status":2,"result":"请求错误"})

# 发送私密消息
@app.route("/sendPriMess",methods=["POST"])
def sendPriMess():
    if request.method=='POST':
        mess_info =request.get_json()
        fromUser = mess_info.get("fromUser")
        toUser = mess_info.get("toUser")
        message = mess_info.get("message")
        if fromUser == "":
            return jsonify({"status":0,"result":"relogin"}) 
        if toUser =="":
            return jsonify({"status":0,"result":"who"})
        messObj = Message(from_user=fromUser,to_user=toUser,content=message,status=0)
        result = messObj.insert_message()
        return jsonify(result)
    else:
        return jsonify({"status":2,"result":"请求错误"})

# 查询群聊消息
@app.route("/pubMess",methods=["POST"])
def pubMess():
    if request.method=='POST':
        fromUser = request.get_json().get("fromUser")
        messObj = Message(fromUser)
        mess_data = messObj.find_message_many({"toUser":""},50)
        return jsonify(mess_data)
    else:
        return jsonify({"status":0,"result":"请求错误"})

# 查询私密消息
@app.route("/priMess",methods=["POST"])
def priMess():
    if request.method=='POST':
        fromUser=request.get_json().get("fromUser")
        toUser = request.json.get("toUser")
        messObj = Message(fromUser,toUser)
        mess_data = messObj.find_message_many({"$or":[{"fromUser":fromUser,"toUser":toUser},{"fromUser":toUser,"toUser":fromUser}]},50)
        return jsonify(mess_data)
    else:
        return jsonify({"status":2,"result":"请求错误"})

if __name__ == "__main__":
    app.run('0.0.0.0','80',debug=True)
