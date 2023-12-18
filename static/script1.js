// Get the last element of class initialText
const x = document.getElementsByClassName("initialText");
const containerElement = document.querySelector(".sub_container");
scrollToBottom();

// Get the text content of the element
if (x != null) {
  const textToSpeak = x[x.length - 1].textContent;

  // Create a SpeechSynthesisUtterance object
  const utterance = new SpeechSynthesisUtterance();
  utterance.voice = speechSynthesis
    .getVoices()
    .find(
      (voice) =>
        voice.name === "Microsoft Zira Desktop - English (United States)"
    );
  utterance.rate = 0.7;
  utterance.text = textToSpeak;

  // Speak the text
  speechSynthesis.speak(utterance);
}

function scrollToBottom() {
  containerElement.scrollTop = containerElement.scrollHeight; // Scroll to the bottom
}
