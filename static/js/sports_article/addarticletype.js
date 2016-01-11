function art_MsgboxBase(sportsmsgbox){
    this.msgboxbase = sportsmsgbox;
}

art_MsgboxBase.prototype = {
    ok: function(){
        $(".welllistelem").each(function(){
          if($(this).find('.titletext').text() == $(".removemsgbox .removeditem").text()){
              $(this).remove();
              return;
          }
        });
        return this.msgboxbase.ok();
    },
    cancel: function(){
        return this.msgboxbase.cancel();
    }
};




function operationremove(jqobj){  
    // close project
    var closeitem = jqobj.parent().parents('.row').find('h1').text();
    
    $(".removeditem").text(closeitem);
    $(".sports_msgbox").show();
    
}

function addarticleselector(){
    $("#demo_box").show();
}

$("#alertremoved").click(function(){
//    $(".sports_msgbox").hide();

    // process delete item
    var artmsgbox = new art_MsgboxBase(msgboxconsole);
    artmsgbox.ok();

    // $(".welllistelem").each(function(e){
    //     if($(this).find('.titletext').text() == $(".removemsgbox .removeditem").text()){
    //         $(this).remove();
    //         return;
    //     }
    // });
});

$(function(){
    $(".titlewell").prepend('<span class="glyphicon glyphicon-arrow-left" onClick="javascript:history.back(-1)"></span>');
    $(".titlewell").append('<span class="glyphicon glyphicon-plus" onclick="addarticleselector()"></span>');

    var operation = '<span class="glyphicon glyphicon-ok-circle operationbutton" style="font-color:#7FB651"></span><span class="glyphicon glyphicon-remove-circle operationremove" onclick="operationremove($(this))"></span>';

    $(".well .row .col-xs-6").append(operation);

    $(".operationbutton").on('click', function(){
        var classname = $(this).attr("class");
        //var aria_pressed = $(this).attr("aria-pressed");
        
        if(classname.indexOf('ok') > 0 ){
            $(this).removeClass("glyphicon-ok-circle");
            $(this).addClass("glyphicon-ban-circle");
            $(this).css('color', "#C85252");
        }else{
            $(this).removeClass("glyphicon-ban-circle");
            $(this).addClass("glyphicon-ok-circle");
            $(this).css('color', "#7FB97F");
        }
        
        return;
    });

    
});

