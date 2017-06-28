$('#id_onoff').change(function () {
    if ($(this).prop('checked') === true) {
        $(this).val('yes');
        $('#message-wrapper').hide();
    } else {
        $(this).val('no');
        $('#message-wrapper').show();
    }
});

$('#testing_webhook').on('click', function () {
    $.get($(this).data('url'))
});

$('#delete_bot_form').submit(function () {
    var answer = confirm("Delete this bot?");
    if (answer == false) return false;
});