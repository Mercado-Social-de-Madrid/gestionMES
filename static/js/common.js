
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


    $('.gallery-form').on('submit', function(event ){
        var order = 0;

        $('.gallery-form-photo').each(function(){
            var $question = $(this);
            $question.find('input[id$="order"]').val(order);
            order++;
        });
    });

    $('.check-onload-form-errors .form-errors').each(function(i,elem){
        var error = $(elem);
        console.log(error);
        var container = error.parents('.expansion-panel');
        var header = container.find('.expansion-panel-toggler .text-warning').removeClass('invisible');

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


	var toastCounter = 1;
    $($('.toast-messages .toast').get().reverse()).each(function(){
        var message = $(this);
        setTimeout(function(){ message.fadeOut(); }, TOAST_DELAY * toastCounter);
        toastCounter++;
    });

    $('form.auto-fill-order').on('submit', function(event ){

        $('.auto-fill-order-group').each(function(){
            var order = 1;
            $(this).find('.auto-fill-order-input').each(function(){
                $(this).val(order);
                order++;
            });
        });

    });

    initElems($('body'));

});

function initElems(container){
    container.find('.floating-label .form-control').floatinglabel();
    container.find('.show-at-load').modal('show');
    container.find('.datepicker').pickdate();
    container.find('.ajax-load').ajaxLoader();
    container.find('.ajax-filter').ajaxFilter();

    container.find('[data-toggle="tooltip"]').tooltip();

    container.find(".link-row").click(function(e) {
        var target = $(e.target);
        if (!target.is('button') && !target.parents('button').length && !target.is('a') && !target.parents('a').length){
            window.location = $(this).data("href");
        }

    });

    container.find('.special-select').select2({ 'theme': 'default custom-select' });

    container.find('.popup-gallery').magnificPopup({
		delegate: 'a',
		type: 'image',
		mainClass: 'mfp-img-mobile',
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0,1] // Will preload 0 - before current, and 1 after the current image
		}
	});

    container.find('.color-widget').each(function(){
        $(this).wrap('<div class="color-container"></div>').spectrum({ preferredFormat: "hex"}).show();
    });
    container.find('.fa-selector').each(function(){
        $(this).iconpicker();
    });

    container.find('.enhanced-select').each(function(){
        var control = $(this);
        var select = control.find('select').addClass('form-control');
        control.find('.tags_declaration > li').each(function(){
            var tag = $(this);
            select.find('option[value="' + tag.attr('data-pk') + '"]').attr('data-color', tag.attr('data-color'));
        })

        select.select2({
            dropdownAutoWidth: true,
            templateResult: function formatSelect(tag){
                var selected = select.find('option[value="' + tag.id + '"]')
                var color = selected.attr('data-color');
                if (color){
                    return $('<span class="tag-bulleted"></span>').text(tag.text).prepend($('<span></span>').css('background-color', color));
                }

                var image = selected.attr('data-image');
                if (image){
                    return $('<span class="tag-image"></span>').text(tag.text).prepend($('<div class="profile-circle"><img src="'+image+'"></div>').css('background-color', color));
                }
            },
            templateSelection: function formatTag(tag){
                var color = select.find('option[value="' + tag.id + '"]').attr('data-color');
                if (color)
                    return $('<span class="tag-selected"></span>').text(tag.text).css('background-color', color);
                else return tag.text;
            }
        });

        control.find('.select2').addClass('form-control input-group').css('width','100%').css('height','auto');
        control.find('.select2-search__field').css('width', '100%');
        setTimeout( function(){ control.css('width', '500px;'); }, 200);
   });
}

function showToast(message, messageClasses){
    var toast = $('<div class="toast"></div>').text(message).addClass(messageClasses);
    toast.appendTo('#main-toasts');
    setTimeout(function(){ toast.fadeOut(); }, TOAST_DELAY);
}

function show_fees(numWorkers, aproxIncome){
    var fees = $('#fees-table td[data-min-income]');

    function updateFee(){
        var workers = numWorkers.val();
        var income = aproxIncome.val();

        fees.each(function(i, elem){
            var fee = $(elem).removeClass('assigned-fee');
            if ((income >= fee.data('min-income')) && (income <= fee.data('max-income')) &&
                (workers >= fee.data('min-workers')) && (workers <= fee.data('max-workers'))){
                fee.addClass('assigned-fee');
            }
        });
    }

    numWorkers.on('input', updateFee);
    aproxIncome.on('input', updateFee);
    updateFee();
}
