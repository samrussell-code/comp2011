$(document).ready(function() {

    // Configure ajaxSetup so that the CSRF token is added to the header of every request
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            var csrf_token = "{{ csrf_token() }}"; // Use Flask-WTF csrf_token function
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRF-Token", csrf_token());
            }
        }
    });

    // Attach a function to trigger when users click on the voting links - either an up vote, or a down vote
    $("a.vote").on("click", function() {
        var clicked_obj = $(this);

        // Which idea was clicked? Fetch the idea ID
        var idea_id = $(this).attr('id');
        // Is it an upvote or downvote?
        var vote_type = $(this).children()[0].id;

        // This is the actual call which sends data to the server. It captures the data we need in order to update the vote count: the ID of the idea which was clicked, and which count to increment.
        $.ajax({
            url: '/vote',
            type: 'POST',
            data: JSON.stringify({ idea_id: idea_id, vote_type: vote_type, csrf_token: csrf_token}),
            // We are using JSON, not XML
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response);

                // Update the html rendered to reflect new count
                // Check which count to update
                if(vote_type == "up") {
                    clicked_obj.children()[1].innerHTML = " " + response.upvotes;
                } else {
                    clicked_obj.children()[1].innerHTML = " " + response.downvotes;
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});
