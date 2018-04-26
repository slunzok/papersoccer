$(function() {
    // initialise
    $('ul#accordion > li > ul').hide();
    $('ul#accordion > li#active > ul').show();

    // accordion
    $('ul#accordion > li > h1').click(function() {
        // do nothing if already expanded
        if($(this).next().css('display') == 'none') {
            $('ul#accordion > li > ul').slideUp();
            $(this).next().slideDown();
        }
    });
});
