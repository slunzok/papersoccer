String.prototype.hashCode = function(){
    var hash = 0;
    if (this.length == 0) return hash;
    for (i = 0; i < this.length; i++) {
        char = this.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}

// initial
//var id = 0;
var rotated = 0;
//var moves = [];
var board = [];

// określenie dozwolonego obszaru 'klikania' i zapisanie aktualnej pozycji kursora
var xrange = [];
var yrange = [];
var cursorX = 4;
var cursorY = 6;
for(var i=3;i<6;i++){xrange.push(i);}
for(var i=5;i<8;i++){yrange.push(i);}

// mazak Gmocha
var gmochId = 0;
var gmochMode = 0;
var gmochMoves = [];
var gmochBlocked = [];
var gmochPermutation = [];

// inne
var multiMove = 0;
var activeArea = 0;
var boxSize = 34;
var halfBox = 17;

var cutMode = 0;

// canvas
var canvas = document.getElementById("myCanvas");
var context = canvas.getContext("2d");

getStartingBoard();
drawGameState();

document.getElementById("state").innerHTML = Number(id) + "/" + moves.length;

// początek - obsługa myszki
// https://www.kirupa.com/canvas/working_with_the_mouse.htm
var canvasPosition = getPosition(canvas);

canvas.addEventListener("mousemove", checkArea, false);
canvas.addEventListener("mousedown", buttonPress, false);

// dodałem jeszcze load, bo w przeciwnym razie pojawiaja sie (przynajmniej u mnie :P) ujemne wartosci w mouseX :(
window.addEventListener("load", updatePosition, false)
window.addEventListener("scroll", updatePosition, false);
window.addEventListener("resize", updatePosition, false);
     
function updatePosition() {
    canvasPosition = getPosition(canvas);
}

function getPosition(element) {
    var xPosition = 0;
    var yPosition = 0;
     
    while (element) {
        xPosition += (element.offsetLeft - element.scrollLeft + element.clientLeft);
        yPosition += (element.offsetTop - element.scrollTop + element.clientTop);
        element = element.offsetParent;
    }
    return {
        x: xPosition,
        y: yPosition
    };
}

function checkArea(e) {

    if (cutMode == 1) {

        if (gmochMode == 0) {

            var mouseX = e.clientX - canvasPosition.x;
            var mouseY = e.clientY - canvasPosition.y;

            var boxX = Math.floor(mouseX/boxSize);
            var boxY = Math.floor(mouseY/boxSize);

            if (xrange.indexOf(boxX) >= 0 && yrange.indexOf(boxY) >= 0 && !(boxX == cursorX && boxY == cursorY)) {
                /* 
                0 -> x:  0, y: -1
                1 -> x:  1, y: -1
                2 -> x:  1, y:  0
                3 -> x:  1, y:  1
                4 -> x:  0, y:  1
                5 -> x: -1, y:  1
                6 -> x: -1, y:  0
                7 -> x: -1, y: -1
                */
                if (boxX-cursorX == 0 && boxY-cursorY == -1) {
                    moveType = "0";
                } else if (boxX-cursorX == 1 && boxY-cursorY == -1) {
                    moveType = "1";
                } else if (boxX-cursorX == 1 && boxY-cursorY == 0) {
                    moveType = "2";
                } else if (boxX-cursorX == 1 && boxY-cursorY == 1) {
                    moveType = "3";
                } else if (boxX-cursorX == 0 && boxY-cursorY == 1) {
                    moveType = "4";
                } else if (boxX-cursorX == -1 && boxY-cursorY == 1) {
                    moveType = "5"; 
                } else if (boxX-cursorX == -1 && boxY-cursorY == 0) {
                    moveType = "6";
                } else if (boxX-cursorX == -1 && boxY-cursorY == -1) {
                    moveType = "7";
                }

                if (board[cursorX][cursorY].indexOf(moveType) == -1) {
                    activeArea = 1;
                    drawGameState();
                    drawCircle(halfBox+boxX*boxSize, halfBox+boxY*boxSize, 3);
                } else {
                    drawGameState();
                }
            } else {
                // po wyjściu z aktywnej strefy, ustaw zmienna na 0 i nie rysuj boiska przy kazdym ruchu myszy :)
                if (activeArea == 1){
                    activeArea = 0;
                    drawGameState();
                }
            }
        }
    }

    // debug
    // document.getElementById('mouse').innerHTML = boxX + ',' + boxY;
    // document.getElementById('mouse').innerHTML = mouseX + ',' + mouseY;
}

function buttonPress(e) {

    if (cutMode == 1) {

        if (gmochMode == 0) {

            if (e.button == 0) {

                var mouseX = e.clientX - canvasPosition.x;
                var mouseY = e.clientY - canvasPosition.y;

                var boxX = Math.floor(mouseX/boxSize);
                var boxY = Math.floor(mouseY/boxSize);

                if (xrange.indexOf(boxX) >= 0 && yrange.indexOf(boxY) >= 0 && !(boxX == cursorX && boxY == cursorY)) {
                    /* 
                    0 -> x:  0, y: -1
                    1 -> x:  1, y: -1
                    2 -> x:  1, y:  0
                    3 -> x:  1, y:  1
                    4 -> x:  0, y:  1
                    5 -> x: -1, y:  1
                    6 -> x: -1, y:  0
                    7 -> x: -1, y: -1
                    */
                    if (boxX-cursorX == 0 && boxY-cursorY == -1) {
                        moveType = "0";
                        reverseMoveType = "4";
                    } else if (boxX-cursorX == 1 && boxY-cursorY == -1) {
                        moveType = "1";
                        reverseMoveType = "5";
                    } else if (boxX-cursorX == 1 && boxY-cursorY == 0) {
                        moveType = "2";
                        reverseMoveType = "6";
                    } else if (boxX-cursorX == 1 && boxY-cursorY == 1) {
                        moveType = "3";
                        reverseMoveType = "7";
                    } else if (boxX-cursorX == 0 && boxY-cursorY == 1) {
                        moveType = "4";
                        reverseMoveType = "0";
                    } else if (boxX-cursorX == -1 && boxY-cursorY == 1) {
                        moveType = "5";
                        reverseMoveType = "1"; 
                    } else if (boxX-cursorX == -1 && boxY-cursorY == 0) {
                        moveType = "6";
                        reverseMoveType = "2";
                    } else if (boxX-cursorX == -1 && boxY-cursorY == -1) {
                        moveType = "7";
                        reverseMoveType = "3";
                    }

                    if (board[cursorX][cursorY].indexOf(moveType) == -1) {
                        board[cursorX][cursorY] = board[cursorX][cursorY] + moveType;
                        board[boxX][boxY] = board[boxX][boxY] + reverseMoveType;
               
                        if (board[boxX][boxY].length == 1) {
                            if (multiMove == 0) {
                                // pojedynczy ruch (tzn. o długości jeden, np. 0, 4)
                                moves.push(moveType);
                                next();
                            } else {
                                // ostatni ruch w wieloruchu
                                moves[moves.length-1] = moves[moves.length-1] + moveType;
                                multiMove = 0;
                            }
                        } else {
                            if (multiMove == 0) {
                                // pierwszy ruch w wieloruchu
                                moves.push(moveType);
                                next();
                                multiMove = 1;
                            } else {
                                // kolejny ruch w wieloruchu
                                moves[moves.length-1] = moves[moves.length-1] + moveType;
                            }
                        } 

                        cursorX = boxX;
                        cursorY = boxY;

                        xrange = [];
                        yrange = [];
                        for(var i=cursorX-1;i<cursorX+2;i++){xrange.push(i);}
                        for(var i=cursorY-1;i<cursorY+2;i++){yrange.push(i);}

                        // pilka w srodku bramki
                        // poprawic, bo jak cofne, to nie dziala :(
                        // w sumie jednak dziala, musze to przemyslec
                        //if (cursorX == 4 && (cursorY == 0 || cursorY == 12)) {
                            //board[cursorX][cursorY] = "01234567";
                        //}

                        if (cursorX == 4 && cursorY == 0) {
                            if (moveType == "1") {
                                board[cursorX][cursorY] = "01234675";
                            } else if (moveType == "0") {
                                board[cursorX][cursorY] = "01235674";
                            } else if (moveType == "7") {
                                board[cursorX][cursorY] = "01245673";
                            }
                            goal = 1;
                            document.getElementById("username").innerHTML = '<label for="id_username">Nick:</label> <input type="text" name="username" class="scheme" autofocus required id="id_username" />';
                            document.getElementById("password1").innerHTML = '<label for="id_password1">Hasło:</label> <input type="password" name="password1" class="scheme" required id="id_password1" />';
                            document.getElementById("password2").innerHTML = '<label for="id_password2">Powtórz:</label> <input type="password" name="password2" class="scheme" required id="id_password2" />';
                            document.getElementById("email").innerHTML = '<label for="id_email">*Email:</label> <input type="text" name="email" class="scheme" id="id_email" />';
                            document.getElementById("kurnik").innerHTML = '<label for="id_kurnik">*Kurnik:</label> <input type="text" name="kurnik" class="scheme" id="id_kurnik" />';
                            document.getElementById("not_required").innerHTML = '* Pola nieobowiązkowe, ale warto je podać (np. jeśli zapomnisz hasła, to jedynie na podstawie tych pól będziesz mógł udowodnić, że jesteś właścicielem konta)';
                            document.getElementById("register_account").innerHTML = '<label></label> <input name="create_custom_replay" type="submit" value="Utwórz konto" />';
                            gmochToggleForm('register_account_form', 'register_an_account');
                        } else if (cursorX == 4 && cursorY == 12) {
                            if (moveType == "3") {
                                board[cursorX][cursorY] = "01234567";
                            } else if (moveType == "4") {
                                board[cursorX][cursorY] = "12345670"
                            } else if (moveType == "5") {
                                board[cursorX][cursorY] = "02345671"
                            }
                            goal = 1;
                            document.getElementById("username").innerHTML = '<label for="id_username">Nick:</label> <input type="text" name="username" class="scheme" autofocus required id="id_username" />';
                            document.getElementById("password1").innerHTML = '<label for="id_password1">Hasło:</label> <input type="password" name="password1" class="scheme" required id="id_password1" />';
                            document.getElementById("password2").innerHTML = '<label for="id_password2">Powtórz:</label> <input type="password" name="password2" class="scheme" required id="id_password2" />';
                            document.getElementById("email").innerHTML = '<label for="id_email">*Email:</label> <input type="text" name="email" class="scheme" id="id_email" />';
                            document.getElementById("kurnik").innerHTML = '<label for="id_kurnik">*Kurnik:</label> <input type="text" name="kurnik" class="scheme" id="id_kurnik" />';
                            document.getElementById("not_required").innerHTML = '* Pola nieobowiązkowe, ale warto je podać (np. jeśli zapomnisz hasła, to jedynie na podstawie tych pól będziesz mógł udowodnić, że jesteś właścicielem konta)';
                            document.getElementById("register_account").innerHTML = '<label></label> <input name="create_custom_replay" type="submit" value="Utwórz konto" />';
                            gmochToggleForm('register_account_form', 'register_an_account');
                        }

                        drawGameState();
                    }
                }
            }
        }
    }
}

// koniec - obsługa myszki

function prev() {
    if (gmochMode == 1){
        if (gmochId > 0){gmochId--;}
        document.getElementById("state").innerHTML = Number(gmochId+1) + "/" + gmochMoves.length;
    } else {
        if (id > 0){id--;}
        document.getElementById("state").innerHTML = Number(id) + "/" + moves.length;
    }
    drawGameState();
}

function next() {
    if (gmochMode == 1){
        if (gmochId < gmochMoves.length-1){gmochId++;}
        document.getElementById("state").innerHTML = Number(gmochId+1) + "/" + gmochMoves.length;
    } else {
        if (id <= moves.length-1){id++;}
        document.getElementById("state").innerHTML = Number(id) + "/" + moves.length;
    }
    drawGameState();
}

function rotate() {

    var rotatedMove = "";

    // 1A. ruchy wykonane przez użytkownika
    for(var i=0;i<moves.length;i++){
        for(var j=0;j<moves[i].length;j++){
            if (Number(moves[i][j]) < 4){
                rotatedMove = rotatedMove + (Number(moves[i][j])+4).toString(10);
            } else {
                rotatedMove = rotatedMove + (Number(moves[i][j])-4).toString(10);
            }
        }
        moves[i] = rotatedMove;
        rotatedMove = "";
    }

    // 1B. ruchy wykonane przez mazak Gmocha
    if (gmochMode == 1) {
        for(var i=0;i<gmochMoves.length;i++){
            for(var j=0;j<gmochMoves[i].length;j++){
                if (Number(gmochMoves[i][j]) < 4){
                    rotatedMove = rotatedMove + (Number(gmochMoves[i][j])+4).toString(10);
                } else {
                    rotatedMove = rotatedMove + (Number(gmochMoves[i][j])-4).toString(10);
                }
            }
            gmochMoves[i] = rotatedMove;
            rotatedMove = "";
        }
    }

    // 2. boisko
    var tmpBoard = [];

    for (i=0;i<9;i++) {
        tmpBoard[i] = [];
        for (j=0;j<13;j++) {
            tmpBoard[i][j] = "";
        }
    }

    for (var i=0;i<9;i++) {
        for(var j=0;j<13;j++){
            for(var k=0;k<board[i][j].length;k++){
                if (Number(board[i][j][k]) < 4){
                    rotatedMove = rotatedMove + (Number(board[i][j][k])+4).toString(10);
                } else {
                    rotatedMove = rotatedMove + (Number(board[i][j][k])-4).toString(10);
                }
            }
            tmpBoard[8-i][12-j] = rotatedMove;
            rotatedMove = "";
        }
    }

    board = tmpBoard.slice(0, tmpBoard.length);

    // 3. kursor

    cursorX = 8-cursorX;
    cursorY = 12-cursorY;

    xrange = [];
    yrange = [];
    for(var i=cursorX-1;i<cursorX+2;i++){xrange.push(i);}
    for(var i=cursorY-1;i<cursorY+2;i++){yrange.push(i);}

    if (rotated == 0) {
        rotated = 1;
    } else if (rotated == 1) {
        rotated = 0;
    }

    drawGameState();
}

function manageMoves() {

    if (cutMode == 0) {

        cutMode = 1;

        removeMoves = moves.length - id;
        moves.splice(id,removeMoves);

        for (var i=0; i<moves.length;i++) {
            for (var j=0; j<moves[i].length;j++) {
                if (moves[i][j] == "0") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "0";
                    board[cursorX][cursorY-1] = board[cursorX][cursorY-1] + "4";   

                    cursorY = cursorY - 1;
                } else if (moves[i][j] == "1") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "1";
                    board[cursorX+1][cursorY-1] = board[cursorX+1][cursorY-1] + "5";

                    cursorX = cursorX + 1;
                    cursorY = cursorY - 1;
                } else if (moves[i][j] == "2") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "2";
                    board[cursorX+1][cursorY] = board[cursorX+1][cursorY] + "6";

                    cursorX = cursorX + 1;
                } else if (moves[i][j] == "3") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "3";
                    board[cursorX+1][cursorY+1] = board[cursorX+1][cursorY+1] + "7";

                    cursorX = cursorX + 1;
                    cursorY = cursorY + 1;
                } else if (moves[i][j] == "4") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "4";
                    board[cursorX][cursorY+1] = board[cursorX][cursorY+1] + "0";

                    cursorY = cursorY + 1;
                } else if (moves[i][j] == "5") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "5";
                    board[cursorX-1][cursorY+1] = board[cursorX-1][cursorY+1] + "1";

                    cursorX = cursorX - 1;
                    cursorY = cursorY + 1;
                } else if (moves[i][j] == "6") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "6";
                    board[cursorX-1][cursorY] = board[cursorX-1][cursorY] + "2";

                    cursorX = cursorX - 1;
                } else if (moves[i][j] == "7") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "7";
                    board[cursorX-1][cursorY-1] = board[cursorX-1][cursorY-1] + "3";

                    cursorX = cursorX - 1;
                    cursorY = cursorY - 1;
                }
            }
        }

        xrange = [];
        yrange = [];
        for(var i=cursorX-1;i<cursorX+2;i++){xrange.push(i);}
        for(var i=cursorY-1;i<cursorY+2;i++){yrange.push(i);}

        next();

        document.getElementById("cut_back_accept").value = "cofnij ruch";
        document.getElementById("save_replay").style.display = "inline";

    } else if (cutMode == 1) {

        if (gmochMode == 0) {

            if (moves.length == id) {
                // wytnij ostatni znak z tablicy board dla aktualnej pozycji kursora
                // w tablicy board będzie to np. "3", a w tablicy moves "7" (czyli to co jest wyświetlane na żółto na stronie)
                // nie ma to znaczenia, od której strony to będę sprawdzał, osobiście jednak będę korzystał z wartości z tablicy board
                // będę mógł skorzystać ze ściagawki z checkArea i buttonPress :)
                lastMove = board[cursorX][cursorY].slice(-1);

                // jeśli długość jest równa 1, to zwróci pusty string dla elementy tablicy board
                lastMoveLength = board[cursorX][cursorY].length;
                removeLastMove = board[cursorX][cursorY].slice(0, lastMoveLength-1);
                board[cursorX][cursorY] = removeLastMove;

                /* 
                0 -> x:  0, y: -1
                1 -> x:  1, y: -1
                2 -> x:  1, y:  0
                3 -> x:  1, y:  1
                4 -> x:  0, y:  1
                5 -> x: -1, y:  1
                6 -> x: -1, y:  0
                7 -> x: -1, y: -1
                */

                if (lastMove == "0") {
                    cursorY = cursorY-1;
                } else if (lastMove == "1") {
                    cursorX = cursorX+1;
                    cursorY = cursorY-1;
                } else if (lastMove == "2") {
                    cursorX = cursorX+1;
                } else if (lastMove == "3") {
                    cursorX = cursorX+1;
                    cursorY = cursorY+1;
                } else if (lastMove == "4") {
                    cursorY = cursorY+1
                } else if (lastMove == "5") {
                    cursorX = cursorX-1;
                    cursorY = cursorY+1;
                } else if (lastMove == "6") {
                    cursorX = cursorX-1;
                } else if (lastMove == "7") {
                    cursorX = cursorX-1;
                    cursorY = cursorY-1;
                }

                // jeden ruch w moves wymaga usunięcia dwóch znaków w dwóch różnych komórkach tablicy board
                // powtórz dla nowych wartości kursora
                lastMoveLength = board[cursorX][cursorY].length;
                removeLastMove = board[cursorX][cursorY].slice(0, lastMoveLength-1);
                board[cursorX][cursorY] = removeLastMove;

                xrange = [];
                yrange = [];
                for(var i=cursorX-1;i<cursorX+2;i++){xrange.push(i);}
                for(var i=cursorY-1;i<cursorY+2;i++){yrange.push(i);}

                userMove = moves[moves.length-1].length;
                if (userMove == 1){
                    moves.splice(moves.length-1,1);
                    multiMove = 0;
                    prev();
                } else {
                    moves[moves.length-1] = moves[moves.length-1].slice(0, userMove-1);
                    multiMove = 1;
                    drawGameState();
                }

            } else {
                while (moves.length != id) {

                    lastMove = board[cursorX][cursorY].slice(-1);

                    lastMoveLength = board[cursorX][cursorY].length;
                    removeLastMove = board[cursorX][cursorY].slice(0, lastMoveLength-1);
                    board[cursorX][cursorY] = removeLastMove;

                    if (lastMove == "0") {
                        cursorY = cursorY-1;
                    } else if (lastMove == "1") {
                        cursorX = cursorX+1;
                        cursorY = cursorY-1;
                    } else if (lastMove == "2") {
                        cursorX = cursorX+1;
                    } else if (lastMove == "3") {
                        cursorX = cursorX+1;
                        cursorY = cursorY+1;
                    } else if (lastMove == "4") {
                        cursorY = cursorY+1
                    } else if (lastMove == "5") {
                        cursorX = cursorX-1;
                        cursorY = cursorY+1;
                    } else if (lastMove == "6") {
                        cursorX = cursorX-1;
                    } else if (lastMove == "7") {
                        cursorX = cursorX-1;
                        cursorY = cursorY-1;
                    }

                    lastMoveLength = board[cursorX][cursorY].length;
                    removeLastMove = board[cursorX][cursorY].slice(0, lastMoveLength-1);
                    board[cursorX][cursorY] = removeLastMove;

                    userMove = moves[moves.length-1].length;
                    if (userMove == 1){
                        moves.splice(moves.length-1,1);
                        multiMove = 0;
                    } else {
                        moves[moves.length-1] = moves[moves.length-1].slice(0,userMove-1);
                        multiMove = 1;
                    }
                }

                xrange = [];
                yrange = [];
                for(var i=cursorX-1;i<cursorX+2;i++){xrange.push(i);}
                for(var i=cursorY-1;i<cursorY+2;i++){yrange.push(i);}

                next();
            }
        }
        else {
            for (var m=0;m<gmochMoves[gmochId].length;m++) {
                if (gmochMoves[gmochId][m] == "0") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "0";
                    board[cursorX][cursorY-1] = board[cursorX][cursorY-1] + "4";   

                    cursorY = cursorY - 1;
                } else if (gmochMoves[gmochId][m] == "1") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "1";
                    board[cursorX+1][cursorY-1] = board[cursorX+1][cursorY-1] + "5";

                    cursorX = cursorX + 1;
                    cursorY = cursorY - 1;
                } else if (gmochMoves[gmochId][m] == "2") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "2";
                    board[cursorX+1][cursorY] = board[cursorX+1][cursorY] + "6";

                    cursorX = cursorX + 1;
                } else if (gmochMoves[gmochId][m] == "3") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "3";
                    board[cursorX+1][cursorY+1] = board[cursorX+1][cursorY+1] + "7";

                    cursorX = cursorX + 1;
                    cursorY = cursorY + 1;
                } else if (gmochMoves[gmochId][m] == "4") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "4";
                    board[cursorX][cursorY+1] = board[cursorX][cursorY+1] + "0";

                    cursorY = cursorY + 1;
                } else if (gmochMoves[gmochId][m] == "5") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "5";
                    board[cursorX-1][cursorY+1] = board[cursorX-1][cursorY+1] + "1";

                    cursorX = cursorX - 1;
                    cursorY = cursorY + 1;
                } else if (gmochMoves[gmochId][m] == "6") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "6";
                    board[cursorX-1][cursorY] = board[cursorX-1][cursorY] + "2";

                    cursorX = cursorX - 1;
                } else if (gmochMoves[gmochId][m] == "7") {
                    board[cursorX][cursorY] = board[cursorX][cursorY] + "7";
                    board[cursorX-1][cursorY-1] = board[cursorX-1][cursorY-1] + "3";

                    cursorX = cursorX - 1;
                    cursorY = cursorY - 1;
                }
            }

            moves.push(gmochMoves[gmochId]);
            id++;

            xrange = [];
            yrange = [];
            for(var i=cursorX-1;i<cursorX+2;i++){xrange.push(i);}
            for(var i=cursorY-1;i<cursorY+2;i++){yrange.push(i);}
                
            gmochId = 0;
            gmochMoves = [];
            gmochBlocked = [];
            gmochPermutation = [];

            marker();
            prev();
        }
    }
}

