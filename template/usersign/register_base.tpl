<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="utf8">
  <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <title>SOBOB {{title or ""}}</title>

    <meta name="viewport" content="user-scalable=no" />
    <!-- 新 Bootstrap 核心 CSS 文件 -->
    <link rel="stylesheet" href="/static/bt/css/bootstrap.min.css">

    <!-- 可选的Bootstrap主题文件（一般不用引入） -->
    <link rel="stylesheet" href="/static/bt/css/bootstrap-theme.min.css">

    <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
    <script src="/static/bt/js/jquery.min.js"></script>

    <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
    <script src="/static/bt/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="/static/css/sports_publicdefine.css" type="text/css" media="screen" />
  </head>
  <body>
    <div class="well well-lg titlewell">
      <span class="title">{{title}}</span>
      <span class="glyphicon glyphicon-home" onclick="javascript:window.location.href='/sports/mainpage'"></span>
    </div>
    <div class="container">
      {{!include}}
    </div>
    
  </body>
</html>
