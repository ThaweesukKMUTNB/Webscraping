
#############################################โน๊ต เหลือต่อ csv concat ตรง search callback เวลาหาคีเวิด
from PyQt5 import QtCore, QtGui, QtWidgets,QtWebEngineWidgets
import PyQt5

## import manager class - get reqeust,get soup etc.
from manager import *

## import web scrape class
from gamespot import *
from gameinformer import *
from gematsu import *
from verge import * 
from techradar import *
from pocket_lint import *
from bgr import *
from ign import *
from tweet_manager import *


##import pyqt5 component
from PyQt5.QtWidgets import QCompleter,QWidget,QVBoxLayout,QLabel,QInputDialog
from PyQt5.QtCore import Qt
from model import *
import os
from PyQt5.QtWidgets import QScrollArea
import traceback, sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import *
from pythainlp.corpus import thai_stopwords
import glob
from PyQt5.QtWebEngineWidgets import *
from io import StringIO 
import pandas as pd
from ModelTreeview import *

class WorkerSignals(QObject):
    
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
 

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

      
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    
    def run(self):
       

        try:
            result = self.fn(*self.args, **self.kwargs)
            print('result',result)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  
        finally:
            self.signals.finished.emit()  


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
               

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1600, 1000))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

       
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)

########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############
########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############

        self.file_ex = None

        self.graph_tab = QtWidgets.QTabWidget(self.tab_2)
        self.graph_tab.setGeometry(QtCore.QRect(971, 90, 600, 332))
        self.graph_tab.setObjectName("graph_tab")

        self.label_graph = QLabel('GRAPH', self.tab_2)
        self.label_graph.setGeometry(QtCore.QRect(971, 70, 41, 16))

        self.plot_layout = QtWidgets.QGridLayout(self.graph_tab)
        self.plot_layout.setContentsMargins(1, 1, 1, 1)
        self.plot_layout.setObjectName("plot_layout")

        
        self.lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit.setGeometry(QtCore.QRect(290, 30, 241, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.combobox = QtWidgets.QComboBox(self.tab_2)
        self.combobox.setGeometry(QtCore.QRect(540, 30, 81, 22))
        self.combobox.addItems(["Thai","English"])
        self.combobox.setObjectName("combobox")
        
        self.label_1 = QtWidgets.QLabel(self.tab_2)
        self.label_1.setGeometry(QtCore.QRect(290, 10, 91, 16))
        self.label_1.setObjectName("label")
        self.dateEdit = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit.setGeometry(QtCore.QRect(630, 30, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(630, 10, 51, 16))
        self.label_2.setObjectName("label_2")

        self.label_db = QLabel('DATAFRAME', self.tab_2)
        self.label_db.setGeometry(QtCore.QRect(290, 70, 61, 16))
        self.tableView = QtWidgets.QTableView(self.tab_2)

        self.tableView.setGeometry(QtCore.QRect(290, 90, 671, 781))
        self.tableView.setObjectName("tableView")

        self.tableView_2 = QtWidgets.QTableView(self.tab_2)
        self.tableView_2.setGeometry(QtCore.QRect(10, 500, 261, 401))
        self.tableView_2.setObjectName("tableView_2")

        self.open_button = QtWidgets.QPushButton(self.tab_2)
        self.open_button.setGeometry(QtCore.QRect(86, 450, 91, 21))
        self.open_button.setObjectName("open_button")
        self.open_button.clicked.connect(self.openfile_callback)

        self.export_button = QtWidgets.QPushButton(self.tab_2)
        self.export_button.setGeometry(QtCore.QRect(555, 880, 91, 21))
        self.export_button.setObjectName("export_button")
        self.export_button.clicked.connect(self.export_file)

        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit_2.setGeometry(QtCore.QRect(750, 30, 110, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(750, 10, 51, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QLabel('Language',self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(540, 10, 51, 16))
        self.label_6 = QLabel('Related words',self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(10, 480, 131, 20))
        

        self.treeview2 = QtWidgets.QTreeView(self.tab_2)
        self.treeview2.setGeometry(QtCore.QRect(10, 90, 261, 351))
        self.treeview2.setObjectName("TreeView")
       
        
        ######################################

        self.model2 = CheckableFileSystemModel()
        self.model2.setRootPath("E:\\Users\\glory\\OneDrive\\Documents\\Project\\twitterDB")
        self.treeview2.setModel(self.model2)
        self.treeview2.setSortingEnabled(True)
        self.treeview2.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        for i in range(1, self.model2.columnCount()):
            self.treeview2.header().hideSection(i)

        self.check = []
        self.model2.checkStateChanged.connect(self.updateLog)
        QtCore.QTimer.singleShot(0, lambda: self.treeview2.expand(self.model2.index(0, 0)))
        self.treeview2.setRootIndex(self.model2.index(r"E:\Users\glory\OneDrive\Documents\Project\twitterDB"))
        
        self.progressbar = QtWidgets.QProgressBar(self.tab_2)
        self.progressbar.setGeometry(QtCore.QRect(10, 30, 261, 20))
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(500)
        

        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 71, 20))
        self.label_4.setObjectName("label_4")

        self.search_button1 = QtWidgets.QPushButton(self.tab_2)
        self.search_button1.setGeometry(QtCore.QRect(870, 30, 91, 23))
        self.search_button1.setObjectName("search_button1")
        self.search_button1.clicked.connect(self.run_thread_tweet)

        self.seeword_button = QtWidgets.QPushButton(self.tab_2)
        self.seeword_button.setGeometry(QtCore.QRect(96, 911, 100, 23))
        self.seeword_button.setObjectName("see_button1")
        self.seeword_button.clicked.connect(self.run_thread_open)

########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############
########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############ ########## TWEET GUI ############
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 842, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def updateLog(self, path, checked):
        if checked:
            if path in self.check:
                self.check.remove(path)
            else:
            #print('Path '+ path +' has been checked')
                self.check.append(path)
                print(self.check)
        else:
            #print('Path '+ path + ' has been unchecked')
            self.check.remove(path)
            print(self.check)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_button1.setText(_translate("MainWindow", "Search"))
        self.open_button.setText(_translate("MainWindow", "OpenFile"))
        self.export_button.setText(_translate("MainWindow", "Export"))
        self.seeword_button.setText(_translate("MainWindow", "See Related words"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "TWEET"))

        self.label_1.setText(_translate("MainWindow", "Search Keyword"))
        self.label_2.setText(_translate("MainWindow", "Date start"))
        self.label_3.setText(_translate("MainWindow", "Date end"))
        self.label_4.setText(_translate("MainWindow", "Keyword list"))

    
    def insert_table(self,df):
        model = PandasModel(df)
        self.tableView.setModel(model)

    def insert_table2(self,df):
        model = PandasModel(df)
        self.tableView_2.setModel(model)
   

        
########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############
########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############

    def openfile_callback(self):

        checkbox = self.check
        all_filepath = []
        self.new_all = []
        for i in checkbox:
            if i.endswith('.csv'):
                all_filepath.append(i)

            else:
                for dirpath,subdirs,files in os.walk(i):
                    for x in files:
                        if x.endswith(".csv"):
                            all_filepath.append(os.path.join(dirpath, x))

        for i in all_filepath:
            x = i.replace('/','\\')
            self.new_all.append(x)

        print(self.new_all)

        self.df = pd.concat(map(pd.read_csv, self.new_all), ignore_index=True)
        self.insert_table(self.df)
        #data = self.count_word_value_gui(self.new_all)
        #self.insert_table2(data)

        for i in reversed(range(self.plot_layout.count())): 
            self.plot_layout.itemAt(i).widget().setParent(None)
        self.v = WebEngineView()
        self.chart = tweet.plot(self,self.new_all)
        self.file_save(self.df)

        self.v.updateChart(self.chart)
        self.plot_layout.addWidget(self.v)

    
    def to_dataframe(self,data):
        return pd.DataFrame.from_dict(data)

    def export_file(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'input dialog', 'FileName')
        if ok:
            df = self.to_dataframe(self.file_ex)
            df.to_csv(text + '.csv' , index = False,encoding = 'utf-8')
        print('export success')
        
    def file_save(self,data):
        self.file_ex = data
        print(self.file_ex)


    def tweet_callback(self,progress_callback):
        key = self.lineEdit.text()
        sdate = self.dateEdit.date().toPyDate()
        edate = self.dateEdit_2.date().toPyDate()
        language = str(self.combobox.currentText())
        print(language)
        if language == "Thai" :
            lan = "th"
        else :
            lan = "en"

        tw = tweet(key,sdate,edate,lan)
        data = tw.get_data_on_date()
        self.insert_table(data[0])
        self.insert_table2(data[1])
        range_date = pd.date_range(sdate,edate,freq='d')
        all_file = []
        for i in range_date:
            self.path = "E:\\Users\\glory\\OneDrive\\Documents\\Project\\twitterDB"
            newpath = os.path.join(self.path, key)
            newpath_2 = os.path.join(newpath, lan)
            date = i.strftime("%Y-%m-%d")
            filename = newpath_2 + "\\" + key +"("+ date +")" + "-" + lan + ".csv"
            
            all_file.append(filename)
        self.chart = tw.plot(all_file)
        self.file_save(data[0])

        progress_callback.emit(0+0)

    def remove_url_gui(self,txt):
        return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

    def remove_url_th_gui(self,txt):

        return " ".join(re.sub("([^\u0E00-\u0E7Fa-zA-Z' ]|^'|'$|''|(\w+:\/\/\S+))", "", txt).split())
        
    def count_word_value_gui(self,progress_callback):
        count_word = {}
        self.wordlist = []
        stop=list(thai_stopwords())
        stop.append(' ')
        df = self.file_ex
        for i in df['Fulltext']:
            if df['Language'][1] == 'en':
                fulltext = i
                text = self.remove_url_gui(fulltext)
                textbb = TextBlob(text)
                clean_word = textbb.noun_phrases
                text_ns = [item for item in clean_word]
                for w in text_ns:
                    if w in count_word:
                        count_word[w] +=1
                    else:
                        count_word[w] = 1

            else :
                fulltext = i
                text = self.remove_url_th_gui(fulltext)
                text2 = word_tokenize(text, engine='newmm')
                text4= [item for item in text2 if item not in stop]
                for w in text4:
                    if w in count_word:
                        count_word[w] +=1
                    else:
                        count_word[w] = 1
        cw1 = sorted(count_word.items(), key=lambda x: x[1],reverse=True)
        for i in cw1:
            temp = {}
            temp['Words'] = i[0]
            temp['frequency'] = i[1]
            self.wordlist.append(temp)
            word = pd.DataFrame.from_dict(self.wordlist)
        #print(self.wordlist)
        self.insert_table2(word[:20])
            
        progress_callback.emit(0+0)
        

    def signal_accept(self,msg):
        self.progressbar.setValue(int(msg))
        print('msg',msg)
        if self.progressbar.value() == 99:
            self.progressbar.setValue(0)
            

########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############
########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############ ########## TWEET FUNC ############







    def thread_progress(self):
        print('Done')

    def print_output(self):
        print('data crawled')

    def thread_complete(self):
        for i in reversed(range(self.plot_layout.count())): 
            self.plot_layout.itemAt(i).widget().setParent(None)
        self.v = WebEngineView()
        self.v.updateChart(self.chart)
        self.plot_layout.addWidget(self.v)
        print("THREAD COMPLETE!")

    def run_thread(self):
        # Pass the function to execute
        worker = Worker(self.search_button_callback) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.thread_progress)

        # Execute
        self.threadpool.start(worker)

    def run_thread2(self):
        # Pass the function to execute
        worker = Worker(self.list_keyword) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.thread_progress)

        # Execute
        self.threadpool.start(worker)

    def run_thread_tweet(self):
        # Pass the function to execute
        worker = Worker(self.tweet_callback) # Any other args, kwargs are passed to the run function
        worker.signals.progress.connect(self.signal_accept)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.thread_progress)
        

        # Execute
        self.threadpool.start(worker)

    def run_thread_open(self):
        worker = Worker(self.count_word_value_gui) # Any other args, kwargs are passed to the run function
        worker.signals.progress.connect(self.signal_accept)
        #worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.thread_progress)

        # Execute
        self.threadpool.start(worker)

    def thread(self):
        t1=Thread(target=self.search_button_callback)
        t1.start()       

class Popup(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(600, 300)
        self.label = QLabel('Dick', self)

class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def init(self, parent=None):
        super().init(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def onDownloadRequested(self, download):
        if (
            download.state()
            == QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested
        ):
            path,  = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr("Save as"), download.path()
            )
            if path:
                download.setPath(path)
                download.accept()

    def createWindow(self, type):
            if type == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
                window = QtWidgets.QMainWindow(self)
                view = QtWebEngineWidgets.QWebEngineView(window)
                window.resize(800,550)
                window.setCentralWidget(view)
                window.show()
                return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output, "html", **kwargs)
        self.setHtml(output.getvalue())




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
