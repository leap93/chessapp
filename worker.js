onmessage = (e) => {
	var workerResult = pickMoveInner(e.data[0], e.data[1], e.data[2]);
	postMessage([workerResult, e.data[3]]);

};


function Board(pieces){
	this.allMoves = [];
	this.pieces = pieces;
	this.boardGrid = [null, Array.apply(null, Array(9)).map(function (x) { return null; }), Array.apply(null, Array(9)).map(function (x) { return null; }), Array.apply(null, Array(9)).map(function (x) { return null; }), Array.apply(null, Array(9)).map(function (x) { return null; }), Array.apply(null, Array(9)).map(function (x) { return null; }), Array.apply(null, Array(9)).map(function (x) { return null; }), Array.apply(null, Array(9)).map(function (x) { return null; }), Array.apply(null, Array(9)).map(function (x) { return null; })];
	for(var piece in pieces){
		this.boardGrid[pieces[piece].x][pieces[piece].y] = pieces[piece]
	}
}

function removePiece(x, y, board){
	for(var index in board.pieces){
		var piece = board.pieces[index];
		if(piece.x == x && piece.y == y){
			board.pieces.splice(index, 1);
			return piece;
		}
	}				
	return null;
}

function copyBoard(board){
	var pieces = []
	for(var x = 0; x < board.pieces.length; x++){
		pieces.push(copyPiece(board.pieces[x]));
	}
	var boardCopy = new Board(pieces);
	return boardCopy;
}

function Move(x, y, dx, dy, piece){
	this.x = x;
	this.y = y;
	this.dx = dx;
	this.dy = dy;
	this.piece = piece;
}

function execute(board, move){
	move.isEnPassant = false;
	move.isShortCastling = false;
	move.isLongCastling = false;
	move.pawnToQueen = false;
	//check if the move is a castling
	if(move.piece.type == "king" && move.x == 5 && move.dx == 3){
		board.boardGrid[4][move.y] = board.boardGrid[1][move.y];
		board.boardGrid[1][move.y] = null;
		board.boardGrid[4][move.y].x = 4;
		move.longCastling = true;
	}
	if(move.piece.type == "king" && move.x == 5 && move.dx == 7){
		board.boardGrid[6][move.y] = board.boardGrid[8][move.y];
		board.boardGrid[8][move.y] = null;
		board.boardGrid[6][move.y].x = 6;
		move.shortCastling = true;
	}								

	//check if pawn is converted to a queen
	if(move.piece.name == "wpawn" && move.dy == 8){
		move.pawnToQueen = true;
		move.piece.name = "wqueen";
		move.piece.type = "queen";	
	}
	if(move.piece.name == "bpawn" && move.dy == 1){
		move.pawnToQueen = true;
		move.piece.name = "bqueen";
		move.piece.type = "queen";	
	}

	move.removedPiece = removePiece(move.dx, move.dy, board);
	move.piece.x = move.dx;
	move.piece.y = move.dy;
	board.boardGrid[move.dx][move.dy] = move.piece;
	board.boardGrid[move.x][move.y] = null;				
	board.allMoves.push(move);
}		

function undo(board, move){
	move.piece.x = move.x;
	move.piece.y = move.y;
	board.boardGrid[move.dx][move.dy] = move.removedPiece;
	if(move.removedPiece !== null){
		board.pieces.push(move.removedPiece);
	}
	
	board.boardGrid[move.x][move.y] = move.piece;
	if(move.pawnToQueen){
		move.piece.name = move.piece.color + "pawn";
		move.piece.type = "pawn";
	}
	if(move.shortCastling){
		board.boardGrid[8][move.y] = board.boardGrid[6][move.y];
		board.boardGrid[6][move.y] = null;
		board.boardGrid[8][move.y].x = 8;						
	}
	if(move.longCastling){
		board.boardGrid[1][move.y] = board.boardGrid[4][move.y];
		board.boardGrid[4][move.y] = null;
		board.boardGrid[1][move.y].x = 1;					
	}					
	board.allMoves.pop();
}		

function Piece(name, x, y){
	this.name = name;
	this.x = x;
	this.y = y;
	this.color = name.charAt(0);
	this.type = name.substring(1);
}		

function hasMoved(board, piece){
	for(var move in board.allMoves){
		if(board.allMoves[move].piece.name == piece.name && board.allMoves[move].piece.x == piece.x && board.allMoves[move].piece.y == piece.y){
			return true;
		}
	}
	return false;
};			

