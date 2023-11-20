document.addEventListener('DOMContentLoaded', function() {
    var isLoading = false;
    var page = 2;

    function fetchMessages() {
        isLoading = true;
        var loadingContainer = document.getElementById('loading-container');
        if (loadingContainer) {
            loadingContainer.innerHTML = '<img src="{{ url_for("static", filename="loading.gif") }}" alt="Loading...">';
            console.log('Fetching page ' + page);
            fetch('/movie_card?page=' + page)
                .then(function(response) {
                    return response.text();
                })
                .then(function(html) {
                    var messageContainer = document.getElementById('movie-grid');
                    messageContainer.insertAdjacentHTML('beforeend', html);
                    isLoading = false;
                    page += 1;
                    console.log('Fetched page ' + (page - 1));
                });
        } else {
            console.error('Loading container not found');
        }
    }

    window.addEventListener('scroll', function() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 && !isLoading) {
            console.log('Triggering fetchMessages');
            fetchMessages();
        }
    });

    fetchMessages();
});