function setGmochMode() {

    if (cutMode == 0) {
        alert("Najpierw utnij ruch w miejscu, którym chcesz, później możesz uruchomić mazak Gmocha");
    } else if (cutMode == 1) {
        if (multiMove == 0) {
            if (gmochMode == 0) {
                document.getElementById("gmoch").style.backgroundColor = "#ac1d1d";
                gmochMode = 1;

                document.getElementById("cut_back_accept").value = "zatwierdź ruch";
                document.getElementById("all_moves").style.display = "inline";
                document.getElementById("poss").style.display = "inline";
                document.getElementById("block").style.display = "inline";
                document.getElementById("perm").style.display = "inline";

                marker();
                prev();
            } else {
                document.getElementById("gmoch").style.backgroundColor = "#81AC00";
                gmochMode = 0;

                document.getElementById("cut_back_accept").value = "cofnij ruch";
                document.getElementById("all_moves").style.display = "none";
                document.getElementById("poss").style.display = "none";
                document.getElementById("block").style.display = "none";
                document.getElementById("perm").style.display = "none";

                gmochId = 0;
                gmochMoves = [];
                gmochBlocked = [];
                gmochPermutation = [];

                next();
            }
        } else {
            alert("Najpierw zakończ ten ruch, później uruchom mazak Gmocha.");
        }
    }
}

