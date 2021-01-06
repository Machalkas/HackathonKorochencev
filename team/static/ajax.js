var is_hidden=false;
var btn_its_clear='<button type="button" class="btn btn-primary btn-red header-logout"  data-dismiss="modal" id="modal-submit">Ясно</button>';
$("#submit").click(function () {
    document.getElementById("submit").value = "Загрузка";
    console.log($("#form").serialize());
    console.log($("#form"));
    $.ajax({
        url: '/team/manageteam',
        method: 'post',
        dataType: 'html',
        data: $("#form").serialize() + "&action=update",
        success: function (data) {
            console.log(data);
            console.log("-------");
            var x = JSON.parse(data);
            // console.log(x);
            $('#name').html(x["data"]["name"]);
            $('#description').html(x["data"]["description"]);
            $('#link').html(x["data"]["link"]);
            l_team = x["data"]["name"];
            l_desc = x["data"]["description"];
            l_link = x["data"]["link"];
            checkForm();
            $('#result_form').html("")
        },
        error: function (data) {
            console.log(data["error"]);
            try {
                var x = JSON.parse(data["responseText"]);
                $('#result_form').html(x["error"]["name"]["0"])
            }
            catch {
                $('#result_form').html("Ошибка подключения к серверу")
            }
        }
    });
    document.getElementById("submit").value = "Отправить";
});

function leaveTeam(pk) {
    let send = {
        action: "delete-members",
        members: { 0: pk }
    };
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: '/team/manageteam',
        method: 'post',
        dataType: 'json',
        data: send,
        success: function (data) {
            window.location = "/";
        },
        error: function (data) {
            console.log(data.responseJSON["error"]);
            showModal('Ошибка',data.responseJSON["error"],btn_its_clear);
        },
    });
}

function update(team_id, element_id) {
    let send = {
        action: "request",
        team: team_id
    }
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: '/team/manageteam',
        method: 'get',
        dataType: 'json',
        data: send,
        success: function (data) {
            // console.log(data);
            let element = document.getElementById(element_id);
            Increase(Number(data["score"]), element_id, Number(element.innerHTML));
            updateMembers(data["members"]);
        },
        error: function () {
            console.log("Ошибка подключения к серверу")
        }
    });
    setTimeout(update, 10000, team_id, element_id);
}

function submitMembers() {
    let btn = document.getElementById("set_leader0");
    let j = 0;
    let id = null;
    while (btn) {
        if (btn.style.backgroundColor == "goldenrod") {
            id = btn.getAttribute('userid');
            console.log(id);
            break;
        }
        j += 1;
        btn = document.getElementById("set_leader" + j);
    }
    if (id != null) {
        let send = {
            action: "change-leader",
            member: id,
            team: team_pk
        };
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: '/team/manageteam',
            method: 'post',
            dataType: 'json',
            data: send,
            success: function (data) {
                update(team_pk, 'score');
                cancelMembers;
            },
            error: function (data) {
                console.log(data.responseJson["error"]);
                showModal('Ошибка',data.responseJSON["error"],btn_its_clear);
                cancelMembers;
            },
        });
    }
}

function updateMembers(members) {
    console.log("is hidden "+is_hidden);
    let buttons ='<a class="btn btn-primary btn-green" id="submit_members" hidden="'+is_hidden+'" onclick="submitMembers()">Применить</a>\n<a class="btn btn-secondary" id="cancel_members" hidden="'+is_hidden+'" onclick="cancelMembers()">Отмена</a>\n';
    let star_icon = '<svg width="1.3em" height="1.3em"\nviewBox="0 0 16 16" class="bi bi-star-fill" fill="gold" xmlns="http://www.w3.org/2000/svg"\nstyle="margin-left:100%">\n<path\nd="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.283.95l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />\n</svg>\n';
    let div = document.getElementById('members');
    let data = "";
    for (let i = 0; i < members.length; i++) {
        data += '<div class="row mb-3">\n<div class="col-1 themed-grid-col">\n';
        if (members[i]['is_lider'] == true) {
            data += star_icon;
        }
        data += '</div>\n<div class="col-3 themed-grid-col">' + members[i]["first_name"] + ' ' + members[i]["last_name"] + '</div>\n<div class="col-3 themed-grid-col"><a href="mailto:' + members[i]["email"] + '">' + members[i]["email"] + '</a></div>\n<div class="col-3 themed-grid-col">' + members[i]["specialization"] + '<a class="btn btn-secondary btn-sm btn-gold" id="set_leader' + i + '" userid=' + members[i]["id"] + ' onclick="selectLeader(' + i + ')" hidden="'+is_hidden+'">Лидер</a> <a class="btn btn-secondary btn-sm btn-red header-logout" id="delete_member' + i + '" userid=' + members[i]["id"] + ' onclick="selectMember(' + i + ')" hidden="'+is_hidden+'">Удалить</a></div>\n</div>\n';
    }
    data+=buttons;
    div.innerHTML = data;
}

