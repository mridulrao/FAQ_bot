var messages = [], //array that hold the record of each string in chat
  lastUserMessage = "", //keeps track of the most recent input string from the user
  botMessage = "", //var keeps track of what the chatbot is going to say
  botName = 'GEUBOT' //name of the chatbot

function get_bot_responce() {
    return $.ajax({
        url : "",
        type : "GET",
        dataType : 'json',
        success : (data) => {
            //console.log(data)
        },
        error : (error) =>{
            console.log(error)
        }
    });
}

function send_query(query){
    console.log(query)
    $.ajax({
        type : "POST",
        url : "",
        data : {"query" : query},

        success : function(data){
            console.log("Sent query")
        },
        error : function(data){
            console.log("Could not sent data")
        }
    })
}

async function chatbotResponse() {
  //
  result = await get_bot_responce();
  botMessage = result['context']
  //botMessage = "hehehehe" //negate sentense
  //console.log(botMessage)

  if(result['query_flag'] == true){
    document.getElementById("useful").hidden = false;
    document.getElementById("not_useful").hidden = false;
  }
  else{
    document.getElementById("useful").hidden = true;
    document.getElementById("not_useful").hidden = true;
  }
}
//****************************************************************
//
//this runs each time enter is pressed.
//It controls the overall input and output
async function newEntry() {
  //if the message from the user isn't empty then run 
  if (document.getElementById("chatbox").value != "") {
    //pulls the value from the chatbox ands sets it to lastUserMessage
    console.log("Generating responce")
    lastUserMessage = document.getElementById("chatbox").value;
    send_query(lastUserMessage)
    //sets the chat box to be clear
    document.getElementById("chatbox").value = "";
    //adds the value of the chatbox to the array messages
    messages.push(lastUserMessage);
    //Speech(lastUserMessage);  //says what the user typed outloud
    //sets the variable botMessage in response to lastUserMessage
    await chatbotResponse();
    //add the chatbot's name and message to the array messages
    messages.push("<b>" + botName + ":</b> " + botMessage);
    //outputs the last few array elements of messages to html
    for (var i = 1; i < 8; i++) {
      if (messages[messages.length - i])
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
    }
  }
}

async function RemarkNewEntry(){
  var result = await get_bot_responce();
  msg = result['context']
  messages.push("<b>" + botName + ":</b> " + msg);

  for (var i = 1; i < 8; i++) {
    if (messages[messages.length - i])
      document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
  }
}

//runs the keypress() function when a key is pressed
document.onkeypress = keyPress;
//if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  document.getElementById("useful").hidden = true;
  document.getElementById("not_useful").hidden = true;
  if (key == 13 || key == 3) {
    newEntry();
  }
  if (key == 38) {
    console.log('hi')
      //document.getElementById("chatbox").value = lastUserMessage;
  }
}

// url is empty because, the url to chatbot is also empyt(defualt)
// if the user is satified with answer 
$('#useful').click(function(e) {
    e.preventDefault();

    $.ajax({
        type : "POST",
        url : "",
        data : {"validity" : "Useful"},

        success : function(response){
            console.log("Sent responce")
            RemarkNewEntry();
        },
        error : function(response){
            console.log("Could not send responce")
        }
    })
})

//if user is not satisfied with answer
$('#not_useful').click(function(e) {
    e.preventDefault();

    $.ajax({
        type : "POST",
        url : "",
        data : {"validity" : "Not Useful"},

        success : function(data){
            console.log("Sent responce")
            console.log(get_bot_responce())
        },
        error : function(data){
            console.log("Could not send responce")
        }
    })
})

//clears the placeholder text ion the chatbox
//this function is set to run when the users brings focus to the chatbox, by clicking on it
function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
}