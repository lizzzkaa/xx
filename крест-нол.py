import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f5")

        self.color_x = "#d63031"
        self.color_o = "#0984e3"
        self.bg_color = "#f0f0f5"
        self.btn_bg = "#ffffff"

        self.board = [''] * 9
        self.current_player = 'X'
        self.game_active = False
        self.scores = {'X': 0, 'O': 0}
        self.moves_count = {'X': 0, 'O': 0}
        self.player_symbol = 'X'

        self.create_start_screen()

    def create_start_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg=self.bg_color, padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Крестики-нолики", font=("Segoe UI", 24, "bold"),
                 fg="#2d3436", bg=self.bg_color).pack(pady=20)

        tk.Label(frame, text="Выберите, за кого играть:", font=("Segoe UI", 12),
                 bg=self.bg_color).pack(pady=10)

        tk.Button(frame, text="Играть за X (красные)", font=("Segoe UI", 10, "bold"),
                  width=20, bg="#ffeaa7", fg="#d63031", pady=10,
                  command=lambda: self.start_game('X')).pack(pady=10)

        tk.Button(frame, text="Играть за O (синие)", font=("Segoe UI", 10, "bold"),
                  width=20, bg="#a29bfe", fg="#0984e3", pady=10,
                  command=lambda: self.start_game('O')).pack(pady=10)

    def start_game(self, symbol):
        self.player_symbol = symbol
        self.game_active = True
        self.board = [''] * 9
        self.moves_count = {'X': 0, 'O': 0}
        self.current_player = symbol
        self.clear_screen()
        self.setup_game_ui()

    def setup_game_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        board_frame = tk.Frame(main_frame, bg=self.bg_color)
        board_frame.grid(row=0, column=0, padx=30, pady=20)

        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=("Arial", 24, "bold"),
                                width=6, height=3, bg=self.btn_bg, relief="solid",
                                command=lambda i=i, j=j: self.player_move(i, j))
                btn.grid(row=i, column=j, padx=3, pady=3)
                self.buttons.append(btn)

        info_frame = tk.Frame(main_frame, bg=self.bg_color, width=200)
        info_frame.grid(row=0, column=1, sticky="n", padx=10)
        info_frame.grid_propagate(False)

        tk.Label(info_frame, text=f"Вы играете за: {self.player_symbol}",
                 font=("Segoe UI", 12, "bold"),
                 fg=self.color_x if self.player_symbol == 'X' else self.color_o,
                 bg=self.bg_color).pack(pady=10)

        self.turn_label = tk.Label(info_frame, text=f"Ход: {self.current_player}",
                                   font=("Segoe UI", 14, "bold"), bg=self.bg_color)
        self.turn_label.pack(pady=15)

        self.moves_label = tk.Label(info_frame, text="Ходы в партии:\nX: 0\nO: 0",
                                    font=("Segoe UI", 12), bg=self.bg_color, justify="left")
        self.moves_label.pack(pady=20)

        self.score_label = tk.Label(info_frame, text=f"Победы:\nX: {self.scores['X']} | O: {self.scores['O']}",
                                    font=("Segoe UI", 12), bg=self.bg_color, fg="#636e72")
        self.score_label.pack(pady=20)

        tk.Button(info_frame, text="🔄 Новая игра", font=("Segoe UI", 10, "bold"),
                  bg="#dfe6e9", command=self.reset_game).pack(pady=10)
        tk.Button(info_frame, text="🏠 В меню", font=("Segoe UI", 10, "bold"),
                  bg="#dfe6e9", command=self.create_start_screen).pack(pady=5)

    def player_move(self, row, col):
        if not self.game_active or self.current_player != self.player_symbol:
            return
        index = row * 3 + col
        if self.board[index] == '':
            self.board[index] = self.player_symbol
            self.buttons[index].config(text=self.player_symbol,
                fg=self.color_x if self.player_symbol == 'X' else self.color_o)
            self.moves_count[self.player_symbol] += 1
            self.update_moves_display()

            if self.check_winner(self.player_symbol):
                self.end_game(self.player_symbol)
            elif self.check_draw():
                self.end_game(None)
            else:
                ai = 'O' if self.player_symbol == 'X' else 'X'
                self.current_player = ai
                self.turn_label.config(text=f"Ход: {ai}")
                self.root.after(600, self.ai_move)

    def ai_move(self):
        if not self.game_active:
            return
        ai = 'O' if self.player_symbol == 'X' else 'X'
        pl = self.player_symbol
        if self.current_player != ai:
            return

        for i in range(9):
            if self.board[i] == '':
                self.board[i] = ai
                if self.check_winner(ai):
                    self.board[i] = ai
                    self.buttons[i].config(text=ai, fg=self.color_o if ai == 'O' else self.color_x)
                    self.moves_count[ai] += 1
                    self.update_moves_display()
                    self.end_game(ai)
                    return
                self.board[i] = ''

        for i in range(9):
            if self.board[i] == '':
                self.board[i] = pl
                if self.check_winner(pl):
                    self.board[i] = ai
                    self.buttons[i].config(text=ai, fg=self.color_o if ai == 'O' else self.color_x)
                    self.moves_count[ai] += 1
                    self.update_moves_display()
                    self.current_player = pl
                    self.turn_label.config(text=f"Ход: {pl}")
                    return
                self.board[i] = ''

        empty = [i for i in range(9) if self.board[i] == '']
        if empty:
            i = random.choice(empty)
            self.board[i] = ai
            self.buttons[i].config(text=ai, fg=self.color_o if ai == 'O' else self.color_x)
            self.moves_count[ai] += 1
            self.update_moves_display()

            if self.check_winner(ai):
                self.end_game(ai)
            elif self.check_draw():
                self.end_game(None)
            else:
                self.current_player = pl
                self.turn_label.config(text=f"Ход: {pl}")

    def check_winner(self, p):
        win = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for c in win:
            if self.board[c[0]] == self.board[c[1]] == self.board[c[2]] == p:
                for i in c:
                    self.buttons[i].config(bg="#55efc4")
                return True
        return False

    def check_draw(self):
        return '' not in self.board

    def end_game(self, w):
        self.game_active = False
        if w:
            self.scores[w] += 1
            msg = "Вы выиграли!" if w == self.player_symbol else "Бот выиграл!"
            messagebox.showinfo("Победа!", msg)
        else:
            messagebox.showinfo("Ничья", "Ничья!")
        self.score_label.config(text=f"Победы:\nX: {self.scores['X']} | O: {self.scores['O']}")

    def update_moves_display(self):
        self.moves_label.config(text=f"Ходы в партии:\nX: {self.moves_count['X']}\nO: {self.moves_count['O']}")

    def reset_game(self):
        self.board = [''] * 9
        self.moves_count = {'X': 0, 'O': 0}
        self.current_player = self.player_symbol
        self.game_active = True
        for b in self.buttons:
            b.config(text="", fg="black", bg=self.btn_bg)
        self.turn_label.config(text=f"Ход: {self.current_player}")
        self.update_moves_display()

    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()