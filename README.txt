
Total time: 0.464526 s
File: .\connect3.py
Performance testing on AB vs Minimax, speaks for itself
Function: abTEST at line 405

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
   405                                           @profile
   406                                           def abTEST():
   407         1         16.0     16.0      0.0      randomPlayer1 = RandomPlayer("X")
   408         1          6.0      6.0      0.0      MiniMaxPlayer = miniMaxPlayer("O")
   409         1         10.0     10.0      0.0      alphaBetaPlayer = AlphaBetaPlayer("O")
   410
   411         1         15.0     15.0      0.0      board = Connect3Board(sys.argv[2] if len(sys.argv) > 2 else None)
   412         1        914.0    914.0      0.1      print "MINIMAX"
   413         1         12.0     12.0      0.0      game = Game(randomPlayer1, MiniMaxPlayer, board)
   414         1          1.0      1.0      0.0      i = 0
   415        11         13.0      1.2      0.0      while i < 10:
   416        10    1340586.0 134058.6     80.0          game.playgame()
   417        10         35.0      3.5      0.0          i = i + 1
   418         1       1279.0   1279.0      0.1      print "ALPHA BETA"
   419         1         11.0     11.0      0.0      game2= Game(randomPlayer1, alphaBetaPlayer,board)
   420         1          1.0      1.0      0.0      i = 0
   421        11         13.0      1.2      0.0      while i < 10:
   422        10     333701.0  33370.1     19.9          game2.playgame()
   423        10         35.0      3.5      0.0          i = i +1