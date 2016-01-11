<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
  <meta name="viewport" content="user-scalable=no" />  
  <head>
    <title>{{title or "SOBOB"}}</title>

    <!-- 新 Bootstrap 核心 CSS 文件 -->
    <link rel="stylesheet" href="/static/bt/css/bootstrap.min.css">
    <!-- 可选的Bootstrap主题文件（一般不用引入） -->
    <link rel="stylesheet" href="/static/bt/css/bootstrap-theme.min.css">
    <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
    <script src="/static/bt/js/jquery.min.js"></script>

    <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
    <script src="/static/bt/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="/static/css/sports_social/socialpublic.css" type="text/css" media="screen" />

   </head>
   <body>
     %include('sports_header.tpl', title=title)
     {{!include}}
     <script type="text/javascript">
       $(function(){
       $(".footerblock li[class=active]").removeClass("active");
       $("#footersocial").addClass("active");
       })
     </script>

  </body>
</html>


