from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import os,pyperclip
class ClipboardThread(qt2.QThread):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text=text
    def run(self):
        clipboard=pyperclip
        clipboard.copy(self.text)
class dialog(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("المفضلة")
        self.parent_window=parent
        self.إظهار_البحث=qt.QLabel("البحث")
        self.البحث=qt.QLineEdit()
        self.البحث.setAccessibleName("البحث")
        self.البحث.textChanged.connect(self.search_items)
        self.العناصر_المفضلة=qt.QListWidget()
        self.العناصر_المفضلة.setAccessibleName("العناصر المفضلة")
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_selected_item)
        qt1.QShortcut("ctrl+d", self).activated.connect(self.delete_selected_item)
        l=qt.QVBoxLayout(self)
        l.addWidget(self.إظهار_البحث)
        l.addWidget(self.البحث)
        l.addWidget(self.العناصر_المفضلة)
        self.setLayout(l)
        self.load_favorite_items()
    def add_item_to_list_widget(self, text):
        item=qt.QListWidgetItem(text)
        self.العناصر_المفضلة.addItem(item)
    def search_items(self):
        search_text=self.البحث.text().lower()
        for i in range(self.العناصر_المفضلة.count()):
            item=self.العناصر_المفضلة.item(i)
            item.setHidden(search_text not in item.text().lower())
    def copy_selected_item(self):
        current_item=self.العناصر_المفضلة.currentItem()
        if current_item:
            text=current_item.text()
            self.clipboard_thread=ClipboardThread(text)
            self.clipboard_thread.start()
    def delete_selected_item(self):
        current_row=self.العناصر_المفضلة.currentRow()
        if current_row != -1:
            item=self.العناصر_المفضلة.takeItem(current_row)
            text=item.text()
            self.delete_favorite_file(text)
            del item
            if text in self.parent_window.favorite_text_to_file:
                del self.parent_window.favorite_text_to_file[text]
    def delete_favorite_file(self, text):
        file_name=self.parent_window.favorite_text_to_file.get(text)
        if file_name:
            file_path=os.path.join(self.parent_window.clipboard_favorite_folder, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
    def load_favorite_items(self):
        for text, file_name in self.parent_window.favorite_text_to_file.items():
            self.add_item_to_list_widget(text)