$(function(){
    $(".titlewell .title").text("添加科目");
    $(".titlewell").prepend('<span class="glyphicon glyphicon-arrow-left titleback"\
                            onClick="javascript :history.back(-1);" style="font-size:5em; float:left; padding-top:0.25em"></span>');
    $("#subjectcontent").qeditor({});
    var description = "<b>科目经验介绍：</b><p>（运动科目经验时间）</p><p><br></p><p><b>联系方式：</b></p><p>（填写手机号，或其它通讯方式，方便参与者联系）</p><p><br></p><p><b>个人特色：</b></p><p>（个人在这个项目上面有那些优势）</p><p><br></p>";
    $(".qeditor_preview").html(description);
});

$(".searchblock").click(function(){
    var inputstring = $(this).parent().siblings('input').val();
    $(".titlemsginfo span").remove();
    if(inputstring != ""){
      $("#myModal").modal('show');
      $("#suggestId").val(inputstring);

      $.post("/sports/personalsocial/queryblockajax", {key:inputstring}, function(data){
          if(data['status'] < 0){
              alert("query error1!!!"+data['status']);
          }else{
              $(".searchresult").empty();
              $(".searchresult").append('<hr>');
              $(".searchresult").append('<ul class="list-group"></ul>');
              if(data['data'].length == 0){
                  var li = '<li class="list-group-item">没有找到相应的科目</li>';
                  $(".searchresult ul").append(li);
                  return;
              }
              for(var i=0; i<data['data'].length; i++){
                  var li = '<li class="list-group-item" onclick="listitemclik($(this))">'+data['data'][i]+'</li>';

                  $(".searchresult ul").append(li);
              }
          }
      }, "json");
    }else{
        $(".titlemsginfo").append('<span class="tmpinfo" style="color:red; font-size:0.5em"> (输入内容为空)</span>');
    }
});


function listitemclik(thisobj){
    var $obj = thisobj;
    $("#suggestId").val($obj.text());
    $(".gameaddress").val($obj.text());
}

$("#submitsubject").click(function(){
    var subjectname = $(".gameaddress").val();
    var descripthtml = $(".qeditor_preview").html();
    var descripttext = $(".qeditor_preview").text();
    var blankpatt = /\s+/g;

    var flag = true;
    $(".titlemsginfo").text("*");
    $(".descriptionmsginfo").text("*");
    if(subjectname.replace(blankpatt, "").length < 2){
        $(".titlemsginfo").text("(请通过搜索分类填入正确的科目名称)");
        flag = false;
    }

    if(descripttext.replace(blankpatt, "").length < 10){
        $(".descriptionmsginfo").text("(您的描述过于简单)");
        flag = false;
    }

    if(flag == true){
        $.post("/sports/personalsocial/submitsubjectajax", {subject: subjectname.replace(blankpatt, ""), descript: descripthtml}, 
               function(data){
                   if(data['status'] == 0){
                       // success
                       window.location.href="/sports/personalsocial/providesubject";
                   }else if(data['status'] == -3){
                       $(".titlemsginfo").text("(请通过搜索分类填入正确的科目名称)");
                   }else if(data['status'] == -2){
                       // need to login
                       window.location.href="/sports/login";
                   }else{
                       alert("系统错误！code:"+data["status"]);
                   }
               }, "json");
    }
    return false;
});
