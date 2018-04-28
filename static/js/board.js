// canvas
var canvas = document.getElementById('myCanvas');
var context = canvas.getContext('2d');

// initial
var id = 0;
var rotated = 0;
var elements = [];

var boxSize = 34;
var halfBox = 17;

drawGameState();

document.getElementById("state").innerHTML = Number(id) + "/" + moves.length;
document.getElementById("player1").innerHTML = '<img class="match" src="/static/img/color/' + players[1] + '.png" alt="" /> ' + players[2] + ' &rarr; ' + players[0];
document.getElementById("player2").innerHTML = '<img class="match" src="/static/img/color/' + players[4] + '.png" alt="" /> ' + players[5] + ' &rarr; ' + players[3];

function prev() {
    if (id > 0){id--;}
    document.getElementById("state").innerHTML = Number(id) + "/" + moves.length;
    drawGameState();

    var check_element = elements.indexOf(Number(id));
    if (check_element == -1){
        if (elements.length == 0){
            document.getElementById("status").value = "dodaj schemat";
            document.getElementById("status").style.backgroundColor = "#81AC00";
        } else {
            document.getElementById("status").value = "dodaj element";
            document.getElementById("status").style.backgroundColor = "#81AC00";
        }
    } else {
        document.getElementById("status").value = "usuń element";
        document.getElementById("status").style.backgroundColor = "#ac1d1d";
    }
}

function next() {
    if (id <= moves.length-1){id++;}
    document.getElementById("state").innerHTML = Number(id) + "/" + moves.length;
    drawGameState();

    var check_element = elements.indexOf(Number(id));
    if (check_element == -1){
        if (elements.length == 0){
            document.getElementById("status").value = "dodaj schemat";
            document.getElementById("status").style.backgroundColor = "#81AC00";
        } else {
            document.getElementById("status").value = "dodaj element";
            document.getElementById("status").style.backgroundColor = "#81AC00";
        }
    } else {
        document.getElementById("status").value = "usuń element";
        document.getElementById("status").style.backgroundColor = "#ac1d1d";
    }
}

function rotate() {

    var rotatedMove = '';

    for(var i=0;i<moves.length;i++){
        for(var j=0;j<moves[i].length;j++){
            if (Number(moves[i][j]) < 4){
                rotatedMove = rotatedMove + (Number(moves[i][j])+4).toString(10);
            } else {
                rotatedMove = rotatedMove + (Number(moves[i][j])-4).toString(10);
            }
        }
        moves[i] = rotatedMove;
        rotatedMove = '';
    }

    if (rotated == 0) {
        rotated = 1;
        document.getElementById("id_board").selectedIndex = 1;
        document.getElementById("player1").innerHTML = '<img class="match" src="/static/img/color/' + players[4] + '.png" alt="" /> ' + players[5] + ' &rarr; ' + players[3];
        document.getElementById("player2").innerHTML = '<img class="match" src="/static/img/color/' + players[1] + '.png" alt="" /> ' + players[2] + ' &rarr; ' + players[0];
    } else if (rotated == 1) {
        rotated = 0;
        document.getElementById("id_board").selectedIndex = 0;
        document.getElementById("player1").innerHTML = '<img class="match" src="/static/img/color/' + players[1] + '.png" alt="" /> ' + players[2] + ' &rarr; ' + players[0];
        document.getElementById("player2").innerHTML = '<img class="match" src="/static/img/color/' + players[4] + '.png" alt="" /> ' + players[5] + ' &rarr; ' + players[3];
    }

    drawGameState();
}

function newScheme() {

    var check_element = elements.indexOf(Number(id));

    if (check_element == -1){
        if (elements.length == 0){
            elements.push(Number(id));
            document.getElementById("status").value = "usuń element";
            document.getElementById("status").style.backgroundColor = "#ac1d1d";
            document.getElementById("schemeElements").innerHTML = "&bull; " + elements;
            document.getElementById("id_elements").value = elements;
            document.getElementById("showElements").style.display = "block";
        } else {
            if (Number(id) > elements[elements.length-1]){
                elements.push(Number(id));
                document.getElementById("status").value = "usuń element";
                document.getElementById("status").style.backgroundColor = "#ac1d1d";
                document.getElementById("schemeElements").innerHTML = "&bull; " + elements;
                document.getElementById("id_elements").value = elements;
            } else {
                alert("Co tak nie po kolei? :D");
            }
        }
    } else {
        if (elements.length == 1){
            elements.splice(check_element, 1);
            document.getElementById("status").value = "dodaj schemat";
            document.getElementById("status").style.backgroundColor = "#81AC00";
            //document.getElementById("schemeElements").innerHTML = "&bull; " + elements;
            //document.getElementById("id_elements").value = elements;
            document.getElementById("showElements").style.display = "none";
            document.getElementById("send_form").style.backgroundColor = "#81AC00";
            document.getElementById("scheme_form_fields").style.display = "none";
        } else {
            elements.splice(check_element, 1);
            document.getElementById("status").value = "dodaj element";
            document.getElementById("status").style.backgroundColor = "#81AC00";
            document.getElementById("schemeElements").innerHTML = "&bull; " + elements;
            document.getElementById("id_elements").value = elements;
        }
    }
}

