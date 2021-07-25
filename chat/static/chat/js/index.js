//globel variables
let hostname_ = window.location.host;
let protocol_ = window.location.protocol+ "//";

let LogInUserId = JSON.parse(
  document.querySelector("#logedInUserId").textContent
);

//adding click even listener to all friends div
friendsDiv = document.querySelectorAll(".friend");
Array.from(friendsDiv).forEach((div) => {
  div.style.cursor = "pointer";
  div.addEventListener("click", loadChat);
});

//function to load previous messages
function loadChat() {
  try {
    document.querySelector(".activeFriend").className = "friend";
  } catch (error) {
    null;
  }
  
  document.getElementById(this.id).className += " activeFriend";
  let friend = this.id.replace("friend-", "");
  let url = protocol_ + hostname_ + `/get-messages/${friend}`
  fetch(url, {
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHTTPRequest",
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let chatBox = document.querySelector(".message-area");
      chatBox.innerHTML = "";

      data.forEach((msg) => {
        let floatProp = null;
        if (msg.sender == friend) floatProp = "left";
        else floatProp = "right";
        let msgDiv = `<div class="message ${floatProp} ">
                                    <div class="orient">
                                    ${msg["text"]}
                                    </div>
                                </div>`;
        chatBox.innerHTML += msgDiv;
      });

      try {
        //for auto scrolling
        offsetTop = chatBox.lastChild.offsetTop;
        chatBox.scrollTo(0, offsetTop);
      } catch (error) {
        console.log(error);
      }
      startMessaging(friend);
    });
}

//function which start websocket connection & start communication
function startMessaging(friendId) {
  let groupId = createGroupId(friendId.toString(), LogInUserId.toString());
  let msgInput = document.querySelector("#msg-text-input");
  let sendBtn = document.querySelector("#send-btn");

  let websocket = new WebSocket(
    "ws://" + hostname_ + "/chat/" + groupId.toString() + "/"
  );

  msgInput.focus();
  msgInput.onkeyup = function (e){
    if(e.keyCode === 13){
      sendBtn.click();
    }
  }

  sendBtn.onclick = function (e) {
    let msg = {
      text: msgInput.value,
      sender: LogInUserId,
      receiver: friendId,
    };

    websocket.send(JSON.stringify(msg));
    msgInput.value = "";
  };

  websocket.onmessage = function (e) {
    let chatBox = document.querySelector(".message-area");
    let msg = JSON.parse(e.data);
    if (msg.sender == friendId) 
      floatProp = "left";
    else 
      floatProp = "right";
    
    let msgDiv = `<div class="message ${floatProp} ">
                                <div class="orient">
                                ${msg["text"]}
                                </div>
                            </div>`;
    chatBox.innerHTML += msgDiv;

    //for auto scrolling
    offsetTop = chatBox.lastChild.offsetTop;
    chatBox.scrollTo(0, offsetTop);
  };
}

//function to create unique group id
function createGroupId(a, b) {
  let groupId =
    Math.max(parseInt(a), parseInt(b)) *
    (Math.max(parseInt(a), parseInt(b)) + 1);
  groupId = groupId / 2 + Math.min(parseInt(a), parseInt(b));
  return groupId;
}

//function to add search functionality
function searchFriends(){
  let searchBox = document.querySelector("div.searchBox");
  let searchform = searchBox.firstElementChild;
  let searchBoxInput = searchform.querySelectorAll('input')[1];
  searchBoxInput.setAttribute('list', 'users-list') 

  searchform.addEventListener('submit', addFriend);

  let userList = document.createElement("datalist")
  userList.id = "users-list";
  let url = protocol_ + hostname_ + "/get-users/"
  fetch(url, {
  headers :{
    Accept:"application/json",
    "X-Requested-With" : "XMLHTTPRequest",
  }
  })
  .then((response) => {
    return response.json();
  })
  .then((data) => {

    try {
      data.forEach((user) => {
        let newOption = document.createElement('option');
        newOption.value = user['email'];
        newOption.innerText = user['username'];     
        userList.appendChild(newOption); 
      });
      searchBox.appendChild(userList);
    } catch (error) {
      console.log(error)
    }
  });
}

searchFriends();

function addFriend(e){
  e.preventDefault();
  let form = new FormData(this);
  let url = protocol_ + hostname_ + "/add-friend/"
  fetch(url, {
  method: 'POST',
  credentials: 'same-origin',
  headers: {
      'Accept':'application/json',
      'X-Requested-With': 'XMLHTTPRequest',
      'X-CSRFToken':form.get('csrfmiddlewaretoken').toString(),
    },
    body:JSON.stringify({ 'name':form.get('user-name').toString()}),
  })
  .then( response => {
    return response.json();
  })
  .then(data => {
    let friendsArea = document.querySelector("div.friends-area");
    friendsArea.innerHTML += `
    <div class="friend" id="friend-${data['id']}">
    <div class="image">
        <div class="i">
        
        </div>
    </div>

    <div class="friend-info">
        <div class="name"> ${data['name']} </div>
        <div class="status"></div>
    </div>
</div>
    `
  })

}