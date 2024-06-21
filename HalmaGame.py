import time

from GameState import GameState
from vars import board, weights
import pygame
import sys


class HalmaGame:
    def __init__(self, player, init_board=None, player_1_weights=None, player_2_weights=None):
        self.player = player
        self.game_state = GameState(board_str=init_board if init_board else board, player=1)
        self.weights = {
            1: player_1_weights if player_1_weights else weights(),
            2: player_2_weights if player_2_weights else weights()
        }
        self.player_1_weights = player_1_weights if player_1_weights else weights()
        self.player_2_weights = player_2_weights if player_2_weights else weights()
        self.visited_nodes = 0

    def change_player(self):
        self.player = 1 if self.player == 2 else 2

    def make_move(self, depth=2):
        best_value, best_state = self.minimax(self.game_state, depth, -sys.maxsize, sys.maxsize, True)
        self.game_state = best_state  # Update the game state to the best found state
        print("Best val: ", best_value)
        print("Visited nodes: ", self.visited_nodes)
        return best_state

    def run_game(self, round_show, depth=2):
        time_start = time.time()
        game_round = 0
        while not self.game_state.is_terminal(self.player):
            game_round += 1
            self.make_move(depth=depth)
            if game_round % round_show == 0:
                self.game_state.draw_board()
            print(f"""
----------------------------------------------------------------------------------------------------
Round [{game_round}], player: [{self.player}] {self.game_state.evaluate(self.player, self.weights[self.player])}
----------------------------------------------------------------------------------------------------
            """)
            self.change_player()
        else:
            time_end = time.time()
            print(f"Player [{self.player}] won!\n", self.game_state)
            pygame.quit()

    def minimax(self, state, depth, alpha, beta, maximizing_player):
        # print(f"alpha: {alpha} --- beta: {beta}")
        if depth == 0 or state.is_terminal(self.player):
            return state.evaluate(player=self.player, weights=self.weights[self.player])[0], state

        if maximizing_player:
            max_eval = -sys.maxsize
            best_state = None
            if not state.possible_game_states:
                state.get_possible_game_states(self.player)
            for child in state.possible_game_states:
                self.change_player()
                self.visited_nodes += 1
                eval, _ = self.minimax(child, depth - 1, alpha, beta, False)
                self.change_player()
                if eval > max_eval:
                    max_eval = eval
                    best_state = child
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_state
        else:
            min_eval = sys.maxsize
            best_state = None
            if not state.possible_game_states:
                state.get_possible_game_states(self.player)
            for child in state.possible_game_states:
                self.change_player()
                self.visited_nodes += 1
                eval, _ = self.minimax(child, depth - 1, alpha, beta, True)
                self.change_player()
                if eval < min_eval:
                    min_eval = eval
                    best_state = child
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_state


if __name__ == "__main__":
    game = HalmaGame(player=1,
                     player_1_weights=weights(goal_distance=1),
                     player_2_weights=weights(goal_distance=1, proximity_heuristic=0.6))
    game.run_game(100, 2)

