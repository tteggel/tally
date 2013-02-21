<form action="new" method="POST">
<div id="new" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="newModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="newModalLabel">Create a new tally</h3>
  </div>
  <div class="modal-body">
      <fieldset>
        <legend>Legend</legend>
        <label>Label name</label>
        <input type="text" placeholder="Type something…">
        <span class="help-block">Example block-level help text here.</span>
        <label class="checkbox">
          <input type="checkbox"> Check me out
        </label>
    <button type="submit" class="btn">Submit</button>
      </fieldset>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button>
    <button type="submit" class="btn btn-primary">Create</button>
  </div>
</div>
</form>
