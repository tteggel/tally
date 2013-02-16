%include header title='Tally'
<h1 id="value">{{value}}</h1>
<form action="{{key}}/inc" method="POST">
  <button type="submit" id="inc" class="btn btn-large btn-success inc" href="#" name="inc" value="1">+1</button>
</form>
<form action="{{key}}/inc" method="POST">
  <button type="submit" class="btn btn-large btn-success inc" href="#" name="inc" value="-1">-1</button>
</form>
<script type="text/javascript" src="/static/js/tally.js"></script>
%include footer
