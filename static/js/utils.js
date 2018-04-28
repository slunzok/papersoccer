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

function sortTable(n, tableToSort) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(tableToSort);
  switching = true;
  dir = "asc"; 

  while (switching) {
    switching = false;
    rows = table.getElementsByTagName("TR");

    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;

      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];

      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch= true;
          break;
        }
      }
    }

    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++; 
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

