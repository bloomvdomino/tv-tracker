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
        const request = new XMLHttpRequest();

        request.open('PATCH', url);
        request.setRequestHeader('Content-Type', 'application/json');
        request.send();

        request.onloadend = function() {
            location.reload(true);
        }
    }
})();
