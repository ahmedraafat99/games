import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self):
        self.name = ""
        self.sympol = ""

    def choose_name(self, name):
        self.name = name

    def choose_sympol(self, sympol):
        # Ensure the symbol is a single alphabet letter
        while True:
            if len(sympol) == 1 and sympol.isalpha():
                self.sympol = sympol.upper()  # Converts the symbol to uppercase
                break
            else:
                # Display error if the symbol is invalid
                sympol = simpledialog.askstring("Player Symbol", f"Choose a symbol for {self.name} (1 letter only):")
                if not sympol:  # If the user cancels or enters nothing
                    break


class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def update_board(self, choice, sympol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = sympol
            return True
        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]


class Game:
    def __init__(self, root):
        self.root = root
        self.players = [Player(), Player()]
        self.board = Board()
        self.current_player_index = 0

        self.setup_gui()
        self.set_player_details()

    def setup_gui(self):
        self.root.title("X-O Game")

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.root, text=str(i+1), width=40, height=10, command=lambda i=i: self.play_turn(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

        self.status_label = tk.Label(self.root, text="Player 1's turn", font=("Arial", 14))
        self.status_label.grid(row=3, column=0, columnspan=3)

        self.restart_button = tk.Button(self.root, text="Restart", width=10, height=2, command=self.restart_game)
        self.restart_button.grid(row=4, column=0, columnspan=3)

    def set_player_details(self):
        player1_name = self.ask_for_name(1)
        self.players[0].choose_name(player1_name)
        player1_sympol = self.ask_for_symbol(1)
        self.players[0].choose_sympol(player1_sympol)

        player2_name = self.ask_for_name(2)
        self.players[1].choose_name(player2_name)
        player2_sympol = self.ask_for_symbol(2)
        self.players[1].choose_sympol(player2_sympol)


    def ask_for_name(self, player_num):
        name = simpledialog.askstring("Player Name", f"Enter name for Player {player_num}:")
        return name

    def ask_for_symbol(self, player_num):
        symbol = simpledialog.askstring("Player Symbol", f"Choose a symbol for Player {player_num} (1 letter only):")
        return symbol

    def play_turn(self, cell):
        player = self.players[self.current_player_index]
        if self.board.update_board(cell + 1, player.sympol):
            self.buttons[cell].config(text=player.sympol, state=tk.DISABLED)
            if self.check_win():
                self.show_winner(player)
            elif self.check_draw():
                self.show_draw()
            else:
                self.switch_player()

    def check_win(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]]:
                return True
        return False

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index
        current_player = self.players[self.current_player_index]
        self.status_label.config(text=f"{current_player.name}'s turn ({current_player.sympol})")

    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"{winner.name} wins!")
        self.restart_game()

    def show_draw(self):
        messagebox.showinfo("Game Over", "It's a draw!")
        self.restart_game()

    def restart_game(self):
        self.board.reset_board()
        for button in self.buttons:
            button.config(text=str(self.buttons.index(button) + 1), state=tk.NORMAL)
        self.status_label.config(text="Player 1's turn")
        self.current_player_index = 0


if __name__ == "__main__":
    import tkinter.simpledialog as simpledialog

    root = tk.Tk()
    game = Game(root)
    root.mainloop()
