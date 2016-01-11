<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>{{title or "SOBOB"}}</title>
    <!-- 新 Bootstrap 核心 CSS 文件 -->
    <link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css">

    <!-- 可选的Bootstrap主题文件（一般不用引入） -->
    <link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">

    <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
    <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>

    <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
    <script src="//cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
  </head>
  <body>

    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="true">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <!-- <a class="navbar-brand" href="#">Brand</a> -->
        </div>

        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <!-- <ul class="nav navbar-nav"> -->
          <!--   <li class="active"><a href="#">Link <span class="sr-only">(current)</span></a></li> -->
          <!--   <li><a href="#">Link</a></li> -->
          <!--   <li class="dropdown"> -->
          <!--     <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a> -->
          <!--     <ul class="dropdown-menu"> -->
          <!--       <li><a href="#">Action</a></li> -->
          <!--       <li><a href="#">Another action</a></li> -->
          <!--       <li><a href="#">Something else here</a></li> -->
          <!--       <li role="separator" class="divider"></li> -->
          <!--       <li><a href="#">Separated link</a></li> -->
          <!--       <li role="separator" class="divider"></li> -->
          <!--       <li><a href="#">One more separated link</a></li> -->
          <!--     </ul> -->
          <!--   </li> -->
          <!-- </ul> -->
          <div class="userinfo nav navbar-nav navbar-left">
            <span class="glyphicon glyphicon-user" id="usericon"></span>
            <span id="userinfo">中华人民共和国前进吧</span>
          </div>
          <form class="navbar-form nav navbar-nav navbar-right" role="search">
            <div class="form-group">
              <input type="text" class="form-control" id="searchinput" placeholder="Search">
            </div>
            <button type="submit" class="btn btn-default"><span class="glyphicon glyphicon-search search"></span><span class="searchword">搜索<span></button>
          </form>
          <!-- <ul class="nav navbar-nav navbar-right"> -->
          <!--   <\!-- <li class="dropdown"> -\-> -->
          <!--   <\!--   <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a> -\-> -->
          <!--   <\!--   <ul class="dropdown-menu"> -\-> -->
          <!--   <\!--     <li><a href="#">Action</a></li> -\-> -->
          <!--   <\!--     <li><a href="#">Another action</a></li> -\-> -->
          <!--   <\!--     <li><a href="#">Something else here</a></li> -\-> -->
          <!--   <\!--     <li role="separator" class="divider"></li> -\-> -->
          <!--   <\!--     <li><a href="#">Separated link</a></li> -\-> -->
          <!--   <\!--   </ul> -\-> -->
          <!--   <\!-- </li> -\-> -->
          <!-- </ul> -->
        </div><!-- /.navbar-collapse -->
      </div><!-- /.container-fluid -->
    </nav>

    {{!include}}
  </body>
</html>
