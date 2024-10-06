import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class CreepyPalWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("CreepyPal - MC Assistant")
        self.root.geometry("1100x650")

        # 初始化合成图显示的布尔变量
        self.is_image_visible = True

        # 加载固定的背景图片
        self.background_image = ImageTk.PhotoImage(Image.open("background.jpg"))

        # 创建合成图列表，与背景图片对应
        self.synthesis_images = [
            ImageTk.PhotoImage(Image.open("Crafting-Table.png")),  # 第一页显示工作台合成图
            ImageTk.PhotoImage(Image.open("Sticks.png")),          # 第二页显示木棍合成图
            ImageTk.PhotoImage(Image.open("Pickaxe.png"))          # 第三页显示镐子合成图
        ]
        self.current_background_index = 0

        # 创建Canvas显示背景图片
        self.canvas = tk.Canvas(self.root, width=1405, height=700)
        self.canvas.pack(fill="both", expand=True)

        # 设置固定背景图片
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        # 初始化合成图的 Label
        self.synthesis_label = tk.Label(self.root)

        # 翻页按钮
        self.prev_button = tk.Button(self.root, text="Previous", command=self.prev_page)
        self.prev_button.place(x=390, y=400)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_page)
        self.next_button.place(x=480, y=400)

        # 文本输入框
        self.input_label = tk.Label(self.root, text="Send your Question&Goal:")
        self.input_label.place(x=10, y=50)

        self.input_box = tk.Entry(self.root, width=80)
        self.input_box.place(x=200, y=50)

        # 文本输出框
        self.output_label = tk.Label(self.root, text="CreepyPal:")
        self.output_label.place(x=105, y=150)

        self.output_box = tk.Text(self.root, height=15, width=70)
        self.output_box.place(x=200, y=150)

        # 发送按钮
        self.send_button = tk.Button(self.root, text="Send", command=self.get_answer)
        self.send_button.place(x=770, y=45)

        # 显示/隐藏合成图按钮
        self.toggle_image_button = tk.Button(self.root, text="Show/Hide Image", command=self.toggle_synthesis_image)
        self.toggle_image_button.place(x=850, y=150)

        # 初始化显示合成图
        self.update_synthesis_image()

    def update_synthesis_image(self):
        """更新合成图"""
        if self.is_image_visible:
            self.synthesis_label.config(image=self.synthesis_images[self.current_background_index])
            self.synthesis_label.place(x=800, y=200)  # 显示合成图
        else:
            self.synthesis_label.place_forget()  # 隐藏合成图

    def prev_page(self):
        """翻页到前一张合成图"""
        self.current_background_index = (self.current_background_index - 1) % len(self.synthesis_images)
        self.update_synthesis_image()

    def next_page(self):
        """翻页到后一张合成图"""
        self.current_background_index = (self.current_background_index + 1) % len(self.synthesis_images)
        self.update_synthesis_image()

    def get_answer(self):
        """根据用户输入返回路线建议"""
        question = self.input_box.get()
        if not question:
            messagebox.showwarning("Type error", "Please enter a question or keyword!")
            return

        # 模拟生成回答的部分
        response = f"Based on your question '{question}', we recommend that you collect the following resources and perform these synthetic routes..."

        # 显示在输出框中
        self.output_box.delete(1.0, tk.END)  # 清空之前的内容
        self.output_box.insert(tk.END, response)

    def toggle_synthesis_image(self):
        """切换合成图的显示和隐藏状态"""
        self.is_image_visible = not self.is_image_visible
        self.update_synthesis_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = CreepyPalWindow(root)
    root.mainloop()
