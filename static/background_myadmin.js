function checkimagesize(filepath, upfile){
	var MAXSIZE = 2 * 1024 * 1024;
	var ERROR_IMGSIZE = "图片大小不能超过2M";
	var filetarget = document.getElementById(upfile).files.item(0);
    if(filetarget == null){
        return false;
    }
	if( filetarget.size > 0 && filetarget.size < MAXSIZE){
		  var src = window.URL.createObjectURL(filetarget);
          $("#previewimg").attr('src', src);
          $("#previewimg").show();
        return true;
	}else{
		if(filetarget.size < 1){
		  alert("文件错误！");
		}else{
		  alert(ERROR_IMGSIZE);
		}
        return false;
	}
}

function qeditorsetting(){
    var toolbar = $("#articlecontent").parent().find(".qeditor_toolbar");
      var link = toolbar.find("a.qe-image");
      link.attr("data-action","");
      link.click(function(e){
        addimagemodal();
        return false;
      });

      var urllink = toolbar.find("a.qe-link");
      urllink.attr("data-action","");
      urllink.click(function(e){
        addurllinkmodal();
        return false;
      });
}

function ajaxFileUpload(cropinfo, upfile) {
    $.ajaxFileUpload
    (
        {
            url: '/sports/background/uploadimages', //用于文件上传的服务器端请求地址
            type: 'post',
            data: cropinfo,
            secureuri: false, //是否需要安全协议，一般设置为false
            fileElementId: upfile, //文件上传域的ID
            dataType: 'JSON', //返回值类型 一般设置为json
            success: function (data, status)  //服务器成功响应处理函数
            {
                var jdata = JSON.parse(data);
                if (jdata.status == 0) {
                    $(".imageshowarea").append('<img src="'+jdata.imglink+'" id="previewimg" style="width:50%; height:14em;" alt="" />');
                    $(".imageshowarea").append('<div class="alert alert-success" role="alert" id="resultimg"></div>');
                    $("#resultimg").text("(copy it) http://"+window.location.host+jdata.imglink);
                }else{
                    $(".imageshowarea").append("<p>服务器错误，请重试！</p>");
                }
                $("#uploadbutton").hide();
            },
            error: function (data, status, e)//服务器响应失败处理函数
            {
                //alert(e);
                $(".imageshowarea").append("<p>"+e+"</p>");
            }
        }
    );
    $("#loader").shCircleLoader('destroy');
    $("#uploadbutton").hide();
    $(".imageshowarea").empty();
    return false;
}
