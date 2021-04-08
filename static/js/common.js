
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
    function loadResults(resultsContainer, url, keepUrl){
        if (url == null || url == '' || url.startsWith('#')){
            return;
        }
        resultsContainer.addClass('loading-container');
        $.get(url, {}, function(data){
            resultsContainer.find('.results').html(data);
            initElems(resultsContainer);

            resultsContainer.removeClass('loading-container');
            if (!keepUrl){

                var preserveHistory = resultsContainer.attr('data-preservehistory');
                if (!preserveHistory || preserveHistory != 'true')
                    window.history.replaceState({}, '', url);
            }

        });
    }


    $.fn.ajaxLoader = function( url_or_action ) {
        this.each(function(){
            var self = $(this);
            var initialUrl = self.attr('data-initial');
            var keepUrl = (self.attr('data-keepurl') != null) && (self.attr('data-keepurl')!='');

            if ( url_or_action != null) {

                if (url_or_action === 'reload'){
                    var current = self.find('.pagination .page-item.active > a').attr('href');
                    loadResults(self, current, keepUrl);
                    return self;
                }

                loadResults(self, url);
                return self;
            }

            if ((initialUrl != null) && (initialUrl!='')){
                loadResults(self, initialUrl, keepUrl);
            }

            self.on('click', '.pagination a', function(e){
                e.preventDefault();
                if ($(this).parent().hasClass('active'))
                    return;
                var url = $(this).attr('href');
                if ((url.startsWith('?')) && (initialUrl != null)){
                    url = initialUrl + url;
                }
                loadResults(self, url, keepUrl);
            });

        });

    };

     $.fn.ajaxFilter = function() {
        var self = this;
        var resultsTarget = self.attr('data-results') || '#results';
        var resultsContainer = $(resultsTarget);
        var initialUrl = resultsContainer.attr('data-initial');
        var filterUrl = ((initialUrl != null) && (initialUrl!=''))? initialUrl : '';
        var parentAjax = false;

        ajaxContainer = self.parents('.ajax-load');
        if (ajaxContainer.length > 0){
            parentAjax = true;
            filterUrl = ajaxContainer.eq(0).attr('data-initial');
            self.siblings('.ajax-load').find('.loading-spinner').remove();
        }

        filterUrl += filterUrl.includes('?') ? '&' : '?';
        self.on('submit', function(e){
            e.preventDefault();
            var query = filterUrl + self.serialize();
            loadResults(resultsContainer, query, parentAjax)
        });

        self.on('change', 'select', function(e){
            var query = filterUrl + self.serialize();
            loadResults(resultsContainer, query, parentAjax);
        });

        self.on('click', '.pagination a', function(e){
            e.preventDefault();
            if ($(this).parent().hasClass('active'))
                return;
            var url = $(this).attr('href')
            loadResults(self, url, parentAjax);
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

    $('.form-photo').on('change', 'input[type="file"]', function(){
        var input = this;
        var imgTarget = $(input).parents('.file-field').attr('data-img-target');
        var target = $(imgTarget);
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                if (imgTarget){
                    target.attr('src', e.target.result);
                }
                else{
                    target.css('background-image', 'url(' + e.target.result + ')');
                    target.parent().addClass('uploaded');
                }
            }
            reader.readAsDataURL(input.files[0]);
        }
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

    // To avoid validation issues in Chrome with hidden inputs in expansion panels, we check for them before submitting the form
    $('form').find('[type="submit"]').on('click', function(e){
        $(this).parents('form').find('input[required],select[required]').each(function(){
            var input = $(this);
            if (input.val() == null || input.val() == '' || input.val().length == 0){
                // Check if it is inside an expansion panel to be able to show the HTML5 validation
                var containerPanel = input.parents('.expansion-panel');
                if (containerPanel.length > 0){
                    if (!containerPanel.hasClass('show')){
                        containerPanel.find('.expansion-panel-toggler').click();
                    }
                }
            }
        });
    });

    $('form.ajax-form').on('submit', function(e){
        e.preventDefault();
        var self = $(this);
        var results = self.find('.results');
        var formData = new FormData(this);

        self.find('[type="submit"]').hide();
        results.addClass('loading-container');

        $.ajax({
            url: self.attr('action'),
            type: 'POST',
            enctype: 'multipart/form-data',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data, status){
                var messages = results.removeClass('loading-container').find('.messages').show();
				if ('results' in data){
                    for (var i=0; i<data['results'].length; i++){
                        messages.append($('<li>').text(data['results'][i]));
                    }
				}
				results.addClass('success');
			},

			error: function (response, status, error) {
			    results.removeClass('loading-container')
				var result = response.responseJSON;
				if (result && 'form_errors' in result){
				    for (var fieldName in result['form_errors']){
				        if (fieldName == '__all__'){
                            results.find('.form-errors').text(result['form_errors'][fieldName]).show();
				            continue;
				        }
				        var field = self.find('[name="'+fieldName+'"]');
				        var fieldContainer = self.find('[name="'+fieldName+'"]').parents('.form-group')
				        var errorLabel = fieldContainer.find('.form-errors');
				        if (errorLabel.length == 0){
				            var errorLabel = $('<div class="d-block invalid-feedback form-errors"></div>').appendTo(fieldContainer);
				        }
				        errorLabel.text(result['form_errors'][fieldName]);
				    }
				}
			}
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
    container.find('[data-toggle="popover"]').popover()
    container.find('[data-toggle="tooltip"]').tooltip();

    if (container.closest('[data-prevent-link="true"]').length == 0){
        container.find(".link-row").click(function(e) {
            var target = $(e.target);
            if (!target.is('button') && !target.parents('button').length && !target.is('a') && !target.parents('a').length){
                window.location = $(this).data("href");
            }
        });
    }

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

    container.find('.threestate-checkbox').each(function(){
        var checkbox = $(this).find('input[type="checkbox"]');
        var select =  $(this).find('select');
        if (select.val() == null || select.val() == ''){
            checkbox.prop('indeterminate', true);
            checkbox.data('indeterminate', 'true');
        }
        else{
            checkbox.prop('indeterminate', false);
            checkbox.data('indeterminate', 'false');
            if (select.val() == 'true'){
                checkbox.prop('checked', 'true');
            }
            checkbox.data('checked', select.val());
        }
        checkbox.on('click', function(e){
            if (checkbox.data('indeterminate')=='true'){
                checkbox.data('indeterminate', 'false');
                checkbox.data('checked', 'true');
                select.val('true');
            }
            else if (checkbox.data('checked')=='true'){
                checkbox.data('indeterminate', 'false');
                checkbox.data('checked', 'false');
                select.val('false');
            }
            else{
                checkbox.data('indeterminate', 'true');
                checkbox.data('checked', 'false');
                select.val(null);
            }
            checkbox.prop('indeterminate', checkbox.data('indeterminate')=='true');
            checkbox.prop('checked', checkbox.data('checked')=='true');
            select.change();
        });
    });

    container.find('[data-visible-by]').each(function(){
        var input = $(this);
        var visibleBy = container.find(input.attr('data-visible-by'));
        visibleBy.on('keyup change', function(){
            value = visibleBy.val();
            input.toggle(value !== null && value !== '')
        });
        visibleBy.change();
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
            if ((income >= fee.data('min-income')) && (income < fee.data('max-income')) &&
                (workers >= fee.data('min-workers')) && (workers <= fee.data('max-workers'))){
                fee.addClass('assigned-fee');
            }
        });
    }

    numWorkers.on('input', updateFee);
    aproxIncome.on('input', updateFee);
    updateFee();
}