function isLegalMove(dx, dy, board, piece){
	if(dx > 8 || dx < 1 || dy > 8 || dy < 1){
		return false;
	}
	if(piece.type == "pawn"){
		return isLegalMovePawn(piece, dx, dy, board);
	}else if(piece.type == "knight"){
		return isLegalMoveKnight(piece, dx, dy, board);
	}else if(piece.type == "bishop"){
		return isLegalMoveBishop(piece, dx, dy, board);
	}else if(piece.type == "rook"){
		return isLegalMoveRook(piece, dx, dy, board);
	}else if(piece.type == "queen"){
		return isLegalMoveRook(piece, dx, dy, board) || isLegalMoveBishop(piece, dx, dy, board);
	}else{
		return isLegalMoveKing(piece, dx, dy, board);
	}
}

function copyPiece(piece){
	return new Piece(piece.name, piece.x, piece.y);
}				
		
function isLegalMovePawn(piece, dx, dy, board){
	var destination = board.boardGrid[dx][dy];
	if(piece.color == "w"){
		if(piece.y == 2 && piece.y + 2 == dy && piece.x == dx && destination === null && board.boardGrid[dx][dy-1] === null){
			return true;
		}
		if(piece.y + 1 == dy && piece.x == dx && destination === null){
			return true;
		}					
		
		if(piece.y + 1 == dy && Math.abs(piece.x - dx) == 1 && destination !== null && destination.color == "b"){
			return true;
		}							
	}else{
		if(piece.y == 7 && piece.y - 2 == dy && piece.x == dx && destination === null && board.boardGrid[dx][dy+1] === null){
			return true;
		}
		if(piece.y - 1 == dy && piece.x == dx && destination === null){
			return true;
		}					
		
		if(piece.y - 1 == dy && Math.abs(piece.x - dx) == 1 && destination !== null && destination.color == "w"){
			return true;
		}						
	}		
	return false;
}

function isLegalMoveKnight(piece, dx, dy, board){
	var destination = board.boardGrid[dx][dy];
	if(destination !== null && destination.color == piece.color){
		return false;
	}
	if((Math.abs(piece.x - dx) == 2 && Math.abs(piece.y - dy) == 1) || (Math.abs(piece.x - dx) == 1 && Math.abs(piece.y - dy) == 2)){
		return true;
	}
	return false;
}

function isLegalMoveBishop(piece, dx, dy, board){
	var destination = board.boardGrid[dx][dy];
	if(destination !== null && destination.color == piece.color){
		return false;
	}
	if(Math.abs(piece.x - dx) != Math.abs(piece.y - dy)){
		return false;
	}
	for(var d = 1; d < Math.abs(piece.x - dx); d++){
		if(board.boardGrid[piece.x+Math.sign(dx - piece.x)*d][piece.y+Math.sign(dy - piece.y)*d] !== null){
			return false;
		}			
	}
	return true;
}			

function isLegalMoveRook(piece, dx, dy, board){
	var destination = board.boardGrid[dx][dy];
	if(destination !== null && destination.color == piece.color){
		return false;
	}		
	
	if(piece.y == dy){
		for(var d = 1; d < Math.abs(piece.x - dx); d++){
			if(board.boardGrid[piece.x+Math.sign(dx - piece.x)*d][piece.y] !== null){
				return false;
			}					
		}
	}else if(piece.x == dx){
		for(var d = 1; d < Math.abs(piece.y - dy); d++){
			if(board.boardGrid[piece.x][piece.y+Math.sign(dy - piece.y)*d] !== null){
				return false;
			}					
		}				
	}else{
		return false;
	}
	return true;
}				

