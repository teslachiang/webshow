$(function(){
    $(".titlewell").prepend('<span class="glyphicon glyphicon-arrow-left titleback"\
                            onClick="javascript :history.back(-1);" style="font-size:5em; float:left; padding-top:0.25em"></span>');

    $("#costcheckbox input").bootstrapSwitch({'onText':"是", 
                                              'offText':"否", 
                                              'state': false,
                                              'size':"large",
                                              'offColor': 'danger',
                                              'onColor': 'success'});

    $("#subjectcontent").qeditor({});

    $("#startdate, .input-daterange input").datepicker({language:'zh-CN',
                                                        calendarWeeks: true,
                                                        clearBtn: true,
                                                        autoclose: true,
                                                        format:"yyyy/mm/dd",
                                                        startDate:"0d",
                                                        todayHighlight: true
                                                       });
    // $(".input-daterange input").each(function(){
    //     $(this).datepicker("clearDates");
    // });
    
});

$("#costcheckbox").on('switchChange.bootstrapSwitch', function(e, data){
    if(data){
        $(".costdetail").hide();
    }else{
        $(".costdetail").show();
    }
});


function baidusearch(addresskeyword){
    var  map = new BMap.Map("allmap");
    map.centerAndZoom(new BMap.Point(116.404, 39.915), 11);
    var local = new BMap.LocalSearch(map, {
		renderOptions:{map: map},
        onSearchComplete: function(results){
            if(local.getStatus() == BMAP_STATUS_SUCCESS){
                //results.getCurrentNumPois()
                var firstpoi = results.getPoi(0);
                $(".selectresult").empty();
                $(".selectedresult").empty();
                $(".gameaddress").empty();
                $(".selectresult").append('<p class="addressnotifyinfo">当前选择地址为：</p>');
                $(".selectresult").append("<p style='font-size:2.2em'>"+firstpoi.address+"</p>");
                $(".gameaddress").val(firstpoi.address);
            }
        }
    });
    
    var address = addresskeyword;
	local.search(address);
    
    var geoc = new BMap.Geocoder();
    function showInfo(e){
        var pt = e.point;
        $(".selectresult").empty();
        $(".selectedresult").empty();
        $(".gameaddress").empty();
        var info = map.getInfoWindow();
        var pt = info.getPosition();

        geoc.getLocation(pt, function(rs){
            var addComp = rs.addressComponents;
            var provice = "";
            if(addComp.provice != undefined){
                provice = addComp.provice;
            } 
           // $(".gameaddress").append(provice+" "+ addComp.city + " " + addComp.district + " " + addComp.street + " " + addComp.streetNumber);
        });
        $(".selectedresult").append("<span id='lng'>"+pt.lng+"</span><span id='lat'>"+pt.lat+"</span>");
        $(".selectresult").append('<p class="addressnotifyinfo">当前选择地址为：</p>');
        $(".selectresult").append(info.getTitle());
        $(".selectresult").append(info.getContent());
        $(".selectresult p:nth-of-type(2)").css("line-height", '40px');
        $(".selectresult p:nth-of-type(2)").css("font-size","2.2em");
        $(".selectresult p:nth-of-type(2) a").css("font-size","1em");
        $(".selectresult p:nth-of-type(2)").css("width","100%");
        $(".selectresult tr td:first-child").css("width","80px");

        var $gc = $(info.getContent());
        var showaddress = $gc.find("table tr:first-child td:last-child").text();
        $(".gameaddress").val(showaddress);
    }
	map.addEventListener("click", showInfo);
}

// $("#addaddressfinish").click(function(){
//    // $(".gameaddress").val();
// });

$("#addressstring").click(function(){  
    $("#myModal").modal('show');
    var address = $(".gameaddress").val();
    $("#suggestId").val(address);
    baidusearch(address);
});

$("#search").click(function(){
    var address = $("#suggestId").val();
    baidusearch(address);
});

$("#submitgame").click(function(){
    var title = $("#tasktitle").val();
    var startdate = $("#startdate input").val();
    var sendstartdate = $(".input-daterange input:first-child").val();
    var sendenddate = $(".input-daterange input:last-child").val();

    var isfree = $("#costcheckbox input[type=checkbox]")[0].checked;
    var costvalue = 0;
    if(isfree == false){
        costvalue = $("#costvalue").val();
    }

    var description = $(".qeditor_preview").text();
    var gameaddress = $(".gameaddress").val();
        
    var flag = 0;
    $(".msginfo").each(function(e){
       $(this).text("*"); 
    });
    var st = new Date(startdate);
    var nst = new Date(sendstartdate);
    var net = new Date(sendenddate);
    if(title.replace(/(\s*)/g, "").length == 0){
        flag = -1;
        $(".titlemsginfo").text(" 填写标题");
        $("#tasktitle").addClass("focus");
    }else if(startdate.length == 0){
        flag = -2;
        $(".startdatemsginfo").text(" 选择日期");
        $("#startdate input").addClass("focus");
    }else if(sendenddate.length == 0){
        flag = -3;
        $(".senddatemsginfo").text(" 选择结束日期");        
        $(".input-daterange input:first-child").addClass("focus");
    }else if(sendstartdate.length == 0){
        flag = -4;
        $(".senddatemsginfo").text(" 选择起始日期");
        $(".input-daterange input:last-child").addClass("focus");
    }else if(st < nst){
        flag = -4;
        $(".senddatemsginfo").text(" 起始日期在活动后");
    }else if(nst > net){
        flag = -4;
        $(".senddatemsginfo").text(" 起始日期不正确");
    }else if(st > net){
        flag = -4;
        $(".senddatemsginfo").text(" 结束日期在活动后");
    }else if(description.length < 10){
        flag = -5;
        $(".descriptionmsginfo").text(" 填写活动描述");
        $("#subjectcontent").addClass("focus");
    }else if(gameaddress.length == 0){
        flag = -6;
        $(".addressmsginfo").text(" 填写活动地址");
        $(".gameaddress").addClass("focus");
    }
    var _projectkey = $("#projectkey").text();
    
    if(flag == 0){
        $.post("/sports/personalsocial/modifygameajax", {tasktitle:title, cost: costvalue, 
                                      start: startdate, 
                                      tstart: sendstartdate, tend: sendenddate,
                                      descript: $(".qeditor_preview").html(),
                                      address: gameaddress, projectkey: _projectkey 
                                     }, function(data){
                                         if(data['status'] == 0){
                                             // add project info ok
                                             window.location.href = "/sports/personalsocial/schedule";
                                         }else{
                                             alert("server save error!!! code:"+data['status']);
                                         }
                                     }, 'json');
    }

    return false; 
});
