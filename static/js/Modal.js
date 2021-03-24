var func=null;
var Modal_btn_its_clear='<button type="button" class="btn btn-primary btn-red header-logout"  data-dismiss="modal" id="modal-submit">Ясно</button>';
var Modal_btn_logout='<button type="button" class="btn btn-primary btn-red header-logout"  data-dismiss="modal" id="modal-submit" onclick="'+func+'">Выйти</button><button type="button" class="btn btn-secondary btn-green header-join" data-dismiss="modal" id="modal-cancel" onclick="">Отмена</button>'
var Modal_btn_chose='<button type="button" class="btn btn-secondary btn-green header-join" data-dismiss="modal" id="modal-cancel" onclick="'+func+'">Подтвердить</button><button type="button" class="btn btn-primary btn-red header-logout"  data-dismiss="modal" id="modal-submit" onclick="">Отмена</button>'
function showModal(title, body, footer=Modal_btn_its_clear, f=null){
    if (f!=null && typeof(f)=='string'){
        func=f;
    }
    document.getElementById("modal-title").innerHTML=title;
    document.getElementById("modal-body").innerHTML=body;
    document.getElementById("modal-footer").innerHTML=footer;
    $("#Modal").modal();
}