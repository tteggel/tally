(function () {
  var websocket, key;

  // hook up to doc ready
  $(ready);

  function ready() {
    if ('WebSocket' in window && typeof WebSocket == 'function') {
      key = document.location.pathname.substr(1).split('/')[0];
      hijack();
      listen();
    }
  }

  function hijack() {
    // hands-up mofos.

    function inc_click(event) {
      event.preventDefault();
      var inc = event.target.value;
      websocket.send(JSON.stringify({'message':'inc', 'key': key, 'inc': inc}));
    }

    $('.inc').click(inc_click);
  }

  function listen() {
    function message(event) {
      decoded = JSON.parse(event.data);
      if(decoded &&
         decoded.message && decoded.message === "changed" &&
         (decoded.value || decoded.value === 0)) {
        $('#value').text(decoded.value);
      }
    }

    websocket = new ReconnectingWebSocket(document.location.href.replace('http', 'ws'));
    websocket.onmessage = message;
  }

}());
