"use strict";
var res;

function getBillById(id) {
    $.post({
        url: '/bill',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({bill_id: id})
    }, function(data) {
        if (data) {
            $('#tracker').show();
            $('#search-div').hide();
            $('#select-other').show();

            data = JSON.parse(data);
            res = data;
            setBillState(res.state)
        }
        else
            console.log('invalid query :(')// invalid query :(
    })
}

function setBillState(state) {

}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});