$(document).ready(function () {

    // Display Speak Message (for animations or header text)
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }

    // Display hood animation
    eel.expose(ShowHood);
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    // Display user's message in chat UI
    eel.expose(senderText);
    function senderText(message) {
        const mainDiv = document.getElementById("messageSection");
        if (message.trim() !== "") {
            const newText = `<div class="message user-message">${message}</div>`;
            mainDiv.innerHTML += newText;
            mainDiv.scrollTop = mainDiv.scrollHeight;
            document.getElementById("userInput").value = "";
        }
    }

    // Display bot's response in chat UI
    eel.expose(receiverText);
    function receiverText(message) {
        const mainDiv = document.getElementById("messageSection");
        if (message.trim() !== "") {
            const newText = `<div class="message bot-message">${message}</div>`;
            mainDiv.innerHTML += newText;
            mainDiv.scrollTop = mainDiv.scrollHeight;
        }
    }

    // Send button click event
    document.getElementById("sendBtn").addEventListener("click", () => {
        const userText = document.getElementById("userInput").value;
        if (userText.trim() === "") return;

        senderText(userText); // Show user's message

        eel.chatBot(userText)(function (response) {
            receiverText(response); // Show bot's response
        });
    });

});
