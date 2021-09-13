$(function () {
    $('#rechazar_ticket_btn').on('click',function(){
        var ticket_id = $('#ticket_id_template').val();
        window.location.href = '/helpdesk/ticket/reject/' +  ticket_id;
    });
}
);
