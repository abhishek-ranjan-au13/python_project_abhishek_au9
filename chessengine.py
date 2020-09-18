"""
This class is resposible for storing all the info about the current state of a chess chess.. It will also be responsible
for determining the valid moves at the current state..It will also keep a move log...
"""
class GameState():
    def __init__(self):
        #board is an 8x8 2-D list, each element of the line has 2 characters..
        # The 1st character represents the colour of the peice i.e black(b)and white(w)
        # the second character represents the type of the piece king(K),Queen(Q),Ruk(R),Bishop(B),knight(K),Pawn(p)
        # "--" blank space with no piece,choosen a string to avoid "int"to"str" conversion..
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]
        self.moveFunction = {'p': self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves,
                             'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whitemove = True  #to determine whose turne it is
        self.movelog = [] # A list to keep track what moves have taken place



    """
    takes a move as a parameter and execute it, will not work for castling and en-passant and also actually 
    pawn promotion as well
    """
    def makeMove(self,move):
        self.board[move.startRow][move.startcol] = "--" #when start is aempty string
        self.board[move.endRow] [move.endcol] = move.pieceMoved
        self.movelog.append(move) #log the move so we can undo it later
        self.whitemove = not self.whitemove #swap players
    """
    undo the last move
    """

    def undoMove(self):
        if len(self.movelog) != 0 : #make sure that there is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startcol] = move.pieceMoved
            self.board[move.endRow][move.endcol] = move.pieceCaptured
            self. whitemove = not self.whitemove #swap players
    """
    
    all moves considering checks 
    """
    def getValidMoves(self):
        return self.getAllpossibleMoves() #for now just not worry about checks

    """
    all moves without considering checks
    """
    def getAllpossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #nimber of columns in a given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whitemove) or (turn == 'b' and not self.whitemove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r,c,moves)
                    # if piece == "p":
                    #     self.getPawnMoves(r,c,moves)
                    # elif piece == "R":
                    #     self.getRookMoves(r,c,moves)
                    # elif piece == "N":
                    #     self.getKnightMoves(r,c,moves)
                    # elif piece == "B":
                    #     self.getBishopMoves(r,c,moves)
                    # elif piece == "Q":
                    #     self.getQueenMoves(r,c,moves)
                    # elif piece == "k":
                    #     self.getKingMoves(r,c,moves)





        return moves
    """
    get all pawn moves for the pawn located at row, col and add these moves to the list
    """

    def getPawnMoves(self, r, c, moves):
        if self.whitemove: #white pawn moves
            if self.board[r-1][c] == "--" : #1pawn moves
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--" : #2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))

            if c-1 >= 0 : #captures to the left
                if self.board[r-1][c-1][0]=='b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7 : #(length of board) captures to the right
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: #black pawn moves
            if self.board[ r + 1][c] == "--": # 1 square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #2nd square
                    moves.append(Move((r,c), (r+2, c), self.board))
            #captures
            if c-1 >= 0: #capture to left
                if self.board[r+1][c-1][0] == "w": #enemy piece to capture
                    moves .append(Move((r,c),(r+1, c-1), self.board))
            if c+1 <= 7: #capture to the right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1, c+1), self.board))


    """
    get all rook moves for the rook located at row, col and add these moves to the list
    """

    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1)) #up, left, down, right
        enemyColor = "b" if self.whitemove else "w"
        for d in directions:
            for i in range (1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0  <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break

    """get all knight moves for the rook located at row, col and add these moves to the list
    """

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whitemove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = r + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    moves.append(Move((r,c), (endRow, endCol), self.board))



    """
    get all bishop moves for the rook located at row, col and add these moves to the list
    """

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #4 diagonals
        enemyColor = "b" if self.whitemove else "w"
        for d in directions:
            for i in range(1, 8): #bishop can move max of 7 squares
                endrow = r + d[0] * i
                endcol = r + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endPiece = self.board[endrow][endcol]
                    if endPiece == '--': # empty space valid
                        moves.append(Move((r,c), (endrow, endcol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece Valid
                        moves.append(Move((r,c), (endrow, endcol), self.board))
                        break
                    else : # friendly piece invalid
                        break
                else: #off board
                    break

    """
    get all queen moves for the rook located at row, col and add these moves to the list
    """

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    """
    get all king moves for the rook located at row, col and add these moves to the list
    """

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whitemove else "b"
        for i in range (8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8 :
                endpiece = self.board[endRow][endCol]
                if endpiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    moves.append(Move((r,c), (endRow, endCol), self.board))





class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()} #reversing the dictonary
    filesTocols = {"a": 0, "b": 1, "c":2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k,v in filesTocols.items()}

    def __init__(self, startsq, endsq, board):
        self.startRow = startsq[0]
        self.startcol = startsq[1]
        self.endRow = endsq[0]
        self.endcol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startcol]
        self.pieceCaptured = board[self.endRow][self.endcol]
        self.moveID = self.startRow * 1000 + self.startcol * 100 + self.endRow * 10 + self.endcol

    """
    overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getchessNotation(self):
        return self.getRankFile(self.startRow,self.startcol) + self.getRankFile(self.endRow, self.endcol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+ self.rowsToRanks[r]
