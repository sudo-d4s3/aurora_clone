from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QListWidgetItem
from bs4 import BeautifulSoup as bs
from aurora_clone_frontend import Ui_MainWindow
import sys, re


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #hide popout character panel
        self.ui.newchar_frame.hide()

        #hide subraces
        self.ui.subrace_label_listWidget.hide()
        self.ui.subrace_listWidget.hide()

        #new character button
        self.ui.newchar_button.clicked.connect(self.newchar_panel_logic)
        
        #add races to listwidget items
        with open('sources/players-handbook.index', 'r') as file:
            content = file.readlines()
            content = "".join(content)
            bs_content = bs(content, 'lxml')
            result = bs_content.find_all("file", {'name': re.compile('race-.*?\.xml')})
            for x in range(len(result)):
                output = re.split('"', str(result[x]))
                outstr = output[1]
                QListWidgetItem(outstr[5:-4], self.ui.race_listWidget)
        
        #select a race in listwidget
        self.ui.race_listWidget.itemClicked.connect(self.raceClicked_event)
        self.ui.race_listWidget.itemActivated.connect(self.raceDoubleClicked_event)
        global has_race_been_clicked
        has_race_been_clicked = True

        #select a subrace in listwidget
        self.ui.subrace_listWidget.itemClicked.connect(self.subraceClicked_event)
        

    def newchar_panel_logic(self):
        self.ui.newchar_button.hide()
        self.ui.newchar_frame.show()

    def raceClicked_event(self, item):
        with open('sources/players-handbook/races/race-' + str(item.text()) + '.xml', 'r') as file:
            content = file.readlines()
            content = "".join(content)
            bs_content = bs(content, 'lxml')
            result = bs_content.find("element", {'type': 'Race'})
            self.ui.race_desc_view.setHtml(str(result))

    def raceDoubleClicked_event(self, item):
        global has_race_been_clicked
        if has_race_been_clicked == True:
            race_bak = item.text()
            self.ui.race_listWidget.clear()
            item = QListWidgetItem(race_bak, self.ui.race_listWidget)
            self.ui.race_listWidget.setCurrentItem(item)
            self.ui.subrace_label_listWidget.show()
            self.ui.subrace_listWidget.show()
            with open('sources/players-handbook/races/race-' + race_bak + '.xml', 'r') as file:
                content = file.readlines()
                content = "".join(content)
                bs_content = bs(content, 'lxml')
                result = bs_content.find_all("element", {'type': 'Race Variant' })
                result += bs_content.find_all("element", {'type': 'Sub Race'})
                for x in range(len(result)):
                    output = re.split('"', str(result[x]))
                    outstr = output[3]
                    QListWidgetItem(outstr, self.ui.subrace_listWidget)
            has_race_been_clicked = False
        else:
            self.ui.subrace_listWidget.clear()
            self.ui.subrace_label_listWidget.hide()
            self.ui.subrace_listWidget.hide()
            self.ui.race_listWidget.clear()
            with open('sources/players-handbook.index', 'r') as file:
                content = file.readlines()
                content = "".join(content)
                bs_content = bs(content, 'lxml')
                result = bs_content.find_all("file", {'name': re.compile('race-.*?\.xml')})
                for x in range(len(result)):
                    output = re.split('"', str(result[x]))
                    outstr = output[1]
                    QListWidgetItem(outstr[5:-4], self.ui.race_listWidget)
            has_race_been_clicked = True


    def subraceClicked_event(self, item):
        with open('sources/players-handbook/races/race-' + self.ui.race_listWidget.currentItem().text() + '.xml', 'r') as file:
            content = file.readlines()
            content = "".join(content)
            bs_content = bs(content, 'lxml')
            result = bs_content.find_all("element", {'name': item.text()})
            result += bs_content.find_all("element",  {'name': item.text()})
            self.ui.race_desc_view.setHtml(str(result))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
