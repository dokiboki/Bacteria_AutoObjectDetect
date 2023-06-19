from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QPushButton, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap
from PIL import Image
import os
import cv2
from ultralytics import YOLO
import hashlib
import datetime
import matplotlib.pyplot as plt
import sqlite3
key = Fernet.generate_key()

nowftime = datetime.datetime.now()  # 获取当前日期和时间
dt_string = nowftime.strftime("%Y-%m-%d_%H-%M-%S")  # 转换为字符串格式
keyfname = "key_" + dt_string + ".txt"  # 拼接文件名
with open(keyfname, "wb") as f:  # 打开一个以当前日期和时间命名的文件
    f.write(key)  # 将密钥写入文件
print(f"{keyfname}")

SAVE_picPATH = r'tYOLO//tYOLO'
model = YOLO(r"tYOLO//refresh.pt")
folder_path = r"tuberculosis.v2i.yolov8//testFOLDER"
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def decrypt_allpng(self,key):
        # 使用 Fernet 模块的 Fernet 类，创建一个 Fernet 对象，传入密钥
        f = Fernet(key)
        # 使用 PyQt5.QtWidgets 模块的 QFileDialog 类的 askDirectory 方法，弹出一个对话框，让用户选择一个文件夹
        folder_path = QFileDialog.getExistingDirectory()
        # 遍历文件夹下的所有文件
        for file in os.listdir(folder_path):
        # 获取文件的完整路径
            file_path = os.path.join(folder_path, file)
        # 判断文件是否是图片（根据扩展名）
            if file_path.endswith(('.png')):
        # 打开图片文件，读取二进制数据
                with open(file_path, 'rb') as image_file:
                    encrypted_data = image_file.read()
    # 使用 Fernet 对象的 decrypt 函数，对加密数据进行解密，得到解密结果
                    decrypted_data = f.decrypt(encrypted_data)
    # 打开图片文件，写入解密结果（覆盖原始数据）
                with open(file_path, 'wb') as image_file:
                    image_file.write(decrypted_data)
    # 打印提示信息
            print(f'Decrypted {file_path}')
            self.label.setText(f'Decrypted {file_path}')
    def encrypt_allpng(self,key):
            # 使用 Fernet 模块的 Fernet 类，创建一个 Fernet 对象，传入密钥
        f = Fernet(key)
        # 使用 PyQt5.QtWidgets 模块的 QFileDialog 类的 askDirectory 方法，弹出一个对话框，让用户选择一个文件夹
        folder_path = QFileDialog.getExistingDirectory()
        # 遍历文件夹下的所有文件
        for file in os.listdir(folder_path):
            # 获取文件的完整路径
            file_path = os.path.join(folder_path, file)
            # 判断文件是否是图片（根据扩展名）
            if file_path.endswith(('.png')):
                # 打开图片文件，读取二进制数据
                with open(file_path, 'rb') as image_file:
                    image_data = image_file.read()
                # 使用 Fernet 对象的 encrypt 函数，对图片数据进行加密，得到加密结果
                encrypted_data = f.encrypt(image_data)
                # 打开图片文件，写入加密结果（覆盖原始数据）
                with open(file_path, 'wb') as image_file:
                    image_file.write(encrypted_data)
                # 打印提示信息
                print(f'Encrypted {file_path}')
                self.label.setText(f'Encrypted {file_path}')
    def initUI(self):
        self.setWindowTitle("Image Processing App")
        self.label = QLabel(self)
        self.setGeometry(50,50, 800, 600)
        grid = QGridLayout()
        grid.addWidget(self.label, 4, 0)
        central_widget = QWidget(self)
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)
        self.image_frame1 = QLabel(self)
        self.image_frame1.setFixedSize(640, 480)
        grid.addWidget(self.image_frame1, 0, 0)
        self.image_frame2 = QLabel(self)
        self.image_frame2.setFixedSize(540, 380)
        grid.addWidget(self.image_frame2, 0, 3)
        start_button = QPushButton("启动", self)
        start_button.clicked.connect(self.startProcessing)
        grid.addWidget(start_button, 1, 0)
        change_model_button = QPushButton("更换模型", self)
        change_model_button.clicked.connect(self.changeModel)
        grid.addWidget(change_model_button, 1, 1)
        change_path_button = QPushButton("更改工作路径", self)
        change_path_button.clicked.connect(self.changePath)
        grid.addWidget(change_path_button, 1, 2)
        encrypt_allpng_button = QPushButton("加密图", self)
        encrypt_allpng_button.clicked.connect(lambda: self.encrypt_allpng(key))
        grid.addWidget(encrypt_allpng_button, 1, 3)
        decrypt_allpng_button = QPushButton("解密图", self)
        decrypt_allpng_button.clicked.connect(lambda: self.decrypt_allpng(key))
        grid.addWidget(decrypt_allpng_button, 1, 4)
        keyfnameb_button = QPushButton("选择密钥文件", self)
        keyfnameb_button.clicked.connect(self.keyfnameb_button)
        grid.addWidget(keyfnameb_button, 2, 4)
        change_save_path_button = QPushButton("更改保存位置", self)
        change_save_path_button.clicked.connect(self.change_save_path_button)
        grid.addWidget(change_save_path_button, 1, 5)
    def keyfnameb_button(self):
        keyfname, _ = QFileDialog.getOpenFileName(self, "选择密钥文件")
        if keyfname:
            global key
            with open(keyfname, "rb") as f:  # 打开key.txt文件
                key = f.read()  # 读取文件内容

    
        pass
    def startProcessing(self):
        files = os.listdir(folder_path)
        image_files = [file for file in files if file.endswith(
            (".jpg", ".jpeg", ".png"))]
        # image_files.sort(key=lambda x: os.path.getmtime(
        #     os.path.join(folder_path, x)))
        self.process_images(image_files, folder_path)
    def changeModel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择模型文件", "", "Model Files (*.pt)")
        if file_path:
            global model
            model_path = os.path.abspath(file_path)
            model = YOLO(model_path)
    # 导入 os, cryptography.fernet 和 PyQt5.QtWidgets 模块
    # 定义一个函数，接受密钥，对用户选择的文件夹下的所有图片内容进行加密
    def change_save_path_button(self):
        global SAVE_picPATH
        SAVE_picPATH = QFileDialog.getExistingDirectory()
    def changePath(self):
        global folder_path
        folder_path = QFileDialog.getExistingDirectory(self, "选择将要处理的文件夹", "")
    def calculate_md5(self, file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
        md5_hash = hashlib.md5()
        md5_hash.update(content)
        md5_value = md5_hash.hexdigest()
        return md5_value
    def process_images(self, image_files, folder_path):
        now = datetime.datetime.now()
        coun = 1
        conn = sqlite3.connect('image_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                md5 TEXT,
                filepath TEXT,
                created_at TEXT,
                updated_at TEXT,
                labels TEXT
            )
        ''')
        conn.commit()
        for file in image_files:
            filename = os.path.join(folder_path, file)
            filename = os.path.normpath(filename)
            cursor.execute(
                'SELECT md5 FROM images WHERE filepath = ?', (filename,))
            result = cursor.fetchone()
            if result is None:
                im1 = Image.open(filename)
                results = model.predict(source=im1)
                res_plotted = results[0].plot(
                    line_width=5, conf=True, boxes=True, labels=False, pil=True)
                boxes = results[0].boxes
                names = model.names
                sums = {}
                counts = {}
                for box in boxes:
                    cls = box.cls.item()
                    conf = box.conf.item()
                    if cls not in sums:
                        sums[cls] = 0
                        counts[cls] = 0
                    sums[cls] += conf
                    counts[cls] += 1
                for cls in sums:
                    average = sums[cls] / counts[cls]
                img = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                fig = plt.figure()
                plt.imshow(img)
                label_text = ''
                for namee, countt in counts.items():
                    label_text += f"{names[namee]}已识别:{countt} A_conf: {average:.3f} "
                plt.rcParams['font.sans-serif'] = ['SimHei']
                title_text = f"{label_text}"
                date_time = now.strftime("%Y-%m-%d___%H-%M-%S-") + str(coun)
                plt.title(title_text, fontsize=14, fontweight='bold')
                plt.figtext(0.5, 0.05, date_time, color='black', fontsize=10,
                            fontweight='bold', ha='center', va='center')
                save_fn = "BD_" + date_time + ".png"
                fig.savefig(os.path.join(SAVE_picPATH, save_fn))
                print("成功选择图片：", filename, "保存的文件:", save_fn)
                coun += 1
                md5 = self.calculate_md5(filename)
                cursor.execute('''
                    INSERT INTO images (md5, filepath, created_at, updated_at, labels)
                    VALUES (?, ?, ?, ?, ?)
                ''', (md5, filename, date_time, date_time, label_text))
                conn.commit()
                pixmap=QPixmap(filename)
                pixmap = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
                self.image_frame2.setPixmap(pixmap)
                self.image_frame2.update()  # 添加这一行
                pixmap=QPixmap(os.path.join(SAVE_picPATH, save_fn))
                pixmap = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
                self.image_frame1.setPixmap(pixmap)
                self.image_frame1.update()  # 添加这一行
                QTimer.singleShot(2000, lambda: None)
                QApplication.processEvents()  # 添加这一行
                plt.close()
            else:
                print("未选择图片")
        cursor.close()
        conn.close()
        print("\n")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    conn = sqlite3.connect('image_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM images')
    conn.commit()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
