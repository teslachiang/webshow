$(function(){
    $(".titlewell .title").text("活动日程");
    $(".titlewell").prepend('<span class="glyphicon glyphicon-search titlesearch"></span>');
    $(".titlewell").append('<span class="glyphicon glyphicon-plus titleaddgame" onclick="location=\'/sports/personalsocial/addgame\'"></span>');
});

$(".titletext").click(function(){
    var projectkey = $(this).find(".titlekey").text();
    window.location.href = "/sports/personalsocial/taskdetail?key="+projectkey;
})
