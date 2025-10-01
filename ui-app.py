from sys import exec_prefix

from PyQt5 import QtWidgets, uic
import math
import sys

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        #super(QtWidgets.QMainWindow, self).__init__()
        super().__init__()
        uic.loadUi('ui/calculator.ui', self)

        self.block_digits = False
        self.block_operators = True

        # Добавление события на кнопки-цифры
        self.digit_buttons = [
            self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4,
            self.btn_5, self.btn_6, self.btn_7, self.btn_8, self.btn_9
        ]
        for button in self.digit_buttons:
            button.clicked.connect(self._on_digit_btn_clicked)

        # Операции
        self.btn_plus.clicked.connect(self._on_button_plus_clicked)
        self.btn_minus.clicked.connect(self._on_button_minus_clicked)
        self.btn_multiply.clicked.connect(self._on_button_multiply_clicked)
        self.btn_divide.clicked.connect(self._on_button_divide_clicked)
        self.btn_sqrt.clicked.connect(self._on_button_sqrt_clicked)
        # Группы
        self.btn_start_group.clicked.connect(self._on_start_group_clicked)
        self.btn_close_group.clicked.connect(self._on_close_group_clicked)
        # Функциональные кнопки
        self.btn_exec.clicked.connect(self._on_exec_clicked)
        self.btn_clear.clicked.connect(self._on_button_clear_clicked)

    def _on_digit_btn_clicked(self):
        clicked_btn = self.sender()
        digit_value = clicked_btn.objectName().split('_')[1]

        if self.block_operators:
           self.block_operators = False

        if digit_value == '0':
            if self.textEdit.toPlainText() == '' or not self.textEdit.toPlainText()[-1].isdigit():
                self.textEdit.setPlainText(self.textEdit.toPlainText() + digit_value)
                self.block_digits = True
            else:
                self.textEdit.setPlainText(self.textEdit.toPlainText() + digit_value)

        else:
            if not self.block_digits:
                self.textEdit.setPlainText(self.textEdit.toPlainText() + digit_value)
            else:
                self.textEdit.setPlainText(self.textEdit.toPlainText() + ',' + digit_value)
                self.block_digits = False

    def _on_button_plus_clicked(self):
        if not self.block_operators:
            self.textEdit.setPlainText(self.textEdit.toPlainText() + '+')
            self.block_operators = True
            self.block_digits = False

    def _on_button_minus_clicked(self):
        self.textEdit.setPlainText(self.textEdit.toPlainText() + '-')
        self.block_operators = True
        self.block_digits = False


    def _on_button_multiply_clicked(self):
        if not self.block_operators:
            self.textEdit.setPlainText(self.textEdit.toPlainText() + '×')
            self.block_operators = True
            self.block_digits = False

    def _on_button_divide_clicked(self):
        if not self.block_operators:
            self.textEdit.setPlainText(self.textEdit.toPlainText() + '÷')
            self.block_operators = True
            self.block_digits = False

    def _on_button_sqrt_clicked(self):
        self.textEdit.setPlainText(self.textEdit.toPlainText() + '√(')
        self.block_operators = True

    def _on_start_group_clicked(self):
        if self.textEdit.toPlainText()[-1].isdigit():
            self.textEdit.setPlainText(self.textEdit.toPlainText() + '×(')
        else:
            self.textEdit.setPlainText(self.textEdit.toPlainText() + '(')
    def _on_close_group_clicked(self):
        self.textEdit.setPlainText(self.textEdit.toPlainText() + ')')

    def _on_exec_clicked(self):
        if not self.block_operators:
            str_data = self.textEdit.toPlainText()
            if '\n' in str_data:
                expression = str_data.split('\n')[-1]
            else:
                expression = str_data
            expression = expression.replace(',', '.')
            expression = expression.replace('×', '*')
            expression = expression.replace('÷', '/')
            expression = expression.replace('√', 'math.sqrt')
            result = eval(expression)
            result = round(result, 4)
            if result == int(result):
                result = int(result)
            stroke_result = str(result).replace('.', ',')
            self.textEdit.setPlainText(self.textEdit.toPlainText() + '\n' + stroke_result)

    def _on_button_clear_clicked(self):
        self.textEdit.setPlainText('')








def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
