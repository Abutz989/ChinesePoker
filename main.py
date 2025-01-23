import Games
import ComPlayer as Players
import argparse

if __name__ == "__main__":
    ##
    # # player = Players.StupidPlayer(
    # # player = Players.GreedyMovePlayer()
    # # player = Players.CompetativePlayer()
    # # player = Players.MinMaxPlayer()
    # # game = Games.KeyBoardGame(player)
    # ##
    # # player1 = Players.StupidPlayer()
    # player1 = Players.CompetativePlayer()
    # player2 = Players.GreedyMovePlayer()
    # # player1 = Players.MinMaxPlayer()
    # # player2 = Players.MinMaxPlayerV2()
    # game = Games.AutoGame(player1,player2)
    
    
    
    # game.run_game()
    # python main.py -game KeyBoardGame  
    # python main.py -game AutoGame -player1 StupidPlayer -player2 GreedyMovePlayer

    games = {'KeyBoardGame': Games.KeyBoardGame, 'AutoGame': Games.AutoGame}

    move_players = {'StupidPlayer': Players.StupidPlayer,
                    'GreedyMovePlayer': Players.GreedyMovePlayer,
                    'CompetativePlayer': Players.CompetativePlayer,
                    'MinMaxPlayer': Players.MinMaxPlayer,
                    'MinMaxPlayerV2': Players.MinMaxPlayerV2,
                    }

    parser = argparse.ArgumentParser()

    parser.add_argument('-game', default='AutoGame', type=str,
                        help='Option to Player keyboard game or virtual game with agents.',
                        choices=games)

    parser.add_argument('-player1', default='MinMaxPlayer', type=str,
                        help='The type of the first player(Move player).',
                        choices=move_players.keys())
    parser.add_argument('-player2', default='CompetativePlayer', type=str,
                        help='The type of the second player(Index Player).',
                        choices=move_players.keys())

    args = parser.parse_args()

    # Players inherit from AbstractPlayer
    player_1_type = args.player1
    player_2_type = args.player2
    

    # print game info to terminal
    print(f'Starting {args.game}!')

    # create game with the given args
    if args.game == 'AutoGame':
        # Create players
        player_1 = move_players[player_1_type]()
        player_2 = move_players[player_2_type]()

        print(args.player1, 'VS', args.player2)
       
        game = games[args.game](player_1, player_2)
    else:
        player_1 = move_players[player_1_type]()
        game = games[args.game](player_1)
        print('Push the buttons to move')

    # start playing!
    game.run_game()