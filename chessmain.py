"""
This is our main driver file. it will be responsible for handling user input and displaying the current GameState
object.
"""
import pygame as p
from chess import chessengine
width = height = 512
dimension = 8 #dimensions of a chess board are 8x8
sq_size = height//dimension
max_fps = 15 #for animation
Images = {}

"""
INITIALIZING a global dictonary of images. This will be called exactly once in the main
"""
def loadimages():
    pieces = ['wp', "wR", "wN", "wB", "wQ", "wK", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for piece in pieces:
      Images[piece] = p.transform.scale(p.image.load("images/"+ piece + ".png"),(sq_size,sq_size))
    #Note: we can access an image by saying 'Images['wp']' and sq size by sq size to fit the image in a square
"""
the main driver for our code. this will handle user input and updating the graphics
"""
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variables for when a move is made
    
    loadimages() #we gonna call this function once to avoid lag
    running = True
    sq_selected = () #tuple(x,y),keep track of the last click of the user.
    player_clicks = []  #keeps track of the players clicks [(x0,y0),(x1,y1)..]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()# x,y location of mouse
                col = location[0]//sq_size
                row = location[1]//sq_size
                if sq_selected == (row, col): #the user selected the same square twice
                    sq_selected = () # then deselect the move
                    player_clicks = [] #clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected) #append for both 1st and 2nd clicks
                if len(player_clicks) == 2: #after 2nd click
                    move = chessengine.Move(player_clicks[0],player_clicks[1], gs.board)
                    print(move.getchessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sq_selected = () #reset user clicks
                        player_clicks = [] #or we will have more than two moves
                    else:
                        player_clicks = [sq_selected]


            #key handelers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawgamestate(screen, gs)
        clock.tick(max_fps)
        p.display.flip()
"""
this function draws squres on the board since getting called in while loop and uses 'gs' to have that board 
"""
def drawgamestate(screen, gs):
    drawboard(screen) #draw squares on the board
    drawpieces(screen,gs.board) #draw pieces on top of those squares
"""
Draw Squares on the board
"""
def drawboard(screen):
    colors = [p.Color("white"), p.Color('gray')]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


"""
Draw the pieces on the board using the gamestate.board.....NOTE : THE ORDER IS IMPORTANT SQUARES SHOULD BE MADE FIRST
THEN THE PIECES 
"""
def drawpieces(screen,board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != '--': #not empty square
                screen.blit(Images[piece], p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))


if __name__ == "__main__":
    main()

