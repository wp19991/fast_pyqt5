from PyQt5.QtWidgets import QMainWindow
from ui.main_window import Ui_MainWindow as main_window
from win.search_widget import search_widget


class main_win(QMainWindow, main_window):
    def __init__(self):
        super(main_win, self).__init__()
        self.setupUi(self)

        self.search_widget = search_widget(self)
        self.main_layout.addWidget(self.search_widget)
        self.search_widget.show()







