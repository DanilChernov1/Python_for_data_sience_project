import os
import random
import shutil
import sys
from datetime import date

import apimoex
import pandas as pd
import requests
import seaborn as sns
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt

sns.set(rc={'figure.figsize': (12, 6)})
list_of_companies = list(
    pd.DataFrame(apimoex.get_board_securities(session=requests.Session(), table='securities')).SECID)
years = ['2011', '2012',
         '2013', '2014',
         '2015', '2016',
         '2017', '2018',
         '2019', '2020',
         '2021', '2022']


def request(name_of_company, first_date, second_date):  # Запрос по определенной компании
    return pd.DataFrame(apimoex.get_market_history(session=requests.Session(), security=name_of_company, columns=None,
                                                   start=first_date, end=second_date))


def download(dataframe, name):  # скачивание акции по дате
    dataframe.TRADEDATE = dataframe.TRADEDATE.apply(lambda x: x[:7])
    dates = pd.DataFrame(dataframe.TRADEDATE.value_counts()).reset_index().rename(columns={'index': 'dates'}).dates
    dates = list(dates)
    dates.sort()
    month_dates = []
    for i in dates:
        i += '-01'
        month_dates.append(i)
        if i.endswith('02-01'):
            i = i[:7] + '-28'
        else:
            i = i[:7] + '-30'
        month_dates.append(i)
    for i in range(0, len(month_dates), 2):
        df = pd.DataFrame(
            apimoex.get_market_history(session=requests.Session(), security=name, columns=None, start=month_dates[i],
                                       end=month_dates[i + 1]))
        if df.empty:
            pass
        else:
            year = month_dates[i][:4]
            if not os.path.exists('Archive_of_Accounting/{}/{}'.format(year, name)):
                os.mkdir('Archive_of_Accounting/{}/{}'.format(year, name))
                if not os.path.exists('Archive_of_Accounting/{}/{}/{}.csv'.format(year, name, month_dates[i])):
                    df.to_csv(path_or_buf='Archive_of_Accounting/{}/{}/{}.csv'.format(year, name, month_dates[i]))
                else:
                    pass
            else:
                if not os.path.exists('Archive_of_Accounting/{}/{}/{}.csv'.format(year, name, month_dates[i])):
                    df.to_csv(path_or_buf='Archive_of_Accounting/{}/{}/{}.csv'.format(year, name, month_dates[i]))
                else:
                    pass