function isLegalMoveKing(piece, dx, dy, board){
	if(board.boardGrid[1][1] !== null && board.boardGrid[5][1] !== null && !hasMoved(board.boardGrid[1][1], board) && !hasMoved(board.boardGrid[5][1], board) && board.boardGrid[2][1] === null && board.boardGrid[3][1] === null && board.boardGrid[4][1] === null && piece.x == 5 && piece.y == 1 && dx == 3 && dy == 1 && piece.name == "wking"){
		return true;
	}				

	if(board.boardGrid[8][1] !== null && board.boardGrid[5][1] !== null && !hasMoved(board.boardGrid[8][1], board) && !hasMoved(board.boardGrid[5][1], board) && board.boardGrid[6][1] === null && board.boardGrid[7][1] === null && piece.x == 5 && piece.y == 1 && dx == 7 && dy == 1 && piece.name == "wking"){
		return true;
	}	

	if(board.boardGrid[1][8] !== null && board.boardGrid[5][8] !== null && !hasMoved(board.boardGrid[1][8], board) && !hasMoved(board.boardGrid[5][8], board) && board.boardGrid[2][8] === null && board.boardGrid[3][8] === null && board.boardGrid[4][8] === null && piece.x == 5 && piece.y == 8 && dx == 3 && dy == 8 && piece.name == "bking"){
		return true;
	}				

	if(board.boardGrid[8][8] !== null && board.boardGrid[5][8] !== null && !hasMoved(board.boardGrid[8][8], board) && !hasMoved(board.boardGrid[5][8], board) && board.boardGrid[6][8] === null && board.boardGrid[7][8] === null && piece.x == 5 && piece.y == 8 && dx == 7 && dy == 8 && piece.name == "bking"){
		return true;
	}					
	
	var destination = board.boardGrid[dx][dy];
	if(destination !== null && destination.color == piece.color){
		return false;
	}
	if(Math.abs(piece.x - dx) > 1 || Math.abs(piece.y - dy) > 1){
		return false;
	}
	
	return true;
}




//generates all the possible moves. does not take check into account
function generatePossibleMoves(piece, board){
	moves = [];
		
	if(piece.type == "knight"){
		if(isLegalMove(piece.x + 2, piece.y + 1, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x + 2, piece.y + 1, piece));
		}				
		if(isLegalMove(piece.x + 2, piece.y - 1, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x + 2, piece.y - 1, piece));
		}	
		if(isLegalMove(piece.x + 1, piece.y + 2, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x + 1, piece.y + 2, piece));
		}	
		if(isLegalMove(piece.x + 1, piece.y - 2, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x + 1, piece.y - 2, piece));
		}	
		if(isLegalMove(piece.x - 2, piece.y + 1, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x - 2, piece.y + 1, piece));
		}	
		if(isLegalMove(piece.x - 2, piece.y - 1, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x - 2, piece.y - 1, piece));
		}	
		if(isLegalMove(piece.x - 1, piece.y + 2, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x - 1, piece.y + 2, piece));
		}	
		if(isLegalMove(piece.x - 1, piece.y - 2, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x - 1, piece.y - 2, piece));
		}						
		return moves;
	}
		
	var y = piece.y + 1;
	while(y <= 8){
		if(isLegalMove(piece.x, y, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x, y, piece));
		}else{
			break;
		}
		y++;
	}
	
	y = piece.y - 1;
	while(y >= 1){
		if(isLegalMove(piece.x, y, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x, y, piece));
		}else{
			break;
		}	
		y--;
	}				
	
	var x = piece.x + 1;
	while(x <= 8){
		if(isLegalMove(x, piece.y, board, piece)){
			moves.push(new Move(piece.x, piece.y, x, piece.y, piece));
		}else{
			break;
		}				
		x++;
	}
	
	x = piece.x - 1;
	while(x >= 1){
		if(isLegalMove(x, piece.y, board, piece)){
			moves.push(new Move(piece.x, piece.y, x, piece.y, piece));
		}else{
			break;
		}					
		x--;
	}					
	
	var d = 1;
	while(piece.x + d <= 8 && piece.y + d <= 8){
		if(isLegalMove(piece.x + d, piece.y + d, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x + d, piece.y + d, piece));
		}else{
			break;
		}
		d++;
	}

	d = 1;
	while(piece.x - d >= 1 && piece.y - d>= 1){
		if(isLegalMove(piece.x - d, piece.y - d, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x - d, piece.y - d, piece));
		}else{
			break;
		}
		d++;
	}

	d = 1;
	while(piece.x + d <= 8 && piece.y - d>= 1){
		if(isLegalMove(piece.x + d, piece.y - d, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x + d, piece.y - d, piece));
		}else{
			break;
		}
		d++;
	}				

	d = 1;
	while(piece.x - d >= 1 && piece.y + d <= 8){
		if(isLegalMove(piece.x - d, piece.y + d, board, piece)){
			moves.push(new Move(piece.x, piece.y, piece.x - d, piece.y + d, piece));
		}else{
			break;
		}
		d++;
	}
	return moves;			
}			

//takes out the moves that cause check
function filteredMoves(moves, color, board){
	var uncheckedMoves = [];
	for(var i = 0; i < moves.length; i++){
		if(!kingChecked(moves[i], color, board)){
			uncheckedMoves.push(moves[i]);
		}
	}
	return uncheckedMoves;
}

