$(function(){
    $(".demo_li").click(function(){
        //$("#demo_box").css("padding-top", "0");
        var demolitext = $(this).text();
        $(".subselect").each(function(){
            if($(this).attr("name") == demolitext){
                $(this).show();
            }else{
                $(this).hide();
            }
        });
    });
})

$(".subbutton button").click(function(){
    //$("#demo_box").css("padding-top", "10%");
    $(".subselect").hide();
    $("#demo_box").hide();
})

$(".subitem").click(function(){
    if($(this).css("background-color") == "rgb(78, 125, 9)"){
        $(this).css("background-color", "rgb(154, 205, 50)");
    }else{
        $(this).css("background-color", "rgb(78, 125, 9)");
    }
})
