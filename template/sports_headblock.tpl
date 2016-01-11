<div class="headblock">
  <div class="well itemlistpageuserinfowell">
    <div class="row">
      <div class="col-xs-2">
        <img id="shortcutimg" src="{{shortcut}}" onClick="javascript:window.location.href='/sports/personalinfo/basic'" alt="" />
      </div>
      <div class="col-xs-8">
        <p id="username">{{nickname}}</p>
        <p id="useruid">{{username}}</p>
      </div>
      <div class="col-xs-2">
        <span id="qrcode" class="glyphicon glyphicon-qrcode" aria-hidden="true"></span>
      </div>
    </div>
  </div>
</div>

%include("sports_qrcode.tpl", nickname=nickname, shortcut=shortcut, md5id=md5id)