//checks if the move causes check
function kingChecked(move, color, board){
	execute(board, move);

	var kingX;
	var kingY;
	//find the king
	for(var x = 0; x < board.pieces.length; x++){
		var piece = board.pieces[x];
		if(piece.name == color+"king"){
			kingX = piece.x;
			kingY = piece.y;
			break;
		}
	}
	//set opponent color
	var opponent = "w";
	if(color == "w"){
		opponent = "b";
	}
	var isChecked = false;
	moves = allLegalMoves(opponent, board);
	
	//check if any opponent pieces can capture the king
	for(var i = 0; i < moves.length; i++){
		var isChecked = moves[i].dx == kingX && moves[i].dy == kingY;				
		if(isChecked){
			isChecked = true;
			break;
		}
	}			
	undo(board, move);
	return isChecked;	
}


function allLegalMoves(color, board){
	var moves = [];
	for(var x = 0; x < board.pieces.length; x++){
		var piece = board.pieces[x];
		
		if(piece.color == color){
			var allMoves = generatePossibleMoves(piece, board);
			for(var y = 0; y < allMoves.length; y++){
				moves.push(allMoves[y]);
			}			
		}
	}
	return moves;
}			

function pickMoveInner(max, dept, boardCopy){
	var moves = "";			
	var maxMove = "";
	var maxScore = 0;
	var color = "w";
	var opponent = "b";
	if(max){
		moves = allLegalMoves("w", boardCopy);
		maxScore = -1000000000;
	}else{
		color = "b";
		opponent = "w";
		moves = allLegalMoves("b", boardCopy);
		maxScore = 1000000000;
	}				
	
	//check all moves and how they score
	for(var a = 0; a < moves.length; a++){
		var move = moves[a];					
		
		//make the move in the virtual board
		execute(boardCopy, move);										

		var score = 0;
		//if the desired dept is reach score the board. Otherwise search deeper
		if(dept == 1){
			score = scoreBoard(boardCopy);
		}else{
			score = pickMoveInner(!max, dept-1, boardCopy);
		}
					
		//update the best score if a better is found
		if((!max && score < maxScore) || (max && score > maxScore)){
			maxMove = move;
			maxScore = score;
		}

		//undo the move
		undo(boardCopy, move);
		
	}
	moves = undefined;
	return maxScore;		
}			

//score the current virtual board
function scoreBoard(boardCopy){
	var score = 0;
	var pieces = boardCopy.pieces;
	for(var x = 0; x < pieces.length; x++){
		
		var scorePiece = pieces[x];
		var type = scorePiece.type;

		//pawn score based on it's placement on board
		if(type == "pawn"){
			if(scorePiece.color == "w"){						
				if(scorePiece.y == 8){
					score = score + 80;
				}else{
					score = score + scorePiece.y + 10;
				}
			}else{
			
				if(scorePiece.y == 1){
					score = score - 80;
				}else{
					score = score + scorePiece.y - 9 - 10;
				}
			}
		}
		var pointing = 0;

		//material score
		if(type == "knight" || type == "bishop"){
			pointing = 30;
		}
		else if(type == "rook"){
			pointing = 50;
		}					
		else if(type == "queen"){
			pointing = 80;
		}							
		else if(type == "king"){
			pointing = 1000;
			if(scorePiece.color == "b"){
				pointing = 10000;
			}
			
			var adjScore = 3;
			
			//King security evaluation
			for(var dx = -1; dx <= 1; dx++){
				for(var dy = -1; dy <= 1; dy++){
					
					if(scorePiece.x + dx > 8 || scorePiece.x + dx < 1 || scorePiece.y + dy > 8 || scorePiece.y + dy < 1){
						if(scorePiece.color == "w"){
							score = score + adjScore - 1;
						}else{
							score = score - adjScore + 1;
						}
						
						
						continue;
					}
					
					var adjScorePiece = boardCopy.boardGrid[scorePiece.x + dx][scorePiece.y + dy];
					if(scorePiece.color == "w"){
						if(adjScorePiece !== null && adjScorePiece.color == "w"){
							score = score + adjScore;
						}
					}else{
						if(adjScorePiece !== null && adjScorePiece.color == "b"){
							score = score - adjScore;
						}								
					}
				}
			}
			
		}						
		if(scorePiece.color == "w"){
			score = score + pointing;
		}else{
			score = score - pointing;
		}			
	}				
	return score + Math.round(Math.random() * 8 - 4);

}