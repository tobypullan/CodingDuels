var socket = io();
var gameid;
console.log("creating room")
socket.emit("join room");
socket.on("room created", function (data) {
    console.log("room joined");
    console.log(data);
    gameid = data;
    console.log(gameid)
    // socket.emit('join room', {room: gameid});
});



socket.on("connect_error", (err) => {
    console.log(`connect_error due to ${err.message}`);
    console.log(err.description);
    console.log(err.context)
});
document.getElementById("selectQuestion").onclick = function () {
    console.log("emitting selected question")
    let tagsElement = document.getElementById("tags");
    socket.to(gameid).emit("select question", { tags: tagsElement.value, gameid: gameid });
};


document.getElementById("removeQuestion").onclick = function () {
    socket.to(gameid).emit("remove question", { questionTitle: document.getElementById("removeQuestionTitle").value });
};

document.getElementById("gameid-input").value = gameid;

var buttons = document.getElementsByClassName("selectQuestionTable");
for (var i = 0; i < buttons.length; i++) {
    buttons[i].onclick = function () {
        console.log("emitting question" + i + this.getAttribute("titleData"))
        socketio.emit("select question", { title: this.getAttribute("titleData"), gameid: gameid });
    };
}

socket.on("question removed", function (data) {
    console.log("running question removed function");
    removeFromRemoval(data["title"]);
    showNotification(data["title"], "removed");
});


function showNotification(data, type) {
    console.log("showing notification")
    console.log(data)
    var exisitingNotification = document.getElementById("notification");
    if (exisitingNotification) {
        exisitingNotification.parentNode.removeChild(exisitingNotification);
        console.log("removed existing notification")
    }

    var notification = document.createElement("div");
    if (type == "selected") {
        notification.className = "notification is-success";
    } else if (type == "removed") {
        notification.className = "notification is-danger";
    }
    notification.id = "notification";
    // notification.style.position = "fixed"; // Add this line
    // notification.style.zIndex = "1000"; // Add this line
    // notification.style.left = "50%"; // Add this line
    // notification.style.top = "50%"; // Add this line
    // notification.style.transform = "translate(-50%, -50%)"; // Add this line
    // notification.style.backgroundColor = "white"; // Add this line
    // notification.style.padding = "20px"; // Add this line
    // notification.style.border = "1px solid black"; // Add this line

    notification.style.position = "fixed"; // Position the notification fixed
    notification.style.bottom = "20px"; // 20px from the bottom
    notification.style.right = "20px"; // 20px from the right

    notification.textContent = data + " has been " + type;
    var deleteButton = document.createElement("button");
    deleteButton.className = "delete";
    deleteButton.type = "button";
    deleteButton.addEventListener('click', function () {
        notification.parentNode.removeChild(notification);
    });
    notification.appendChild(deleteButton);
    document.body.appendChild(notification);
}

function addQuestionToRemoval(data) {
    var table = document.getElementById("removeTable");
    var row = document.createElement("tr");
    var question = document.createElement("td");
    question.textContent = data["title"];
    var remove = document.createElement("td");
    var removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "button is-one-quarter removeQuestionTable";
    removeButton.textContent = "Remove";
    removeButton.onclick = function () {
        socketio.emit("remove question", { title: data["title"] });
        console.log("emitting question for removal" + data["title"])
    };
    remove.appendChild(removeButton);
    row.appendChild(question);
    row.appendChild(remove);
    table.appendChild(row);
}

socket.on("question selected", function (data) {
    console.log(data);
    showNotification(data.title, "selected");
    addQuestionToRemoval(data);
});

function removeFromRemoval(title) {
    console.log("running remove from removal function")
    var table = document.getElementById("removeTable");
    var rows = table.getElementsByTagName("tr");
    for (var i = 1; i < rows.length + 1; i++) {
        var row = rows[i];
        console.log(row)
        var question = row.getElementsByTagName("td")[0].textContent;
        console.log(question)
        console.log(title)
        if (question == title) {
            console.log("removing row - running if statement")
            row.parentNode.removeChild(row);
        }
    }
}