import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import design  # Это наш конвертированный файл дизайна


# Главный класс приложения (наследуемся от design)
class MainApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.buttonClicked)  # соединяем кнопку и функцию buttonClicked
        self.tableWidget.setHorizontalHeaderLabels(["1", "2", "3", "4", "5"])  # загаловки строчек таблицы
        self.tableWidget.setVerticalHeaderLabels(["1", "2", "3", "4", "5"])  # заголовки столбцов таблицы
        self.tableWidget.setColumnCount(5)  # кол-во столбцов
        self.tableWidget.setRowCount(5)  # кол-во строчек
        # abc - алфавит
        self.abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p',
                    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        # заполняем таблицу нашим алфавитом
        self.update_table(self.abc)

    # функция заполняет таблицу контентом
    def update_table(self, content):
        table = self.tableWidget
        table.setColumnCount(5)
        table.setRowCount(5)
        # подгоняем размер ячеек под содержимое
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        # заполняем ячейки
        # i - номер строки (с 0)
        # j - номер столбца (с 0)
        # QTableWidgetItem - преобразует строку в ячейку таблицы
        # 5*i+j - получаем порядок элемента в массиве по его координатам
        for i in range(5):
            for j in range(5):
                table.setItem(i, j, QTableWidgetItem(content[5 * i + j]))

    # функция убирает повторяющиеся буквы в строке
    def remove_replays(self, text):
        result = []
        for c in text:
            if c not in result:
                result.append(c)
        # result - список, поэтому его нужно перевести в строку
        # "".join() - переводит список в строку, где "" - символ, который заполняется между элементами списка
        result = "".join(result)
        return result

    # функция находит символ "c" в списке "abc", и возвращает его координаты i и j
    def find_char(self, abc, c):
        # x = 5*i + j - формула нахождения номера символа в строке, зная его координаты
        # j = x - 5*i - как найти j, зная i и x
        x = abc.index(c) # находим порядковый номер символа в строке
        i = x // 5
        j = x - 5 * i
        return [i, j]    # возвращаем массив из координат и порядкового номера

    # функция, которая вызывается при нажатии на кнопку
    def buttonClicked(self):
        # self.result - наше поле, куда мы выводим результат, а метод clear() его отчищает
        self.result.clear()
        # получаем с текстовых полей ключ и текст
        key = self.lineEdit.text()
        text = self.lineEdit_2.text()
        # если текст пустой, по пишем ошибку, и выходим из функции
        if text == "":
            QtWidgets.QMessageBox.critical(None, "Error", "Text is empty!")
            return
        # делаем все заглавные буквы в тексте и ключе строчными
        text, key = text.lower(), key.lower()
        # заменяем все j на i
        text, key = text.replace("j", "i"), key.replace("j", "i")
        # удаляем повторные символы в ключе
        key = self.remove_replays(key)
        # формруем новый алфавит
        new_abc = self.abc
        # добабвляем в начало наш ключ (он в виде строки, мы его преобразуем в список с помощью split)
        new_abc = key.split() + new_abc
        # удаляем повторные символы, т.к. функция принимает текст, то мы преобразуем список new_abc в текст
        new_abc = self.remove_replays("".join(new_abc))
        # функция remove_replays вернула нам строку, нам её нужно преобразовать обратно в текст
        new_abc.split()
        # заносим наш новый алфавит в табличку
        self.update_table(new_abc)
        # result - новый пустой список, в который мы потом будет заносить результат кодирования
        result = []
        # циклом for проходимся по всем символам в тексте, "c" - символ, от англ. слова char
        for c in text:
            if c == " ":                            # Если наш символ - пробел
                self.result.append("\n")            # В наше поле с результатом делаем отступ (новую строку)
                result.append(" ")                  # Добавляем пробел в список с результатом
                continue                            # переходим ко следующей итерации (к следующему символу)
            # находим координаты символа, el - массив
            # el[0] - i
            # el[1] - j
            # el[2] - x
            # x - порядок символа в алфавите
            el = self.find_char(new_abc, c)
            # если номер строки - последний, то делаем её = -1, чтобы потом добавить 1 и получить 0
            if el[0] == 4:
                el[0] = -1
            # находим по таблице новый символ, который лежит на следующей строке того же столбца
            new_c = self.tableWidget.item(el[0] + 1, el[1]).text()
            # добавляем в список result новый символ
            result.append(new_c)
            # добавляем в текстовое поле с результатом такую вещь: [c] -> [new_c]
            self.result.append("[{}] -> [{}]".format(c, new_c))
        # добавляем в текстовое поле наш результат
        self.result.append("".join(result))


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainApp()  # Создаём объект класса MainApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
