import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtGui import QTextDocument
from PyQt5.QtCore import QDate
from UI import Ui_MainWindow as GUI


class Main(QMainWindow,GUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.define_vars()
        self.handleEvents()
    
    def recImportUI(func):
        def _wrapper(*args):
            self=args[0]
            if self.confirm_dialog('import'):
                func(self)
                self.ent_kwords.setText(self.current_record['Keys'])
                self.ent_text.setPlainText(self.current_record['Text'])
                self.checkbox_mode.setChecked(True)
                self.hideHistory()
        return _wrapper

    def dbCreate(self):
        tmp = QFileDialog.getSaveFileName(directory='Database', filter='Файлы баз данных SQLITE (*.sqlite)',caption='Создание БД')[0]
        if tmp:
            db_connection = QSqlDatabase('QSQLITE')
            db_connection.setDatabaseName(tmp)
            if not db_connection.open():
                return self.db_error(db_connection.lastError().databaseText())
            query = '''CREATE TABLE IF NOT EXISTS "Notes" (
                        "ID"	INTEGER NOT NULL UNIQUE,
                        "Date"	TEXT,
                        "Keys"	TEXT,
                        "Text"	TEXT,
                        PRIMARY KEY("ID" AUTOINCREMENT)
                        ); '''
            db_connection.exec_(query)
            db_connection.close()
            self.dbLoad(tmp)
    def dbLoad(self, path=None):
        self.db_path = path if path else QFileDialog.getOpenFileName(directory='Database', filter='Файлы баз данных SQLITE (*.sqlite);; Все файлы (*)',caption='Загрузка БД')[0]
        if self.db_path:

            if self.db_connection: self.db_connection.close()
            self.db_connection = QSqlDatabase('QSQLITE')
            self.db_connection.setDatabaseName(self.db_path)
            if not self.db_connection.open():
                return self.db_error(self.db_connection.lastError().databaseText())

            self.db_initView()
            self.setWindowTitle('Цифровой дневник - ' + Path(self.db_path).stem+' - файл базы данных')
            self.frame_rechandle.setEnabled(True)
            self.label_2.setVisible(False)
            self.frame_dbhandle.setEnabled(True)
    def dbChange(self):
        date = QDate.currentDate().toString('dd/MM/yy')
        kwords = self.ent_kwords.text().strip().replace("'", '"')
        text = self.ent_text.toPlainText().replace("'", '"')
        sender = QApplication.instance().sender().objectName()

        if(kwords and text):
            if sender =='button_dbinsert':
                query=f'''INSERT INTO Notes(Date,Keys,Text) VALUES('{date}','{kwords}','{text}')'''
                self.current_record = {key:None for key in self.current_record}
                self.record_imported=False
                
            elif sender=='button_dbupdate':
                query = f'''UPDATE Notes SET Keys='{kwords}', Text='{text}' WHERE ID={self.current_record['ID']} '''
                self.current_record['Keys']=kwords
                self.current_record['Text']=text
                
            
            
            self.button_dbupdate.setEnabled(False)

            self.db_connection.exec_(query)
            self.db_connection.commit()
            self.dbLoad(self.db_path)
    def dbClose(self):
        self.db_connection.close()
        self.hideHistory()
        self.label_2.setVisible(True)
        self.frame_rechandle.setEnabled(False)
        self.frame_dbhandle.setEnabled(False)
        self.record_imported=False
        self.setWindowTitle('Цифровой дневник')
   
    def menuOpen(self):
        path = QFileDialog.getOpenFileName(filter='Текстовые файлы (*.txt)',caption='Открытие файла')[0]
        if path:
            with open(path, 'r', encoding="utf-8") as file:
                buf = file.read().strip()

                kwords,text = buf.split('\n',1)

                if not kwords.startswith('--') and not kwords.endswith('--'):
                    text = kwords+'\n'+text
                    kwords=''

                self.ent_text.setPlainText(text)
                self.ent_kwords.setText(kwords[2:-2])
                self.current_record = {key:None for key in self.current_record}
                self.setWindowTitle('Цифровой дневник - ' + Path(path).stem+' - текстовый файл')
                if self.db_connection: self.db_connection.close()
                self.db_path=None
                self.frame_rechandle.setEnabled(False)
                self.label_2.setVisible(True)
                self.hideHistory()                     
    def menuSave(self):
        path = QFileDialog.getSaveFileName(filter='Текстовые файлы (*.txt)',caption='Сохранение файла')[0]
        if path:
            with open(path, 'w', encoding="utf-8") as file:
                kwords = self.ent_kwords.text().strip()
                text = self.ent_text.toPlainText()
                file.write('--'+kwords+'--'+'\n'+text)
    def menuPrint(self):
        printer = QPrinter()
        pdialog = QPrintDialog(printer,self)
        if pdialog.exec_():
            date = self.current_record['Date'] if self.db_path else QDate.currentDate().toString('dd/MM/yy')
            doc = QTextDocument(f'{date}\tТема: {self.ent_kwords.text().strip()}\n\n{self.ent_text.toPlainText().strip()}')
            doc.print_(printer)
    def encryptData(self):
        if(not self.ent_xor.isReadOnly()):
            enter = self.ent_xor.text().strip()
            if enter.isdigit() or enter=='' and self.current_record: 
                key = int(self.ent_xor.text().strip()) if enter.isdigit() else 0  
                kwords = str(self.xor(self.current_record['Keys'],key))
                text =  str(self.xor(self.current_record['Text'],key))
                self.ent_kwords.setText(kwords)
                self.ent_text.setPlainText(text)

    @recImportUI
    def recImport(self):
        values = [str(self.tbl_database.model().data(item)).strip() for item in self.tbl_database.selectedIndexes()]
        self.current_record = dict(zip(list(self.current_record.keys()),values))
        self.record_imported = True
        self.checkbox_xor.setChecked(False)
        self.ent_xor.setReadOnly(True)
if (__name__ == '__main__'):
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('content/style.qss').read_text())
    window = Main()
    window.show()
    app.exec()


