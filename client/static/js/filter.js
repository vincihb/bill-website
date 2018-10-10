var init = true
function postResultAndRefresh(res) {
    content = {'res': res, 'init': init};
    init = false;

    $.ajax({
        url: '/result',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(content)
    }).done(function(data) {
        if (data) {
            $('#title')[0].innerHTML = data;
            $('#no')[0].disabled= false;
        }
        else {
            $('#title')[0].innerHTML = 'Error!';
            $('#no')[0].disabled= true;
        }
    }).fail(function(err) {
        $('#title')[0].innerHTML = 'Error!';
        $('#no')[0].disabled= false;
        console.error(err);
    });
}