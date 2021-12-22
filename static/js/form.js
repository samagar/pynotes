$(document).ready(function(){

    $("#update").click(function(event){
    event.preventDefault();

    var note_id = $('#note_id').text();
    var title = $('#title').val();
    var detail = tinymce.get("detail").getContent();
    
    $.ajax({
        data: {
            'title': title,
            'detail': detail,
            'note_id': note_id,
        },
        type: 'POST',
        url: '/update',
        success: function(response) { 
            location.reload()
        },
        error: function(exception) {
            alert('Exception:', exception);
        }
    });
    });

    $('#search').on('input', function() {
        $("#flashmsg").text("updated text").show();
    });

    $("#delete").click(function(event){
        event.preventDefault();
        var note_id = $('#note_id').text();
    
        $.ajax({
            data: {
                'note_id': note_id,
            },
            type: 'POST',
            url: '/delete',
            success: function(response) { 
                var mydata = response['var1']
                $("#flashmsg").text(mydata).show()
                location.reload()
            },
            error: function(exception) {
                alert('Exception:', exception);
            }
        });      
    });

    $("#add").click(function(event){
        event.preventDefault();
        var title = $('#title').val();
        var detail = tinymce.get("detail").getContent();    
    
        $.ajax({
            data: {
                'title': title,
                'detail': detail,
            },
            type: 'POST',
            url: '/add',
            success: function(response) { 
                location.reload()
            },
            error: function(exception) {
                alert('Exception:', exception);
            }
        });
    });

    $(".sidebar").click(function(event){
        var $div = $(this);
        var note_id = $div.attr("value")
        var callfrom = 'select'
        $.ajax({
            data: {
                'note_id': note_id
            },
            type: 'GET',
            url: '/select',
            success: function(response) { 
                var title = response['title']
                var detail = response['detail']
                tinymce.get("detail").setContent(detail)
                $("#title").val(title)
                $("#note_id").text(note_id)
                $("#activity").show()
                $("#update").show()
                $("#delete").show()
                $("#add").css('display','none')
            },
            error: function(exception) {
                alert('Exception:', exception);
            }
        });
    });

    $("#new").click(function(event){
        event.preventDefault();
        var callfrom = 'new'
        $.ajax({
            data: {'callfrom': callfrom},
            type: 'POST',
            url: '/main',
            success: function(response) { 
                var title = response['title']
                var detail = response['detail']
                tinymce.get("detail").setContent("")
                $("#title").val("")
                $("#note_id").text("")
                $("#activity").hide()
                $("#update").hide()
                $("#delete").hide()
                $("#add").css('display','inline')
            },
            error: function(exception) {
                alert('Exception:', exception);
            }
        });
    });
    
});