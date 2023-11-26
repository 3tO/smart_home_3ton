var client;
let timeout_f;

var connectOptions = {
  timeout: 30,
  reconnect: true,
  cleanSession: false,
  mqttVersion: 4,
  keepAliveInterval: 10,
  onSuccess: onConnect,
  onFailure: onFailure
}

function reload_page() {
  client.disconnect();
  console.log('reload');
  document.location.reload();
}

function connect() {
  try {
    client = new Paho.MQTT.Client('192.168.1.200', 9001, '', 'mozila1' + Math.random().toString(16).slice(2));

    // connectOptions.userName = document.forms.sender.user.value;
    client.connect(connectOptions);
    console.log('connect');
    // document.getElementById("connect_btn").disabled = true;
  } catch (ex) {
    // document.getElementById("connect_btn").disabled = false;
    console.log(ex);
  }
}

function onConnect() {
  let topics = ['/basement/kotel/water', '/basement/kotel/smoke', '/outside/temp']
  // console.log('on connect');
  client.onMessageArrived = function(message) {
    console.log("onMessageArrived: " + message.destinationName + " - " + message.payloadString);

    if (topics.includes(message.destinationName)) {
      // document.getElementById(message.destinationName).innerHTML = message.payloadString + " - " + (Date.now()/1000).toString().slice(-5);
      clearTimeout(timeout_f);
      if (typeof htc === 'undefined') {
        timeout_f = setTimeout(reload_page, 3000);
      } else {
        timeout_f = setTimeout(send_ajax, 3000);
      }
    }
  }
  client.subscribe("#", { qos: 1 });
  // client.subscribe("/outside/temp", { qos: 2 });
}

function onFailure(err) {
  console.log('on failure', JSON.stringify(err));
}

function send() {
   var message = new Paho.MQTT.Message(document.forms.sender.message.value);
   message.destinationName =document.forms.sender.topic.value;
   message.qos = 2;
   client.send(message);
}

connect()
// t = setTimeout(reload_page, 3000);