function cleanalert(){
    $(".alert").empty();
    $(".alert").hide();
}

function showAlertBox(contents){
    $(".alert").append('<span class="glyphicon glyphicon-info-sign"></span>'+contents);
    $(".alert").show();
    setTimeout("cleanalert()", 3000);
}

function StandardPost(url, args) 
{
    var form = $("<form method='post'></form>");
    form.attr({"action":url});
    for(arg in args){
        var input = $("<input type='hidden'>");
        input.attr({"name":arg});
        input.val(args[arg]);
        form.append(input);
    }
    form.submit();
}

function isEmail(str){ 
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/; 
    return reg.test(str); 
} 

$("#forgetpwd").click(function(){
    var user = $("#username").val();
    $("#forgetpwd").attr("href", "/sports/forgetpwd?user="+user);
})

$("#registersign").click(function(){
    $(".alert").empty();

    var containSpecial = /[(\ )]/;
    var passwordcheck = /^[0-9a-zA-Z]*$/g;

    var username = $("#username").val();
    var password = $("#password").val();
    var checkcode = $("#checkcode").val();

    if(isEmail(username) == false){
        showAlertBox('邮箱地址不正确');
        return false;
    }

    if(username == ""){
        showAlertBox('邮箱地址为空');
        return false;
    }

    if(password == ""){
        showAlertBox('密码为空');
        return false;
    }

    if(checkcode == ""){
        showAlertBox('验证码为空');
        return false;
    }

    if(password.length < 6){
        showAlertBox("密码长度不足6位");
        return false;
    }

    if(checkcode.length < 2){
        showAlertBox("验证码错误");
        return false;
    }

    var reg = /checkcode\/(.+?).png$/;
    var regnumber = /checkcode\/(.+?)_number.png$/;
    var checkimg = $("img.checkcodeimg").attr("src").match(reg)[1];
    var checknumberimg = $(".guiderwords img").attr("src").match(regnumber)[1];

    if(containSpecial.test(username)){
        showAlertBox("用户名中包含了空格");
        return false;
    }
    if(passwordcheck.test(password)==false){
        showAlertBox("密码中包含非数字或字母字符");
        return false;
    }

    $.post("/checkregisterinfoconfirm", {code:checkcode, checkcode:checkimg, numbercode:checknumberimg, user:username, pwd:password}, function(data){
        
        if(data['status'] != 0){
            // need to reload check code
            if(data['status'] == -11){
                if(data["flag"] == -3){
                    showAlertBox("用户名已经存在");
                }else{
                    showAlertBox("登陆系统错误");
                }
            }
            else if(data['status'] == -4){
                showAlertBox("验证码错误");
            }else if(data['status'] == -7){
                showAlertBox("用户名已经存在");         
            }
            else{
                showAlertBox("登陆系统错误");
            }
            // forcus update image
            var mstime = new Date();
            $("#checkword img").attr("src", "/static/checkcode/"+ data['ck'][1] +".png?time="+mstime.getSeconds());
            $(".guiderwords img").attr("src", "/static/checkcode/"+ data['ck'][0] +"_number.png?time="+mstime.getSeconds());      
            $("#registersign").removeClass("disabled");
        }else{// return to home page
            if(document.referrer != "" || document.referrer.indexOf("register") < 0){
                // jump to pre page
                //self.location=document.referrer;  
                StandardPost("/sports/personalinfo/basic",{username:username, password:password});        
            }else{
                // if no pre page jump to self info
                StandardPost("/sports/personalinfo/basic",{username:username, password:password});
            }
        }
    }, "json");
    $("#registersign").addClass("disabled");
    return false;
})


$("#loginsign").click(function(){
    $(".alert").empty();

    var containSpecial = /[(\ )]/;
    var passwordcheck = /^[0-9a-zA-Z]*$/g;

    var username = $("#username").val();
    var password = $("#password").val();

    if(username == ""){
        showAlertBox("用户名为空");
        return false;
    }
    if(password == ""){
        showAlertBox("密码为空");
        return false;
    }

    $.post("/checklogininfoconfirm", {user:username, pwd:password}, function(data){
        if(data['status'] != 0){
            
            if(data['status'] == -2){
                if(data['flag'] == -3){
                    showAlertBox("密码错误");
                }else{
                    showAlertBox("登陆系统错误");
                }                
            }
            else{
                showAlertBox("登陆系统错误");
            }
            $("#loginsign").removeClass("disabled");
        }else{// return to home page
            if(document.referrer != ""){
                // jump to pre page
                //self.location=document.referrer;          
                StandardPost("/sports/personalinfo/basic",{username:username, password:password});
            }else{
                // if no pre page jump to self info
                StandardPost("/sports/personalinfo/basic",{username:username, password:password});
            }
        }
    }, "json");
    $("#loginsign").addClass("disabled");
    return false;
})
