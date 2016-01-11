function showmodalmsg(title, content, msgtype){
         $("#myUserInfoModal .modal-body").empty();
         $("#myModalLabel").text(title);
         var hidetype = '<span class="modalhideinfo" style="display:none">'+msgtype+'</span>';
         $("#myUserInfoModal .modal-body").append(hidetype);
         $("#myUserInfoModal .modal-body").append(content);
         if(msgtype == "headimage"){
             $("#myUserInfoModal .modal-footer button:last").hide();
         }else{
             $("#myUserInfoModal .modal-footer button:last").show();
         }
         $("#myUserInfoModal").modal("show");
}

$("#shortcut").click(function(){
    $("#myUserInfoModal .modal-body").empty();
    var showcontent = "<div class='row'>\
        <div class='col-xs-2'>\
        <div class='uploadobject'>\
        <input type='file' id='upfile' name='upfile' accept='.png,.jpg,.jpeg' class='up_input'><span class='up_icon'></span></div> <p><span class='help-block iconnote'>点击图标选择图片</span></p></div>\
        <div class='col-xs-6'><div class='shortcutpreview'></div></div>\
        <div class='col-xs-4'>\
        <button type='button' id='uploadbutton' data-loading-text='上传中' onclick='uploadingshortcut()' autocomplete='off' class='btn btn-default uploadshortcut' style='display:none'><span class='glyphicon glyphicon-cloud-upload'></span><span>上传头像</span></button> </div></div> <br /><div class='img-container'></div>";
    showmodalmsg("编辑头像", showcontent, "headimage");
    initialupfileobject();
});

function imagerotate(deg){
    var degree = deg*10;
    var $image = $('#previewimg');
    $image.cropper('rotate', degree);
}

function cropperpreviewimage(){
    var $image = $('#previewimg'), cropBoxData, canvasData;
    
    cropBoxData = $image.cropper('getCropBoxData');
	canvasData = $image.cropper('getCanvasData');
	$image.cropper('destroy');

    var options = {
        aspectRatio:1.0,
        movable: true,
        center: true,
        preview: '.shortcutpreview',
        crop: function(e){
           
        }
    };

    options.built = function () {
        $image.cropper('setCropBoxData', cropBoxData);
        $image.cropper('setCanvasData', canvasData);
    };
    $image.cropper('destroy').cropper(options);
   
    if($('#previewimg').length > 0){
        if($(".imgrotate").length == 0){
            var bprotate = '<button class="btn btn-primary imgrotate" onclick="imagerotate(1)" id="imgrotateplus"><span class="glyphicon glyphicon-repeat"></span></button>';
            var bmrotate = '<button class="btn btn-primary imgrotate" onclick="imagerotate(-1)" id="imgrotateminus"><span class="glyphicon glyphicon-repeat" style="transform:scaleX(-1)"></span></button>';
            $("#myUserInfoModal .modal-footer").prepend(bprotate);
            $("#myUserInfoModal .modal-footer").prepend(bmrotate);
        }else{
            $(".imgrotate").show();
        }
    }
    //return $image.cropper('getData');
}

function checkimagesize(filepath){
    var MAXSIZE = 1000 * 1024;
	var ERROR_IMGSIZE = "图片大小不能超过3M";
    var filetarget = document.getElementById("upfile").files.item(0);
    if(filetarget == null){
        return -1;
    }
    if( filetarget.size > 0 && filetarget.size < 3*MAXSIZE){
        var src = window.URL.createObjectURL(filetarget);
        //$(".modal-dialog").css("margin-top", "10%");
	    $(".img-container").append('<img src="'+src+'" id="previewimg" style="width:100%" alt="" />');
        $("#previewimg").show();
         if($("#previewimg").length>0){
		    $("#uploadbutton").removeAttr("disabled");										 
	    }
        cropperpreviewimage();
    }else{
        if(filetarget.size < 1){
            alert("文件错误！");
        }else{
            alert(ERROR_IMGSIZE);
        }
        return -1;
    }
    return 0;
}

function ishideimagepreview(flag){
    if(flag){
        $("#previewimg").hide();
        $(".shortcutpreview").hide();
        $(".uploadshortcut").hide();
        $(".imgrotate").hide();
    }else{
        $(".shortcutpreview").show();
        $(".uploadshortcut").show();
        $("#previewimg").show();
        $(".imgrotate").show();
    }
}
     