def graphic(df, first, second, comboboxvalue):
    if comboboxvalue == "Lineplot":

        founding_time = (pd.to_datetime(second) - pd.to_datetime(first))
        if founding_time.days <= 30:
            df = df.groupby(['TRADEDATE', 'BOARDID'], as_index=False) \
                .agg({'CLOSE': 'mean'}) \
                .rename(columns={'CLOSE': 'MEAN_CLOSE_PRICE'})
            fig = plt.figure()
            fig.patch.set_facecolor('none')
            fig.patch.set_alpha(0.6)
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor('orange')
            ax.patch.set_alpha(1.0)
            sns.lineplot(data=df, x=df.TRADEDATE, y=df.MEAN_CLOSE_PRICE, hue=df.BOARDID) \
                .set(title='\nCost of stocks')
            plt.xticks(rotation=25)
            if not os.path.exists('Graphs'):
                os.mkdir('Graphs')
            plt.tight_layout()
            plt.savefig('Graphs/graphics.png')
        elif 30 < founding_time.days < 1000:
            df.TRADEDATE = df.TRADEDATE.apply(lambda x: x[:7])
            df = df.groupby(['TRADEDATE', 'BOARDID'], as_index=False) \
                .agg({'CLOSE': 'mean'}) \
                .rename(columns={'CLOSE': 'MEAN_CLOSE_PRICE'})
            fig = plt.figure()
            fig.patch.set_facecolor('none')
            fig.patch.set_alpha(0.6)
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor('orange')
            ax.patch.set_alpha(1.0)
            sns.lineplot(data=df, x=df.TRADEDATE, y=df.MEAN_CLOSE_PRICE, hue=df.BOARDID) \
                .set(title='\nCost of stocks')
            plt.xticks(rotation=45)
            if not os.path.exists('Graphs'):
                os.mkdir('Graphs')
            plt.tight_layout()
            plt.savefig('Graphs/graphics.png')
        else:
            df.TRADEDATE = df.TRADEDATE.apply(lambda x: x[:4])
            df = df.groupby(['TRADEDATE', 'BOARDID'], as_index=False) \
                .agg({'CLOSE': 'mean'}) \
                .rename(columns={'CLOSE': 'MEAN_CLOSE_PRICE'})
            fig = plt.figure()
            fig.patch.set_facecolor('none')
            fig.patch.set_alpha(0.6)
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor('orange')
            ax.patch.set_alpha(1.0)
            sns.lineplot(data=df, x=df.TRADEDATE, y=df.MEAN_CLOSE_PRICE, hue=df.BOARDID) \
                .set(title='\nCost of stocks')
            plt.xticks(rotation=45)
            if not os.path.exists('Graphs'):
                os.mkdir('Graphs')
            plt.tight_layout()
            plt.savefig('Graphs/graphics.png')
    else:
        founding_time = (pd.to_datetime(second) - pd.to_datetime(first))
        if founding_time.days <= 30:
            df = df.groupby(['TRADEDATE', 'BOARDID'], as_index=False) \
                .agg({'CLOSE': 'mean'}) \
                .rename(columns={'CLOSE': 'MEAN_CLOSE_PRICE'})
            fig = plt.figure()
            fig.patch.set_facecolor('none')
            fig.patch.set_alpha(0.6)
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor('orange')
            ax.patch.set_alpha(1.0)
            sns.barplot(data=df, x=df.TRADEDATE, y=df.MEAN_CLOSE_PRICE, hue=df.BOARDID) \
                .set(title='\nCost of stocks')
            plt.xticks(rotation=25)
            if not os.path.exists('Graphs'):
                os.mkdir('Graphs')
            plt.tight_layout()
            plt.savefig('Graphs/graphics.png')
        elif 30 < founding_time.days < 1000:
            df.TRADEDATE = df.TRADEDATE.apply(lambda x: x[:7])
            df = df.groupby(['TRADEDATE', 'BOARDID'], as_index=False) \
                .agg({'CLOSE': 'mean'}) \
                .rename(columns={'CLOSE': 'MEAN_CLOSE_PRICE'})
            fig = plt.figure()
            fig.patch.set_facecolor('none')
            fig.patch.set_alpha(0.6)
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor('orange')
            ax.patch.set_alpha(1.0)
            sns.barplot(data=df, x=df.TRADEDATE, y=df.MEAN_CLOSE_PRICE, hue=df.BOARDID) \
                .set(title='\nCost of stocks')
            plt.xticks(rotation=45)
            if not os.path.exists('Graphs'):
                os.mkdir('Graphs')
            plt.tight_layout()
            plt.savefig('Graphs/graphics.png')
        else:
            df.TRADEDATE = df.TRADEDATE.apply(lambda x: x[:4])
            df = df.groupby(['TRADEDATE', 'BOARDID'], as_index=False) \
                .agg({'CLOSE': 'mean'}) \
                .rename(columns={'CLOSE': 'MEAN_CLOSE_PRICE'})
            fig = plt.figure()
            fig.patch.set_facecolor('none')
            fig.patch.set_alpha(0.6)
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor('orange')
            ax.patch.set_alpha(1.0)
            sns.barplot(data=df, x=df.TRADEDATE, y=df.MEAN_CLOSE_PRICE, hue=df.BOARDID) \
                .set(title='\nCost of stocks')
            plt.xticks(rotation=45)
            if not os.path.exists('Graphs'):
                os.mkdir('Graphs')
            plt.tight_layout()
            plt.savefig('Graphs/graphics.png')


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Sem Python in Data Science")
        self.setWindowIcon(QtGui.QIcon("2.jpg"))
        self.pixmap = None
        self.name_of_company = ''
        self.three_company = None
        self.company = None
        self.name_of_company = None
        self.second_date = None
        self.first_date = None
        self.setObjectName("MainWindow")
        self.resize(850, 750)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("#centralwidget {background-image: url(1.jpg);}")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 20, 261, 81))

        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "background-color: rgb(255, 100, 0);\n "
                                      "border-radius: 16px;\n"
                                      "font: 16pt \"MS Shell Dlg 2\";"
                                      "font-weight: 700;\n")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(260, 150, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(80, 70, 111, 41))
        self.dateEdit.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(255, 100, 0);\n "
                                    "border-radius: 16px;\n"
                                    "font: 12pt \"MS Shell Dlg 2\";")
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.dateEdit.setFont(font)
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2014, 9, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2012, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setMaximumDate(QtCore.QDate(2022, 12, 31))
        self.dateEdit.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.dateEdit.setCalendarPopup(False)
        self.dateEdit.setObjectName("dateEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 120, 221, 21))
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.label.setStyleSheet("font: 16pt \n;")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 40, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(80, 160, 111, 41))
        self.dateEdit_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "background-color: rgb(255, 100, 0);\n "
                                      "border-radius: 16px;\n"
                                      "font: 12pt \"MS Shell Dlg 2\";")
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.dateEdit_2.setFont(font)
        self.dateEdit_2.setDateTime(QtCore.QDateTime(QtCore.QDate(2014, 9, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_2.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2012, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_2.setMaximumDate(QtCore.QDate(2022, 12, 31))
        self.dateEdit_2.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.dateEdit_2.setCalendarPopup(False)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 130, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.graph = QtWidgets.QLabel(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(10, 290, 781, 241))
        self.graph.setText("")
        self.graph.setObjectName("graph")
        self.terminal = QtWidgets.QTextBrowser(self.centralwidget)
        self.terminal.setGeometry(QtCore.QRect(250, 220, 261, 61))
        self.terminal.setUndoRedoEnabled(True)
        self.terminal.setObjectName("terminal")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(260, 190, 241, 31))
        self.label_4.setStyleSheet("font: 16pt \n;"
                                   "font-weight: 700;\n")
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(620, 20, 161, 81))
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(255, 100, 0);\n "
                                        "border-radius: 16px;\n"
                                        "font: 12pt \"MS Shell Dlg 2\";")
        self.all_time = QtWidgets.QCheckBox(self.centralwidget)
        self.all_time.setGeometry(QtCore.QRect(610, 140, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.all_time.setFont(font)
        self.all_time.setObjectName("all_time")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(610, 170, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(590, 210, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(255, 100, 0);\n"
                                        "font-weight: 700;\n"
                                        "font: 10pt;")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(590, 250, 181, 31))
        self.pushButton_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(255, 100, 0);\n"
                                        "font-weight: 700;\n"
                                        "font: 10pt;")
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.filedialog = QtWidgets.QComboBox(self.centralwidget)
        self.filedialog.setGeometry(80, 240, 110, 40)
        self.filedialog.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "background-color: rgb(255, 100, 0);\n "
                                      "border-radius: 16px;\n"
                                      "font: 12pt \"MS Shell Dlg 2\";")
        self.filedialog.addItems(["Lineplot", "Barplot"])

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("MainWindow", "Загрузить данные"))
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "yyyy-MM"))
        self.label.setText(_translate("MainWindow", "Введите название ID акции"))
        self.label_2.setText(_translate("MainWindow", "первая дата"))
        self.dateEdit_2.setDisplayFormat(_translate("MainWindow", "yyyy-MM"))
        self.label_3.setText(_translate("MainWindow", "вторая дата"))
        self.label_4.setText(_translate("MainWindow", "Результат"))
        self.pushButton_2.setText(_translate("MainWindow", "Показать\n"
                                                           " 3 случайных ID"))
        self.all_time.setText(_translate("MainWindow", "За всё время"))
        self.checkBox.setText(_translate("MainWindow", "Все акции"))
        self.pushButton_3.setText(_translate("MainWindow", "Создать папку с файлами"))
        self.pushButton_4.setText(_translate("MainWindow", "Конвертировать в ZIP"))

        self.pushButton.clicked.connect(self.logic)
        self.all_time.clicked.connect(self.is_all_date)
        self.pushButton_2.clicked.connect(self.show_3_random)
        self.pushButton_3.clicked.connect(self.creating_folders)
        self.pushButton_4.clicked.connect(self.to_zip)

    def logic(self):  # логика программы
        self.first_date = self.dateEdit.dateTime().toString('yyyy-MM-dd')
        self.second_date = self.dateEdit_2.dateTime().toString('yyyy-MM-dd')
        self.name_of_company = self.textEdit.toPlainText().upper()
        if not os.path.exists('Archive_of_Accounting'):
            self.terminal.setText('Сначала создайте архив')
            return 0
        if self.name_of_company == '' and not self.checkBox.isChecked():
            self.terminal.setText("Ничего не введено")
        elif self.all_time.isChecked() and not self.checkBox.isChecked():

            self.company = request(self.name_of_company, first_date='2011-01-01', second_date='2022-12-31')
            if self.company.empty:
                self.terminal.setText('Данной акции не существует')
            else:
                download(self.company, self.name_of_company)
                graphic(self.company, '2011-01-01', '2022-12-31', self.filedialog.currentText())
                self.pixmap = QtGui.QPixmap("Graphs/graphics.png")
                self.pixmap = self.pixmap.scaled(720, 405, QtCore.Qt.KeepAspectRatio)
                self.graph.resize(self.pixmap.width(), self.pixmap.height())
                self.graph.setPixmap(self.pixmap)
                self.terminal.setText('Скачивание завершено!')
        elif (self.all_time.isChecked() or not self.all_time.isChecked()) and self.checkBox.isChecked():
            self.download_all()
        else:
            if self.first_date >= self.second_date:
                self.terminal.setText('Первая дата больше второй, следует исправить')
            else:
                self.company = request(self.name_of_company, self.first_date, self.second_date)
                if self.company.empty:
                    self.terminal.setText('Данной акции не существует')
                else:
                    self.company = self.company.query(
                        f'TRADEDATE >= "{self.first_date}" and TRADEDATE <= "{self.second_date}"')
                    if self.company.shape[0] == 0:
                        self.terminal.setText('Данных нет :(')
                    else:
                        self.company = request(self.name_of_company, self.first_date, self.second_date)
                        graphic(self.company, self.first_date, self.second_date, self.filedialog.currentText())
                        download(self.company, self.name_of_company)
                        # graphic(self.company)
                        self.pixmap = QtGui.QPixmap("Graphs/graphics.png")
                        self.pixmap = self.pixmap.scaled(830, 500, QtCore.Qt.KeepAspectRatio)
                        self.graph.resize(self.pixmap.width(), self.pixmap.height())
                        self.graph.setPixmap(self.pixmap)
                        self.terminal.setText('Скачивание завершено!')

    def is_all_date(self):  # переключение даты
        if self.all_time.isChecked():
            self.dateEdit.setEnabled(False)
            self.dateEdit_2.setEnabled(False)
        else:
            self.dateEdit.setEnabled(True)
            self.dateEdit_2.setEnabled(True)

    def download_all(self):  # вспомогательная функция
        if self.all_time.isChecked():
            for name in list_of_companies:
                self.company = request(name, first_date='2011-01-01', second_date='2022-12-31')
                if self.company.empty:
                    pass
                else:
                    download(self.company, name)
        else:
            for name in list_of_companies:
                self.company = request(name, self.first_date, self.second_date)
                if self.company.empty:
                    pass
                else:
                    download(self.company, name)
        self.terminal.setText('Скачивание завершено!')

    def creating_folders(self):  # создание архива
        if not os.path.exists('Archive_of_Accounting'):
            os.mkdir('Archive_of_Accounting')
        for year in years:
            if not os.path.exists('Archive_of_Accounting/{}'.format(year)):
                os.mkdir('Archive_of_Accounting/{}'.format(year))
        self.terminal.setText('Архив создан!')

    def show_3_random(self):
        self.three_company = []
        for company in range(0, 3):
            company = random.choice(list_of_companies)
            self.three_company.append(company)
        self.three_company = str(self.three_company).replace("[", '') \
            .replace("]", '') \
            .replace("'", '') \
            .replace(',', '') \
            .replace(' ', '\n')
        self.terminal.setText(self.three_company)

    def to_zip(self):
        if not os.path.exists('Archive_of_Accounting'):
            self.terminal.setText('Сначала создайте архив')
        else:
            shutil.make_archive('Archive_of_Accounting {} '.format(date.today()), 'zip', 'Archive_of_Accounting')


def Application():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("App.jpg"))
    window = Window()

    window.show()
    sys.exit(app.exec_())
