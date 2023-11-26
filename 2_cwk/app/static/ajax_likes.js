$(document).ready(function () {
    // Function to handle like button click
    function handleLikeButtonClick() {
        // Store a reference to the clicked element
        var $likeIcon = $(this);
        var movieId = $likeIcon.data('movie-id');
        var likesCountSpan = $likeIcon.siblings('.likes-count');
        var responseLocation = $('#response-' + movieId);

        // Check if the like button is already toggled as liked
        var isLiked = $likeIcon.hasClass('liked');

        // Determine the endpoint based on whether it's liked or unliked
        var endpoint = isLiked ? '/unlike_movie/' : '/like_movie/';

        // Make an AJAX request to the determined endpoint
        $.ajax({
            type: 'POST',
            url: endpoint + movieId,
            data: { isLiked: isLiked },
            success: function (data) {
                // Update the likes count on success
                likesCountSpan.text(data.likes);
                responseLocation.text(data.message);

                // Toggle the like button icon and update the image source
                $likeIcon.toggleClass('liked');
                var newImageSrc = isLiked ? likeIconUrl : likedIconUrl;
                $likeIcon.attr('src', newImageSrc);
            },
            error: function (error) {
                console.log(error);
            }
        });
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
    $('.like-icon').keydown(function(event) {
        if (event.key === 'Enter' || event.keyCode === 13) {
            // Trigger the click event when Enter is pressed
            $(this).click();
        }
    });
});
