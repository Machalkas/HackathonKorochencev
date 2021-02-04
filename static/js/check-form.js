function checkForm(form) {
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