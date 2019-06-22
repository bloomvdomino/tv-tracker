(function () {
    'use strict';

    $('.watch-next-btn').click(function(event) {
        $('.loader').css('display', 'flex');

        const url = $(event.target).data('watch-next-url');
        $.post(url).always(function() {
            location.reload(true);
        });
    });
})();
