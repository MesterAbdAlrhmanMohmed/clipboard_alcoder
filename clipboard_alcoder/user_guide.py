from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
class dialog(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("دليل المستخدم")
        self.الدليل=qt.QListWidget()
        self.الدليل.addItem("CTRL+C. نسخ العنصر")
        self.الدليل.addItem("CTRL+D. حذف العنصر")                
        self.الدليل.addItem("CTRL+F. إضافى العنصر الى المفضلة")
        self.الدليل.addItem("CTRL+shift+Z. إخفاء وإظهار البرنامج")
        l=qt.QVBoxLayout(self)
        l.addWidget(self.الدليل)                