var imagespan = '<div class="uploadimage"><span class="glyphicon glyphicon-picture"></span><input type="file" accept=".png,.jpg,.jpeg" onchange="uploadimage($(this))"/></div>';

var currentimg;
function removeimage(imageobj){
    $(".sports_msgbox").show();
    currentimg = imageobj;
}

$(".removemsgbox #alertremoved").click(function(){
    currentimg.remove();
    $(".articleimageadd").append(imagespan);
   // $(".removemsgbox").hide();
});

// $(".removemsgbox a:last-child").click(function(){
//     $(".removemsgbox").hide();
// });
function quitnewarticle(){
    $("#mypublisharticleModal .modal-body").empty();
    var msgcontent = '<p>您确定退出发表文章？</p>';
    $("#mypublisharticleModal .modal-title").text("提醒");
    $("#mypublisharticleModal .modal-body").append(msgcontent);
    $("#mypublisharticleModal .modal-footer .modalfootersure").show();
    $("#mypublisharticleModal .modal-footer .modalfootersure").attr("onclick", "javascript:history.back(-1)");
    $("#mypublisharticleModal").modal('show');
}


function selectfriends(flag, atsomeone){
    if(atsomeone == 1){
        localStorage['atwhosee'] = "yes";
    }else{
        localStorage['opentowho'] = "part";
    }
    window.location.href = "/sports/personalsocial/addnewfriends?type=circle&flag="+flag+"&to="+atsomeone;
}

function opentowhomodal(){
    $("#mypublisharticleModal .modal-title").text("对谁开放");
    $("#mypublisharticleModal .modal-body").empty();
    var msgcontent = '<ul class="list-group">\
        <li class="list-group-item"><span>公开</span><input type="radio" opentowho="all" class="forwhoradio" name="forwho" /><span class="help-block">(对所有人可见)</span></li>\
  <li class="list-group-item"><span>私人</span><input type="radio" opentowho="private" class="forwhoradio" name="forwho" /><span class="help-block">(仅自己可见)</span> </li>\
  <li class="list-group-item"><span>部分好友</span><input type="radio" opentowho="part" class="forwhoradio" name="forwho" onclick="selectfriends(0, -1)" /><span class="help-block">(指定部分好友可见)</span> </li>\
  <li class="list-group-item"><span>不给谁看</span><input type="radio" opentowho="part" class="forwhoradio" name="forwho" onclick="selectfriends(1, -1)" /><span class="help-block">(指定部分好友不可见)</span> </li></ul>';
    
    $("#mypublisharticleModal .modal-body").append(msgcontent);

    if(localStorage['opentowho'] == "all" || localStorage['opentowho'] == undefined){
        $("#mypublisharticleModal .modal-body .list-group li:first-child input").attr("checked", true);
    }else if(localStorage['opentowho'] == "private"){
        $("#mypublisharticleModal .modal-body .list-group li:nth-child(2) input").attr("checked", true);
    }else{
        if(localStorage['towhosee'] != undefined || localStorage['towhosee'] != ""){
            $("#mypublisharticleModal .modal-body .list-group li:nth-child(3) input").attr("checked", true);  
        }
        if(localStorage['blocktosee'] != undefined || localStorage['blocktosee'] != ""){
            $("#mypublisharticleModal .modal-body .list-group li:nth-child(4) input").attr("checked", true);
        }
    }


    $("#mypublisharticleModal .modal-footer .modalfootersure").hide();
    $("#mypublisharticleModal").modal('show');
}

function alerttoseemodal(){
    selectfriends(0, 1);
}

function binaryToBlob(data) {
    var arrayBuffer = new ArrayBuffer(data.length);
    var arr = new Uint8Array(arrayBuffer);
    for(var i = 0, l = data.length; i < l; i++) {
        arr[i] = data.charCodeAt(i);
    }
    var dataView = new DataView(arrayBuffer);
    var blob = new Blob([dataView], { type: "image/png" });
   
    return blob;
};

function dataUrlToBlob(dataurl) {
    // data:image/jpeg;base64,xxxxxx
    var datas = dataurl.split(',', 2);
    var blob = binaryToBlob(atob(datas[1]));
    blob.fileType = datas[0].split(';')[0].split(':')[1];
    blob.name = blob.fileName = 'pic.' + blob.fileType.split('/')[1];
    return blob;
};

