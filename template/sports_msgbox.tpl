<div class="sports_msgbox" style="display:none">
  <div class="alert alert-danger removemsgbox">
    <p>{{!content}}</p>
    <p>
    %if defined('ok'):
      <a class="btn btn-danger" id="alertremoved">确定</a>
    %end
    %if defined('cancel'):
      <a class="btn btn-warning" id="alertcancel">取消</a>
    %end
    </p>
  </div>
</div>

<script type="text/javascript" src="/static/js/sports_msgbox.js"></script>
