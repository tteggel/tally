%include header title='Tally'

<div class="jumbotron">

%if name:
<h1>{{!name}}</h1>
%end

%if desc:
<p>{{!desc}}</p>
%end

<div id="value">{{int(value)}}</div>

%if unit:
<div id="unit" class="text-right"><small>{{!unit}}</small></div>
%end

<div class="controls controls-row">
  <form action="{{key}}/inc" method="POST">
%for button in buttons:
  <button type="submit" id="inc" class="btn btn-success btn-large inc" href="#" name="inc" value="{{button}}">\\
%if button>0:
+\\
%end
{{int(button)}}</button>
%end
</form>
</div>

<script type="text/javascript" src="/static/js/tally.js"></script>

</div>

%include footer