function gmochToggleForm(content, toggle) {

    if (goal == 0) {
        alert("Najpierw odblokuj boisko, później strzel w środek bramki (udowodnisz tym samym, że jesteś człowiekiem)");
    }
    else {
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
}

function marker() {

    var gmochMultiMoves = [];
    var hashCodes = [];
    var endLoop = 0;

    while (endLoop == 0) {

        // pierwsza głębokość przeszukiwania - sprawdzenie wszystkich 8 prawidłowych ruchów
        if (gmochMoves.length == 0 && gmochMultiMoves.length == 0) {

            if (board[cursorX][cursorY].indexOf("0") == -1) {
                if (board[cursorX][cursorY-1].length == 0 || cursorY-1 == 0) {
                    gmochMoves.push("0");
                } else if (board[cursorX][cursorY-1].length == 7) {
                    gmochBlocked.push("0");
                } else {
                    gmochMultiMoves.push("0");
                }
            }
               
            if (board[cursorX][cursorY].indexOf("1") == -1) {
                if (board[cursorX+1][cursorY-1].length == 0 || cursorY-1 == 0) {
                    gmochMoves.push("1");
                } else if (board[cursorX+1][cursorY-1].length == 7) {
                    gmochBlocked.push("1");
                } else {
                    gmochMultiMoves.push("1");
                }
            }

            if (board[cursorX][cursorY].indexOf("2") == -1) {
                if (board[cursorX+1][cursorY].length == 0) {
                    gmochMoves.push("2");
                } else if (board[cursorX+1][cursorY].length == 7) {
                    gmochBlocked.push("2");
                } else {
                    gmochMultiMoves.push("2");
                }
            }

            if (board[cursorX][cursorY].indexOf("3") == -1) {
                if (board[cursorX+1][cursorY+1].length == 0 || cursorY+1 == 12) {
                    gmochMoves.push("3");
                } else if (board[cursorX+1][cursorY+1].length == 7) {
                    gmochBlocked.push("3");
                } else {
                    gmochMultiMoves.push("3");
                }
            }

            if (board[cursorX][cursorY].indexOf("4") == -1) {
                if (board[cursorX][cursorY+1].length == 0 || cursorY+1 == 12) {
                    gmochMoves.push("4");
                } else if (board[cursorX][cursorY+1].length == 7) {
                    gmochBlocked.push("4");
                } else {
                    gmochMultiMoves.push("4");
                }
            }
                             
            if (board[cursorX][cursorY].indexOf("5") == -1) {
                if (board[cursorX-1][cursorY+1].length == 0 || cursorY+1 == 12) {
                    gmochMoves.push("5");
                } else if (board[cursorX-1][cursorY+1].length == 7) {
                    gmochBlocked.push("5");
                } else {
                    gmochMultiMoves.push("5");
                }
            }

            if (board[cursorX][cursorY].indexOf("6") == -1) {
                if (board[cursorX-1][cursorY].length == 0) {
                    gmochMoves.push("6");
                } else if (board[cursorX-1][cursorY].length == 7) {
                    gmochBlocked.push("6");
                } else {
                    gmochMultiMoves.push("6");
                }
            }
                      
            if (board[cursorX][cursorY].indexOf("7") == -1) {
                if (board[cursorX-1][cursorY-1].length == 0 || cursorY-1 == 0) {
                    gmochMoves.push("7");
                } else if (board[cursorX-1][cursorY-1].length == 7) {
                    gmochBlocked.push("7");
                } else {
                    gmochMultiMoves.push("7");
                }
            }

        } else {

            // 1. Utworzenie tymczasowej tablicy tmpBoard i cursorList (+ zmienne tmpCursorX, tmpCursorY)
            var newGmochMultiMoves = [];  

            for(var i=0; i<gmochMultiMoves.length; i++) {
                    
                var tmpBoard = [];

                for (var k=0;k<9;k++) {
                    tmpBoard[k] = [];
                    for (var l=0;l<13;l++) {
                        tmpBoard[k][l] = board[k][l];
                    }
                }

                var tmpCursorX = cursorX;
                var tmpCursorY = cursorY;

                var tmpCursorList = [];

                // 2. Dodanie do tymczasowej tablicy tmpBoard trwających, niedokończonych wieloruchów
                // aby móc poźniej sprawdzać, czy to koniec wieloruchu, czy będzie dalsza głębokość
                for (var m=0;m<gmochMultiMoves[i].length;m++) {
                    if (gmochMultiMoves[i][m] == "0") {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "0";
                        tmpBoard[tmpCursorX][tmpCursorY-1] = tmpBoard[tmpCursorX][tmpCursorY-1] + "4";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "0"]);
                        tmpCursorY = tmpCursorY - 1;
                        tmpCursorList.push([tmpCursorX, tmpCursorY, "4"]);
                    } else if (gmochMultiMoves[i][m] == "1") {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "1";
                        tmpBoard[tmpCursorX+1][tmpCursorY-1] = tmpBoard[tmpCursorX+1][tmpCursorY-1] + "5";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "1"]);
                        tmpCursorX = tmpCursorX + 1;
                        tmpCursorY = tmpCursorY - 1;
                        tmpCursorList.push([tmpCursorX, tmpCursorY, "5"]);
                    } else if (gmochMultiMoves[i][m] == "2") {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "2";
                        tmpBoard[tmpCursorX+1][tmpCursorY] = tmpBoard[tmpCursorX+1][tmpCursorY] + "6";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "2"]);
                        tmpCursorX = tmpCursorX + 1;
                        tmpCursorList.push([tmpCursorX, tmpCursorY, "6"]);
                    } else if (gmochMultiMoves[i][m] == "3") {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "3";
                        tmpBoard[tmpCursorX+1][tmpCursorY+1] = tmpBoard[tmpCursorX+1][tmpCursorY+1] + "7";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "3"]);
                        tmpCursorX = tmpCursorX + 1;
                        tmpCursorY = tmpCursorY + 1;
                        tmpCursorList.push([tmpCursorX, tmpCursorY, "7"]);
                    } else if (gmochMultiMoves[i][m] == "4") {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "4";
                        tmpBoard[tmpCursorX][tmpCursorY+1] = tmpBoard[tmpCursorX][tmpCursorY+1] + "0";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "4"]);
                        tmpCursorY = tmpCursorY + 1;
                        tmpCursorList.push([tmpCursorX, tmpCursorY, "0"]);
                    } else if (gmochMultiMoves[i][m] == "5") {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "5";
                        tmpBoard[tmpCursorX-1][tmpCursorY+1] = tmpBoard[tmpCursorX-1][tmpCursorY+1] + "1";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "5"]);
                        tmpCursorX = tmpCursorX - 1;
                        tmpCursorY = tmpCursorY + 1;
                        tmpCursorList.push([tmpCursorX, tmpCursorY, "1"]);
                    } else if (gmochMultiMoves[i][m] == "6") {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "6";
                        tmpBoard[tmpCursorX-1][tmpCursorY] = tmpBoard[tmpCursorX-1][tmpCursorY] + "2";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "6"]);
                        tmpCursorX = tmpCursorX - 1;
                        tmpCursorList.push([tmpCursorX, tmpCursorY, "2"]);
                    } else if (gmochMultiMoves[i][m] == "7") {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "7";
                        tmpBoard[tmpCursorX-1][tmpCursorY-1] = tmpBoard[tmpCursorX-1][tmpCursorY-1] + "3";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "7"]);
                        tmpCursorX = tmpCursorX - 1;
                        tmpCursorY = tmpCursorY - 1;
                        tmpCursorList.push([tmpCursorX, tmpCursorY, "3"]);
                    }
                } // end for loop: gmochMultiMoves[i].length (po pojedyńczym elemencie tablicy wieloruchów)

                // 3. Na koniec sprawdzenie 8 ruchów. Jeśli można zrobić dany ruch
                // to sprawdź, czy to koniec wieloruchu, blokada, a może dalszy ciąg wieloruchu

                if (tmpBoard[tmpCursorX][tmpCursorY].indexOf("0") == -1) {
                    if (tmpBoard[tmpCursorX][tmpCursorY-1].length == 0 || tmpCursorY-1 == 0) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "0";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "0"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochMoves.push(gmochMultiMoves[i] + "0");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "0");
                        }
                    } else if (tmpBoard[tmpCursorX][tmpCursorY-1].length == 7) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "0";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "0"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochBlocked.push(gmochMultiMoves[i] + "0");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "0");
                        }
                    } else {
                        newGmochMultiMoves.push(gmochMultiMoves[i] + "0");
                    }
                }

                if (tmpBoard[tmpCursorX][tmpCursorY].indexOf("1") == -1) {
                    if (tmpBoard[tmpCursorX+1][tmpCursorY-1].length == 0 || tmpCursorY-1 == 0) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "1";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "1"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochMoves.push(gmochMultiMoves[i] + "1");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "1");
                        }
                    } else if (tmpBoard[tmpCursorX+1][tmpCursorY-1].length == 7) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "1";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "1"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochBlocked.push(gmochMultiMoves[i] + "1");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "1");
                        }
                    } else {
                        newGmochMultiMoves.push(gmochMultiMoves[i] + "1");
                    }
                }

                if (tmpBoard[tmpCursorX][tmpCursorY].indexOf("2") == -1) {
                    if (tmpBoard[tmpCursorX+1][tmpCursorY].length == 0) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "2";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "2"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochMoves.push(gmochMultiMoves[i] + "2");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "2");
                        }
                    } else if (tmpBoard[tmpCursorX+1][tmpCursorY].length == 7) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "2";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "2"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochBlocked.push(gmochMultiMoves[i] + "2");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "2");
                        }
                    } else {
                        newGmochMultiMoves.push(gmochMultiMoves[i] + "2");
                    }
                }

                if (tmpBoard[tmpCursorX][tmpCursorY].indexOf("3") == -1) {
                    if (tmpBoard[tmpCursorX+1][tmpCursorY+1].length == 0 || tmpCursorY+1 == 12) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "3";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "3"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochMoves.push(gmochMultiMoves[i] + "3");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "3");
                        }
                    } else if (tmpBoard[tmpCursorX+1][tmpCursorY+1].length == 7) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "3";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "3"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochBlocked.push(gmochMultiMoves[i] + "3");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "3");
                        }
                    } else {
                        newGmochMultiMoves.push(gmochMultiMoves[i] + "3");
                    }
                }

                if (tmpBoard[tmpCursorX][tmpCursorY].indexOf("4") == -1) {
                    if (tmpBoard[tmpCursorX][tmpCursorY+1].length == 0 || tmpCursorY+1 == 12) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "4";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "4"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochMoves.push(gmochMultiMoves[i] + "4");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "4");
                        }
                    } else if (tmpBoard[tmpCursorX][tmpCursorY+1].length == 7) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "4";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "4"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochBlocked.push(gmochMultiMoves[i] + "4");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "4");
                        }
                    } else {
                        newGmochMultiMoves.push(gmochMultiMoves[i] + "4");
                    }
                }

                if (tmpBoard[tmpCursorX][tmpCursorY].indexOf("5") == -1) {
                    if (tmpBoard[tmpCursorX-1][tmpCursorY+1].length == 0 || tmpCursorY+1 == 12) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "5";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "5"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochMoves.push(gmochMultiMoves[i] + "5");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "5");
                        }
                    } else if (tmpBoard[tmpCursorX-1][tmpCursorY+1].length == 7) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "5";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "5"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochBlocked.push(gmochMultiMoves[i] + "5");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "5");
                        }
                    } else {
                        newGmochMultiMoves.push(gmochMultiMoves[i] + "5");
                    }
                }

                if (tmpBoard[tmpCursorX][tmpCursorY].indexOf("6") == -1) {
                    if (tmpBoard[tmpCursorX-1][tmpCursorY].length == 0) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "6";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "6"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochMoves.push(gmochMultiMoves[i] + "6");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "6");
                        }
                    } else if (tmpBoard[tmpCursorX-1][tmpCursorY].length == 7) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "6";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "6"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochBlocked.push(gmochMultiMoves[i] + "6");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "6");
                        }
                    } else {
                        newGmochMultiMoves.push(gmochMultiMoves[i] + "6");
                    }
                }

                if (tmpBoard[tmpCursorX][tmpCursorY].indexOf("7") == -1) {
                    if (tmpBoard[tmpCursorX-1][tmpCursorY-1].length == 0 || tmpCursorY-1 == 0) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "7";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "7"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochMoves.push(gmochMultiMoves[i] + "7");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "7");
                        }
                    } else if (tmpBoard[tmpCursorX-1][tmpCursorY-1].length == 7) {
                        tmpBoard[tmpCursorX][tmpCursorY] = tmpBoard[tmpCursorX][tmpCursorY] + "7";

                        tmpCursorList.push([tmpCursorX, tmpCursorY, "7"]);
                        boardClicks = tmpCursorList.sort();
                        boardString = tmpCursorList.join("");
                        boardFingerprint = boardString.hashCode();

                        if (hashCodes.indexOf(boardFingerprint) == -1) {
                            hashCodes.push(boardFingerprint);
                            gmochBlocked.push(gmochMultiMoves[i] + "7");
                        } else {
                            gmochPermutation.push(gmochMultiMoves[i] + "7");
                        }
                    } else {
                        newGmochMultiMoves.push(gmochMultiMoves[i] + "7");
                    }
                }

            } // end for loop: gmochMultiMoves.length (po całej tablicy wieloruchów)

            gmochMultiMoves = newGmochMultiMoves.slice(0, newGmochMultiMoves.length);
            if (gmochMultiMoves.length == 0) {endLoop = 1; bull_color = '<span class="green_bull">&bull;</span>';}
            else {bull_color = '<span class="red_bull">&bull;</span>';}

            document.getElementById("all_moves").innerHTML = bull_color + " " + Number(gmochMoves.length+gmochBlocked.length+gmochPermutation.length);
            document.getElementById("poss").value = gmochMoves.length + " ruchów";
            document.getElementById("block").value = gmochBlocked.length + " blocków";
            document.getElementById("perm").value = gmochPermutation.length + " powtórzeń";
        }
    } // end while loop
}

