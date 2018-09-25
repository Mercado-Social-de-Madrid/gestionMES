
var TOAST_DELAY = 1200;


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

(function( $ ) {
    function loadResults(resultsContainer, url){
        if (url == null || url == '' || url.startsWith('#')){
            return;
        }
        resultsContainer.addClass('loading-container');
        $.get(url, {}, function(data){
            resultsContainer.find('.results').html(data);
            resultsContainer.find('[data-toggle="tooltip"]').tooltip();
            resultsContainer.find(".link-row").click(function() {
                window.location = $(this).data("href");
            });
            resultsContainer.removeClass('loading-container');
            var preserveHistory = resultsContainer.attr('data-preservehistory');
            if (!preserveHistory || preserveHistory != 'true')
                window.history.replaceState({}, '', url);
        });
    }

    $.fn.ajaxLoader = function( url_or_action ) {
        var self = this;

        if ( url_or_action != null) {

            if (url_or_action === 'reload'){
                var current = self.find('.pagination .page-item.active > a').attr('href');
                loadResults(self, current);
                return self;
            }

            loadResults(self, url);
            return self;
        }

        var initialUrl = self.attr('data-initial');
        if ((initialUrl != null) && (initialUrl!='')){
            loadResults(self, initialUrl);
        }

        self.on('click', '.pagination a', function(e){
            e.preventDefault();
            if ($(this).parent().hasClass('active'))
                return;
            var url = $(this).attr('href')
            loadResults(self, url);
        });

    };

     $.fn.ajaxFilter = function() {
        var self = this;
        var resultsTarget = self.attr('data-results') || '#results';
        var resultsContainer = $(resultsTarget);
        var initialUrl = resultsContainer.attr('data-initial');
        var filterUrl = ((initialUrl != null) && (initialUrl!=''))? initialUrl : '' + '?';

        self.on('submit', function(e){
            e.preventDefault();
            var query = filterUrl + self.serialize();
            loadResults(resultsContainer, query)
        });

        self.on('change', 'select', function(e){
            var query = filterUrl + self.serialize();
            loadResults(resultsContainer, query);
        });

        self.on('click', '.pagination a', function(e){
            e.preventDefault();
            if ($(this).parent().hasClass('active'))
                return;
            var url = $(this).attr('href')
            loadResults(self, url);
        });

    };

}( jQuery ));

function showToast(message, messageClasses){
    var toast = $('<div class="toast"></div>').text(message).addClass(messageClasses);
    toast.appendTo('#main-toasts');
    setTimeout(function(){ toast.fadeOut(); }, TOAST_DELAY);
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(function(){
    
    var menu = $('#navbar-menu');

    $('.floating-label .form-control').floatinglabel();
    $('.show-at-load').modal('show');
    $('.datepicker').pickdate();
    $('.ajax-load').ajaxLoader();
    $('.ajax-filter').ajaxFilter();

    $('[data-toggle="tooltip"]').tooltip();

    $(".link-row").click(function() {
        window.location = $(this).data("href");
    });

    $('.gallery-form').on('submit', function(event ){
        var order = 0;

        $('.gallery-form-photo').each(function(){
            var $question = $(this);
            $question.find('input[id$="order"]').val(order);
            order++;
        });
    });

     $(".gallery-form").on('change', '.form-photo > input', function(){
        var input = this;
        var target = $(input).siblings('.thumb');
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                 target.css('background-image', 'url(' + e.target.result + ')');
                 target.parent().addClass('uploaded');
            }
            reader.readAsDataURL(input.files[0]);
        }
    });

    $('.popup-gallery').magnificPopup({
		delegate: 'a',
		type: 'image',
		mainClass: 'mfp-img-mobile',
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0,1] // Will preload 0 - before current, and 1 after the current image
		}
	});

	var toastCounter = 1;
    $($('.toast-messages .toast').get().reverse()).each(function(){
        var message = $(this);
        setTimeout(function(){ message.fadeOut(); }, TOAST_DELAY * toastCounter);
        toastCounter++;
    });

});



function showToast(message, messageClasses){
    var toast = $('<div class="toast"></div>').text(message).addClass(messageClasses);
    toast.appendTo('#main-toasts');
    setTimeout(function(){ toast.fadeOut(); }, TOAST_DELAY);
}

