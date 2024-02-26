import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
       
        self.current_player = 'X'
        self.game_over = False   #stll game not ended

        self.buttons = [[None, None, None] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    master, text="", font=('Arial', 20, 'bold'),
                    width=8, height=4, bg='white', fg='black',
                    command=lambda i=i, j=j: self.make_move(i, j)
                )
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.reset_button = tk.Button(master, text="Replay", font=('Arial', 14, 'bold'), bg='#4CAF50', fg='white',
                                      command=self.reset_board)
        self.reset_button.grid(row=3, column=1, pady=10)

    def make_move(self, row, col):
        if not self.game_over and self.buttons[row][col]['text'] == "":
            self.buttons[row][col]['text'] = self.current_player
            self.buttons[row][col]['state'] = 'disabled'
            if self.check_winner(row, col):
                self.game_over = True
                self.highlight_winner(row, col)
                self.show_winner_popup()
            elif self.check_draw():
                self.game_over = True
                self.show_draw_popup()
            else:
                self.switch_player()

    def check_winner(self, row, col):
        # Check row
        if all(self.buttons[row][c]['text'] == self.current_player for c in range(3)):
            return True

        # Check column
        if all(self.buttons[r][col]['text'] == self.current_player for r in range(3)):
            return True

        # Check diagonals
        if row == col and all(self.buttons[i][i]['text'] == self.current_player for i in range(3)):
            return True
        if row + col == 2 and all(self.buttons[i][2 - i]['text'] == self.current_player for i in range(3)):
            return True

        return False

    def check_draw(self):
        return all(self.buttons[i][j]['text'] != "" for i in range(3) for j in range(3))

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset_board(self):
        self.game_over = False
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ""
                self.buttons[i][j]['state'] = 'normal'
                self.buttons[i][j]['bg'] = 'white'
                self.reset_button['state'] = 'normal'

    def highlight_winner(self, row, col):
        # Highlight winning row
        for c in range(3):
            self.buttons[row][c]['bg'] = '#FA7227'

        # Highlight winning column
        for r in range(3):
            self.buttons[r][col]['bg'] = '#FA7227'

        # Highlight winning diagonal (if applicable)
        if row == col:
            for i in range(3):
                self.buttons[i][i]['bg'] = '#FA7227'

        if row + col == 2:
            for i in range(3):
                self.buttons[i][2 - i]['bg'] = '#FA7227'

    def show_winner_popup(self):
        winner = f"Player {self.current_player}"
        messagebox.showinfo("Winner!", f"{winner} wins!")
        self.ask_replay()

    def show_draw_popup(self):
        messagebox.showinfo("Draw!", "It's a draw!")
        self.ask_replay()

    def ask_replay(self):
        replay = messagebox.askyesno("Replay", "Do you want to play again?")
        if replay:
            self.reset_board()
        else:
            self.master.destroy()

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
