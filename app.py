
from tkinter import *
import random


# Recursive minimax function to determine the optimal move score for a Tic-Tac-Toe game:
"""
    This function checks for a winner or a full board first. If neither, it recurses through all
    possible moves, updating the board and evaluating potential outcomes, using the maximization
    or minimization strategy based on the player's turn.
"""
def minimax(board, depth, is_maximizing):
    score = check_winner_minimax(board)

    if score == 10:
        return score
    if score == -10:
        return score
    if not empty_spaces_minimax(board):
        return 0

    if is_maximizing:
        best_score = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = ai_player
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = human_player
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

# Function to find the best move for the AI
def best_move():
    best_score = -1000
    move = None
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == "":
                buttons[i][j]['text'] = ai_player
                score = minimax(board_state(), 0, False)
                buttons[i][j]['text'] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    buttons[move[0]][move[1]]['text'] = ai_player
    if check_winner():
        highlight_winner()
    else:
        switch_player()

# Function to get the current state of the board
def board_state():
    board = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(buttons[i][j]['text'])
        board.append(row)
    return board

# Function to evaluate if there's a winner
def check_winner_minimax(b):
    for row in range(3):
        if b[row][0] == b[row][1] == b[row][2] != "":
            return 10 if b[row][0] == ai_player else -10
    for col in range(3):
        if b[0][col] == b[1][col] == b[2][col] != "":
            return 10 if b[0][col] == ai_player else -10
    if b[0][0] == b[1][1] == b[2][2] != "":
        return 10 if b[0][0] == ai_player else -10
    if b[0][2] == b[1][1] == b[2][0] != "":
        return 10 if b[0][2] == ai_player else -10
    return 0

# Function to check if there are empty spaces left on the board
def empty_spaces_minimax(b):
    for i in range(3):
        for j in range(3):
            if b[i][j] == "":
                return True
    return False

# Function to handle the next turn
def next_turn(row, column):
    global player
    if buttons[row][column]['text'] == "" and not check_winner():
        buttons[row][column]['text'] = player
        if check_winner():
            label.config(text=(player + " wins"))
            highlight_winner()
        elif empty_spaces() is False:
            label.config(text="Tie!")
        else:
            switch_player()

# Function to switch the player after a turn
def switch_player():
    global player
    if game_mode.get() == 1 and player == human_player:
        player = ai_player
        label.config(text=(ai_player + " turn"))
        window.after(1000, best_move)
    elif game_mode.get() == 2:  # AI vs AI mode
        player = 'o' if player == 'x' else 'x'
        label.config(text=(player + " turn"))
        window.after(1000, ai_random_move)
    else:
        player = human_player if player == ai_player else ai_player
        label.config(text=(player + " turn"))

# Function to make a random move for AI
def ai_random_move():
    empty = []
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == "":
                empty.append((i, j))
    if empty:
        move = random.choice(empty)
        buttons[move[0]][move[1]]['text'] = player 
        if check_winner():
            highlight_winner()
        else:
            switch_player()

# Function to check if there's a winner
def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            return True
    for col in range(3):
        if buttons[0][col]['text'] == buttons[1][col]['text'] == buttons[2][col]['text'] != "":
            return True
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        return True
    return False

# Function to check if there are any empty spaces left
def empty_spaces():
    spaces = 9
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != "":
                spaces -= 1
    return spaces != 0

# Function to start a new game
def new_game():
    global player
    player = human_player
    label.config(text=player + " turn")
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg="#F0F0F0")
    if game_mode.get() == 2:
        start_ai_vs_ai()

# Function to highlight the winning sequence
def highlight_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            for col in range(3):
                buttons[row][col].config(bg="light green")
    for col in range(3):
        if buttons[0][col]['text'] == buttons[1][col]['text'] == buttons[2][col]['text'] != "":
            for row in range(3):
                buttons[row][col].config(bg="light green")
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        for idx in range(3):
            buttons[idx][idx].config(bg="light green")
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg="light green")
        buttons[1][1].config(bg="light green")
        buttons[2][0].config(bg="light green")

# Function to start AI vs AI game automatically
def start_ai_vs_ai():
    if game_mode.get() == 2:
        ai_random_move()

# Setting up the main window
window = Tk()
window.title("Tic-Tac-Toe")
players = ["x", "o"]
human_player = random.choice(players)
ai_player = "o" if human_player == "x" else "x"
player = human_player

# Game mode selection (Human vs Human, Human vs AI, AI vs AI)
game_mode = IntVar()
human_vs_human = Radiobutton(window, text="Human vs. Human", variable=game_mode, value=0, command=start_ai_vs_ai)
human_vs_ai = Radiobutton(window, text="Human vs. AI", variable=game_mode, value=1, command=start_ai_vs_ai)
ai_vs_ai = Radiobutton(window, text="AI vs. AI", variable=game_mode, value=2, command=start_ai_vs_ai)
human_vs_human.pack(side="top")
human_vs_ai.pack(side="top")
ai_vs_ai.pack(side="top")
game_mode.set(0)

# Label to display turn information
label = Label(text=player + " turn", font=('consolas', 40))
label.pack(side="top")

# Button to restart the game
reset_button = Button(text="restart", font=('consolas', 20), command=new_game)
reset_button.pack(side="top")

# Frame to hold the game buttons
frame = Frame(window)
frame.pack()

# Creating the 3x3 grid of buttons for the game
buttons = [[0, 0, 0] for _ in range(3)]
for row in range(3):
    for column in range(3):
        button = Button(frame, text="", font=('consolas', 40), width=5, height=2,
                        command=lambda row=row, column=column: next_turn(row, column))
        button.grid(row=row, column=column)
        buttons[row][column] = button


# Start the GUI event loop
if __name__ == "__main__":
    window.mainloop()
