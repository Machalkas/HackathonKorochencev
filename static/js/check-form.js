function checkForm(form, max_file_size=null) {
    let is_valid = true;
    let is_file_valid = true;

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
        if (max_file_size!=null && form.elements[i].type == "file") {
            if (document.getElementById(form.elements[i].id).files.length > 0) {
                let size = document.getElementById(form.elements[i].id).files[0].size;
                if (size / 1048576 > max_file_size) {
                    form.elements[i].style = "background-color:rgba(248, 37, 37, 0.527);";
                    valid = false;
                    is_file_valid = false;
                }
            }
        }
        elem_valid[i] = valid;
    }
    if (max_file_size==null){
        return is_valid;
    }
    return [is_valid, is_file_valid];
}