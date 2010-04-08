function updateNoteItem(elm, note) {
    elm.attr('id', note.id);
    elm.find('.content').html(note.content);
    elm.find('.time').text(note.modified);
    if (note.timestamp) {
        elm.attr('timestamp', note.timestamp);    
    }
    return elm;
}

function loadOnScroll() {
    $(window).scroll(function(){
        var lowestTop = $(document).height() - $(window).height();
        if ($(window).scrollTop() == lowestTop) {
            var last_node = $('.messages .note:last');
            var timestamp = last_node.attr('timestamp');
            $.getJSON('/note/list', {timestamp: timestamp}, function(notes){
                if (notes) {
                    var note_template = $("#note_template");
                    $.each(notes, function(i){
                        var note = this;
                        var note_elm = note_template.clone();
                        updateNoteItem(note_elm, note);
                        last_node.after(note_elm);
                        last_node = note_elm;
                        note_elm.fadeIn("slow");
                    }); //each
                } //if
            }); //post
        } //if
    });
}

function makeNoteDeletable() {
    $(".action a.del").live('click', function(){
        var rm_url = $(this).attr('href');
        if (rm_url) {
            var note_wrapper = $(this).closest('.note');
            var note_id = note_wrapper.attr('id');
            $.post(
                rm_url,
                {note_id: note_id},
                function(success){
                    if (success) {
                        note_wrapper.remove();
                    }
                },
                'json'
            );
        }
        return false;
    });
}
