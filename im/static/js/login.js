$(document).ready(function() {
    $(".register>a").click(function(){
        $(".login-box").css("display","none");
        $(".register-box").css("display","block");
    });

    $(".register>span>a").click(function(){
        $(".login-box").css("display","none");
        $(".reset-box").css("display","block");
    });

    $("body").keypress(function(event){
        if(event.key=="Enter"){
            if($(".login-box").css("display")=="block"){
                login();
            }
            if($(".register-box").css("display")=="block"){
                register();
            }
            if($(".reset-box").css("display")=="block"){
                resetpass();
            }
        }
    })

    $(".textCode img").attr('src', "/getImg");

    $(".textCode img").click(function(){
        $(".textCode img").attr('src', "/getImg?" + Math.random());
    })
})

/* 登录判断 */
function login() {
    $.ajax({
        type: "POST",
        url: "/login",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "userName": $("input[name=loginUserName]").val(),
            "userPass": $("input[name=loginUserPass]").val()
        }),
        success: function(message) {
            var status = message["status"];
            if(status==1){
                $.cookie('name', $("input[name=loginUserName]").val(),{path:'/'});
                window.location.href="/index";
            }else{
                alert(message["result"]);
            }
        },
        error: function(message) {
            console.log(message)
        }
    })
}

/* 注册用户 */
function register(){
    $.ajax({
        type: "POST",
        url: "/reg",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "userName": $("input[name=registerUserName]").val(),
            "userPass": $("input[name=registerUserPass]").val(),
            "code": $("input[name=code]").val(),
            "petName": $("input[name=petName]").val()
        }),
        success: function(message) {
            var status = message["status"];
            if(status===1){
                $(".register-box").css("display","none");
                $(".login-box").css("display","block");
            }else{
                alert(message["result"])
            }
        },
        error: function(message) {
            console.log(message)
        }
    })
}

function resetpass(){
    $.ajax({
        type: "POST",
        url: "/reset",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "userName": $("input[name=resetname]").val(),
            "userPass": $("input[name=resetpass]").val(),
            "petName": $("input[name=resetpetname]").val()
        }),
        success: function(message) {
            var status = message["status"];
            if(status===1){
                $(".reset-box").css("display","none");
                $(".login-box").css("display","block");
            }else{
                alert(message["result"])
            }
        },
        error: function(message) {
            console.log(message)
        }
    })
}
