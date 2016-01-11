$(function(){
   $("#myAritcleModal").on('hidden.bs.modal', function(e){
       $("#articlecomment").val("");
   });

   $("#myAritcleModal").on('shown.bs.modal', function(e){
       $(".releasecomment").attr("disabled", true);
   });

   $("img[class!=imgheadshortcut]").parent().css("text-align", 'center');
})

function readytoinputcomment(){
    $(".releasecomment").attr("disabled", false);
}

$(".writecomment").click(function(){
    $("#myAritcleModal").modal('show');
});

$(".addtofavor").click(function(){
    if($(".user_headshortcut").length == 0){
        window.location.href="/sports/login";
    }else{
        window.location.href="/sports/articles/addtofavor";
    }
});

$(".releasecomment").click(function(){
    // first check the user is login in.
    // use ajax post comment data
   $.post("");
});
