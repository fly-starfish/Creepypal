import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

# 个性化窗口，选择背景主题
class PersonalizationWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Personalization")
        self.setGeometry(100, 100, 400, 300)

        # 添加背景图片
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("personalization_background.jpg")  # 你的背景图片文件路径
        self.background_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background_label.resize(self.size())
        self.background_label.lower()  # 确保背景在最底层，按钮在其上面

        # 创建五个按钮，分别代表不同的主题，主题背景图片和对应的主界面背景图片
        characters = ["Villager", "Creeper", "Skeleton", "Enderman", "Zombie"]
        themes = [
            {"start": "villager.png", "main": "villager_main.png"},
            {"start": "creeper.png", "main": "creeper_main.png"},
            {"start": "skeleton.png", "main": "skeleton_main.png"},
            {"start": "enderman.png", "main": "enderman_main.png"},
            {"start": "zombie.png", "main": "zombie_main.png"}
        ]

        for i, character in enumerate(characters):
            button = QPushButton(character, self)
            button.setGeometry(50, 50 + i * 40, 300, 30)
            button.clicked.connect(lambda _, theme=themes[i]: self.set_theme(theme))

    def set_theme(self, theme):
        # 设置开始界面的背景为选定的主题，主界面背景为对应的背景
        self.main_window.selected_theme = theme["start"]
        self.main_window.selected_main_theme = theme["main"]
        self.main_window.update_background()  # 更新开始界面背景
        self.close()

    def resizeEvent(self, event):
        # 当窗口大小变化时，重新调整背景图大小
        self.background_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background_label.resize(self.size())
        super().resizeEvent(event)

# 主菜单窗口
class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_theme = "background.jpg"  # 默认开始界面背景
        self.selected_main_theme = "background.jpg"  # 默认主界面背景
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CreepyPal - Main Menu")
        self.setGeometry(100, 100, 400, 300)

        # 加载开始界面背景图
        self.background_label = QLabel(self)
        self.update_background()

        # 个性化按钮
        self.settings_button = QPushButton("Personalize", self)
        self.settings_button.setGeometry(230, 50, 100, 40)
        self.settings_button.clicked.connect(self.show_personalization)

        # 开始按钮
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(70, 50, 100, 40)
        self.start_button.clicked.connect(self.open_creepy_pal_window)

    def show_personalization(self):
        self.personalization_window = PersonalizationWindow(self)
        self.personalization_window.show()

    def open_creepy_pal_window(self):
        # 打开 CreepyPalWindow 界面，传递选择的主界面背景
        self.creepy_pal_window = CreepyPalWindow(self, self.selected_main_theme)
        self.creepy_pal_window.show()
        self.close()

    def update_background(self):
        # 使用个性化的开始界面背景
        self.background_pixmap = QPixmap(self.selected_theme)
        self.background_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background_label.resize(self.size())

    def resizeEvent(self, event):
        # 当主菜单窗口大小变化时，重新调整背景图大小
        self.update_background()
        super().resizeEvent(event)

# CreepyPal 游戏助手窗口（即主界面）
class CreepyPalWindow(QMainWindow):
    def __init__(self, main_menu, theme):
        super().__init__()
        self.main_menu = main_menu
        self.theme = theme  # 主界面背景
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CreepyPal - MC Assistant")
        self.setGeometry(100, 100, 1100, 650)

        # 加载个性化或默认的主界面背景图片
        self.background_label = QLabel(self)
        self.update_background()

        # 返回主菜单按钮
        self.back_button = QPushButton("Return to Main Menu", self)
        self.back_button.setGeometry(950, 600, 150, 40)  # 在右下角设置按钮位置
        self.back_button.clicked.connect(self.return_to_main_menu)

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

    def return_to_main_menu(self):
        self.main_menu.show()  # 显示主菜单
        self.close()  # 关闭 CreepyPal 窗口

    def on_input_change(self, text):
        if not text:
            self.input_box.setPlaceholderText("Send your Question&Goal")

    def get_answer(self):
        question = self.input_box.text()
        if question == "" or question == "Send your Question&Goal":
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

    def update_background(self):
        # 主界面使用个性化或默认的背景
        self.background_pixmap = QPixmap(self.theme)
        self.background_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background_label.resize(self.size())

    def resizeEvent(self, event):
        # 当主界面窗口大小变化时，重新调整背景图大小
        self.update_background()
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenuWindow()
    main_menu.show()
    sys.exit(app.exec_())
