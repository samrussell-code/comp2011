$(document).ready(function () {
    // Function to handle like button click
    function handleLikeButtonClick() {
        var movieId = $(this).data('movie-id');
        var likesCountSpan = $(this).siblings('.likes-count');
        var responseLocation = $('#response-' + movieId);

        // Check if the like button is already toggled as liked
        var isLiked = $(this).hasClass('liked');

        // Simulate an AJAX request (replace this with your actual AJAX request)
        // For this example, we're updating the likes count and response location immediately
        var currentLikes = parseInt(likesCountSpan.text());

        if (isLiked) {
            // If already liked, decrement the counter and update the response
            likesCountSpan.text(currentLikes - 1);
            // responseLocation.text("Unliked!");
        } else {
            // If not liked, increment the counter and update the response
            likesCountSpan.text(currentLikes + 1);
            // responseLocation.text("Liked!");
        }

        // Toggle the like button icon and update the image source
        $(this).toggleClass('liked');
        var newImageSrc = isLiked ? 'likes_ico.png' : 'likes_ico_liked.png';
        $(this).attr('src', 'static/' + newImageSrc);
    }

    // Initial setup for like button click event on existing movie cards
    $(".like-icon").on("click", handleLikeButtonClick);

    // Set up an event listener for newly loaded movie cards
    $(document).on('DOMNodeInserted', function (e) {
        if ($(e.target).hasClass('container')) {
            // Newly added movie card, attach the like button click event
            $(e.target).find(".like-icon").on("click", handleLikeButtonClick);
        }
    });
});
