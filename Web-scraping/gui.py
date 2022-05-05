
#############################################
from PyQt5 import QtCore, QtGui, QtWidgets,QtWebEngineWidgets

## import manager class - get reqeust,get soup etc.
from manager import *
from web_search_keyword import *
## import web scrape class
from gamespot import *
from gameinformer import *
from gematsu import *
from verge import * 
from techradar import *
from pocket_lint import *
from tech import *
from polygon import *
from guardian import *
from common import *
from compgamer import *
from kotaku import *
from rockpapaershotgun import *
from pcgamer import *
from pcgamesn import *
from videogameschronicle import *
from digitaltrends import *
from zeenews import *
from venturebeat import *
from pocketgamer import *
from gamingintel import *
from gamemonday import *
from gamingdose import *
from thisisgamethailand import *
from game_ded import*
##import pyqt5 component
from PyQt5.QtWidgets import QCompleter,QWidget,QVBoxLayout,QLabel,QFileSystemModel
from PyQt5.QtCore import Qt,QModelIndex
from model import *
import os
from PyQt5.QtWidgets import QScrollArea
import traceback, sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

import threading
import time
from functools import partial

from PyQt5.QtWebEngineWidgets import *
import altair as alt
from io import StringIO

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
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  
        finally:
            self.signals.finished.emit()  


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        self.website_name = ['gamespot','gameinformer','techradar','gematsu','verge','pocket-lint',
        'tech','polygon','common','compgamer','kotaku','rockpapershotgun','pcgamer','pcgamesn','videogameschronicle','digitaltrends','zeenews'
        ,'venturebeat','pocketgamer','gamingintel','gamemonday','gamingdose','thisisgamethailand'
        ,'game_ded']
        

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 851)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1100, 851))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.main_intab = QtWidgets.QTabWidget(self.tab)
        self.main_intab.setGeometry(QtCore.QRect(320, 100, 691, 641))
        self.main_intab.setObjectName("main_intab")
        self.intab1 = QtWidgets.QWidget()
        self.intab2 = QtWidgets.QWidget()
        self.main_intab.addTab(self.intab1,"")
        self.main_intab.addTab(self.intab2,"")

        self.lo = QtWidgets.QWidget(self.intab2)
        self.lo.setGeometry(QtCore.QRect(0, 0, 691, 620))
        self.lo.setObjectName("lo")

        self.plot_layout = QVBoxLayout(self.lo)

        self.search_bar = QtWidgets.QLineEdit(self.tab)
        self.search_bar.setGeometry(QtCore.QRect(320, 30, 431, 21))
        self.search_bar.setObjectName("search_bar")
        self.completer = QCompleter(self.website_name)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_bar.setCompleter(self.completer)

        self.searchkeyword_bar = QtWidgets.QLineEdit(self.tab)
        self.searchkeyword_bar.setGeometry(QtCore.QRect(850, 30, 160, 21))
        self.searchkeyword_bar.setObjectName("search_bar")

        self.search_button = QtWidgets.QPushButton(self.tab)
        self.search_button.setGeometry(QtCore.QRect(755, 30, 91, 21))
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.run_thread)

        self.key_button = QtWidgets.QPushButton(self.tab)
        self.key_button.setGeometry(QtCore.QRect(1010, 30, 91, 21))
        self.key_button.clicked.connect(self.run_thread3)


        self.label = QLabel('Keyword list:', self.tab)
        self.label.setGeometry(QtCore.QRect(0, 100, 61, 16))

        self.label2 = QLabel('Search Website name:', self.tab)
        self.label2.setGeometry(QtCore.QRect(320, 10, 121, 16))

        self.label3 = QLabel('Search Keyword:', self.tab)
        self.label3.setGeometry(QtCore.QRect(850, 10, 121, 16))

        # self.label4 = QLabel('Ref link:', self.tab)
        # self.label4.setGeometry(QtCore.QRect(60, 300, 121, 16))

        self.tableView = QtWidgets.QTableView(self.intab1)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 691, 620))
        self.tableView.setObjectName("tableView")
        self.tableView.doubleClicked.connect(self.doubleClicked_table)

        # self.ref_tableView = QtWidgets.QTableView(self.tab)
        # self.ref_tableView.setGeometry(QtCore.QRect(70, 320, 180, 390))

        path = 'C:\\Users\\Nachanon\\Desktop\\Web-scraping\\Web-scrape\\data'
        self.filemodel = QFileSystemModel()
        self.filemodel.setRootPath(path)
        self.proxy_model = QSortFilterProxyModel(recursiveFilteringEnabled = True, filterRole = QFileSystemModel.FileNameRole)
        self.proxy_model.setSourceModel(self.filemodel)


        self.key_tree = QtWidgets.QTreeView(self.tab)
        self.key_tree.setGeometry(QtCore.QRect(0, 120, 300, 620))
        self.key_tree.setObjectName("key_tree")
        self.key_tree.setModel(self.proxy_model)
        self.key_tree.setRootIndex(self.proxy_model.mapFromSource(self.filemodel.index(path)))
        self.key_tree.setColumnWidth(0,200)
        self.key_tree.setAlternatingRowColors(True)
        self.key_tree.doubleClicked.connect(self.key_tree_dbclicked)

    
        
   
  

        self.date1 = QDateEdit(self.tab)
        self.date1.setGeometry(QtCore.QRect(330, 60, 140, 21))

        self.date2 = QDateEdit(self.tab)
        self.date2.setGeometry(QtCore.QRect(480, 60, 140, 21))

        self.radiobutton = QRadioButton('Active Date Range',self.tab)
        self.radiobutton.setGeometry(QtCore.QRect(630, 60, 171, 21))

        self.tabWidget.addTab(self.tab, "")
       
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 842, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.threadpool = QThreadPool()


        # self.run_thread2()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_bar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Search for Website name</p><p><br/></p></body></html>"))
        self.search_bar.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Search for Website name</p></body></html>"))
        self.key_button.setText(_translate("MainWindow", "Keyword"))
        self.search_button.setText(_translate("MainWindow", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "WEB"))
    

        self.main_intab.setTabText(self.main_intab.indexOf(self.intab1), _translate("MainWindow", "Data"))
        self.main_intab.setTabText(self.main_intab.indexOf(self.intab2), _translate("MainWindow", "Graph"))
    def plot(self,x,y):
        categories = x
        values = y
        source = pd.DataFrame({"category": categories, "value": values})
        
    

        circle = alt.Chart(source).encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(field="category", type="nominal"),tooltip = ["category","value"]
).resolve_scale(theta = 'independent')

        self.chart = circle.mark_arc(outerRadius=120) 
       # text = base.mark_text(radius=140, size=20).encode(text="Region:N")
        return self.chart

    def key_tree_dbclicked(self,index):
        x= ['Positive','Negative','Neutral']
        y = []
        source_index = self.proxy_model.mapToSource(index)
        indexItem = self.filemodel.index(source_index.row(), 0, source_index.parent())
        fileName = self.filemodel.fileName(indexItem)
        filePath = self.filemodel.filePath(indexItem)
        path = filePath.split('/',5)[5]
        
        
        print(fileName)
        print(filePath)
        try:
            df = pd.read_csv(filePath)
            df = df.loc[df['content'] != 'No Content.']
            df = df.dropna()
    
            self.insert_table(df)
            posi = df[(df['sentiment'] == 'Positive')]['sentiment'].count()
            y.append(posi)
            neg =df[(df['sentiment'] == 'Negative')]['sentiment'].count()
            y.append(neg)
            neu = df[(df['sentiment'] == 'Neutral')]['sentiment'].count()
            y.append(neu)

            self.chart = self.plot(x,y)
            self.thread_complete()
        except:
            df = pd.read_csv(filePath)
            try:
            
                df = df.loc[df['count_keyword'] > 0]
            except:
                pass
           
    
            self.insert_table(df)
    def list_keyword(self, progress_callback):
        self.key_list.clear()
        mn = manage('')
        key = mn.get_keyword_folder()
        print(key)
        self.key_list.addItems(key)
        progress_callback.emit(0+0)

    def non_key_prog(self,webname,url,web_content,lang):

        if not os.path.exists(f'Web-scrape\\data\\web\\en\\{webname}.csv') and not os.path.exists(f'Web-scrape\\data\\web\\th\\{webname}.csv') :
            x= ['Positive','Negative','Neutral']
            y = []
            print('csv file was not found')
            print('creating ............')
            web = web_content()
            mn = manage(url)
            list_data = web.get_content_manager()
            df = mn.to_dataframe(list_data)
            df = df.loc[df['content'] != 'No Content.']
            
      
          
            mn.to_csv(df,f'Web-scrape\\data\\web\\{lang}\\{webname}.csv')
            if self.radiobutton.isChecked() == False:
                self.insert_table(df)
                posi = df[(df['sentiment'] == 'Positive')]['sentiment'].count()
                y.append(posi)
                neg =df[(df['sentiment'] == 'Negative')]['sentiment'].count()
                y.append(neg)
                neu = df[(df['sentiment'] == 'Neutral')]['sentiment'].count()
                y.append(neu)

                self.chart = self.plot(x,y)

               
            else:
                temp_start = self.date1.date()
                sdate = temp_start.toPyDate()

                temp_end = self.date2.date()
                edate = temp_end.toPyDate()

                date_range = pd.date_range(sdate,edate,freq = 'd')
                date_list = []
                for i in date_range:
                    si = str(i.date())
                    sir = si.replace('-','/')
                    date_list.append(sir)
                df_date_range = df.loc[df['date'].isin(date_list)]
                self.insert_table(df_date_range)

                posi = df_date_range[(df_date_range['sentiment'] == 'Positive')]['sentiment'].count()
                y.append(posi)
                neu = df_date_range[(df_date_range['sentiment'] == 'Neutral')]['sentiment'].count()
                y.append(neu)
                neg =df_date_range[(df_date_range['sentiment'] == 'Negative')]['sentiment'].count()
                y.append(neg)

                self.chart = self.plot(x,y)
         

            ref = web.ref_link()
            df_ref = mn.to_dataframe(ref)
            df_ref_s = df_ref.sort_values(by = ['total_ref'], ascending=False)
            mn.to_csv(df_ref_s,f'Web-scrape\\data\\ref-link\\{webname}_link_ref.csv')
            # self.insert_reftable(df_ref_s)
       

     
        else:
     
           
            x= ['Positive','Negative','Neutral']
            y = []
            df = pd.read_csv(f'Web-scrape\\data\\web\\{lang}\\{webname}.csv')
            df = df.loc[df['content'] != 'No Content.']
            df = df.dropna()
            print(f'file {webname}.csv existed.')

            if self.radiobutton.isChecked() == False:
                self.insert_table(df)
                posi = df[(df['sentiment'] == 'Positive')]['sentiment'].count()
                y.append(posi)
                neu = df[(df['sentiment'] == 'Neutral')]['sentiment'].count()
                y.append(neu)
                neg =df[(df['sentiment'] == 'Negative')]['sentiment'].count()
                y.append(neg)

                self.chart = self.plot(x,y)
                
               
            else:
                temp_start = self.date1.date()
                sdate = temp_start.toPyDate()

                temp_end = self.date2.date()
                edate = temp_end.toPyDate()

                date_range = pd.date_range(sdate,edate,freq = 'd')
                date_list = []
                for i in date_range:
                    si = str(i.date())
                    sir = si.replace('-','/')
                    date_list.append(sir)
                df_date_range = df.loc[df['date'].isin(date_list)]
                self.insert_table(df_date_range)
                posi = df_date_range[(df_date_range['sentiment'] == 'Positive')]['sentiment'].count()
                y.append(posi)
                neu = df_date_range[(df_date_range['sentiment'] == 'Neutral')]['sentiment'].count()
                y.append(neu)
                neg =df_date_range[(df_date_range['sentiment'] == 'Negative')]['sentiment'].count()
                y.append(neg)

                self.chart = self.plot(x,y)
              
            # df_ref = pd.read_csv(f'Web-scrape\\data\\ref-link\\{webname}_link_ref.csv')
            # self.insert_reftable(df_ref)

    def got_key_prog(self,key_text,webname,url,lang):
        if not os.path.exists(f'Web-scrape\\data\\keyword\\{key_text}.csv'):
            print('new keyword')
            count_key = []
            data = {}
            df = pd.read_csv(f'Web-scrape\\data\\web\\{lang}\\{webname}.csv')
            mn = manage(url)
            for content in df['content']:
                c = mn.count_keywords(content,key_text)
                count_key.append(c)
            url_temp_list = list(df['url'])
            name_list = list(df['name'])
            date_list = list(df['date'])
            data['name'] = name_list
            data['date'] = date_list
            data['url'] = url_temp_list
            data['count_keyword'] = count_key
            
            df_key = pd.DataFrame(data)
            df_key.to_csv(f'Web-scrape\\data\\keyword\\{key_text}.csv',index = False)
           
            df_key = df_key.loc[df_key['count_keyword'] > 0]
            self.insert_table(df_key)
            # self.run_thread2()
        else:
            print('this keyword was existed')
            df_key = pd.read_csv(f'Web-scrape\\data\\keyword\\{key_text}.csv')
            if df_key.loc[df_key['name'] == webname].shape[0] == 0:
                count_key = []
                data = {}
                df = pd.read_csv(f'Web-scrape\\data\\web\\{lang}\\{webname}.csv')
                mn = manage(url)
                for content in df['content']:
                    c = mn.count_keywords(content,key_text)
                    count_key.append(c)
                url_temp_list = list(df['url'])
                name_list = list(df['name'])
                date_list = list(df['date'])
                data['name'] = name_list
                data['date'] = date_list
                data['url'] = url_temp_list
                data['count_keyword'] = count_key
                df2 = pd.DataFrame(data)

                df_key2 = pd.concat([df_key,df2], ignore_index=True)
                
                df_key2.to_csv(f'Web-scrape\\data\\keyword\\{key_text}.csv',index = False)
                df_key2 = df_key2.loc[df_key2['count_keyword'] > 0]
                self.insert_table(df_key2.loc[df_key2['name'] == webname])
            else:
                df_key = pd.read_csv(f'Web-scrape\\data\\keyword\\{key_text}.csv')
                df_key = df_key.loc[df_key['count_keyword'] > 0]
                self.insert_table(df_key.loc[df_key['name'] == webname])

    def search_keyword(self, progress_callback):
        key_text = self.searchkeyword_bar.text()
        if key_text != '':
            s = search_key(key_text)
            df = s.search()
            df.to_csv(f'Web-scrape\\data\\keyword\\{key_text}.csv',index = False)
            df = df.loc[df['count_keyword'] > 0]
            self.insert_table(df)
        progress_callback.emit(0+0)




    def search_button_callback(self, progress_callback):
        text = self.search_bar.text()
        key_text = self.searchkeyword_bar.text()
        

        if text in self.website_name:
            if text == 'gamespot':
                if key_text == '': #if keyword bar is none
                    self.non_key_prog('gamespot','https://www.gamespot.com/',gamespot_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'gamespot','https://www.gamespot.com/','en')
                
            elif text == 'gameinformer':
                
                if key_text == '': #if keyword bar is none
                    self.non_key_prog('gameinformer','https://www.gameinformer.com/',gameinformer_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'gameinformer','https://www.gameinformer.com/','en')
                       
                    ####################

            
            elif text == 'gematsu':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('gematsu','https://www.gematsu.com/',gematsu_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'gematsu','https://www.gematsu.com/','en')
                #############################

            elif text == 'techradar':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('techradar','https://www.techradar.com/',techradar_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'techradar','https://www.techradar.com/','en')
                #############################


            elif text == 'verge':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('verge','https://www.theverge.com/games',verge_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'verge','https://www.theverge.com/games','en')
                #############################

            
            elif text == 'pocket-lint':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('pocket-lint','https://www.pocket-lint.com/games',pocket_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'pocket-lint','https://www.pocket-lint.com/games','en')
                #############################


            elif text == 'tech':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('tech','https://tech.hindustantimes.com/gaming/',tech_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'tech','https://tech.hindustantimes.com/gaming/','en')
                #############################

            elif text == 'polygon':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('polygon','https://www.polygon.com/',polygon_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'polygon','https://www.polygon.com/','en')
                #############################

            
                
            

            

            elif text == 'common':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('common','https://www.commonsensemedia.org/',common_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'common','https://www.commonsensemedia.org/','en')
                #############################

            elif text == 'compgamer':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('compgamer','https://www.compgamer.com/mainpage/',compgamer_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'compgamer','https://www.compgamer.com/mainpage/','en')
                #############################

            elif text == 'kotaku':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('kotaku','https://kotaku.com/',kotaku_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'kotaku','https://kotaku.com/','en')
                #############################

            elif text == 'rockpapershotgun':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('rockpapershotgun','https://www.rockpapershotgun.com/news/',rockpapershotgun_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'rockpapershotgun','https://www.rockpapershotgun.com/news/','en')
                #############################

            elif text == 'pcgamer':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('pcgamer','https://www.pcgamer.com/au/',pcgamer_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'pcgamer','https://www.pcgamer.com/au/','en')
                #############################

            elif text == 'pcgamesn':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('pcgamesn','https://www.pcgamesn.com/',pcgamesn_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'pcgamesn','https://www.pcgamesn.com/','en')
                #############################
            
            elif text == 'videogameschronicle':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('videogameschronicle','https://www.videogameschronicle.com/',videogameschronicle_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'videogameschronicle','https://www.videogameschronicle.com/','en')
                #############################

            elif text == 'digitaltrends':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('digitaltrends','https://www.digitaltrends.com/gaming/',digitaltrends_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'digitaltrends','https://www.digitaltrends.com/gaming/','en')
                #############################

            elif text == 'zeenews':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('zeenews','https://zeenews.india.com/gaming/',zeenews_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'zeenews','https://zeenews.india.com/gaming/','en')
                #############################

            elif text == 'venturebeat':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('venturebeat','https://venturebeat.com/category/games/',venturebeat_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'venturebeat','https://venturebeat.com/category/games/','en')
                #############################

            elif text == 'pocketgamer':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('pocketgamer','https://www.pocketgamer.com/',pocketgamer_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'pocketgamer','https://www.pocketgamer.com/','en')
                #############################

            elif text == 'gamingintel':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('gamingintel','https://gamingintel.com/',gamingintel_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'gamingintel','https://gamingintel.com/','en')
                #############################

            elif text == 'gamemonday':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('gamemonday','https://www.gamemonday.com/game-news/',gamemonday_content,'en')
                else: #if got keyword
                    self.got_key_prog(key_text,'gamemonday','https://www.gamemonday.com/game-news/','en')
                #############################

            elif text == 'gamingdose':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('gamingdose','https://www.gamingdose.com/',gamingdose_content,'th')
                else: #if got keyword
                    self.got_key_prog(key_text,'gamingdose','https://www.gamingdose.com/','th')
                #############################

            elif text == 'thisisgamethailand':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('thisisgamethailand','https://www.thisisgamethailand.com/',thisisgamethailand_content,'th')
                else: #if got keyword
                    self.got_key_prog(key_text,'thisisgamethailand','https://www.thisisgamethailand.com/','th')
                #############################

            elif text == 'game_ded':

                if key_text == '': #if keyword bar is none
                    self.non_key_prog('game_ded','https://www.game-ded.com/',game_ded_content,'th')
                else: #if got keyword
                    self.got_key_prog(key_text,'game_ded','https://www.game-ded.com/','th')
                #############################

        progress_callback.emit(0+0)
        return 'Done.'
    def insert_table(self,df):
        model = PandasModel(df)
        self.tableView.setModel(model)

    def insert_reftable(self,df):
        model = PandasModel(df)
        self.ref_tableView.setModel(model)
   
    
    def doubleClicked_table(self,item):
        print(item.data())
        self.label.setText(item.data())

    def thread_progress(self):
        print('Done')

    def print_output(self):
        print('data crawled')

    def thread_complete(self):
        print("THREAD COMPLETE!")
        for i in reversed(range(self.plot_layout.count())): 
            self.plot_layout.itemAt(i).widget().setParent(None)
        try:
            self.v = WebEngineView()
            self.v.updateChart(self.chart)
            self.plot_layout.addWidget(self.v)
        except:
            pass

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
    
    def run_thread3(self):
        worker = Worker(self.search_keyword) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.thread_progress)

        # Execute
        self.threadpool.start(worker)

    def thread(self):
        t1=Thread(target=self.search_button_callback)
        t1.start()          

class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def onDownloadRequested(self, download):
        if (
            download.state()
            == QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested
        ):
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr("Save as"), download.path()
            )
            if path:
                download.setPath(path)
                download.accept()

    def createWindow(self, type_):
            if type_ == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
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
