/**
 * Created by Otoniel on 20/11/2016.
 */
function updateViewLibroDiario() {
    var num = document.getElementById("fnum").value;
    var str = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    if (num == 0) {
        document.getElementById("form-container").innerHTML = "";
        return null;
    }

    handler = new XMLHttpRequest();

    handler.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            container = document.getElementById("form-container");
            container.innerHTML = "";
            container.innerHTML = this.responseText;
        }
        if(this.status == 403 || this.status == 404) {
            document.getElementById("form-container").innerHTML = "Atención: " + this.status;
        }
    };

    handler.open("POST", "/get_movimiento_form/",true);
    handler.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    handler.send("mov="+num+"&csrfmiddlewaretoken="+str);
}