function drawBoard() {

    for(var i=0;i<9;i++){
        for(var j=0;j<11;j++){
            context.beginPath();
            //context.arc(17+i*boxSize, 51+j*boxSize, 1, 0, 2 * Math.PI, false);
            context.arc(halfBox+i*boxSize, (boxSize*2-halfBox)+j*boxSize, 1, 0, 2 * Math.PI, false);
            context.fillStyle = '#ececec';
            context.fill();
        }
    }

    context.beginPath();

    //raw values for boxSize = 34
    //context.moveTo(17, 51);
    //context.lineTo(119, 51);
    //context.lineTo(119, 17);
    //context.lineTo(187, 17);
    //context.lineTo(187, 51);
    //context.lineTo(289, 51);
    //context.lineTo(289, 391);
    //context.lineTo(187, 391);
    //context.lineTo(187, 425);
    //context.lineTo(119, 425);
    //context.lineTo(119, 391);
    //context.lineTo(17, 391);
    //context.lineTo(17, 51);

    context.moveTo(boxSize-halfBox, boxSize*2-halfBox);
    context.lineTo(boxSize*4-halfBox, boxSize*2-halfBox);
    context.lineTo(boxSize*4-halfBox, boxSize-halfBox);
    context.lineTo(boxSize*6-halfBox, boxSize-halfBox);
    context.lineTo(boxSize*6-halfBox, boxSize*2-halfBox);
    context.lineTo(boxSize*9-halfBox, boxSize*2-halfBox);
    context.lineTo(boxSize*9-halfBox, boxSize*12-halfBox);
    context.lineTo(boxSize*6-halfBox, boxSize*12-halfBox);
    context.lineTo(boxSize*6-halfBox, boxSize*13-halfBox);
    context.lineTo(boxSize*4-halfBox, boxSize*13-halfBox);
    context.lineTo(boxSize*4-halfBox, boxSize*12-halfBox);
    context.lineTo(boxSize-halfBox, boxSize*12-halfBox);
    context.lineTo(boxSize-halfBox, boxSize*2-halfBox);

    context.lineWidth = 2.5;
    context.strokeStyle = "#ffffff";
    context.stroke();
}

function drawLine(positionX, positionY, newPositionX, newPositionY, width, color) {
    context.beginPath();
    context.moveTo(positionX, positionY);
    context.lineTo(newPositionX, newPositionY);
    context.lineWidth = width;
    context.strokeStyle = color;
    context.stroke();   
}

function drawCircle(positionX, positionY, radius) {
    context.beginPath();
    context.arc(positionX, positionY, radius, 0, 2 * Math.PI, false);
    context.fillStyle = '#d8e000';
    context.fill(); 
}

function drawGameState() {

    context.fillStyle = "#308048";
    context.fillRect(0,0,306,442);
    drawBoard();

    //var positionX = 153;
    //var positionY = 221;

    var positionX = boxSize*5-halfBox;
    var positionY = boxSize*7-halfBox;

    for(var i=0;i<id;i++){
        var move = moves[i].length;
        for(var j=0;j<move;j++){
            if (moves[i][j] == "0"){
                newPositionX = positionX;
                newPositionY = positionY-boxSize;
                if (i == id-1){
                    drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                    if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.5, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (moves[i][j] == "1"){
                newPositionX = positionX+boxSize;
                newPositionY = positionY-boxSize;
                if (i == id-1){
                    drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                    if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (moves[i][j] == "2"){
                newPositionX = positionX+boxSize;
                newPositionY = positionY;
                if (i == id-1){
                    drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                    if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.5, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (moves[i][j] == "3"){
                newPositionX = positionX+boxSize;
                newPositionY = positionY+boxSize;
                if (i == id-1){
                    drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                    if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            }  else if (moves[i][j] == "4"){
                newPositionX = positionX;
                newPositionY = positionY+boxSize;
                if (i == id-1){
                    drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                    if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.5, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (moves[i][j] == "5"){
                newPositionX = positionX-boxSize;
                newPositionY = positionY+boxSize;
                if (i == id-1){
                    drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                    if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (moves[i][j] == "6"){
                newPositionX = positionX-boxSize;
                newPositionY = positionY;
                if (i == id-1){
                    drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                    if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.5, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (moves[i][j] == "7"){
                newPositionX = positionX-boxSize;
                newPositionY = positionY-boxSize;
                if (i == id-1){
                    drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                    if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            }
        }
    }

    // 1,3,5,...
    if (id%2 != 0){
        if (rotated == 0){
            document.getElementById("move").innerHTML = "#1 &rarr; " + moves[id-1];
        } else {
            document.getElementById("move").innerHTML = "#2 &rarr; " + moves[id-1];
        }
    } else {
        if (rotated == 0){
            if (id == 0) {
                document.getElementById("move").innerHTML = "&nbsp;";
            } else {
                document.getElementById("move").innerHTML = "#2 &rarr; " + moves[id-1];
            }
        } else {
            if (id == 0) {
                document.getElementById("move").innerHTML = "&nbsp;";
            } else {
                document.getElementById("move").innerHTML = "#1 &rarr; " + moves[id-1];
            }
        }
    }
}

