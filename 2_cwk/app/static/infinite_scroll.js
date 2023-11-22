document.addEventListener('DOMContentLoaded', function() {
    var isLoading = false;
    var page = 2;
    const movieGrid = document.getElementById('movie-grid');
    const loadingContainer = document.getElementById('loading-container');
    const loadingUrl = movieGrid.getAttribute('data-loading-url');

    function showLoading() {
        loadingContainer.style.display = 'flex';
    }

    function hideLoading() {
        loadingContainer.style.display = 'none';
    }

    function fetchMessages() {
        isLoading = true;
        showLoading();
        console.log('Fetching page ' + page);
        fetch('/movie_card?page=' + page)
            .then(function(response) {
                return response.text();
            })
            .then(function(html) {
                var messageContainer = document.getElementById('movie-grid');
                messageContainer.insertAdjacentHTML('beforeend', html); // Use 'beforeend' here
                isLoading = false;
                page += 1;
                hideLoading();
                console.log('Fetched page ' + (page - 1));
                if (page%5!=0){ // arbitrary extend the number of columns fetched
                    fetchMessages();
                }
            });
    }
    

    window.addEventListener('scroll', function() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 && !isLoading) {
            console.log('Triggering fetchMessages');
            fetchMessages();
        }
    });

    fetchMessages(); // Initial load
});
