$(document).ready(function () {
    function handleLikeButtonClick() {
        // instantiate the icon, the endpoint url, the bool representing if icon is currently in liked state
        var $likeIcon = $(this);
        var movieId = $likeIcon.data('movie-id');
        var likesCountSpan = $likeIcon.siblings('.likes-count');
        var responseLocation = $('#response-' + movieId);

        var isLiked = $likeIcon.hasClass('liked');
        var endpoint = isLiked ? '/unlike_movie/' : '/like_movie/';

        // ajax request
        $.ajax({
            type: 'POST',
            url: endpoint + movieId,
            data: { isLiked: isLiked },
            success: function (data) {
                // we toggle the button, change the message (the like count), change the image and attribute it to $(this)
                likesCountSpan.text(data.likes);
                responseLocation.text(data.message);

                $likeIcon.toggleClass('liked');
                var newImageSrc = isLiked ? likeIconUrl : likedIconUrl;
                $likeIcon.attr('src', newImageSrc);
            },
            error: function (error) {
                console.log(error);
            }
        });
    }

    $(".like-icon").on("click", handleLikeButtonClick);
    // because we are inserting html for more movies with infscroll we must handle those too
    // as this js is configured before the page is loaded, we need it to check for new content after load.
    $(document).on('DOMNodeInserted', function (e) {
        if ($(e.target).hasClass('container')) {
            $(e.target).find(".like-icon").on("click", handleLikeButtonClick);
        }
    });
    // we also should make the request keyboard compatible, so the enter key imitates a mouse click action and calls the main function above
    $('.like-icon').keydown(function(event) {
        if (event.key === 'Enter' || event.keyCode === 13) {
            $(this).click();
        }
    });
});