function selectMember(i) {
    let btn = document.getElementById("delete_member" + i);
    //  console.log(btn.style.color);
    if (btn.style.color == '') {
        btn.style.color = "white";
        btn.style.backgroundColor = "red";
        btn.style.borderColor = "red"

    }
    else {
        btn.style.color = '';
        btn.style.backgroundColor = "";
        btn.style.borderColor = ""
    }
}
function selectLeader(i) {
    let btn = document.getElementById("set_leader0");
    let j = 0;
    while (btn) {
        if (j == i && btn.style.backgroundColor != "goldenrod") {
            btn.style.backgroundColor = "goldenrod";
            btn.style.color = "white";
        }
        else {
            btn.style.backgroundColor = "";
            btn.style.color = "";
        }
        j += 1;
        btn = document.getElementById("set_leader" + j);
    }
}
function activateManageMembers() {
    let i = 0;
    let delete_bt = document.getElementById('delete_member' + i);
    let leader_bt = document.getElementById('set_leader' + i);
    let sub = document.getElementById('submit_members');
    let can = document.getElementById('cancel_members');
    let state = !delete_bt.hidden;
    is_hidden=state;
    sub.hidden = is_hidden;
    can.hidden = is_hidden;
    while (delete_bt) {
        delete_bt.hidden = is_hidden;
        leader_bt.hidden = is_hidden;
        i++;
        delete_bt = document.getElementById('delete_member' + i);
        leader_bt = document.getElementById('set_leader' + i);
    }
}
function cancelMembers() {
    let i = 0;
    let delete_bt = document.getElementById('delete_member' + i);
    let leader_bt = document.getElementById('set_leader' + i);
    let sub = document.getElementById('submit_members');
    let can = document.getElementById('cancel_members');
    let state = true;
    sub.hidden = state;
    can.hidden = state;
    while (delete_bt) {
        delete_bt.hidden = state;
        leader_bt.hidden = state;
        i++;
        delete_bt = document.getElementById('delete_member' + i);
        leader_bt = document.getElementById('set_leader' + i);
    }
}

function submitMembers() {
    var is_success=[null,null];
    let btn = document.getElementById("set_leader0");
    let j = 0;
    let id = null;
    while (btn) {
        if (btn.style.backgroundColor == "goldenrod") {
            id = btn.getAttribute('userid');
            console.log(id);
            break;
        }
        j += 1;
        btn = document.getElementById("set_leader" + j);
    }
    if (id != null) {
        let send = {
            action: "change-leader",
            member: id,
            team: team_pk
        };
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: '/team/manageteam',
            method: 'post',
            dataType: 'json',
            data: send,
            success: function (data) {
                // update(team_pk, 'score');
                // cancelMembers;
                // window.location = "/";
                is_success[0]=true;
                success();
                console.log("success");
            },
            error: function (data) {
                console.log(data["error"]);
                showModal('Ошибка',data.responseJSON["error"],btn_its_clear);
                alert(data.responseJSON["error"]);
                cancelMembers;
                is_success[0]=false;
                success();
            },
        });
    }

    btn = document.getElementById("delete_member0");
    j=0;
    let index=0;
    id='{"action": "delete-members","members":{';
    while(btn){
        if(btn.style.backgroundColor =="red"){
            id+='"'+index+'":'+btn.getAttribute('userid')+',';
            index+=1;
        }
        j+=1;
        btn = document.getElementById("delete_member"+j);
    }
    if (id[id.length - 1] == ',') {
        id = id.slice(0, id.length - 1);
    }
    id+='}}';
    console.log(id);
    send=JSON.parse(id);
    console.log(send);
    if(send['members'][0]){
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: '/team/manageteam',
            method: 'post',
            dataType: 'json',
            data: send,
            success: function (data, is_success) {
                // update(team_pk, 'score');
                // cancelMembers;
                // window.location = "/";
                console.log("success");
                is_success[1]=true;
                success();
            },
            error: function (data, is_success) {
                console.log("error");
                alert(data["error"]);
                cancelMembers;
                is_success[1]=false;
                success();
            },
        });
    }
    function success() {
        if (is_success[0]==true || is_success[0]==true) {
            console.log(is_success);
            window.location = "/";
        }
    }
}

function showModal(title, body, footer){
    document.getElementById("modal-title").innerHTML=title;
    document.getElementById("modal-body").innerHTML=body;
    document.getElementById("modal-footer").innerHTML=footer;
    $("#Modal").modal();
}

update(team_pk, 'score');