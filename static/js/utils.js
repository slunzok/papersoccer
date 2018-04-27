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

function toggleForm(content, toggle) {
    var showContent = document.getElementById(content);
    var displaySetting = showContent.style.display;
    var toggleButton = document.getElementById(toggle);

    if (displaySetting == "block") { 
        showContent.style.display = "none";
        toggleButton.style.backgroundColor = "#81AC00";
    } else { 
        showContent.style.display = "block";
        toggleButton.style.backgroundColor = "#ac1d1d";
    }
}
