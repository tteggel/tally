(function () {
  var websocket, key;

  // hook up to doc ready
  $(ready);

  function ready() {
    key = document.location.pathname.substr(1).split('/')[0];
    hijack();
    listen();
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
    function open(event) {
    }

    function close(event) {
    }

    function message(event) {
      decoded = JSON.parse(event.data);
      if(decoded &&
         decoded.message && decoded.message === "changed" &&
         (decoded.value || decoded.value === 0)) {
        $('#value').text(decoded.value);
      }
    }

    function error(event) {
    }

    websocket = new WebSocket(document.location.href.replace('http', 'ws'));
    websocket.onopen = open;
    websocket.onclose = close;
    websocket.onmessage = message;
    websocket.onerror = error;
  }

}());
