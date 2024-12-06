import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
class Player:
    def __init__(self):
        self.name = ""
        self.sympol = ""
    
    def choose_name(self):
        while True:
            name = input("Enter your name: ")    
            if name.isalpha():
                self.name = name
                break
            print("Invalid name. Please use alphabetic characters only.")
    
    def choose_sympol(self):
        while True:
            sympol = input(f"{self.name}, choose your symbol: ")
            if sympol.isalpha() and len(sympol) == 1:
                self.sympol = sympol.upper()
                break 
            print("Invalid symbol. Please choose a single letter.")

class Menue:
    def display_main_menue(self):
        print("Welcome to my X-O game")
        print("1. Start game")
        print("2. Quit game")
        while True:
            choice = input("Enter your choice: ")
            if choice in ('1', '2'):
                return choice
            print("Invalid choice. Please enter 1 or 2.") 
    
    def display_end_game_menue(self):
        menu_text = """
        Game Over!
        1. Restart game
        2. End game
        """
        choice = input(menu_text)
        return choice
          
class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]
    
    def display_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i+3]))
            if i < 6:
                print("-" * 5)

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
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menue = Menue()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menue.display_main_menue()
        if choice == "1":
            self.setup_players()
            self.play_game()
        else:
            self.quit_game()
            
    def setup_players(self):
        for num, player in enumerate(self.players, start=1):
            print(f"Player {num}, enter your details:")
            player.choose_name()
            player.choose_sympol()
            print("-" * 20)
            clear_screen()

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win() or self.check_drew():
                choice = self.menue.display_end_game_menue()
                if choice == "1":
                    self.restart_game()
                else:
                    self.quit_game()
                    break
    
    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.play_game()

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

    def check_drew(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def play_turn(self):
        player = self.players[self.current_player_index]  
        self.board.display_board()
        print(f"{player.name}'s turn ({player.sympol})")
        while True:
            try:
                cell_choice = int(input('Choose a cell (1-9): '))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.sympol):
                    break
            except ValueError:
                print("Please enter a number between 1-9.")    
        self.switch_player()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index
                    
    def quit_game(self):
        print("Thank you for playing!")

g = Game()
g.start_game()
