import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, \
    QVBoxLayout, QGridLayout, QLabel, QLineEdit, QFormLayout, QCheckBox, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt
from file_browser import FileBrowser
import config_reader
import rlog, time
from Settings import MSettings
import Settings
import csv

__version__ = '0.1'

# Number of months in year
NUM_MONTHS = 9

# Number of weeks in a month
NUM_WEEKS = 4

# Number of days in a week
NUM_DAYS = 7

# Every 9th year, there is a leap day after Day 2
LEAP_DAY_CYCLE = 9

class MaeveUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Variables to track which windows are open
        self.settings_open = False
        self.Maeve_open = False
        rlog.createlog()
        # Setting window color based on theme from settings
        self.setBaseSize(400, 300)
        self.setStyleSheet(Settings.get_theme('background_color'))
        self.setWindowTitle('Date Me')
        # Central widget and general layout of window
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # List of windows created
        self.dialogs = list()
        # Display and buttons
        self._createButtons()

    def _createButtons(self):
        '''
        Input - path where you want csv location
        Input - year
        Output - date list in csv format to desired location
        '''

        buttonsLayout = QFormLayout()
        self.csvPath = FileBrowser(FileBrowser.OpenDirectory)
        self.csvPath.setStyleSheet("open_item_color")
        self.year = QLineEdit()
        self.year.setStyleSheet("open_item_color")

        settingsButton = QPushButton("Settings")
        settingsButton.setStyleSheet(Settings.get_theme("button_color"))
        settingsButton.setFixedSize(200, 40)
        generate = QPushButton("Generate")
        generate.setStyleSheet(Settings.get_theme("button_color"))
        generate.setFixedSize(200, 40)

        yearL = QLabel("Year: ")
        yearL.setStyleSheet(Settings.get_theme("text_color"))
        csvPathL = QLabel("Path: ")
        csvPathL.setStyleSheet(Settings.get_theme("text_color"))

        self.csvPath.setStyleSheet(Settings.get_theme("open_item_color"))

        buttonsLayout.addRow("", settingsButton)
        buttonsLayout.addRow(yearL, self.year)
        buttonsLayout.addRow(csvPathL, self.csvPath)
        buttonsLayout.addRow("", generate)
        # buttonsLayout.setLabelAlignment(Qt.AlignCenter)

        self.generalLayout.addLayout(buttonsLayout)
        settingsButton.clicked.connect(self.settings_clicked)
        generate.clicked.connect(self.generate_clicked)

    def settings_clicked(self):
        if self.settings_open:
            rlog.writelog("You clicked Settings when it was already open")
        else:
            self.settings_dialog = MSettings()
            self.dialogs.append(self.settings_dialog)
            self.settings_dialog.location_on_the_screen()
            self.settings_dialog.show()
            self.settings_open = True
            self.settings_dialog.theme_changed.connect(self.reload_windows)
            self.settings_dialog.window_closed.connect(self.settings_closed)

    def generate_clicked(self):
        print("creating CSV for the year " + str(self.year.text()))
        path = ''
        for y in self.csvPath.getPaths():
            path = y
        filename = path + "/" + str(self.year.text()) + ".csv"
        data = self.create_dates()
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for x in data:
                writer.writerow([str(x)])

    def create_dates(self):
        dates = []
        y = str(self.year.text())
        dates.append("D1" + '.' + y)
        for month in range(1, NUM_MONTHS + 1):
            if month == 3:
                dates.append("D2" + '.' + y)
                if int(int(y)/9) == int(y)/9:
                    dates.append(str("Leap." + y))
            if month == 6:
                dates.append("3" + '.' + y)
            for week in range(1, NUM_WEEKS + 1):
                for day in range(1, NUM_DAYS + 1):
                    temp = str(day) + '.' + str(week) + '.' + str(month) + '.' + y
                    dates.append(temp)
        return dates

    def settings_closed(self):
        self.settings_open = False

    def closeEvent(self, event):
        # recording settings in config
        m = ''
        for y in self.csvPath.getPaths():
            m = y
        if len(self.csvPath.getPaths()) != 0:
            config_reader.setXML('path', str(m))
        else:
            config_reader.setXML('path', '[]')

        for window in QApplication.topLevelWidgets():
            window.close()

    def reload_windows(self):
        if self.settings_open:
            self.settings_dialog.close()
            self.settings_open = False
            self.settings_clicked()
        if self.Maeve_open:
            d = self._centralWidget.children()
            e = reversed(d)

            for g in e:
                g.deleteLater()
            self.setStyleSheet(Settings.get_theme('background_color'))
            self.setWindowTitle('Date Me')
            # Central widget and general layout of window
            self.generalLayout = QVBoxLayout()
            self._centralWidget = QWidget(self)
            self.setCentralWidget(self._centralWidget)
            self._centralWidget.setLayout(self.generalLayout)
            self.dialogs = list()
            # Display and buttons
            self._createButtons()

def main():
    maeve = QApplication(sys.argv)
    maeve.setStyle("Fusion")
    view = MaeveUI()
    view.show()
    view.Maeve_open = True
    sys.exit(maeve.exec_())

if __name__ == '__main__':
    main()