function initialupfileobject(){
    var upfile = document.getElementById("upfile");
    $("#uploadbutton").attr("disabled", "disabled");
    
    ishideimagepreview(true);

    $(".uploadobject").on('change', '#upfile', function(){
	    $(".img-container").empty();
        if(checkimagesize(this.value) < 0){
            $(".uploadshortcut").hide();
            return;
        }
        ishideimagepreview(false);
    });

    $('#myUserInfoModal').on('hidden.bs.modal', function (e) {
        var $image = $('#previewimg'), cropBoxData, canvasData;
        $("#myUserInfoModal .modal-dialog").css("margin-top", "50%");
        if($image.length == 0){
            return;                                         
        }else{
            cropBoxData = $image.cropper('getCropBoxData');
		    canvasData = $image.cropper('getCanvasData');
            $image.cropper('clear');
		    $image.cropper('destroy');
            $image.remove();
        }
        ishideimagepreview(true);
        $(".img-container").empty();
    });
}

function ajaxFileUpload(cropinfo) {
    $.ajax({
        type:'POST',
        url:'/sports/personalinfo/basic/uploadshortcut',
        data:cropinfo,
        dataType: 'JSON',
        success: function(data, status){
            try{
                var jdata = data;
                if (jdata.status != 'error') {
                    //$(".img-container").append('<img src="" id="resultimg" style="width:20em" alt="" />');
                    $("#myUserInfoModal").modal('hide');
                    $("#resultimg").attr("src", jdata.imglink+"?datems="+Date("ms"));
                    $("#shortcut img").attr("src", jdata.imglink+"?datems="+Date("ms"));
                    $("img.usershortcut").attr("src", jdata.imglink+"?datems="+Date("ms"));
                }else{
                    $(".img-container").append("<p>服务器错误，请重试！</p>");
            }}catch(e){
                $(".img-container").append("<p>"+e+"</p>");
            }
            $(".imgrotate").hide();
            $(".uploadshortcut").hide();
        },
        error: function(data, status, e){
            $(".img-container").append("<p>"+e+"</p>");
        }
    });
   
    $("#loader").shCircleLoader('destroy');
    $("#uploadbutton").button('reset');
    $(".img-container").empty();
    return false;
}

function uploadingshortcut(){
    var $image = $('#previewimg'), cropBoxData, canvasData;
    //var cropinfo = $image.cropper('getData');
    var cropinfo = {};
    cropinfo['usermd5'] = $("#regcode span").text();
    //cropBoxData = $image.cropper('getCropBoxData');
    //canvasData = $image.cropper('getCanvasData');
    var result = $image.cropper("getCroppedCanvas", {height:90, width:160});
    $image.cropper('clear');
	$image.cropper('destroy');
    if(result){
        cropinfo['imgBase64'] = result.toDataURL('image/png');
        $(".img-container").empty();
        $(".img-container").append('<div id="loader" style="width: 100px; height: 100px"></div>');
        $('#loader').shCircleLoader();
        ajaxFileUpload(cropinfo);
    }
}

function areaquery(){
    var areainput = $("#areainput").val();
    var widthselect = $("#areainput").css("width");
    areainput = areainput.replace(/\s/g,"");
    if(areainput.length == 0){
        return;
    }
    $(".modal-body select").remove();
    $.post("/sports/personalinfo/basic/querycityinfo", {keywords: areainput}, function(data){
        if(data['status'] == 0){
            var options;
            for(var i=0; i<data['data'].length; i++){
                var city = data['data'][i][0];
                var provice = data['data'][i][1];
                options += "<option style='font-size:2em;'>"+city+"   "+provice+"</option>";
            }
            if(options != null){
                var selectobj = "<select size='6' style='width:"+widthselect+"'>"+options+"</select>";
                $(".modal-body .input-group").after(selectobj);
                $(".modal-body select option").click(function(){
                    $("#areainput").val(this.text);
                });
            }
        }
    }, "json");
    
}