function getStartingBoard() {
    for (i=0;i<9;i++) {
        board[i] = [];
        for (j=0;j<13;j++) {
            board[i][j] = '';
        }
    }

    // góra
    board[0][0] = "01234567";
    board[1][0] = "01234567";
    board[2][0] = "01234567";
    board[3][0] = "0124567";
    board[4][0] = "01267";
    board[5][0] = "0123467";
    board[6][0] = "01234567";
    board[7][0] = "01234567";
    board[8][0] = "01234567";

    board[0][1] = "0124567";
    board[1][1] = "01267";
    board[2][1] = "01267";
    board[3][1] = "067";
    board[5][1] = "012";
    board[6][1] = "01267";
    board[7][1] = "01267";
    board[8][1] = "0123467";

    // dół
    board[0][11] = "0234567";
    board[1][11] = "23456";
    board[2][11] = "23456";
    board[3][11] = "456";
    board[5][11] = "234";
    board[6][11] = "23456";
    board[7][11] = "23456";
    board[8][11] = "0123456";

    board[0][12] = "01234567";
    board[1][12] = "01234567";
    board[2][12] = "01234567";
    board[3][12] = "0234567";
    board[4][12] = "23456";
    board[5][12] = "0123456";
    board[6][12] = "01234567";
    board[7][12] = "01234567";
    board[8][12] = "01234567";

    // lewo i prawo
    for(var i=2;i<11;i++){
        board[0][i] = "04567";
        board[8][i] = "01234";
    }
}

