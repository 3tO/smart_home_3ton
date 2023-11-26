function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


// $("#mysubmit").click(function(e) {
//   e.preventDefault();
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
   // $('.htc_value_2').html('<b>loading ...</b>');
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
function send_ajax(){
  $.ajax({
      //beforeSend: function(){},
      type: 'GET',
      async: true,
      url: '/htc/',
      // timeout: 100,
      cache: false,
      // error: function(){console.log('err');},
      // success: function(){console.log('success');},
      dataType: 'json',
      data: {'time': document.getElementById("htc_value_1").innerHTML,
           },
      //data: {form_data: $('.order-form').serialize()}
  }).done(function(data) {
      if (data['success'] == true) {
          document.getElementById("htc_value_1").innerHTML = data['last_date'];
          document.getElementById("htc_value_2").innerHTML = data['water'];
          document.getElementById("htc_value_3").innerHTML = data['smoke'];
          document.getElementById("htc_value_4").innerHTML = data['outside_temp'];
      }

      var st = document.getElementsByClassName("status")[0];
      if (data['status'] == true) {
        st.style.display = "none";
      } else {
        st.style.display = "inline";
      }
  });
};
// setInterval(send_ajax, 10000);
// send_ajax();
// startTime();
setTimeout(send_ajax, 1000);
setTimeout(startTime, 1000);


  // ----------------------------- task.js ------------------------------------

function startTime() {
    document.getElementById('time_now').innerHTML = getTimeNow();
    t=setTimeout(startTime, 1000);
};
function checkTime(i) {
        if (i<10) {
            i="0" + i;
        }
    return i;
};
function getTimeNow() {
        let tm=new Date();
        let h=tm.getHours();
        let m=tm.getMinutes();
        let s=tm.getSeconds();
        m=checkTime(m);
        s=checkTime(s);
       
    return h+":"+m+":"+s;
};
function soundClick() {
  let audio = new Audio();
  audio.src = audio_dir +  'sound1.ogg';
//  audio.src = 'sound1.mp3';
  audio.play()
};
function start() {
    let time = document.getElementById('set_time').value;
    document.getElementById('time').innerHTML = time*60;
    document.getElementById('set_time').disabled = true;
    document.getElementById('task').disabled = true;
    document.getElementById('start').style.display = "none";
    document.getElementById('stop').disabled = false;
    document.getElementById('pause').style.display = "inline";
    let date = new Date()
    document.getElementById('history').innerHTML += "<p>START:  <b>"
                                                 + getTimeNow()
                                                 +"</b> - "
                                                 + document.getElementById('task').value
                                                 + "</p>";
    
    startTimer();
};
function startTimer() {
    let time = document.getElementById('time').innerText;
    time = --time;
    let m = time/60 >> 0;
    let s = time-m*60;
    document.getElementById('minutes').innerHTML = m;
    document.getElementById('seconds').innerHTML = s;
    document.getElementById('time').innerHTML = time;
    if (typeof tt !== 'undefined'){
        clearTimeout(tt);
    }
    tt=setTimeout(startTimer, 1000);
    
    if (time<1) {
        clearTimeout(tt);
        soundClick();
        document.getElementById('set_time').value = 
                            parseInt(document.getElementById('set_time').value) +1;
                            
        console.log(document.getElementById('set_time').value);
        stop();
    };
};
let paused = false;

function pauseTimer() {
    if (paused!=true){
        clearTimeout(tt);
        paused=true;
        document.getElementById('pause').innerHTML = "start";
        let time = document.getElementById('set_time').value - 
                parseInt(document.getElementById('minutes').innerText) - 1;
        document.getElementById('history').innerHTML += "<p>PAUSE: <b>" +
                                                    getTimeNow() + "</b></p>";
    } else {
        tt=setTimeout(startTimer, 1000);
        paused=false;
        document.getElementById('pause').innerHTML = "pause";
        document.getElementById('history').innerHTML += "<p>PLAY:    <b>" +
                                                    getTimeNow() + "</b></p>";
    };
};
function stop() {
    let time = document.getElementById('set_time').value - 
                parseInt(document.getElementById('minutes').innerText) - 1;

    document.getElementById('all_min').innerHTML = parseInt(document.getElementById('all_min').innerHTML)+ time;
    document.getElementById('count_tasks').innerHTML++

    document.getElementById('set_time').disabled = false;
    document.getElementById('task').disabled = false;
    document.getElementById('stop').disabled = true;
    paused=false;
    document.getElementById('pause').innerHTML = "pause";
    document.getElementById('pause').style.display = "none";
    document.getElementById('start').style.display = "inline";
    document.getElementById('time').innerHTML = "";
    //додати час до задачі
    document.getElementById('set').innerHTML = time;
    document.getElementById('history').innerHTML += "<p>STOP:   <b>" + getTimeNow()
                                                 + "</b> - "
                                                 + document.getElementById('task').value
                                                 +" - <b>"
                                                 + time
                                                 +" min</b></p>";
    // time >> db
    clearTimeout(tt);
    document.getElementById('set_time').value = 25;
};
function setup() {

    document.querySelectorAll('.inputs_set').forEach(item => {
        item.addEventListener("keyup", function(event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                document.getElementById("start").click();
            }
        })
    })
};

function task_visible() {
    if (document.getElementById('management').style.display == "none") {
        document.getElementById('management').style.display = "block";
    } else {
        document.getElementById('management').style.display = "none";
    }
}
setup();
