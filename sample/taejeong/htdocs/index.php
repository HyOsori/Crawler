<!DOCTYPE html>
<link rel="stylesheet" href="style.css">
<html lang="ko" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Search</title>
  </head>
  <body>
    <form class="SearchForm" action="?" method="get">
      <fieldset class="SearchArea">
        <legend>Search</legend>
        <div class="SearchBox">
          <span class="keyword">
            <input type="text" name="keyword" autocomplete="off" value="<?php
                if(array_key_exists("keyword", $_GET)){
                  echo $_GET["keyword"];
                }
              ?>">
          </span>
        </div>
        <button type="submit">
          <img src="img\search_icon.png" alt="search" width="25px" height="25px" margin="auto">
        </button>
      </fieldset>
    </form>
    <div class="ResultArea" style="text-align: left; width = 50">
      <?php
        if(array_key_exists("keyword", $_GET)){
          ini_set("allow_url_fopen", 1);
          $result = file_get_contents("http://localhost:9200/site/everytime/_search?pretty=true&q=".urlencode($_GET["keyword"]));
          if($result){
            $doc = json_decode($result);
            $articles = $doc->hits->hits;
            for($idx = 0, $size = sizeof($articles); $idx < $size; ++$idx){
              $src = $articles[$idx]->_source;
              $title = $src->title;
              $body = $src->body;

              $body_limit = 80;
              $class = "title";
              if($title != ""){
                echo "<a class='title' target='_blank' href=".$src->link.">".$title."</a><br>";
                $class = "body";
                $body_limit = 800;
              }

              if(strlen($body) > $body_limit){
                $body = mb_substr($body, 0, $body_limit, "UTF-8")."...";
              }

              echo "<a class='".$class."' target='_blank' href=".$src->link.">".$body."</a><br>";
              echo "<p>".$src->username." | ".$src->board." | 댓글 ".sizeof($src->comments)."개 | ".$src->timestamp."</p>";
              echo "<br><br>";
            }
          }
        }
      ?>
    </div>
  </body>
</html>
