$(document).ready(function(){
    $("#update").click(function(event){
    event.preventDefault();

    var note_id = $('#note_id').text();
    var title = $('#title').val();
    var detail = tinymce.get("detail").getContent();
    var requesttype = "Update";


    $.ajax({
        data: {
            'title': title,
            'detail': detail,
            'note_id': note_id,
            'requesttype': requesttype,
            'savedata': requesttype
        },
        type: 'POST',
        url: '/add',
        success: function(response) { 
            var mydata = response['var1']
            $("#flashmsg").text(mydata).show();
        },
        error: function(exception) {
            alert('Exception:', exception);
        }
    });
    });
    $('#search').on('input', function() {
        $("#flashmsg").text("updated text").show();
    }); 
});

$(document).ready(function(){
    $("#delete").click(function(event){
    event.preventDefault();
    var note_id = $('#note_id').text();
    var title = $('#title').val();
//    var detail = $('#detail').val();
    var detail = tinymce.get("detail").getContent();
    var requesttype = "Delete";

    $.ajax({
        data: {
            'title': title,
            'detail': detail,
            'note_id': note_id,
            'requesttype': requesttype,
            'savedata': requesttype
        },
        type: 'POST',
        url: '/add',
        success: function(response) { 
            var mydata = response['var1']
            $("#flashmsg").text(mydata).show();
        },
        error: function(exception) {
            alert('Exception:', exception);
        }
    });      
});

$("#save").click(function(event){
    event.preventDefault();
    var note_id = $('#note_id').text();
    var title = $('#title').val();
    var detail = tinymce.get("detail").getContent();
    var requesttype = "Save";


    $.ajax({
        data: {
            'title': title,
            'detail': detail,
            'requesttype': requesttype,
            'savedata': requesttype
        },
        type: 'POST',
        url: '/add',
        success: function(response) { 
            var mydata = response['var1']
            $("#flashmsg").text(mydata).show();
        },
        error: function(exception) {
            alert('Exception:', exception);
        }
    });
});
});