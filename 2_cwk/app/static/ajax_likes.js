$(document).ready(function () {
    // Function to handle like button click
    function handleLikeButtonClick() {
        var movieId = $(this).data('movie-id');
        var likesCountSpan = $(this).siblings('.likes-count');
        var responseLocation = $('#response-' + movieId);

        // Simulate an AJAX request (replace this with your actual AJAX request)
        // For this example, we're updating the likes count and response location immediately
        var currentLikes = parseInt(likesCountSpan.text());
        likesCountSpan.text(currentLikes + 1);
        responseLocation.text("");

        // Toggle the like button icon (add your logic here based on actual server response)
        $(this).toggleClass('liked');
    }

    // Initial setup for like button click event on existing movie cards
    $(".like-icon").on("click", handleLikeButtonClick);

    // Set up an event listener for newly loaded movie cards
    $(document).on('DOMNodeInserted', function (e) {
        // console.log($(e.target).hasClass('container'))
        if ($(e.target).hasClass('container')) {
            // Newly added movie card, attach the like button click event
            $(e.target).find(".like-icon").on("click", handleLikeButtonClick);
        }
    });
});
