%include header title='Tally'
<h1>{{!name}}</h1>
<p>{{!desc}}</p>
<div class="row">
<div class="span3" id="value">{{value}}</div>
<div class="span2"><small>{{unit}}</small></div>
</div>
<form action="{{key}}/inc" method="POST">
  <button type="submit" id="inc" class="btn btn-large btn-success inc" href="#" name="inc" value="1">+1</button>
</form>
<form action="{{key}}/inc" method="POST">
  <button type="submit" class="btn btn-large btn-success inc" href="#" name="inc" value="-1">-1</button>
</form>
<script type="text/javascript" src="/static/js/tally.js"></script>
%include footer
