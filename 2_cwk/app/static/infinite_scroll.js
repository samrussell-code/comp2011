document.addEventListener('DOMContentLoaded', function() {
    // instantiate page number, html class definitions
    var isLoading = false;
    var page = 2;
    const loadingContainer = document.getElementById('loading-container');

    // loading icon that only displays when page is waiting for server response
    function showLoading() {
        loadingContainer.style.display = 'flex';
    }

    function hideLoading() {
        loadingContainer.style.display = 'none';
    }

    // calls the view function for that page, inserts the fetched html and then iterates the page number
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
                messageContainer.insertAdjacentHTML('beforeend', html);
                isLoading = false;
                page += 1;
                hideLoading(); // no longer waiting for server response 
                console.log('Fetched page ' + (page - 1));
                // the page needs to be vertically full on first load so that the user can scroll to trigger the content load
                if (page%7!=0){ // arbitrarily extend the number of rows fetched so enough is loaded initially to fill screen
                    fetchMessages();
                }
            });
    }
    
    // all of this is triggered on a scroll event when the movie grid is 100px or less from the botton of the window
    window.addEventListener('scroll', function() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 && !isLoading) {
            console.log('Triggering fetchMessages');
            fetchMessages();
        }
    });

    fetchMessages(); // first time load
});
