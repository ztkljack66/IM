var pubTime;
var priTime;
var fromUser;
var toUser;


// ********************************* 消息展示 ******************************************
// 展示群聊消息
function showPubMess(messData){
    var status = messData["status"];
    var data = messData["result"];
    if(status==1){
        mess_html="";
        $.each(data,function(index,val){
            if(val["fromUser"] == fromUser){
                mess_html += "<div style='text-align: right;'><p>" + val["datetime"]+"  "+val["fromUser"]+"</p><p style='color:green;'>"+val["content"]+"</p></div>";
            }else{
                mess_html += "<div><p>" + val["fromUser"]+"  "+val["datetime"]+"</p><p>"+val["content"]+"</p></div>";
            }
        })
        $(".box-group-left-middle").html(mess_html);
    }
}
// 展示私密消息
function showPriMess(messData){
    var status = messData["status"];
    var data = messData["result"];
    if(status==1){
        mess_html="";
        $.each(data,function(index,val){
            if(val["fromUser"] == fromUser){
                mess_html += "<div style='text-align: right;'><p>" + val["datetime"]+"  "+val["fromUser"]+"</p><p style='color:green;'>"+val["content"]+"</p></div>";
            }else{
                mess_html += "<div><p>" + val["fromUser"]+"  "+val["datetime"]+"</p><p>"+val["content"]+"</p></div>";
            }
        })
        $(".box-private-middle").html(mess_html);
    }
}

// ********************************** 查询消息 ******************************************
// 获取群聊消息数据
function getPubMessage(){
    $.ajax({
        type: "POST",
        url: "/pubMess",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "fromUser":fromUser
        }),
        success: function(message) {
            showPubMess(message);
        },
        error: function(message) {
            console.log(message)
        }
    })
}
// 获取私密消息数据
function getPriMessage(){
    $.ajax({
        type: "POST",
        url: "/priMess",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "fromUser":fromUser,
            "toUser":toUser
        }),
        success: function(message) {
            showPriMess(message);
        },
        error: function(message) {
            console.log(message)
        }
    })
}

// ********************************** 发送消息 ******************************************
// 发送群聊数据
function sendPubMess(){
    $.ajax({
        type: "POST",
        url: "/sendPubMess",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "fromUser":$(".box-group-right-top>p:last").text(),
            "message": $(".box-group-left-bottom textarea").val()
        }),
        success: function(message) {
            var status = message["status"];
            var data = message["result"]
            if(status==1){
                getPubMessage();
                $(".box-group-left-bottom textarea").val("");
            }else{
                alert(message["result"]);
            }
        },
        error: function(message) {
            console.log(message)
        }
    })
    $(".message").val("");
}
// 发送私密数据
function sendPriMess(){
    $.ajax({
        type: "POST",
        url: "/sendPriMess",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "fromUser":$(".box-group-right-top>p:last").text(),
            "toUser":$(".box-private-top div:eq(0)").text(),
            "message": $(".box-private-bottom textarea").val()
        }),
        success: function(message) {
            var status = message["status"];
            var data = message["result"]
            if(status==1){
                getPriMessage();
                $(".box-private-bottom textarea").val("");
            }else{
                alert(message["result"]);
            }
        },
        error: function(message) {
            console.log(message)
        }
    })
    $(".message").val("");
}

// 获取用户信息
function getUserList(){
    $.ajax({
        type: "POST",
        url: "/ulist",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "fromUser":fromUser,
        }),
        success: function(message) {
            if(message["status"]==1){
                data = message["result"];
                user_html="";
                $.each(data,function(key,val){
                    user_html+="<p style='cursor:pointer;margin-top:5px'>"+val["name"]+"</p>"
                })
                $(".box-group-right-bottom marquee").html(user_html);
            }
        },
        error: function(message) {
            console.log(message)
        }
    })
}

// 注销
function logout(){
    $.cookie('name', null, {path:'/'});
    window.location.href="/";
}

// 返回群聊
function backGroup(){
    $(".box-private").css("display","none");
    $(".box-group").css("display","block");
    clearTimeout(pubTime);
    clearTimeout(priTime);
    pubTime = setInterval(function(){getPubMessage()}, 2000);
}


// 加载赋值
$(document).ready(function() {
    // 获取浏览器cookie中登录用户名
    var my_cookie = $.cookie('name');
    if(typeof my_cookie == "undefined" || my_cookie=="null" || my_cookie==null){
        window.location.href="/";
    }else{
        fromUser=my_cookie;
        $(".box-group-right-top label").text(fromUser);
    }

    $(".box-private").css("display","none");

    // 获取所有用户信息
    getUserList();

    // 定时刷新消息
    if($(".box-group").css("display")=="block"){
        pubTime = setInterval(function(){getPubMessage()}, 2000);
    }
    if($(".box-private").css("display")=="block"){
        priTime = setInterval(function(){getPriMessage()}, 2000);
    }


    // 回车键发送群聊消息
    $("#pubMessage").keypress(function(event){
        if(event.key=="Enter"){
            sendPubMess();
            $(".box-group-left-bottom textarea").val("");
        }
    })

    // 回车键发送私聊消息
    $("#priMessage").keypress(function(event){
        if(event.key=="Enter"){
            sendPriMess();
            $(".box-private-bottom textarea").val("");
        }
    })
})


// 获取用户信息
$(document).on("click",".box-group-right-bottom marquee p", function(){
    toUser=$(this).text()
    $(".box-private").css("display","block");
    $(".box-group").css("display","none");
    $(".box-private-top div:eq(0)").html(toUser);
    getPriMessage();
    clearTimeout(pubTime);
    clearTimeout(priTime);
    priTime = setInterval(function(){getPriMessage()}, 2000);
})