$(".savebtn").click(function(){
    var modaltype = $(".modalhideinfo").text();
    var alertbox = '<div class="alert alert-warning" id="modalmsgbox" role="alert"></div>';
    var tdata;
    $("#modalmsgbox").remove();
    
    if(modaltype == "words"){
      var tdata = $("#wordsinput").val();
      if(tdata.length == 0){
        $("#myUserInfoModal .modal-body").append(alertbox);
        $("#modalmsgbox").removeClass("alert-warning");
        $("#modalmsgbox").addClass("alert-danger");
        $("#modalmsgbox").append("<strong>错误！</strong>您什么也没有填！");
        return;
      }else{
        var blankreg = /\s/g;
        if(blankreg.test(tdata)){
           $("#myUserInfoModal .modal-body").append(alertbox);
           $("#modalmsgbox").append("<strong>警告！</strong>不可包含空格！");
           return;
        }
      }
    }
    if(modaltype == "sex"){
        tdata = $(".radio input:checked").siblings('span').text();
    }
    if(modaltype == "area"){
        tdata = $("#areainput").val();
    }
    if(modaltype == "nickname"){
        tdata = $("#shortnameinput").val();
    }
    if(modaltype == "contact"){
        var tmp = {};
        re= /^(13[0-9]{9})|(15[89][0-9]{8})$/;
        tmp['name'] = $("#contactname").val();
        var pnumber = $("#contactphonenumber").val();
        if(re.test(pnumber)){
            tmp['phonenumber'] = $("#contactphonenumber").val();
        }
        tmp['address'] = $("#contactaddress").val();
        tdata = JSON.stringify(tmp);
    }
    if(modaltype == "headimage"){
        // update head link info
        tdata = null;
        return;
    }
    $("#modalmsgbox").remove();
    $.post("/sports/personalinfo/basic/updatepersonalinfo", {msgtype: modaltype, username: $("#regcode span").text(), dataobj: tdata }, 
            function(data){
                if(data['status'] == 0){
                    $("#myUserInfoModal").modal('hide');
                    if(modaltype == "sex"){
                        $("#sex span").text(tdata);
                    }
                    if(modaltype == "contact"){
                        $("#contact span").text('查看详情');
                    }
                    if(modaltype == "nickname"){
                        $("#shortname span").text(tdata);
                        $(".qrnickname").text(tdata);
                    }
                    if(modaltype == "words"){
                        $("#words span").text(tdata);
                    }
                    if(modaltype == "area"){
                        $("#area span").text(tdata.split(" ")[0]);
                    }
                }else{
                    var alert = '<div class="alert alert-warning" id="modalmsgbox" role="alert"><strong>警告！</strong>填写信息错误！code:'+data['status']+'</div>';
                    $(".modal-body").append(alert);
                }
            }, "json");
});


$("#words").click(function(){
    var content = '<div class="form-group">\
        <input type="text" class="form-control" id="wordsinput" maxlength="30" value="'+$("#words span").text().replace(/(^\s+)|(\s+$)/g,"")+'" placeholder="30字的自我宣言">\
        <p class="help-block">展现自我，让别人更了解你</p></div>';
    showmodalmsg("个人签名", content, "words");

});

$("#area").click(function(){
    var content = '<div class="input-group">\
        <input type="text" class="form-control" id="areainput" maxlength="30" value="'+$("#area span").text().replace(/\s/g, "")+'" placeholder="省份 城市（或区）">\
        <span class="input-group-btn"><button class="btn btn-primary" id="cityquery" onclick="areaquery()" type="button"><span>搜索城市</span></button></span>\
        </div><p class="help-block">区域能帮助我们给你提供跟周到的服务。</p>';
    showmodalmsg("填写区域", content, "area");
});

$("#sex").click(function(){
    var content;
    if($("#sex span").text() == '男'){
        content = '<div class="radio">\
        <label><input type="radio" name="sexradio" id="optionsRadios1" value="man" checked><span>男</span></label>\
      </div>\
      <div class="radio">\
        <label><input type="radio" name="sexradio" id="optionsRadios2" value="female"><span>女</span></label></div>';         
    }else{
        content = '<div class="radio">\
        <label><input type="radio" name="sexradio" id="optionsRadios1" value="man"><span>男</span></label>\
      </div>\
      <div class="radio">\
        <label><input type="radio" name="sexradio" id="optionsRadios2" value="female" checked><span>女</span></label></div>';
    }
    
    showmodalmsg("性别", content, "sex");
});


$("#shortname").click(function(){
    var content = '<div class="form-group">\
        <input type="text" class="form-control" id="shortnameinput" maxlength="10" value="'+$("#shortname span").text().replace(/\s/g, "")+'">\
        <p class="help-block">一个好的昵称容易让别人记住你。</p></div>';
    showmodalmsg("更改昵称", content, "nickname");
});

$("#contact").click(function(){
         var content = '<div class="form-group">\
        <label for="contactname">姓名</label>\
        <input type="text" class="form-control" id="contactname" value="'+contactinfo['name']+'" maxlenght="10" placeholder="姓名">\
      </div>\
      <div class="form-group">\
        <label for="contactphonenumber">手机号码</label>\
        <input type="text" class="form-control" id="contactphonenumber" value="'+contactinfo['phone']+'" maxlenght="10" placeholder="11位手机号码">\
      </div>\
      <div class="form-group">\
        <label for="contactaddress">详细地址</label>\
        <input type="text" class="form-control" id="contactaddress" value="'+contactinfo['address']+'" maxlenght="100" placeholder="街道门牌信息">\
      </div>';
    showmodalmsg("联系方式", content, "contact");
});
