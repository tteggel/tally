%include header title='Hello World'
<h1>{{value}}</h1>
<form action="{{key}}/inc" method="POST">
  <button class="btn btn-large btn-success" href="#" name="inc" value="1">+1</button>
</form>
<form action="{{key}}/inc" method="POST">
  <button class="btn btn-large btn-success" href="#" name="inc" value="-1">-1</button>
</form>
%include footer
