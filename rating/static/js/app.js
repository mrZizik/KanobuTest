/**
 * Created by Ali Abdulmadzhidov on 16.03.17 23:45.
 */

$(document).ready(function() {

    $('.like').click(function() {
        var objid = $(this).attr("data-id");
        var type = $(this).attr("data-type");
        var csrf = $(this).attr("data-csrf-token")
        $.post('/like/'+objid+'/',{"type": type, "csrfmiddlewaretoken": csrf}, function (data) {
            $('#' + type + '_likes_count_'+objid).html("<i class=\"icon-thumbs-up\"></i> " + data.likes);
            $('#' + type + '_dislikes_count_'+objid).html("<i class=\"icon-thumbs-down\"></i> " + data.dislikes);
        });
    });

    $('.dislike').click(function() {
        var objid = $(this).attr("data-id");
        var type = $(this).attr("data-type");
        var csrf = $(this).attr("data-csrf-token")
        $.post('/dislike/'+objid+'/',{"type": type, "csrfmiddlewaretoken": csrf}, function (data) {
            $('#' + type + '_likes_count_'+objid).html("<i class=\"icon-thumbs-up\"></i> " + data.likes);
            $('#' + type + '_dislikes_count_'+objid).html("<i class=\"icon-thumbs-down\"></i> " + data.dislikes);

        });
    });
});