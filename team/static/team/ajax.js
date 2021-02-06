var is_hidden=true;
var btn_its_clear='<button type="button" class="btn btn-primary btn-red header-logout"  data-dismiss="modal" id="modal-submit">Ясно</button>';
$("#submit").click(function () {
    document.getElementById("submit").value = "Загрузка";
    // console.log($("#form").serialize());
    console.log($("#form"));
    $.ajax({
        url: '/team/ajax',
        method: 'post',
        dataType: 'html',
        data: $("#form").serialize() + "&action=update",
        success: function (data) {
           // console.log(data);
           // console.log("-------");
            var x = JSON.parse(data);
            // console.log(x);
            $('#name').html(x["data"]["name"]);
            // $('#description').html(x["data"]["description"]);
            $('#link').html(x["data"]["link"]);
            l_team = x["data"]["name"];
            // l_desc = x["data"]["description"];
            l_link = x["data"]["link"];
            checkForm();
            $('#result_form').html("")
        },
        error: function (data) {
           // console.log(data["error"]);
            try {
                data = JSON.parse(data["responseText"]);
                // console.log(data);
                let errors = "";
                for (i in data["error"]) {
                    console.log(data["error"][i]);
                    errors += '<p class="lead" style="font-size: 1em;">' + data["error"][i] + '</p>\n';
                }
                $('#result_form').html(errors)
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
        action: "delete-member",
        member: pk
    };
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: '/team/ajax',
        method: 'post',
        dataType: 'json',
        data: send,
        success: function (data) {
            window.location = "/";
        },
        error: function (data) {
           // console.log(data.responseJSON["error"]);
            setTimeout(showModal,300,'Ошибка',data.responseJSON["error"]);
            // showModal('Ошибка',data.responseJSON["error"],btn_its_clear);
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
        url: '/team/ajax',
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
    setTimeout(update, 60000, team_id, element_id);
}

function updateMembers(members) {
   // console.log("is hidden "+is_hidden);
    let hidden="";
    if (is_hidden){
        hidden="hidden";
    }
    let buttons ='<a class="btn btn-primary btn-green" id="submit_members" '+hidden+' onclick="submitMembers()">Применить</a>\n<a class="btn btn-secondary" id="cancel_members" '+hidden+' onclick="cancelMembers()">Отмена</a>\n';
    let star_icon = '<svg width="1.3em" height="1.3em"\nviewBox="0 0 16 16" class="bi bi-star-fill" fill="gold" xmlns="http://www.w3.org/2000/svg"\nstyle="margin-left:100%">\n<path\nd="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.283.95l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />\n</svg>\n';
    let div = document.getElementById('members');
    let data = "";
    for (let i = 0; i < members.length; i++) {
        data += '<div class="row mb-3">\n<div class="col-1 themed-grid-col">\n';
        if (members[i]['is_lider'] == true) {
            data += star_icon;
        }
        data += '</div>\n<div class="col-3 themed-grid-col">' + members[i]["first_name"] + ' ' + members[i]["last_name"] + '</div>\n<div class="col-3 themed-grid-col"><a href="mailto:' + members[i]["email"] + '">' + members[i]["email"] + '</a></div>\n<div class="col-3 themed-grid-col">' + members[i]["specialization"] + '<a class="btn btn-secondary btn-sm btn-gold" id="set_leader' + i + '" userid=' + members[i]["id"] + ' onclick="selectLeader(' + i + ')" '+hidden+'>Лидер</a> <a class="btn btn-secondary btn-sm btn-red header-logout" id="delete_member' + i + '" userid=' + members[i]["id"] + ' onclick="selectMember(' + i + ')" '+hidden+'>Удалить</a></div>\n</div>\n';
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
    is_hidden=false;
}

function submitMembers() {
    let btn_del = document.getElementById("delete_member0");
    let j = 0;
    let index = 0;
    delete_id = '{';
    while (btn_del) {
        if (btn_del.style.backgroundColor == "red") {
            delete_id += '"' + index + '":' + btn_del.getAttribute('userid') + ',';
            index += 1;
        }
        j += 1;
        btn_del = document.getElementById("delete_member" + j);
    }
    if (delete_id[delete_id.length - 1] == ',') {
        delete_id = delete_id.slice(0, delete_id.length - 1);
    }
    delete_id += '}';
    delete_id = JSON.parse(delete_id);

    let btn_leader = document.getElementById("set_leader0");
    j = 0;
    let leader_id = null;
    while (btn_leader) {
        if (btn_leader.style.backgroundColor == "goldenrod") {
            leader_id = btn_leader.getAttribute('userid');
            break;
        }
        j += 1;
        btn_leader = document.getElementById("set_leader" + j);
    }
    let send = {
        action: "update-members",
        "delete-members": delete_id,
        leader: leader_id,
        team: team_pk
    };
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: '/team/ajax',
        method: 'post',
        dataType: 'json',
        data: send,
        success: function (data) {
            update(team_pk, 'score');
            cancelMembers;
            window.location.reload();
        },
        error: function (data) {
           console.log(data)
            let error="";
            try {
                if (data.responseJSON["change-leader"]["error"] != undefined) {
                    error += data.responseJSON["change-leader"]["error"] + ". ";
                }
            }
            catch { }
            try {
                if (data.responseJSON["delete-members"]["error"] != undefined) {
                    error += data.responseJSON["delete-members"]["error"];
                }
            }
            catch { }
            if(error!=""){
                showModal('Ошибка',error, btn_its_clear);
            }
            // alert(data.responseJSON["error"]);
        },
    });

}

function showModal(title, body, footer=btn_its_clear){
    document.getElementById("modal-title").innerHTML=title;
    document.getElementById("modal-body").innerHTML=body;
    document.getElementById("modal-footer").innerHTML=footer;
    $("#Modal").modal();
}

var create_team_result_form = document.getElementById("create_team_result_form");
$("#create_team_submit").click(function () {
    if (createTeamCheckForm(document.forms["create_team_form"])) {
        $.ajax({
            url: '/team/ajax',
            method: 'post',
            dataType: 'html',
            data: $("#create_team_form").serialize() + "&action=create-team",
            success: function (data) {
                test = data;
                data = JSON.parse(data);
                location = data["url"];
            },
            error: function (data) {
                data = JSON.parse(data["responseText"]);
                try {
                    create_team_result_form.innerHTML = data["error"]['name'][0];
                } catch {
                    create_team_result_form.innerHTML = data["error"];
                }
            }
        })
    }
    else {
        create_team_result_form.innerHTML = "Заполните все обязательные поля"
    }
});
function createTeamCheckForm(form) {
    let is_valid = true;
    let elem_valid = [];
    elem_valid.length = form.elements.length;
    for (let i = 0; i < form.elements.length; i++) {
        let valid = true;
        form.elements[i].style = "";
        if (form.elements[i].required && form.elements[i].value == "") {
            form.elements[i].style = "background-color:rgba(248, 37, 37, 0.527);";
            valid = false;
            is_valid = false;
        }
        elem_valid[i] = valid;
    }
    return is_valid;
}

update(team_pk, 'score');