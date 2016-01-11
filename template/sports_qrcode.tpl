<!-- Modal -->

<style type="text/css" media="screen">

   #myqrcodeModal{
       font-size: 16px;
   }

   #myqrcodeModal .modal-header{
     height:8.5%;
   }
   .qrdialog{
     width:90%;
     margin-top:20%;
   }
   #myqrModalLabel{
    font-size: 3em;
    font-weight: bold;
    text-shadow: 1px 2px 2px gray;
    color: brown;
    padding: 20px 0px 0 150px;
  }

   #myqrModalLabel img{
      width: 3em;
      height: 3em;
      margin-right: 0.5em;
      border-radius: 50%;
      border: 5px solid;
   }

  
   #myqrcodeModal .qrhelp{
    font-size: 3em;
    text-align: center;
  }
   #myqrcodeModal #qrclose{
     float: right;
   }
   #qrcodeshortcutimg{
       width: 200px;
       height: 200px;
       position: absolute;
       margin: 30% 0 0 38%;
       border-radius: 50%;
       border: 8px solid #C85252;
   }
   .qrcodepng{
      padding: 0 5% 0 5%;
      width: 100%;
      height: 40%;
   }
   #qrheadshortcutimg{
     width:120px;
   }
</style>
<div class="modal fade" id="myqrcodeModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog qrdialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <img id="qrheadshortcutimg" class="usershortcut" src="{{shortcut}}" class="" alt="" /> 
        <h1 class="modal-title" id="myqrModalLabel"><span class="qrnickname">{{nickname}}</span></h1>
       </div>
      <div class="modal-body qrbody">
        <p>
          <img id="qrcodeshortcutimg" class="usershortcut" src="{{shortcut}}" class="" alt="" />
          <img class="qrcodepng" src="/static/qrcode/{{md5id}}_qrcode.png" class="" alt="" />
        </p>
        <p class="help-block qrhelp">扫描上面二维码加关注</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-danger" id="qrclose" data-dismiss="modal"><span class="qrclosebtn">关闭</span></button>
      </div>
    </div>
  </div>
</div>

<script type="text/javascript">
  $("#qrcode").click(function(){
      $("#myqrcodeModal").modal("show");
  })
</script>
