from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import os,about,user_guide
class ClipboardThread(qt2.QThread):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text=text
    def run(self):
        clipboard=qt.QApplication.clipboard()
        clipboard.setText(self.text)
class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("clipboard alcoder")
        self.clipboard_data_folder="clipboard_alcoder_data"
        os.makedirs(self.clipboard_data_folder, exist_ok=True)
        self.setup_ui()
        self.clipboard=qt.QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)        
        self.current_text=""
        self.text_to_file={}
        self.load_items_from_files()
    def setup_ui(self):
        self.إظهار_البحث=qt.QLabel("البحث")
        self.البحث=qt.QLineEdit()
        self.البحث.setAccessibleName("البحث")
        self.البحث.textChanged.connect(self.search_items)
        self.العناصر=qt.QListWidget()
        self.العناصر.setAccessibleName("عناصر الحافِظة")
        self.دليل_المستخدم=qt.QPushButton("دليل المستخدم")
        self.دليل_المستخدم.setDefault(True)
        self.دليل_المستخدم.clicked.connect(self.UserGuide)
        self.عن=qt.QPushButton("عن المطور")
        self.عن.setDefault(True)
        self.عن.clicked.connect(self.about)
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_selected_item)
        qt1.QShortcut("ctrl+d", self).activated.connect(self.delete_selected_item)
        l=qt.QVBoxLayout()
        l.addWidget(self.إظهار_البحث)
        l.addWidget(self.البحث)
        l.addWidget(self.العناصر)
        l.addWidget(self.دليل_المستخدم)
        l.addWidget(self.عن)
        w=qt.QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)
    def on_clipboard_change(self):
        text=self.clipboard.text()  # الحصول على النص من الحافظة
        if text and text != self.current_text:  # التأكد من أن النص غير فارغ ومختلف عن النص الحالي
            self.current_text = text
            if not self.is_text_in_list(text):  # التحقق مما إذا كان النص موجودًا بالفعل في القائمة
                self.add_to_list_widget(text)
                self.save_to_file(text)
    def is_text_in_list(self, text):
        for i in range(self.العناصر.count()):
            item=self.العناصر.item(i)
            if item.text() == text:
                return True
        return False
    def add_to_list_widget(self, text):
        item=qt.QListWidgetItem(text)
        self.العناصر.addItem(item)
        self.text_to_file[text] = f"clipboard_{self.العناصر.count()}.txt"
    def save_to_file(self, text):
        file_name=self.text_to_file[text]
        file_path=os.path.join(self.clipboard_data_folder, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
    def load_items_from_files(self):
        files=os.listdir(self.clipboard_data_folder)
        for file_name in files:
            file_path=os.path.join(self.clipboard_data_folder, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                text=f.read()
                self.text_to_file[text]=file_name
                self.add_to_list_widget(text)
    def copy_selected_item(self):
        current_item=self.العناصر.currentItem()
        if current_item:
            self.clipboard_thread = ClipboardThread(current_item.text())
            self.clipboard_thread.start()
    def delete_selected_item(self):
        current_row=self.العناصر.currentRow()
        if current_row != -1:
            item=self.العناصر.takeItem(current_row)
            text=item.text()
            self.delete_file(text)
            del item
            del self.text_to_file[text]
    def delete_file(self, text):
        file_name=self.text_to_file.get(text)
        if file_name:
            file_path=os.path.join(self.clipboard_data_folder, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
    def search_items(self):
        search_text=self.البحث.text().lower()
        for i in range(self.العناصر.count()):
            item=self.العناصر.item(i)
            item.setHidden(search_text not in item.text().lower())
    def about(self):
        about.dialog(self).exec()
    def UserGuide(self):
        user_guide.dialog(self).exec()
application=qt.QApplication([])
application.setStyle('fusion')
main_window=MainWindow()
main_window.show()
application.exec()