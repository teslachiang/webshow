function dropdownmenu(thisobj){

    if($(".dropdown-menu").is(":hidden") == false){
        $(".dropdown-menu").hide();
    }else{
        $(".dropdown-menu").show();
    }
    if(thisobj.find("ul").length >  0){
        return;
    }
    var menu = '<ul class="dropdown-menu">\
        <li><a href="#" onclick="return dropsubmenuclick($(this))"><span class="glyphicon glyphicon-edit"></span><span class="dropmenustext" name="edit">编辑</span></a></li>\
<li><a href="#" onclick="return dropsubmenuclick($(this))"><span class="glyphicon glyphicon-trash"></span><span class="dropmenustext" name="delete">删除</span></a></li>';
       var isclosed;
       if($(".subjectisclosed").text() == "False"){
           isclosed = '<li><a href="#" onclick="return dropsubmenuclick($(this))"><span class="glyphicon glyphicon-off"></span><span class="dropmenustext" name="close">关闭</span></a></li></ul>';
        }else{
           isclosed = '<li><a href="#" onclick="return dropsubmenuclick($(this))"><span class="glyphicon glyphicon-refresh"></span><span class="dropmenustext" name="open">开启</span></a></li></ul>';
        }
    menu += isclosed;
    thisobj.append(menu);

    $(".dropdown-menu").show();
}

$(".removemsgbox .btn:last-child").click(function(){
   // cancel remove msg box
    $(".removemsgbox").hide();
});

$(".removemsgbox .btn:first-child").click(function(){
   // execute remove msg box
    $(".removemsgbox").hide();
    var subject = $(".providedsubject").text();
    var username = $(".usernamehide").text();

    if(subject.length == 0 || username.length == 0){
        return;
    }
    removetask(username, subject);
});

function dropsubmenuclick(thisobj){
   // $(".dropdown-menu").hide();

    var name = thisobj.find(".dropmenustext").attr("name");
    var subject = $(".providedsubject").text();
    var username = $(".usernamehide").text();
    if(name == "edit"){
        window.location.href = "/sports/personalsocial/editsubject?username="+username+"&subject="+subject;
    }else if(name == "close"){
        window.location.href = "/sports/personalsocial/toggleprovidesubject?username="+username+"&subject="+subject+"&isclose=1";
    }else if(name == "delete"){
        $(".removemsgbox").show();
    }else if(name == "open"){
        window.location.href = "/sports/personalsocial/toggleprovidesubject?username="+username+"&subject="+subject+"&isclose=0";
    }
    return false;
}


function removetask(username, subject){
    $.post("/sports/personalsocial/removesubjectajax", {username:username, subject:subject}, function(data){
        if(data['status'] == 0){
            window.location.href = "/sports/personalsocial/providesubject";
        }else{
            alert("remove suject failed!!! code:"+data['status']);
        }
    }, "json");
    return false;
}

