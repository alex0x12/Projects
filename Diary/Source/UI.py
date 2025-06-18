from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import QPropertyAnimation, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QIcon
import re

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 650)
        MainWindow.setMinimumSize(QtCore.QSize(800, 650))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 650))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("content/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_text = QtWidgets.QFrame(self.centralwidget)
        self.frame_text.setGeometry(QtCore.QRect(10, 65, 780, 472))
        self.frame_text.setMaximumSize(QtCore.QSize(780, 16777215))
        self.frame_text.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_text.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_text.setObjectName("frame_text")
        self.ent_text = QtWidgets.QPlainTextEdit(self.frame_text)
        self.ent_text.setGeometry(QtCore.QRect(10, 10, 760, 455))
        self.ent_text.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.ent_text.setObjectName("ent_text")
        self.ent_text.setReadOnly(True)
        self.frame_toptext = QtWidgets.QFrame(self.centralwidget)
        self.frame_toptext.setGeometry(QtCore.QRect(10, 9, 781, 50))
        self.frame_toptext.setMaximumSize(QtCore.QSize(1180, 50))
        self.frame_toptext.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_toptext.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_toptext.setObjectName("frame_toptext")
        self.ent_kwords = QtWidgets.QLineEdit(self.frame_toptext)
        self.ent_kwords.setGeometry(QtCore.QRect(60, 10, 250, 30))
        self.ent_kwords.setAlignment(QtCore.Qt.AlignCenter)
        self.ent_kwords.setObjectName("ent_kwords")
        self.ent_kwords.setReadOnly(True)
        self.ent_kwords.setMaxLength(40)
        self.label = QtWidgets.QLabel(self.frame_toptext)
        self.label.setGeometry(QtCore.QRect(10, 10, 41, 30))
        self.label.setObjectName("label")
        self.checkbox_mode = QtWidgets.QCheckBox(self.frame_toptext)
        self.checkbox_mode.setGeometry(QtCore.QRect(320, 10, 250, 30))
        self.checkbox_mode.setChecked(True)
        self.checkbox_mode.setObjectName("checkbox_mode")
        self.checkbox_xor = QtWidgets.QCheckBox(self.frame_toptext)
        self.checkbox_xor.setGeometry(QtCore.QRect(500, 10, 250, 30))
        self.checkbox_xor.setChecked(False)
        self.checkbox_xor.setObjectName("checkbox_xor")
        self.checkbox_xor.setEnabled(False)
        self.ent_xor = QtWidgets.QLineEdit(self.frame_toptext)
        self.ent_xor.setGeometry(QtCore.QRect(675, 10, 100, 30))
        self.ent_xor.setAlignment(QtCore.Qt.AlignCenter)
        self.ent_xor.setObjectName("ent_kwords")
        self.ent_xor.setClearButtonEnabled(True)
        self.ent_xor.setReadOnly(True)
        self.ent_xor.setMaxLength(6)
        self.frame_texthandle = QtWidgets.QFrame(self.centralwidget)
        self.frame_texthandle.setGeometry(QtCore.QRect(10, 543, 781, 50))
        self.frame_texthandle.setMaximumSize(QtCore.QSize(1180, 50))
        self.frame_texthandle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_texthandle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_texthandle.setObjectName("frame_texthandle")
        self.button_clear = QtWidgets.QPushButton(self.frame_texthandle)
        self.button_clear.setEnabled(False)
        self.button_clear.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.button_clear.setObjectName("button_clear")
        self.frame_rechandle = QtWidgets.QFrame(self.frame_texthandle)
        self.frame_rechandle.setEnabled(False)
        self.frame_rechandle.setGeometry(QtCore.QRect(119, 0, 491, 50))
        self.frame_rechandle.setMaximumSize(QtCore.QSize(1180, 50))
        self.frame_rechandle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_rechandle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_rechandle.setObjectName("frame_rechandle")
        self.button_dbinsert = QtWidgets.QPushButton(self.frame_rechandle)
        self.button_dbinsert.setGeometry(QtCore.QRect(30, 10, 141, 30))
        self.button_dbinsert.setEnabled(False)
        self.button_dbinsert.setObjectName("button_dbinsert")
        self.button_dbupdate = QtWidgets.QPushButton(self.frame_rechandle)
        self.button_dbupdate.setGeometry(QtCore.QRect(180, 10, 180, 30))
        self.button_dbupdate.setEnabled(False)
        self.button_dbupdate.setObjectName("button_dbupdate")
        self.button_showh = QtWidgets.QPushButton(self.frame_texthandle)
        self.button_showh.setGeometry(QtCore.QRect(620, 10, 150, 30))
        self.button_showh.setObjectName("button_showh")
        self.button_showh.setEnabled(False)
        self.frame_dbhandle = QtWidgets.QFrame(self.centralwidget)
        self.frame_dbhandle.setEnabled(False)
        self.frame_dbhandle.setGeometry(QtCore.QRect(810, 9, 380, 530))
        self.frame_dbhandle.setMaximumSize(QtCore.QSize(380, 16777215))
        self.frame_dbhandle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dbhandle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dbhandle.setObjectName("frame_dbhandle")
        self.tbl_database = QtWidgets.QTableView(self.frame_dbhandle)
        self.tbl_database.setGeometry(QtCore.QRect(10, 90, 361, 431))
        self.tbl_database.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbl_database.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tbl_database.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbl_database.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tbl_database.setWindowTitle('Записи')
        self.tbl_database.verticalHeader().setVisible(False)
        self.tbl_database.setObjectName("tbl_database")
        self.label_3 = QtWidgets.QLabel(self.frame_dbhandle)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 200, 30))
        self.label_3.setObjectName("label_3")
        self.button_dbclose = QtWidgets.QPushButton(self.frame_dbhandle)
        self.button_dbclose.setGeometry(QtCore.QRect(200, 10, 111, 30))
        self.button_dbclose.setObjectName("button_dbclose")
        self.ent_search = QtWidgets.QLineEdit(self.frame_dbhandle)
        self.ent_search.setGeometry(QtCore.QRect(10, 50, 300, 30))
        self.ent_search.setAlignment(QtCore.Qt.AlignCenter)
        self.ent_search.setClearButtonEnabled(True)
        self.ent_search.setObjectName("ent_search")
        
        '''
        self.ent_searchkey = QtWidgets.QLineEdit(self.frame_dbhandle)
        self.ent_searchkey.setGeometry(QtCore.QRect(250, 10, 300, 30))
        self.ent_searchkey.setAlignment(QtCore.Qt.AlignCenter)
        self.ent_searchkey.setClearButtonEnabled(True)
        self.ent_searchkey.setObjectName("ent_searchkey")
        '''
        self.label_2 = QtWidgets.QLabel(self.frame_dbhandle)
        self.label_2.setEnabled(False)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 361, 511))
        self.label_2.setAutoFillBackground(True)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.frame_dbhandlebuttons = QtWidgets.QFrame(self.centralwidget)
        self.frame_dbhandlebuttons.setGeometry(QtCore.QRect(810, 543, 381, 50))
        self.frame_dbhandlebuttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dbhandlebuttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dbhandlebuttons.setObjectName("frame_dbhandlebuttons")
        self.button_hideh = QtWidgets.QPushButton(self.frame_dbhandlebuttons)
        self.button_hideh.setEnabled(True)
        self.button_hideh.setGeometry(QtCore.QRect(280, 10, 90, 30))
        self.button_hideh.setObjectName("button_hideh")
        self.button_loaddb = QtWidgets.QPushButton(self.frame_dbhandlebuttons)
        self.button_loaddb.setGeometry(QtCore.QRect(10, 10, 121, 30))
        self.button_loaddb.setObjectName("button_loaddb")
        self.button_createdb = QtWidgets.QPushButton(self.frame_dbhandlebuttons)
        self.button_createdb.setGeometry(QtCore.QRect(140, 10, 111, 30))
        self.button_createdb.setObjectName("button_createdb")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 24))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.mnu_open = QtWidgets.QAction(MainWindow)
        self.mnu_open.setObjectName("mnu_open")
        self.mnu_save = QtWidgets.QAction(MainWindow)
        self.mnu_save.setObjectName("mnu_save")
        self.mnu_print = QtWidgets.QAction(MainWindow)
        self.mnu_print.setObjectName("mnu_print")
        self.menu.addAction(self.mnu_open)
        self.menu.addAction(self.mnu_save)
        self.menu.addSeparator()
        self.menu.addAction(self.mnu_print)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Цифровой дневник"))
        self.label.setText(_translate("MainWindow", "Тема:"))
        self.checkbox_mode.setText(_translate("MainWindow", "Режим - чтение"))
        self.checkbox_xor.setText(_translate("MainWindow", "XOR-шифрование текста"))
        self.button_clear.setText(_translate("MainWindow", "Очистить"))
        self.button_dbinsert.setText(_translate("MainWindow", "Добавить запись"))
        self.button_dbupdate.setText(_translate("MainWindow", "Сохранить изменения"))
        self.button_dbclose.setText(_translate("MainWindow", "Закрыть БД"))
        self.button_showh.setText(_translate("MainWindow", "История записей"))
        self.label_2.setText(_translate("MainWindow", "Необходима загрузка базы данных!"))
        self.label_3.setText(_translate("MainWindow", "Поиск по таблице:"))
        self.button_hideh.setText(_translate("MainWindow", "Свернуть"))
        self.button_loaddb.setText(_translate("MainWindow", "Загрузить БД"))
        self.button_createdb.setText(_translate("MainWindow", "Создать БД"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.mnu_open.setText(_translate("MainWindow", "Открыть (*.txt)"))
        self.mnu_save.setText(_translate("MainWindow", "Сохранить (*.txt)"))
        self.mnu_print.setText(_translate("MainWindow", "Печать (*.pdf)"))
        

#### VARIABLES

    def define_vars(self):
        self.db_connection = None    
        self.db_path = None
        self.db_model = None

        self.current_record = dict.fromkeys(['ID','Date','Keys','Text'],None)
        self.record_imported = False
        self.current_mode = False

        self.db_proxy_model = QSortFilterProxyModel(self)
        

#### FUNCTIONS

    def showHistory(self):
        self.button_showh.setEnabled(False)
        self.setMaximumWidth(1300)
        window = self.window()
        self.anim = QPropertyAnimation(window, b'minimumWidth')
        self.anim.setDuration(250)
        self.anim.setStartValue(800)
        self.anim.setEndValue(1200)
        self.anim.start()
    def hideHistory(self):
        self.button_showh.setEnabled(True)
        self.setMinimumWidth(800)

        window = self.window()
        self.anim = QPropertyAnimation(window, b'maximumWidth')
        self.anim.setDuration(300)
        self.anim.setStartValue(1200)
        self.anim.setEndValue(800)
        self.anim.start()
    def textChanged(self):
        text = self.ent_text.toPlainText()
        kwords = self.ent_kwords.text().strip()
        if text and kwords:
            self.button_clear.setEnabled(self.current_mode)
            self.button_dbinsert.setEnabled(self.db_path!=''and self.current_mode)
            self.button_dbupdate.setEnabled((text!=self.current_record['Text'] or kwords!=self.current_record['Keys']) and self.record_imported)
            print(self.record_imported)
    def modeChanged(self):
        self.current_mode = False if self.checkbox_mode.isChecked() else True
        tmp = 'Режим - редактирование' if self.current_mode else 'Режим - чтение'
        self.checkbox_mode.setText(tmp)

        self.checkbox_xor.setEnabled(self.current_mode)
        self.checkbox_xor.setChecked(False)
        self.ent_xor.setReadOnly(True)
        self.ent_kwords.setReadOnly(not self.current_mode or self.checkbox_xor.isChecked())
        self.ent_kwords.setClearButtonEnabled(self.current_mode or self.checkbox_xor.isChecked())
        self.ent_text.setReadOnly(not self.current_mode)

        self.button_dbinsert.setEnabled(self.db_path!=None and self.checkbox_mode.isChecked()!=True)
    def textClear(self):
        if self.confirm_dialog('clear'):
            self.ent_kwords.clear()
            self.ent_text.clear()
    def xorChanged(self):
        self.ent_xor.setReadOnly(not self.checkbox_xor.isChecked() or not self.current_mode)
        if(not self.checkbox_xor.isChecked()):
            self.ent_kwords.setText(self.current_record['Keys'])
            self.ent_text.setPlainText(self.current_record['Text'])
            b = False
        else:
            self.current_record['Keys'] = self.ent_kwords.text().strip()
            self.current_record['Text'] = self.ent_text.toPlainText()
            b = True
        self.ent_kwords.setReadOnly(b)
        self.ent_text.setReadOnly(b)

    '''
    def setSearch(self):
        key = self.ent_searchkey.text().strip()
        self.db_proxy_model.setFilterFixedString(self.xor(self.ent_search,key))
    '''

    #### Реализовано в потомке    
    def recImport(self): pass
    def dbLoad(self): pass
    def dbCreate(self):pass
    def dbChange(self): pass
    def dbClose(self): pass
    def menuOpen(self) : pass
    def menuSave(self) : pass
    def menuPrint(self) : pass
    def encryptData(self) : pass

    def handleEvents(self):
        self.ent_text.textChanged.connect(self.textChanged)
        self.ent_kwords.textChanged.connect(self.textChanged)
        self.button_showh.clicked.connect(self.showHistory)
        self.button_hideh.clicked.connect(self.hideHistory)
        self.button_loaddb.clicked.connect(self.dbLoad)
        self.button_createdb.clicked.connect(self.dbCreate)
        self.button_dbinsert.clicked.connect(self.dbChange)
        self.button_dbupdate.clicked.connect(self.dbChange)
        self.button_clear.clicked.connect(self.textClear)
        self.mnu_open.triggered.connect(self.menuOpen)
        self.mnu_save.triggered.connect(self.menuSave)
        self.mnu_print.triggered.connect(self.menuPrint)
        self.checkbox_mode.clicked.connect(self.modeChanged)
        self.checkbox_mode.clicked.connect(self.textChanged)
        self.tbl_database.doubleClicked.connect(self.recImport)
        self.tbl_database.doubleClicked.connect(self.modeChanged)
        self.ent_search.textChanged.connect(self.db_proxy_model.setFilterFixedString)
        self.checkbox_xor.clicked.connect(self.xorChanged)
        self.ent_xor.textChanged.connect(self.encryptData)
        self.checkbox_xor.clicked.connect(self.encryptData) 
        self.button_dbclose.clicked.connect(self.dbClose)

    def db_initView(self):
            self.db_model = QtSql.QSqlTableModel(self,self.db_connection)
            self.db_model.setTable('Notes')
            self.db_model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
            self.db_model.setHeaderData(1, QtCore.Qt.Horizontal, "Дата")
            self.db_model.setHeaderData(2, QtCore.Qt.Horizontal, "Тема")
            self.db_model.setHeaderData(3, QtCore.Qt.Horizontal, "Текст")
            self.db_model.select()

            self.db_proxy_model.setFilterKeyColumn(-1)
            self.db_proxy_model.setSourceModel(self.db_model)
            self.db_proxy_model.sort(0,QtCore.Qt.SortOrder.DescendingOrder)
            self.db_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity(False))

            self.tbl_database.setModel(self.db_proxy_model)
            self.tbl_database.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.tbl_database.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.tbl_database.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.tbl_database.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.ResizeMode.Stretch)
    def confirm_dialog(self, action:str) -> bool:
        msg = QtWidgets.QMessageBox()
        d = {'import':'Импорт', 'clear':'Очистка', 'update':'Сохранение изменений'}
        title = d[action] if action in d.keys() else ''
        msg.setWindowTitle(title)
        msg.setWindowIcon(QIcon('content/icon.ico'))
        msg.setText("Подтвердите действие")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        btn_accept = msg.addButton('Продолжить', QtWidgets.QMessageBox.AcceptRole)
        btn_reject = msg.addButton('Отмена', QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(btn_accept)
        for item in msg.buttons(): item.setFixedSize(QtCore.QSize(100,30))
        msg.exec()
        return True if msg.clickedButton() == btn_accept else False
    def db_error(self, err:str):
        return QtWidgets.QMessageBox.critical(None,
        "Критический сбой",
        f"Ошибка БД:\n[{err}]",
        defaultButton=QtWidgets.QMessageBox.Ok
    )

    @staticmethod
    def xor(string:str, key:int)->str:
        
        if key< 0: return
        try:
            return ''.join([(chr(ord(ch)^key)) for ch in string])
        except Exception :
            return string


        