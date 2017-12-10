#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 23:46:57 2016

@author: aman
"""
# File: chessBoard.py
# Date: November 21, 2016

# This code is an adaptation of the following:
# Chessmastah, started Jan 2012 by Svein Arne Roed
# for the EECS4422 Computer Vision Project 

# Example of using code:
# game = Game()
# game.domove("a7a5")
# game.getpiece("a8")

# b = BoardInterface()
# x = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 0]]
# b.update(x)

class BoardInterface(object):
   
   def __init__(self):
      self.binaryBoard = [[0]*8 for i in range(8)]
      
      for row in [0,1,6,7]:
         for col in range(0,8):
            self.binaryBoard[row][col] = 1
      
      self.game = Game()
      
   def update(self, updatedBoard):
    startrow = 0
    startcol = 0
    endrow = 0
    endcol = 0
    changed = 0;
     
    for row in range(0,8):
      for col in range(0,8):
        if self.binaryBoard[row][col] != updatedBoard[row][col]:
          changed = 1
          if self.binaryBoard[row][col] == 1:
            startrow = row
            startcol = col
          else:
            endrow = row
            endcol = col
    
    if changed:  
      self.binaryBoard[startrow][startcol] = 0
      self.binaryBoard[endrow][endcol] = 1
      
      start = (startrow, startcol)
      end = (endrow, endcol)
      
      self.game.domove(start, end)
        
class Player(object):

    allsquares = [(x, y) for x in range(8) for y in range(8)]

    def __init__(self, colour):
        self.colour   = colour

    def __str__(self):
        return self.colourself.colour

    def getpieces(self, board):
        return [pos for pos in board if board[pos].colour is self.colour]

class Piece(object):

    def __init__(self, piecename, position, player):
        self.colour    = player.colour
        self.piecename = piecename
        self.position  = position
        self.nrofmoves = 0

    def __str__(self):
        if self.colour is 'white':
            if self.piecename is 'p':
                return 'WP'
            else:
                return self.piecename.upper()
        else:
            return self.piecename


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