function getImageBlob(url) {
    var r = new XMLHttpRequest();
    try{
    r.open("GET", url, true);
    // 详细请查看: https://developer.mozilla.org/En/XMLHttpRequest/Using_XMLHttpRequest#Receiving_binary_data
    // XHR binary charset opt by Marcus Granado 2006 [http://mgran.blogspot.com]
    }catch(e){
        
    }
    r.overrideMimeType('text/plain; charset=x-user-defined');
    r.send(null);
    var blob = binaryToBlob(r.responseText);
    blob.name = blob.fileName = url.substring(url.lastIndexOf('/') + 1);
    blob.fileType = "image/jpeg"; //"image/octet-stream";
    return blob;
};

function blobimageprocess(imgobj){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', imgobj.attr("src"));
    // = ../img/logo.png

    xhr.responseType = 'arraybuffer';
    
    xhr.onload = function(e) {
        if (this.status == 200) {
            var uInt8Array = new Uint8Array(this.response);
            var i = uInt8Array.length;
            var biStr = new Array(i);
            while (i--)
            { biStr[i] = String.fromCharCode(uInt8Array[i]);
            }
            var data = biStr.join('');
            var base64 = window.btoa(data);
  
            var blobimg = "data:"+imgobj.attr("type")+";base64,"+base64;
            ajaxFileUpload({'imagebase64': blobimg});
        }
    };

    xhr.send();
}

function uploadimage(imagefileobj){
    var imgfile = imagefileobj[0].files[0];
    var imgsrc = window.URL.createObjectURL(imgfile);
  
    imagefileobj.siblings('span').remove();
    imagefileobj.parent().find('img').remove();
    imagefileobj.parent().prepend('<img type="'+imgfile.type+'" src="'+imgsrc+'" onclick="removeimage($(this))"></img>');
    imagefileobj.remove();
}
function ajaxFileUpload(cropinfo) {
    $.ajax({
        type:'POST',
        url:'/sports/personalsocial/circle/uploadarticle',
        data:cropinfo,
        dataType: 'JSON',
        success: function(data, status){
            try{
                var jdata = data;
                if (jdata.status == 0) {
                    //$(".img-container").append('<img src="" id="resultimg" style="width:20em" alt="" />');
                    $("#myUserInfoModal").modal('hide');
                    $("#resultimg").attr("src", jdata.imglink+"?datems="+Date("ms"));
                    $("#shortcut img").attr("src", jdata.imglink+"?datems="+Date("ms"));
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
    return false;
}

function publisharticle(){
    var artinfo = {};
    artinfo['content'] = $(".articletextarea textarea").val();

    if(localStorage['atwhosee'] == "yes"){
        artinfo['atwhosee'] = localStorage['atwhoseejson'];
    }
    if(localStorage['opentowho'] == "part"){
       if(localStorage['towhosee'] != undefined || localStorage['towhosee'] != ""){
           artinfo['towhosee'] = localStorage['towhosee'];           
       }
       if(localStorage['blockwhosee'] != undefined || localStorage['blockwhosee'] != ""){
           artinfo['blockwhosee'] = localStorage['blockwhosee'];           
       }

    }
    $.post("/sports/personalsocial/circle/uploadarticle", artinfo, function(data){
        
    }, "json");
    $(".uploadimage img").each(function(){
        blobimageprocess($(this));
    });
    localStorage.clear();
}

$(function(){
    $(".titlewell").prepend('<span class="glyphicon glyphicon-arrow-left titleback"\
                            onClick="quitnewarticle()"></span><span class="glyphicon glyphicon-ok-circle" onClick="publisharticle()"></span>');
    
    for(var i=0; i<8; i++){
       $(".articleimageadd").append(imagespan);
    }
    if(localStorage['opentowho'] == "all" || localStorage['opentowho'] == undefined){
        $(".opentowhoselected").text("公开");
    }else if(localStorage['opentowho'] == "private"){
        $(".opentowhoselected").text("私人");
    }else{
        $(".opentowhoselected").text("部分");
    }
    $('#mypublisharticleModal').on('hidden.bs.modal', function (e) {
        $("#mypublisharticleModal .modal-body .forwhoradio").each(function(){
            if($(this).is(":checked") == true){
                localStorage['opentowho'] = $(this).attr("opentowho");
            }
        });
          
        if(localStorage['opentowho'] == "all" || localStorage['opentowho'] == undefined){
            $(".opentowhoselected").text("公开");
        }
        else if(localStorage['opentowho'] == "private"){
            $(".opentowhoselected").text("私人");
        }else{
            $(".opentowhoselected").text("部分");
        }
    });
});

