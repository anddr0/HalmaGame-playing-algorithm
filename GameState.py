import pygame
import numpy as np


class GameState:
    def __init__(self, player, board=None, board_str=None, max_jumps_moves_depth=10):
        if board is None and board_str is None:
            raise Exception("Game state has no any board")
        self.board = np.clip(board, 0, None) if board is not None else self.parse_board_from_input(board_str)
        self.player = player
        self.possible_game_states = []
        self.max_depth_jump_checking = max_jumps_moves_depth        # jumping moves max depth
        self.MIN_GOAL_VALUE = 60
        self.MAX_GOAL_VALUE = 510
        self.MIN_CENTER_VALUE = 40
        self.MAX_CENTER_VALUE = 210
        self.MIN_WALL_VALUE = 80
        self.MAX_WALL_VALUE = 270
        self.MIN_PROXIMITY_VALUE = 2
        self.MAX_PROXIMITY_VALUE = 10

    def parse_board_from_input(self, input_string):
        lines = input_string.strip().split('\n')
        board = []
        for line in lines:
            row = list(map(int, line.split()))
            board.append(row)
        return np.array(board)

    def is_terminal(self, player):
        if self.goal_distance(player) >= 100:
            goal_areas = {
                1: [(i, j) for i in range(14, 16) for j in range(11, 16)] +
                   [(i, j) for i in range(13, 15) for j in range(12, 16)] +
                   [(i, j) for i in range(12, 14) for j in range(13, 16)] +
                   [(i, j) for i in range(11, 13) for j in range(14, 16)],
                2: [(i, j) for i in range(0, 2) for j in range(0, 5)] +
                   [(i, j) for i in range(1, 3) for j in range(0, 4)] +
                   [(i, j) for i in range(2, 4) for j in range(0, 3)] +
                   [(i, j) for i in range(3, 5) for j in range(0, 2)]
            }
            for pos in goal_areas[player]:
                if self.board[pos[0], pos[1]] != player:
                    return False

            return True
        else:
            return False


    def get_possible_game_states(self, player, depth=None):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == player:
                    self.check_adjacent_moves(player, x, y)
                    self.check_jump_moves(player, x, y, depth=0)

    def check_adjacent_moves(self, player, x, y):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                new_y = y + dy
                new_x = x + dx
                if 0 <= new_y < 16 and 0 <= new_x < 16 and self.board[new_y][new_x] == 0:
                    new_board = np.copy(self.board)
                    new_board[y][x] *= -1
                    new_board[new_y][new_x] = player
                    self.possible_game_states.append(GameState(board=new_board, player=self.player))

    def check_jump_moves(self, player, x, y, depth, new_board=None):
        if depth >= self.max_depth_jump_checking:  # Terminate recursion if maximum depth is reached
            return
        board = self.board if new_board is None else new_board
        for dy in [-2, 0, 2]:
            for dx in [-2, 0, 2]:
                if dy == 0 and dx == 0:
                    continue
                mid_y = y + (dy - 1) if dy > 0 else y + (dy + 1) if dy < 0 else y
                mid_x = x + (dx - 1) if dx > 0 else x + (dx + 1) if dx < 0 else x
                new_y = y + dy
                new_x = x + dx
                if (0 <= new_y < 16 and 0 <= new_x < 16 and
                        board[mid_y][mid_x] in range(1, 3) and
                        board[new_y][new_x] == 0):
                    new_board = np.copy(board)
                    new_board[y][x] *= -1
                    new_board[new_y][new_x] = player
                    self.possible_game_states.append(GameState(board=new_board, player=self.player))
                    self.check_jump_moves(player, new_x, new_y, depth+1, new_board)

    def get_heuristic_percentage(self, value, min_value, max_value, revert=False):
        value = max(value, min_value)
        value = min(value, max_value)

        percent = ((max_value - value) / (max_value - min_value)) * 100 if not revert else \
                  ((min_value - value) / (min_value - max_value)) * 100
        return percent

    def goal_distance(self, player):
        goal_position = (15, 15) if player == 1 else (0, 0)
        player_positions = np.argwhere(self.board == player)
        distances = np.sum(np.abs(player_positions - goal_position), axis=1)
        total_distance = np.sum(distances)
        return self.get_heuristic_percentage(total_distance,
                                                 self.MIN_GOAL_VALUE,
                                                 self.MAX_GOAL_VALUE)

    def center_distance(self, player):
        center_position = np.array([8, 8])  # Center position of the board
        player_positions = np.argwhere(self.board == player)
        distance = np.sum(np.abs(player_positions - center_position), axis=1)
        total_center_dist = np.sum(distance)
        return self.get_heuristic_percentage(total_center_dist, self.MIN_CENTER_VALUE, self.MAX_CENTER_VALUE)

    def wall_heuristic(self, player):
        num_rows, num_cols = self.board.shape
        row_counts = np.zeros(num_rows)
        col_counts = np.zeros(num_cols)

        for row in range(num_rows):
            for col in range(num_cols):
                if self.board[row, col] == player:
                    row_counts[row] += 1
                    col_counts[col] += 1

        row_score = np.sum(row_counts ** 2)
        col_score = np.sum(col_counts ** 2)
        total_score = row_score + col_score

        return self.get_heuristic_percentage(total_score, self.MIN_WALL_VALUE, self.MAX_WALL_VALUE, revert=True)

    def proximity_heuristic(self, player):  # Function that calculates how close player's check are
        player_positions = np.argwhere(self.board == player)
        num_positions = len(player_positions)
        if num_positions <= 1:
            return 0 if num_positions <= 1 else 0
        total_distance = 0
        for i in range(num_positions):
            for j in range(i + 1, num_positions):
                distance = np.linalg.norm(player_positions[i] - player_positions[j])
                total_distance += distance

        average_distance = (total_distance / (num_positions * (num_positions - 1) / 2)) if num_positions <= 1 else 0
        return self.get_heuristic_percentage(average_distance,
                                                 self.MIN_PROXIMITY_VALUE,
                                                 self.MAX_PROXIMITY_VALUE)

    def evaluate(self, player, weights):
        scores = {
            "goal_distance": self.goal_distance(player) * weights["goal_distance"],
            "center_distance": self.center_distance(player) * weights["center_distance"],
            "wall_building": self.wall_heuristic(player) * weights["wall_building"],
            "proximity_heuristic": self.proximity_heuristic(player) * weights["proximity_heuristic"]
        }
        # total_score = 0
        # for key, value in scores.items():
        #     total_score += value * weights.get(key, 1)  # 1 as default value for weight

        return sum(scores.values()), scores

    def draw_board(self):
        pygame.init()
        screen_width = 512  # Adding extra width for borders
        screen_height = 512  # Adding extra height for borders
        cell_size = 32
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Board')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))

            # Draw grid
            for x in range(0, screen_width, cell_size):
                pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, screen_height))
            for y in range(0, screen_height, cell_size):
                pygame.draw.line(screen, (0, 0, 0), (0, y), (screen_width, y))

            # Draw cells
            for y, row in enumerate(self.board):
                for x, cell in enumerate(row):
                    color = (255, 0, 0) if cell == 1 else (0, 0, 255) if cell == 2 else (255, 255, 255)
                    if cell < 0:
                        color = (0, 255, 0)  # Green color for cells that came from previous move
                    pygame.draw.rect(screen, color,
                                     (x * cell_size + 1, y * cell_size + 1, cell_size - 2, cell_size - 2))

            pygame.display.flip()
        # else:
        #     pygame.quit()

    def __str__(self):
        return str(self.board)