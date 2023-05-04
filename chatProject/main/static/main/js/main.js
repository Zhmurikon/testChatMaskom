var block = document.getElementsByClassName("messages")[0];
block.scrollTop = block.scrollHeight;
$(document).ready(function () {

    setInterval(function () {
        $.ajax({
            type: 'GET',
            url: "/getmessage",
            success: function (response) {
                //console.log(response);
                $("#messagesContainer").empty();
                for (var key in response.messagesList) {
                    if (response.messagesList[key].changed == false) {
                        var textToSet = response.messagesList[key].text;
                        var dateToSet = response.messagesList[key].date_created;
                    } else {
                        var textToSet = response.messagesList[key].textChanged;
                        var dateToSet = "отредактировано " + response.messagesList[key].dateChanged;
                    }
                    if (USER_ID == response.messagesList[key].user_id) {
                        var temp = '<div class="message your" id="message' + key + '"></div>';
                    } else {
                        var temp = '<div class="message" id="message' + key + '"></div>';
                    }
                    $("#messagesContainer").append(temp);
                    var img = document.createElement('img');
                    img.src = response.messagesList[key].user_profile;
                    $("#message" + key).append(img);
                    temp = '<div class="messageContainer"> <p class="name">' + response.messagesList[key].username;
                    temp = temp + '</p> <p class="text">' + textToSet;
                    temp = temp + '</p> <div class="dateAndButton"> <p class="date">' + dateToSet;
                    if (USER_ID == response.messagesList[key].user_id) {
                        temp = temp + '</p> <div style="display: flex"> <button dataid="' + response.messagesList[key].id + '" onclick="deleteMessage(this)">Удалить</button> <button onclick="openPopup(this)" dataid="' + response.messagesList[key].id + '" style="margin-left: 10px">Редактировать</button></div></div>';
                    } else {

                        temp = temp + '</p> <div style="display: flex"></div></div>';
                    }
                    $("#message" + key).append(temp);
                }
            },
            error: function (response) {
                alert('An error occured')
            }
        });
    }, 1000);
})
$('textarea[name="text"]').val('');
$(document).on('submit', '#post-form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/sendmessage',
        data: {
            text: $('textarea[name="text"]').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            //alert(data)
        }
    });
    $('textarea[name="text"]').val('');
});

function deleteMessage(el) {
    var elId = el.getAttribute('dataid');
    $.ajax({
        type: 'POST',
        url: '/deletemessage',
        data: {
            id: elId,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            //alert(data)
        }
    });
}


function openPopup(el) {
    var elId = el.getAttribute('dataid');
    document.getElementById('popup').style.display = "flex";
    document.getElementById('messageIdToChange').value = elId;
}

function closePopup() {
    document.getElementById('popup').style.display = "none";
}

function updateMessage() {
    var messageId = document.getElementById('messageIdToChange').value;
    $.ajax({
        type: 'POST',
        url: '/updatemessage',
        data: {
            id: messageId,
            text: $('#changeText').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            //alert(data)
        }
    });



    document.getElementById('popup').style.display = "none";
};