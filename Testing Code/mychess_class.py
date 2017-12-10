class Game(object):

    def __init__(self):

        self.board = dict()
        playera = Player('white')
        playerb = Player('black')
        
        for player in [playera, playerb]:
            if player.colour is 'white':
                brow, frow = 0, 1
                player.enpassantrow = 4
            else:
                brow, frow = 7, 6
                player.enpassantrow = 3

            player.longrook  = (brow, 0)
            player.longrook_target = \
            (player.longrook[0], player.longrook[1]+3)
            
            player.shortrook = (brow, 7)
            player.shortrook_target = \
            (player.shortrook[0], player.shortrook[1]-2)
            

            [self.board.setdefault((frow,x), Piece('p', (frow,x), player)) \
            for x in range(8)]
            [self.board.setdefault((brow,x), Piece('r', (brow,x), player)) \
            for x in [0,7]]
            [self.board.setdefault((brow,x), Piece('kn',(brow,x), player)) \
            for x in [1,6]]
            [self.board.setdefault((brow,x), Piece('b', (brow,x), player)) \
            for x in [2,5]]
            self.board.setdefault((brow,3),  Piece('q', (brow,3), player))
            self.board.setdefault((brow,4),  Piece('k', (brow,4), player))

    def printboard(self):

        topbottom=['*','a','b','c','d','e','f','g','h','*']
        sides=['1','2','3','4','5','6','7','8']
        tbspacer=' '*6
        rowspacer=' '*5
        cellspacer=' '*4
        empty=' '*3

        print
        for field in topbottom:
            print "%4s" % field,
        print

        print tbspacer+("_"*4+' ')*8

        for row in range(8):
            print(rowspacer+(('|'+cellspacer)*9))
            print "%4s" % sides[row],('|'),
            for col in range(8):
                if (row, col) not in self.board:
                    print empty+'|',
                else:
                    print "%2s" % self.board[(row, col)],('|'),
            print "%2s" % sides[row],
            print
            print rowspacer+'|'+(("_"*4+'|')*8)
        print

        for field in topbottom:
            print "%4s" % field,

        print "\n"
    
    def domove(self, start, target):

        self.savedtargetpiece = None
        if target in self.board:
            self.savedtargetpiece = self.board[target]

        if self.board[start]:
            self.board[target] = self.board[start]
            self.board[target].position = target
            del self.board[start]
        
        self.printboard()
		
    def getpiece(self, grid):
  	  
        startcol  = int(ord(grid[0].lower())-97)
        startrow  = int(grid[1])-1
        start     = (startrow, startcol)
      
        if start in self.board:
          return self.board[start].piecename