function drawBoard() {

    for(var i=0;i<9;i++){
        for(var j=0;j<11;j++){
            context.beginPath();
            //context.arc(17+i*boxSize, 51+j*boxSize, 1, 0, 2 * Math.PI, false);
            context.arc(halfBox+i*boxSize, (boxSize*2-halfBox)+j*boxSize, 1, 0, 2 * Math.PI, false);
            context.fillStyle = "#ececec";
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
    context.fillStyle = "#d8e000";
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
                    if (gmochMode == 1) {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 1.5, "#ffffff");
                    } else {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                        if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                    }
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
                    if (gmochMode == 1) {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                    } else {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                        if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                    }
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
                    if (gmochMode == 1) {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 1.5, "#ffffff");
                    } else {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                        if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                    }
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
                    if (gmochMode == 1) {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                    } else {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                        if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                    }
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
                    if (gmochMode == 1) {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 1.5, "#ffffff");
                    } else {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                        if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                    }
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
                    if (gmochMode == 1) {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                    } else {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                        if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                    }
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
                    if (gmochMode == 1) {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 1.5, "#ffffff");
                    } else {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                        if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                    }
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
                    if (gmochMode == 1) {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                    } else {
                        drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                        if (j == move-1){drawCircle(newPositionX, newPositionY, 2.5);}
                    }
                }
                else {
                    drawLine(positionX, positionY, newPositionX, newPositionY, 1.2, "#ffffff");
                }
                positionX = newPositionX;
                positionY = newPositionY;
            }
        }
    }

    if (gmochMode == 1) {

        var gmochMove = gmochMoves[gmochId].length;
        for(var j=0;j<gmochMove;j++){
            if (gmochMoves[gmochId][j] == "0"){
                newPositionX = positionX;
                newPositionY = positionY-boxSize;
                drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                if (j == gmochMove-1){drawCircle(newPositionX, newPositionY, 2.5);}
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (gmochMoves[gmochId][j] == "1"){
                newPositionX = positionX+boxSize;
                newPositionY = positionY-boxSize;
                drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                if (j == gmochMove-1){drawCircle(newPositionX, newPositionY, 2.5);}
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (gmochMoves[gmochId][j] == "2"){
                newPositionX = positionX+boxSize;
                newPositionY = positionY;
                drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                if (j == gmochMove-1){drawCircle(newPositionX, newPositionY, 2.5);}
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (gmochMoves[gmochId][j] == "3"){
                newPositionX = positionX+boxSize;
                newPositionY = positionY+boxSize;
                drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                if (j == gmochMove-1){drawCircle(newPositionX, newPositionY, 2.5);}
                positionX = newPositionX;
                positionY = newPositionY;
            }  else if (gmochMoves[gmochId][j] == "4"){
                newPositionX = positionX;
                newPositionY = positionY+boxSize;
                drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                if (j == gmochMove-1){drawCircle(newPositionX, newPositionY, 2.5);}
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (gmochMoves[gmochId][j] == "5"){
                newPositionX = positionX-boxSize;
                newPositionY = positionY+boxSize;
                drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                if (j == gmochMove-1){drawCircle(newPositionX, newPositionY, 2.5);}
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (gmochMoves[gmochId][j] == "6"){
                newPositionX = positionX-boxSize;
                newPositionY = positionY;
                drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                if (j == gmochMove-1){drawCircle(newPositionX, newPositionY, 2.5);}
                positionX = newPositionX;
                positionY = newPositionY;
            } else if (gmochMoves[gmochId][j] == "7"){
                newPositionX = positionX-boxSize;
                newPositionY = positionY-boxSize;
                drawLine(positionX, positionY, newPositionX, newPositionY, 2, "#d8e000");
                if (j == gmochMove-1){drawCircle(newPositionX, newPositionY, 2.5);}
                positionX = newPositionX;
                positionY = newPositionY;
            }
        }
    }

    // 1,3,5,...
    if (id%2 != 0){
        if (rotated == 0){
            if (gmochMode == 0){
                document.getElementById("move").innerHTML = "#1 &rarr; " + moves[id-1];
            } else {
                document.getElementById("move").innerHTML = "#2 &rarr; " + gmochMoves[gmochId];
            }
        } else {
            if (gmochMode == 0){
                document.getElementById("move").innerHTML = "#2 &rarr; " + moves[id-1];
            } else {
                document.getElementById("move").innerHTML = "#1 &rarr; " + gmochMoves[gmochId];
            }
        }
    } else {
        if (rotated == 0){
            if (gmochMode == 0){
                if (id == 0) {
                    document.getElementById("move").innerHTML = "&nbsp;";
                } else {
                    document.getElementById("move").innerHTML = "#2 &rarr; " + moves[id-1];
                }
            } else {
                document.getElementById("move").innerHTML = "#1 &rarr; " + gmochMoves[gmochId];
            }
        } else {
            if (gmochMode == 0){
                if (id == 0) {
                    document.getElementById("move").innerHTML = "&nbsp;";
                } else {
                    document.getElementById("move").innerHTML = "#1 &rarr; " + moves[id-1];
                }
            } else {
                document.getElementById("move").innerHTML = "#2 &rarr; " + gmochMoves[gmochId];
            }
        }
    }
}

