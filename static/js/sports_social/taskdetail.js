$(function(){
    $(".titlewell .title").text("活动详情");
    var taskid = $(".taskid").text();
    $(".titlewell").prepend('<span class="glyphicon glyphicon-edit titleicon" onclick="location=\'/sports/personalsocial/editgame?key='+taskid+'\'"></span>');
    $(".titlewell").append('<span class="glyphicon glyphicon-trash titleicon" onclick="removetask()"></span>');
});

function removetask(){
    var taskid = $(".taskid").text();
    $.post("/sports/personalsocial/removegame", {key: taskid}, function(data){
        if(data['status'] == 0){
            // remove success
            window.location.href = "/sports/personalsocial/schedule";
        }else{
            // remove failed!!
            alert("remove failed, please try again, error code:"+data['status']);
        }
    }, "json");
}

$("#checkmap").click(function(){
    var astr = $("#addressstring").text();
    $("#addressinfo").text(astr);

    var map = new BMap.Map("allmap");
	var point = new BMap.Point(116.331398,39.897445);
	map.centerAndZoom(point,12);

	map.addControl(new BMap.ZoomControl());          
	// 创建地址解析器实例
	var myGeo = new BMap.Geocoder();
	// 将地址解析结果显示在地图上,并调整地图视野
	myGeo.getPoint(astr, function(point){
		if (point) {
			map.centerAndZoom(point, 18);
			map.addOverlay(new BMap.Marker(point));
		}
	}, "北京市");

    $("#mySocialModal").modal('show');
    return false;
});
