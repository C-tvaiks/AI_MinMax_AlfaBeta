import tkinter as tk
from tkinter import ttk
import random

class GameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Skaitļu Spēle")
        self.master.geometry("1010x500")

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.center_frame = tk.Frame(self.main_frame)
        self.center_frame.pack(expand=True, pady=20)

        self.mode_label = tk.Label(self.center_frame, text="Izvēlieties spēles režīmu:", font=("Helvetica", 14))
        self.mode_label.pack()

        self.mode_frame = tk.Frame(self.center_frame)
        self.mode_frame.pack(pady=10)

        self.vs_computer_button = tk.Button(self.mode_frame, text="Spēlēt pret datoru", font=("Helvetica", 12), command=self.vs_computer_mode)
        self.vs_computer_button.pack(side=tk.LEFT, padx=10)

        self.vs_player_button = tk.Button(self.mode_frame, text="Spēlēt pret otru spēlētāju", font=("Helvetica", 12), command=self.vs_player_mode)
        self.vs_player_button.pack(side=tk.LEFT, padx=10)

        self.current_player = 1
        self.player1_points = 0
        self.player2_points = 0
        self.computer_mode = None


    def vs_computer_mode(self):
        self.clear_center_frame()
        self.game_mode = "vs_computer"
        self.choose_computer_mode()

    def choose_computer_mode(self):
       
        self.mode_label = tk.Label(self.center_frame, text="Izvēlieties spēles režīmu:", font=("Helvetica", 14))
        self.mode_label.pack()

        self.minmax_label = tk.Button(self.center_frame, text="MinMax", font=("Helvetica", 12), command=self.minmax)
        self.minmax_label.pack(side=tk.LEFT, padx=10)

        self.alfabeta_label = tk.Button(self.center_frame, text="AlphaBeta", font=("Helvetica", 12), command=self.alfabeta)
        self.alfabeta_label.pack(side=tk.LEFT, padx=10)

    def minmax(self):
        self.clear_center_frame()
        self.computer_mode = "minmax"
        self.choose_first_turn()
    
    def alfabeta(self):
        self.clear_center_frame()
        self.computer_mode = "alfabeta"
        self.choose_first_turn()
    
    def choose_first_turn(self):

        self.mode_label = tk.Label(self.center_frame, text="Izvēlieties kurš iet pirmais:", font=("Helvetica", 14))
        self.mode_label.pack()

        self.player_turn_button = tk.Button(self.center_frame, text="Speletājs", font=("Helvetica", 12), command=self.create_length_selection)
        self.player_turn_button.pack(side=tk.LEFT, padx=10)

        self.computer_turn_button = tk.Button(self.center_frame, text="Dators", font=("Helvetica", 12), command=self.computer_turn)
        self.computer_turn_button.pack(side=tk.LEFT, padx=10)
    
    def computer_turn(self):
        self.current_player = 2
        self.create_length_selection()

    def vs_player_mode(self):
        self.clear_center_frame()
        self.game_mode = "vs_player"
        self.create_length_selection()

    def clear_center_frame(self):
        for widget in self.center_frame.winfo_children():
            widget.destroy()

    def create_length_selection(self):
        self.clear_center_frame()

        self.length_label = tk.Label(self.center_frame, text="Izvēlieties skaitļu virknes garumu:", font=("Helvetica", 14))
        self.length_label.pack()

        self.length_combobox = ttk.Combobox(self.center_frame, values=["15", "16", "17", "18", "19", "20"], font=("Helvetica", 12))
        self.length_combobox.pack()

        self.generate_button = tk.Button(self.center_frame, text="Ģenerēt skaitļu virkni", font=("Helvetica", 12), command=self.generate_sequence)
        self.generate_button.pack(pady=10)

    def generate_sequence(self):
        length = int(self.length_combobox.get())
        self.number_sequence = self.generate_random_sequence(length)
        self.start_game()

    def generate_random_sequence(self, length):
        return [random.choice([1, 2, 3, 4]) for _ in range(length)]

    def start_game(self):
        self.clear_center_frame()

        self.label = tk.Label(self.center_frame, text="Izvēlieties skaitļus no šīs virknes un pieskaitiet savam punktu skaitam:", font=("Helvetica", 14))
        self.label.pack()

        self.remaining_numbers = list(self.number_sequence)

        self.points = 0
        self.points_label = tk.Label(self.center_frame, text=f"Punkti: {self.points}", font=("Helvetica", 14))
        self.points_label.pack()

        self.turn_label = tk.Label(self.main_frame, text="Paņemšanas gājiens: Spēlētājs 1", font=("Helvetica", 14))
        self.turn_label.pack()

        self.player1_points_label = tk.Label(self.main_frame, text="Spēlētājs 1 punkti: 0", font=("Helvetica", 14))
        self.player1_points_label.pack()
        if self.game_mode == "vs_computer":
            self.player2_points_label = tk.Label(self.main_frame, text="Datora punkti: 0", font=("Helvetica", 14))
            self.player2_points_label.pack()
        else:
            self.player2_points_label = tk.Label(self.main_frame, text="Spēlētājs 2 punkti: 0", font=("Helvetica", 14))
            self.player2_points_label.pack()


        self.buttons = []
        for num in self.number_sequence: # number_sequence ir saraksts ar skaitļiem
            button = tk.Button(self.center_frame, text=num, font=("Helvetica", 16), command=lambda n=num: self.choose_number(n))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.buttons.append(button)

        self.player1_points = 0
        self.player2_points = 0
        self.update_turn_label()

        if self.game_mode == "vs_computer":
            if self.current_player == 2:
                self.computer_move()

    

    def switch_players(self):
        self.current_player = 2 if self.current_player == 1 else 1
    
    def update_turn_label(self):
        current_player_text = f"Paņemšanas gājiens: {'Spēlētājs 1' if self.current_player == 1 else 'Dators' if self.game_mode == 'vs_computer' else 'Spēlētājs 2'}"
        self.turn_label.config(text=current_player_text)

    def update_points(self):
        if self.current_player == 1:
            self.player1_points += self.points
        else:
            self.player2_points += self.points
        self.points = 0
        self.player1_points_label.config(text=f"Spēlētājs 1 punkti: {self.player1_points}")
        if self.game_mode == "vs_computer":
            self.player2_points_label.config(text=f"Datora punkti: {self.player2_points}")
        else:
            self.player2_points_label.config(text=f"Spēlētājs 2 punkti: {self.player2_points}")

    def take_or_split_number(self, number, take=True):
        if take:
            self.points += number
            self.points_label.config(text=f"Punkti: {self.points}")
            button = self.buttons[self.remaining_numbers.index(number)]
            button.destroy()
            self.remaining_numbers.remove(number)
            self.update_buttons_text()  
            if not self.remaining_numbers:
                self.end_game()
            self.update_points()
         
            self.switch_players()
            self.update_turn_label()

            if self.game_mode == "vs_computer" and self.current_player == 2:
                self.computer_move()
        else:
            if number == 4:
                self.points += 1
                self.points_label.config(text=f"Punkti: {self.points}")

            half_number = number // 2
            button_index = self.remaining_numbers.index(number)
            button = self.buttons[button_index]
            button.destroy()
            del self.buttons[button_index]
            self.remaining_numbers.remove(number)
            self.remaining_numbers.extend([half_number, half_number])
            self.update_buttons_text()  
            if not self.remaining_numbers:
                self.end_game()
            self.update_points()
            
            self.switch_players()
     
            self.update_turn_label()

            if self.game_mode == "vs_computer" and self.current_player == 2:
                self.computer_move()

    def update_buttons_text(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for num in self.remaining_numbers:
            button = tk.Button(self.center_frame, text=num, font=("Helvetica", 16), command=lambda n=num: self.choose_number(n))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.buttons.append(button)

    def end_game(self):
        self.update_points()
        self.label.pack_forget()
        self.player1_points_label.pack_forget()
        self.player2_points_label.pack_forget()
        self.turn_label.pack_forget()
    
        if self.player1_points > self.player2_points:
            winner_text = "Uzvarēja Spēlētājs 1"
            self.points_label.config(text=f"{winner_text} ar {self.player1_points} punktiem")
        elif self.player2_points > self.player1_points:
            if self.game_mode == "vs_computer":
                winner_text = "Uzvarēja Dators"
            else:
                winner_text = "Uzvarēja Spēlētājs 2"
            self.points_label.config(text=f"{winner_text} ar {self.player2_points} punktiem")
        else:
            winner_text = "Spēle ir neizšķirta"
            self.points_label.config(text=f"{winner_text}")
        
        play_again_button = tk.Button(self.center_frame, text="Spēlēt atkal", font=("Helvetica", 12), command=self.play_again)
        play_again_button.pack(side=tk.LEFT, padx=20, pady=20)

        quit_button = tk.Button(self.center_frame, text="Iziet", font=("Helvetica", 12), command=self.quit_game)
        quit_button.pack(side=tk.RIGHT, padx=20, pady=20)
    
    def play_again(self):
        self.master.destroy()
        if __name__ == "__main__":
            main()

    def quit_game(self):
        self.master.destroy()

    def computer_move(self):  
 
        if self.computer_mode == "minmax":
           print(self.remaining_numbers)
           max_score, best_move = self.minimax_move(self.remaining_numbers, True) # izsauc minmax funkciju
           print("best_move", best_move, "max_score", max_score)
           self.choose_number(best_move[0])

        #if self.computer_mode == "alfabeta":
        #    best_move = self.alfabeta_move() # izsauc alfabeta funkciju
        #    self.choose_number(best_move)  
        
        else:
          best_move = self.find_best_move(self, False) #iegust maksimalo skatili no virknes
          if best_move is not None:
              self.choose_number(best_move) # "Nospiež" skaitli no virknes
          else:
             print("Nav Gajienu")

    def find_best_move(self):
        if not self.remaining_numbers:
            return None 
        return max(self.remaining_numbers)
    


    # number_sequence ir saraksts ar skaitļiem
    # pirms jebkadas funkciajs izsauksanas lietot self."funkcija"(parametrs ja tads ir)

    def alfabeta_move(self, is_maximizing_player): # Šeit implimentet alfabeta
        print("ir alfabeta")
    
    
    def minimax_move(self, nums, is_maximizing_player):
        if not nums:
            return 0, []

        if is_maximizing_player:
            max_score = float('-inf')
            best_moves = []
            for i in range(len(nums)):
                score = nums[i]
                best_subscore = score
                best_submoves = [nums[i]]
                for j in range(2, nums[i] // 2 + 1):
                    subscore, submoves = self.minimax_move([j, nums[i] - j], False)
                    subscore = max(subscore, j)
                    if subscore > best_subscore:
                        best_subscore = subscore
                        best_submoves = [j] + submoves
                if best_subscore > max_score:
                    max_score = best_subscore
                    best_moves = best_submoves
            return max_score, best_moves
        else:
            min_score = float('inf')
            best_moves = []
            for i in range(len(nums)):
                score = nums[i]
                best_subscore = score
                best_submoves = [nums[i]]
                for j in range(2, nums[i] // 2 + 1):
                    subscore, submoves = self.minimax_move([j, nums[i] - j], True)
                    subscore = min(subscore, j)
                    if subscore < best_subscore:
                        best_subscore = subscore
                        best_submoves = [j] + submoves
                if best_subscore < min_score:
                    min_score = best_subscore
                    best_moves = best_submoves
            return min_score, best_moves



    def choose_number(self, number):
        if self.current_player == 2 and self.game_mode == "vs_computer":
            self.points += number
            self.points_label.config(text=f"Punkti: {self.points}")
            button_index = self.remaining_numbers.index(number)
            button = self.buttons.pop(button_index)
            button.destroy()
            self.remaining_numbers.remove(number)
            if not self.remaining_numbers:
                self.end_game()
            self.update_points()
            self.switch_players()
            self.update_turn_label()
        else:
            if number == 2 or number == 4:
                menu = tk.Menu(self.master, tearoff=0)
                menu.add_command(label="Panemt", command=lambda: self.take_or_split_number(number, take=True))
                menu.add_command(label="Sadalīt", command=lambda: self.take_or_split_number(number, take=False))
                menu.post(self.master.winfo_x() + self.master.winfo_width() // 2, self.master.winfo_y() + self.master.winfo_height() // 2)
            else:
                self.points += number
                self.points_label.config(text=f"Punkti: {self.points}")
                button_index = self.remaining_numbers.index(number)
                button = self.buttons.pop(button_index)
                button.destroy()
                self.remaining_numbers.remove(number)
                if not self.remaining_numbers:
                    self.end_game()
                self.update_points()
                self.switch_players()
                self.update_turn_label()

            if self.game_mode == "vs_computer" and self.current_player == 2:
                self.computer_move()


def main():
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()