function SportsBaseMsgBox(){}

SportsBaseMsgBox.prototype = {
    ok: function(){
        $(".sports_msgbox").hide();
    },
    cancel: function(){
        $(".sports_msgbox").hide();
    }
};

var msgboxconsole = new SportsBaseMsgBox();

$("#alertcancel").click(function(){
    msgboxconsole.cancel();
});

$("#alertremoved").click(function(){
    msgboxconsole.ok();
});
