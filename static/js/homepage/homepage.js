
function queryblock(block){
    
    // post send the query result and clear the list list-group

   // var listelem = '<li class="list-group-item" onclick="javascript:window.location.href='/sports/mainpage/article?id={{art['artid']}}'">\
  //  <span class="art_title">{{art['title']}}</span>\
  //  <p><span class="label label-primary art_block" onclick="queryblock($(this))">{{art['block']}}</span><span class="art_timestamp">{{art['timestamp'][2:-3]}}</span></p></li>';
    var blockname = block.text();
    $.post("/sports/query", {type:'block', block:blockname}, function(data){
        
    }, "json");
}

var myscroll;

function destorycircleloader(){
    $('#contentloader').shCircleLoader('destory');
    $('#contentloader').empty();
    // refresh scroll right now!
    setTimeout(function () { myscroll.refresh();}, 0);

    $(".infomsgbox").show();
    setTimeout(function(){$(".infomsgbox").hide();}, 1000);
}

$(function(){
    myscroll = new IScroll(".wrapper", {useTransition:false, tap:true, probeType: 1});
    $(".backtotop").hide();
    myscroll.on('scrollEnd', function(){
        if(myscroll.directionY == 1){
            $(".backtotop").show();
        }
    });

    myscroll.on('scroll', function(){
        if(myscroll.y < myscroll.maxScrollY && Math.abs(myscroll.y - myscroll.maxScrollY) > 150){

            if($("#contentloader .shcl").length == 0){
               $('#contentloader').shCircleLoader({color:"#D77272"});
               setTimeout("destorycircleloader()", 5000);
            }
        }
    });

    $(".list-group-item").on('tap', function(){
        window.location.href = $(this).attr('linkurl');
    });
});

function backtotop(){
    myscroll.scrollToElement(document.querySelector('#scroller li:nth-child(1)'), 1200, null, null, IScroll.utils.ease.elastic);
}

document.addEventListener('touchmove', function (e) { e.preventDefault(); }, false);
