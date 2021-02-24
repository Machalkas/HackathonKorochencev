var start_date, end_date;
function getData() {
    let send={"action":"get-data"}
    $.ajax({
        url: '/ajax',
        method: 'get',
        dataType: 'json',
        data: send,
        success: function (data) {
            // console.log(data);
            start_date=data['start-date'];
            end_date=data['end-date'];
            if (data['start-date']!=null){$("#start").text(formDateTime(start_date))};
            if (data['end-date']!=null){$("#end").text(formDateTime(end_date))};
            if (data['users-count']!=null && $("#users").text()!=data['users-count']){Increase(Number(data['users-count']), 'users', false)};
            if (data['teams-count']!=null&& $("#teams").text()!=data['teams-count']){Increase(Number(data['teams-count']), 'teams', false)};
            timer();
        },
        error: function () {
            console.log("Ошибка подключения к серверу");
        }
    });
}

function timer() {
    let start = start_date;
    let end = end_date;
    let now = new Date();
    let d = 0, h = 0, m = 0, s = 0;
    let day = 'дней';
    if (start != null || end != null) {
        if (start != null && new Date(start) - now > 0) {
            $("#timer-time").fadeIn(0);
            s = parseInt((new Date(start) - now) / 1000);
            $("#timer-title").text("До начала");
        }
        else if (end != null && new Date(end)-now > 0) {
            $("#timer-time").fadeIn(0);
            s = parseInt((new Date(end)-now) / 1000);
            $("#timer-title").text("До конца");
        }
        else if(end != null && new Date(end)-now < 0){
            $("#timer-time").fadeOut();
            $("#timer-title").text("Хаккатон уже закончился");
        }
        else if (end==null && new Date(start) - now < 0){
            $("#timer-time").fadeOut();
            $("#timer-title").text("ПО КОНЯМ!");
        }
        if (s >= 60) {
            m = parseInt(s / 60);
            s %= 60;
        }
        if (m >= 60) {
            h = parseInt(m / 60);
            m %= 60;
        }
        if (h >= 24) {
            d = parseInt(h / 24);
            h %= 24;
        }
        if (d == 0 || d >= 5) {
            day = " дней"
        }
        else if (d == 1) {
            day = " день"
        }
        else if (d <= 4) {
            day = " дня"
        }
        if (s < 10) { s = "0" + s; } else { s += ""; };
        if (m < 10) { m = "0" + m; } else { m += ""; };
        if (h < 10) { h = "0" + h; } else { h += ""; };
        $("#timer-time").html(d + day + "<br>" + h + ":" + m + ":" + s);
        $("#date-time-info").fadeIn(0);
    }
    else{
        $("#date-time-info").fadeOut(0);
    }
    if(start==null){$("#p-start").fadeOut(0);}else{$("#p-start").fadeIn(0);};
    if(end==null){$("#p-end").fadeOut(0);}else{$("#p-end").fadeIn(0);};
    // setTimeout(timer, 1000);
}
setInterval(getData, 60000);
setInterval(timer, 500);
getData();