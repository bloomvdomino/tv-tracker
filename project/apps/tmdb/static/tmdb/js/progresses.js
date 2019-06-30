(function () {
    'use strict';

    const loader = document.getElementById('loader');
    const buttons = document.getElementsByClassName('watch-next-btn');

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', function(event) {
            showLoader();
            sendRequest(event.target.dataset.watchNextUrl);
        });
    }

    function showLoader() {
        loader.style.display = 'flex';
    }

    function sendRequest(url) {
        const xhr = new XMLHttpRequest();

        xhr.open('PATCH', url);
        xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send();

        xhr.onloadend = function() {
            location.reload(true);
        }
    }
})();
