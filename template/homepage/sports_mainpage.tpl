<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
  <meta name="viewport" content="user-scalable=no" />  
  <head>
    %if defined('title'):
    <title>{{get('title')}}</title>
    %else:
    <title>{{ title or "sobob" }}</title>
    %end
    <!-- 新 Bootstrap 核心 CSS 文件 -->
    <link rel="stylesheet" href="/static/bt/css/bootstrap.min.css">
    <!-- 可选的Bootstrap主题文件（一般不用引入） -->
    <link rel="stylesheet" href="/static/bt/css/bootstrap-theme.min.css">
    <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
    <script src="/static/bt/js/jquery.min.js"></script>

    <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
    <script src="/static/bt/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="/static/css/sports_publicdefine.css" type="text/css" media="screen" />

    <style type="text/css" media="screen">
      .titlewell .glyphicon-user{
      float:left;
      }
      .searchcomponent input{
      height: 80px;
      font-size: 40px;
      }

      .nocontentinfo{
      font-size: 4em;
      color: gray;
      text-align: center;
      margin-top: 20%;
      }
  
    </style>

  </head>
  <body>
    <div class="well well-lg titlewell">
      
      <span class="title">{{title}}</span>
      %if defined('username') and username != None and defined('imagelink'):
      %include("sports_userheadshortcut.tpl", imagelink=imagelink)
      %end
    </div>
    <div class="removewellgapblock"></div>
    %include("sports_searchblock.html")

    {{!include}}

  </body>
</html>
