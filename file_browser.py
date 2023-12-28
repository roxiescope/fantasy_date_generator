from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import Settings
import config_reader
import rlog
import sys


class FileBrowser(QWidget):
    OpenFile = 0
    OpenFiles = 1
    OpenDirectory = 2
    SaveFile = 3

    def __init__(self, mode=OpenFile):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.browser_mode = mode
        self.filter_name = 'All files (*.*)'
        self.dirpath = QDir.currentPath()
        self.filepaths = []
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(280)
        self.lineEdit.setText(str(config_reader.getXML('path')))
        self.filepaths.append(str(config_reader.getXML('path')))

        layout.addWidget(self.lineEdit)

        self.button = QPushButton('Search')
        self.button.clicked.connect(self.getFile)
        layout.addWidget(self.button)
        layout.addStretch()

    def getFile(self):
        if self.browser_mode == FileBrowser.OpenFile:
            self.filepaths.append(QFileDialog.getOpenFileName(self, caption='Choose File',
                                                              directory=self.dirpath,
                                                              filter=self.filter_name)[0])
        elif self.browser_mode == FileBrowser.OpenFiles:
            self.filepaths.extend(QFileDialog.getOpenFileNames(self, caption='Choose Files',
                                                               directory=self.dirpath,
                                                               filter=self.filter_name)[0])
        elif self.browser_mode == FileBrowser.OpenDirectory:
            self.filepaths.append(QFileDialog.getExistingDirectory(self, caption='Choose Directory',
                                                                   directory=self.dirpath))
        else:
            options = QFileDialog.Options()
            if sys.platform == 'darwin':
                options |= QFileDialog.DontUseNativeDialog
            self.filepaths.append(QFileDialog.getSaveFileName(self, caption='Save/Save As',
                                                              directory=self.dirpath,
                                                              filter=self.filter_name,
                                                              options=options)[0])
        if len(self.filepaths) == 0:
            return
        else:
            for x in range(len(self.filepaths)):
                self.lineEdit.setText(self.filepaths[x])
        # else:
        #     self.lineEdit.setText(",".join(self.filepaths))


    def getPaths(self):
        return self.filepaths
