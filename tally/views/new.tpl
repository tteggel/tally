<form action="new" method="POST">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="newFormLabel">Create a new tally</h3>
  </div>
  <div class="modal-body">

    <div class="row controls controls-row">
      <input type="text" name="name" class="input-large" placeholder="Name your tally...">
    </div>

    <div class="row controls controls-row">
      <textarea name="desc" placeholder="Describe your tally..." rows="3"></textarea>
    </div>

    <div class="row controls controls-row">
      <label class="span3 vpad12" for="init">Initial value:</label>
      <input type="number" id="init" name="init" class="input-large span2" placeholder="0">
      <input type="text" name="units" class="input-small span3" placeholder="units">
    </div>

    <div class="row controls controls-row">
      <div class="span3 vpad6">Buttons:</div>
      <div class="span8">
        <label class="checkbox-inline">
          <input type="checkbox" name="inc" value="-10"> -10
        </label>
        <label class="checkbox-inline">
          <input type="checkbox" name="inc" value="-1"> -1
        </label>
        <label class="checkbox-inline">
          <input type="checkbox" name="inc" value="+1" checked="checked"> +1
        </label>
        <label class="checkbox-inline">
          <input type="checkbox" name="inc" value="+10"> +10
        </label>
      </div>
    </div>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button>
    <button type="submit" class="btn btn-primary">Create</button>
  </div>
</form>
