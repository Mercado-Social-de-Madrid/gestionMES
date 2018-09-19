
var TOAST_DELAY = 1200;

$(function(){
    
    var menu = $('#navbar-menu');

    $('.floating-label .form-control').floatinglabel();
    $('.show-at-load').modal('show');
    $('.datepicker').pickdate();

    $('[data-toggle="tooltip"]').tooltip();

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

