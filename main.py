import sys
import io

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QPushButton, QListWidgetItem
from PyQt5.QtWidgets import QListWidget, QWidget, QGroupBox
from PyQt5 import uic


class SimplePlanner(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("miniplan.ui", self)
        self.sc = 1

        self.centralwidgetHorizontalLayout = QHBoxLayout(self)

        self.ListWidget.setStyleSheet(
            "QListWidget { background: palette(window); border: none;}"
            "QListWidget::item {"
                "border-style: solid;" 
                "border-width:1px;" 
                "border-color:  black;"
                "margin-right: 30px;"
            "}"
            "QListWidget::item:hover {"
                "border-color: green;"
            "}")

        self.addEventBtn.clicked.connect(self.push_it)

    def push_it(self):
        if self.lineEdit.text():
            date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
            plane = self.lineEdit.text()
            time = self.timeEdit.time().toString()

            item = QListWidgetItem()
            item_widget = QWidget()
            line_text = QLabel(f'{date} {time} - {plane}')
            line_push_button = QPushButton("Погода")
            line_push_button.setObjectName(str(self.sc))
            line_push_button.clicked.connect(self.clicked)
            item_layout = QHBoxLayout()
            item_layout.addWidget(line_text)
            item_layout.addWidget(line_push_button)
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.ListWidget.addItem(item)
            self.ListWidget.setItemWidget(item, item_widget)
            self.sc += 1

            self.ListWidget.sortItems()
        else:
            print("Введите задачу.")

    def clicked(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        print(f'click: {push_button.objectName()}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimplePlanner()
    ex.show()
    sys.exit(app.exec())
