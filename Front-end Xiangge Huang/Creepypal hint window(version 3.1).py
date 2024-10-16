import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class CreepyPalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CreepyPal - MC Assistant")
        self.setGeometry(100, 100, 1100, 650)

        # 加载固定的背景图片
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("background.jpg")
        self.background_label.setPixmap(self.background_pixmap)
        self.background_label.resize(1405, 700)

        # 创建合成图列表，与背景图片对应
        self.synthesis_images = [
            QPixmap("Crafting-Table.png"),
            QPixmap("Sticks.png"),
            QPixmap("Pickaxe.png")
        ]
        self.current_background_index = 0

        # 初始化合成图的 Label
        self.synthesis_label = QLabel(self)
        self.update_synthesis_image()

        # 翻页按钮，用图片铺满按钮
        self.prev_button = QPushButton("Prev", self)
        self.prev_button.clicked.connect(self.prev_page)
        self.prev_button.setGeometry(300, 400, 90, 30)
        self.prev_button.setStyleSheet("QPushButton { background-image: url('cs.png'); background-size: cover; }")

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setGeometry(420, 400, 90, 30)
        self.next_button.setStyleSheet("QPushButton { background-image: url('cs.png'); background-size: cover; }")

        # 文本输入框带占位符
        self.input_box = QLineEdit(self)
        self.input_box.setGeometry(200, 50, 500, 30)
        self.input_box.setFont(QFont("Minecraft", 10))
        self.input_box.setStyleSheet("background: transparent; color: black; border: none;")
        self.input_box.setPlaceholderText("Send your Question&Goal")
        self.input_box.textChanged.connect(self.on_input_change)

        # 文本输出框带占位符，初始化时禁用用户输入
        self.output_box = QTextEdit(self)
        self.output_box.setGeometry(200, 150, 550, 230)
        self.output_box.setFont(QFont("Minecraft", 10))
        self.output_box.setStyleSheet("background: transparent; color: black; border: none;")
        self.output_box.setPlaceholderText("CreepyPal: Output will appear here...")
        self.output_box.setReadOnly(True)

        # 发送按钮用图片铺满按钮
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.get_answer)
        self.send_button.setGeometry(770, 50, 90, 30)
        self.send_button.setStyleSheet("QPushButton { background-image: url('cs.png'); background-size: cover; }")

        # 显示/隐藏合成图按钮用图片铺满按钮
        self.toggle_image_button = QPushButton("Synthesis", self)
        self.toggle_image_button.clicked.connect(self.toggle_synthesis_image)
        self.toggle_image_button.setGeometry(770, 150, 90, 30)
        self.toggle_image_button.setStyleSheet("QPushButton { background-image: url('cs.png'); background-size: cover; }")

    def on_input_change(self, text):
        if not text:
            self.input_box.setPlaceholderText("Send your Question&Goal")

    def get_answer(self):
        question = self.input_box.text()
        if question == "" or question == "Send your Question&Goal":
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Type error", "Please enter a question or keyword!")
            return
        response = f"Based on your question '{question}', we recommend that you collect the following resources and perform these synthetic routes..."
        self.output_box.setText(response)

    def toggle_synthesis_image(self):
        self.synthesis_label.setVisible(not self.synthesis_label.isVisible())

    def update_synthesis_image(self):
        self.synthesis_label.setPixmap(self.synthesis_images[self.current_background_index])
        self.synthesis_label.setGeometry(710, 100, 300, 300)

    def prev_page(self):
        self.current_background_index = (self.current_background_index - 1) % len(self.synthesis_images)
        self.update_synthesis_image()

    def next_page(self):
        self.current_background_index = (self.current_background_index + 1) % len(self.synthesis_images)
        self.update_synthesis_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CreepyPalWindow()
    ex.show()
    sys.exit(app.exec_())
