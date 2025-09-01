# Вариант 10
# Объекты – эллипсы
# Функции:	сегментация
# визуализация
# раскраска

import tkinter as tk      
from tkinter import filedialog  
from tkinter import messagebox  
import random          

# Класс эллипса
class Ellipse:
    def __init__(self, x, y, a, b):  
        self.x = x        
        self.y = y        
        self.a = a         
        self.b = b         
        self.color = "red"

    #  Сегментация
    def is_inside(self, px, py):
        return ((px - self.x)**2 / self.a**2) + ((py - self.y)**2 / self.b**2) <= 1

    #  Визуализация:
    def draw(self, canvas):
        canvas.create_oval(
            self.x - self.a, self.y - self.b, 
            self.x + self.a, self.y + self.b,  
            fill=self.color, outline="black"  
        )

    # меняет цвет
    def set_color(self, color):
        self.color = color

    #  перемещение с ограничением
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # проверяем границы
        if new_x - self.a < 0:         
            new_x = self.a
        if new_x + self.a > 500:        
            new_x = 500 - self.a

        # проверяем границы
        if new_y - self.b < 0:       
            new_y = self.b
        if new_y + self.b > 400:        
            new_y = 400 - self.b

        # применяем новые координаты
        self.x = new_x
        self.y = new_y

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Эллипсы")

        # холст для рисования
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()  # размещает холст

        # привязка клика мыши к обработчику сегментации
        self.canvas.bind("<Button-1>", self.on_canvas_click) 

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.file_entry = tk.Entry(self.frame, width=30)
        self.file_entry.pack(side=tk.LEFT, padx=5)

        self.select_button = tk.Button(self.frame, text="Выбрать файл", command=self.choose_file)
        self.select_button.pack(side=tk.LEFT)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack()

        # Кнопки действий
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

        self.current_ellipse = None 

    # открыть диалог выбора файла
    def choose_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, path)    

    # загрузить данные из файла
    def load_from_file(self):
        path = self.file_entry.get()
        try:
            with open(path, "r") as f:                 
                data = f.readline().strip().split(",")   
                if len(data) != 4:                       
                    raise ValueError("Файл: x,y,a,b")
                x, y, a, b = map(int, data)             
   
                if x - a < 0 or x + a > 500 or y - b < 0 or y + b > 400:
                    messagebox.showwarning("Внимание", "Эллипс слишком большой или выходит за границы.")
                self.current_ellipse = Ellipse(x, y, a, b) 
                messagebox.showinfo("Успех", "Данные загружены.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e)) 

    def visualize(self):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Нет данных.")
            return
        self.canvas.delete("all")        
        self.current_ellipse.draw(self.canvas)  

    # Изменить цвет на случайный
    def change_color(self):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Нет данных.")
            return
        # список цветов
        colors = ["red", "blue", "green", "pink", "purple", "orange", "brown", "cyan", "magenta", "yellow"]
        new_color = random.choice(colors) 
        self.current_ellipse.set_color(new_color)
        self.visualize() 

    # переместить на 20 вправо, 10 вверх
    def move_shape(self):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Нет данных.")
            return
        self.current_ellipse.move(20, -10) 
        self.visualize()  

    # Сохранить в файл
    def save_to_file(self):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Нет данных.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            with open(path, "w") as f:
                values = [self.current_ellipse.x, self.current_ellipse.y, self.current_ellipse.a, self.current_ellipse.b]
                f.write(",".join(map(str, values)))
            messagebox.showinfo("Сохранено", "Данные сохранены.")

    # ГРАФИЧЕСКАЯ СЕГМЕНТАЦИЯ
    def on_canvas_click(self, event):
        if not self.current_ellipse:
            messagebox.showwarning("Ошибка", "Сначала загрузите и нарисуйте эллипс.")
            return

        px, py = event.x, event.y  # координаты клика

        # проверка точки 
        if self.current_ellipse.is_inside(px, py):
            color = "green"  
            msg = "Точка внутри эллипса"
        else:
            color = "red"   
            msg = "Точка снаружи"
        self.canvas.create_oval(px - 3, py - 3, px + 3, py + 3,
                                fill=color, outline="black", width=1)


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk() 
    app = App(root)
    root.mainloop()         
