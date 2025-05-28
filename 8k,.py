#Вариант 10
#Объекты – эллипсы
#Функции:	сегментация
#визуализация
#раскраска
#перемещение на плоскости

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Класс "Эллипс"
class Ellipse:
    def __init__(self, x, y, a, b):
        self.x = x          # Координата X центра
        self.y = y          # Координата Y центра
        self.a = a          # Большая полуось
        self.b = b          # Малая полуось
        self.color = "red"  # Цвет по умолчанию

    # 1. Сегментация 
    def is_inside(self, px, py):
        return ((px - self.x) ** 2 / self.a ** 2) + ((py - self.y) ** 2 / self.b ** 2) <= 1

    # 2. Визуализация 
    def draw(self, canvas):
        canvas.create_oval(
            self.x - self.a, self.y - self.b,
            self.x + self.a, self.y + self.b,
            fill=self.color, outline="black"
        )

    # 3. Раскраска
    def set_color(self, color):
        self.color = color

    # 4. Перемещение на плоскости
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

# --- Графический интерфейс ---
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Эллипсы")

        # Холст для отрисовки
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()

        # Поля управления
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Кнопки
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack()

        self.load_button = tk.Button(self.btn_frame, text="Загрузить", command=self.load_from_file)
        self.load_button.grid(row=0, column=0, padx=5)

        self.draw_button = tk.Button(self.btn_frame, text="Нарисовать", command=self.visualize)
        self.draw_button.grid(row=0, column=1, padx=5)

        self.color_button = tk.Button(self.btn_frame, text="Цвет", command=self.change_color)
        self.color_button.grid(row=0, column=2, padx=5)

        self.move_button = tk.Button(self.btn_frame, text="Переместить", command=self.move_shape)
        self.move_button.grid(row=0, column=3, padx=5)

        self.save_button = tk.Button(self.btn_frame, text="Сохранить", command=self.save_to_file)
        self.save_button.grid(row=0, column=4, padx=5)

        self.file_entry = tk.Entry(self.frame, width=30)
        self.file_entry.pack(side=tk.LEFT, padx=5)

        self.select_button = tk.Button(self.frame, text="Выбрать файл", command=self.choose_file)
        self.select_button.pack(side=tk.LEFT)

        self.ellipses = []  
        self.current_ellipse = None 

    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def load_from_file(self):
        path = self.file_entry.get()
        try:
            with open(path, "r") as f:
                data = f.readline().strip().split(",")
                if len(data) != 4:
                    raise ValueError("Файл должен содержать 4 числа: x, y, a, b")
                x, y, a, b = map(int, data)
                self.current_ellipse = Ellipse(x, y, a, b)
                messagebox.showinfo("Успех", "Данные загружены.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def visualize(self):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Сначала загрузите данные.")
            return
        self.canvas.delete("all")
        self.current_ellipse.draw(self.canvas)

    def change_color(self):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Сначала загрузите данные.")
            return
        new_color = "pink" 
        self.current_ellipse.set_color(new_color)
        self.visualize()

    def move_shape(self):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Сначала загрузите данные.")
            return
        self.current_ellipse.move(20, -10)
        self.visualize()

    def save_to_file(self):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Сначала загрузите данные.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            with open(file_path, "w") as f:
                values = [self.current_ellipse.x, self.current_ellipse.y, self.current_ellipse.a, self.current_ellipse.b]
                f.write(",".join(map(str, values)))
            messagebox.showinfo("Сохранено", "Данные сохранены в CSV.")

# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
