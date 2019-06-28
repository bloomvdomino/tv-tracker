(function () {
    'use strict';

    const loader = document.getElementById('loader');
    const button = document.getElementById('delete-btn');

    button.addEventListener('click', function(event) {
        showLoader();
        sendRequest(event.target.dataset.deleteUrl);
    });

    function showLoader() {
        loader.style.display = 'flex';
    }

    function sendRequest(url) {
        const xhr = new XMLHttpRequest();

        xhr.open('DELETE', url);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send();

        xhr.onloadend = function() {
            window.location.href = JSON.parse(xhr.responseText).redirect_to;
        }
    }
})();
