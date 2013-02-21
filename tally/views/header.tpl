<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{title}} &lt;tally.tteggel.org&gt;</title>
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

    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>

  </head>

  <body>
    <div class="container-narrow">

      <div class="masthead">
        <ul class="nav nav-pills pull-right">
          <li class="active"><a href="/">Home</a></li>
          <li><a href="/new#new" data-toggle="modal">Create a new tally</a></li>
        </ul>
        <h3 class="muted">tally.tteggel.org</h3>
      </div>

      <div id="new" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="newFormLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            %include new
          </div>
        </div>
      </div>

    <hr>
