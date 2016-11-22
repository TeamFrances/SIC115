/**
 * Created by Otoniel on 20/11/2016.
 */
function getTotal(nombreColumna, destColumna) {
    $total = 0.0;

    $x = $(nombreColumna).count;

    for (var c in $(nombreColumna)){
        $total += parseFloat(c.text());
    }


    var x = $(destColumna).innerHTML;

    $(nombreColumna).each(function () {
        $total += (this).text;
        alert("Prueba");
    });

    x = '$ ' + $total;
}