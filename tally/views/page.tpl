<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Tally. Count stuff. &mdash; tally.tteggel.org</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <link href="/static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <link href="/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="/static/css/tally.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="/static/bootstrap/js/html5shiv.js"></script>
    <![endif]-->

    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

  </head>

  <body>

    <div id="new" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="newFormLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          %include new
        </div>
      </div>
    </div>

    <div class="container-narrow">

%if defined('nav') and nav:
      <div class="masthead">
        <ul class="nav nav-pills pull-right">
          <li><a href="/">Home</a></li>
          <li><a href="/new#new" data-toggle="modal">Create a new tally</a></li>
        </ul>
        <h3 class="muted"><a href="http://tally.tteggel.org/">tally.tteggel.org</a></h3>
      </div>
      <hr>
%end

%include

      <hr>

      <div class="footer row">
        <p>
          &copy; <a href="http://tteggel.org">Thom Leggett</a> 2013
          &mdash; <a href="https://twitter.com/thomleggett/">@thomleggett</a>
          &mdash; <a href="https://github.com/thom-leggett/tally">Fork it!</a>
          &mdash; <a href="https://hpcloud.com">Hosted on the HP Cloud</a>
      </div>

    </div> <!-- /container -->

    <script src="/static/bootstrap/js/bootstrap.min.js"></script>

  </body>
</html>
