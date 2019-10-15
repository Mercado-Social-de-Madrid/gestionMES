$.fn.resizeText = function (options) {
    var settings = $.extend({ maxfont: 100, minfont: 5 }, options);
    var style = $('<style>').html('.nodelays ' +
    '{ ' +
        '-moz-transition: none !important; ' +
        '-webkit-transition: none !important;' +
        '-o-transition: none !important; ' +
        'transition: none !important;' +
    '}');

    function shrink(el, fontsize, minfontsize){
        if (fontsize < minfontsize) return;
        el.style.fontSize = fontsize + 'px';
        if (el.scrollHeight > el.offsetHeight) shrink(el, fontsize - 0.2, minfontsize);
    }

    $('head').append(style);

    $(this).each(function(index, el){
        var element = $(el);
        element.addClass('nodelays');
        shrink(el, settings.maxfont, settings.minfont);
        element.removeClass('nodelays');
    });
    style.remove();
}