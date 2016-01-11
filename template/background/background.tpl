<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <!-- 新 Bootstrap 核心 CSS 文件 -->
    <link rel="stylesheet" href="/static/bt/css/bootstrap.min.css">

    <!-- 可选的Bootstrap主题文件（一般不用引入） -->
    <link rel="stylesheet" href="/static/bt/css/bootstrap-theme.min.css">

    <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
    <script src="/static/bt/js/jquery.min.js"></script>

    <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
    <script src="/static/bt/js/bootstrap.min.js"></script>

    <title>{{title or "SOBOB"}}</title>

    <style type="text/css" media="screen">
      #username{
       float: right;
      }
      .username{
        margin-right:1em;
      }
    </style>
  </head>

  <body>
    <div class="container">
      <div class="page-header">
        <h1>文章管理系统 <small id="username"><span class="username"></span><a href="/sports/background/signin" class="btn btn-danger">退出</a></small> </h1>
      </div>
    </div>
    
    {{!include}}
  </body>
</html>
