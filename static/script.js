let recorder = null;

function sendVoiceNote(base64) {
  // Create an instance for Django AJAX
  // $.ajax({
  //   // beforeSend: function (xhr) {
  //   //   xhr.setRequestHeader(
  //   //     "X-CSRFToken",
  //   //     $('meta[name="csrf-token"]').attr("content")
  //   //   );
  //   // },
  //   type: "POST",
  //   url: "", // Replace with your Django URL
  //   data: {
  //     base64: base64, // Base64 encoded audio data
  //     csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]')
  //   },
  //   success: function (response) {
  //     console.log("Voice note sent successfully:", response);
  //   },
  //   error: function (error) {
  //     console.error("Error sending voice note:", error);
  //   },
  // });
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify({ audioData: base64 }));
}

function doRecordAudio() {
  return new Promise(function (resolve) {
    // get user audio media
    navigator.mediaDevices
      .getUserMedia({
        audio: true,
      })
      .then(function (stream) {
        // create media recorder object
        const mediaRecorder = new MediaRecorder(stream);

        // save audio chunks in an array
        const audioChunks = [];
        mediaRecorder.addEventListener("dataavailable", function (event) {
          audioChunks.push(event.data);
        });

        // create a start function
        const start = function () {
          // when recording starts, set the icon to stop
          document.getElementById("icon-record-audio").className =
            "fa fa-stop-circle";

          // on icon clicked
          document.getElementById("icon-record-audio").onclick =
            async function () {
              // stop the recorder
              if (recorder != null) {
                const audio = await recorder.stop();
                // get audio stream
                const reader = new FileReader();
                reader.readAsDataURL(audio.audioBlob);
                reader.onloadend = function () {
                  // get base64
                  let base64 = reader.result;

                  // get only base64 data
                  base64 = base64.split(",")[1];

                  // send base64 to server to save
                  sendVoiceNote(base64);
                };
              }
            };

          // start media recorder
          mediaRecorder.start();
        };

        // create a stop function
        const stop = function () {
          return new Promise(function (resolve) {
            // on recording stop listener
            mediaRecorder.addEventListener("stop", function () {
              // change the icon back to microphone
              document.getElementById("icon-record-audio").className =
                "fa fa-microphone icon_border";

              // reset the onclick listener so when again clicked, it will record a new audio
              document.getElementById("icon-record-audio").onclick =
                async function () {
                  recordAudio();
                };

              // convert the audio chunks array into blob
              const audioBlob = new Blob(audioChunks);

              // create URL object from URL
              const audioUrl = URL.createObjectURL(audioBlob);

              // create an audio object to play
              const audio = new Audio(audioUrl);
              const play = function () {
                audio.play();
              };

              // send the values back to the promise
              resolve({
                audioBlob,
                play,
              });
            });

            // stop the media recorder
            mediaRecorder.stop();
          });
        };

        // send the values back to promise
        resolve({
          start,
          stop,
        });
      });
  });
}

// function to record audio
async function recordAudio() {
  // get permission to access microphone
  navigator.permissions
    .query({ name: "microphone" })
    .then(function (permissionObj) {
      console.log(permissionObj.state);
    })
    .catch(function (error) {
      console.log("Got error :", error);
    });

  // get recorder object
  recorder = await doRecordAudio();

  // start audio
  recorder.start();
}
