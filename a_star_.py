#1WN24CS097

import heapq
class PuzzleState:
    def __init__(self, board, g=0, parent=None):
        self.board = board
        self.g = g
        self.parent = parent
        self.h = self.calculate_manhattan()
        self.f = self.g + self.h
    def calculate_manhattan(self):
        distance = 0
        for i in range(9):
            value = self.board[i]
            if value != 0:
                current_row, current_col = divmod(i, 3)
                goal_index = value - 1
                goal_row, goal_col = divmod(goal_index, 3)
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance
    def get_neighbors(self):
        neighbors = []
        zero_idx = self.board.index(0)
        row, col = divmod(zero_idx, 3)
        moves = []
        if row > 0: moves.append(-3)
        if row < 2: moves.append(3)
        if col > 0: moves.append(-1)
        if col < 2: moves.append(1)
        for move in moves:
            new_zero_idx = zero_idx + move
            new_board = list(self.board)
            new_board[zero_idx], new_board[new_zero_idx] = new_board[new_zero_idx], new_board[zero_idx]
            neighbors.append(PuzzleState(tuple(new_board), self.g + 1, self))
        return neighbors
    def __lt__(self, other):
        return self.f < other.f
    def reconstruct_path(self):
        path = []
        current = self
        while current:
            path.append(current.board)
            current = current.parent
        return path[::-1]
def print_board(board):
    for i in range(0, 9, 3):
        print(list(board[i:i+3]))
    print()
def solve_a_star(start_board, goal_board=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    start_state = PuzzleState(start_board)
    open_set = []
    heapq.heappush(open_set, start_state)
    closed_set = set()
    while open_set:
        current_state = heapq.heappop(open_set)
        if current_state.board == goal_board:
            return current_state.reconstruct_path()
        closed_set.add(current_state.board)
        for neighbor in current_state.get_neighbors():
            if neighbor.board in closed_set:
                continue
            heapq.heappush(open_set, neighbor)
    return None
start_layout = (1, 2, 3, 0, 4, 6, 7, 5, 8)
goal_layout = (1, 2, 3, 4, 5, 6, 7, 8, 0)
print("Searching path...")
solution = solve_a_star(start_layout, goal_layout)
if solution:
    print(f"Solved in {len(solution) - 1} steps!\n")
    for step, board in enumerate(solution):
        print(f"Step {step}:")
        print_board(board)
else:
    print("No solution found.")
