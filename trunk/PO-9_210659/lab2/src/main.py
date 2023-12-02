from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFontDialog, QFileDialog
from PyQt5.QtGui import QTextStream, QFont
from PyQt5.QtCore import QDir, QSettings, Qt, QFile, QIODevice, QCloseEvent
from PyQt5.uic import loadUi
class TextEditor(QMainWindow):

    def __init__(self, filename="", parent=None):
        super(TextEditor, self).__init__(parent)
        loadUi("texteditor.ui", self)  # Загрузка UI файла

        settings = QSettings()
        font = settings.value("viewFont", defaultValue=QFont()).value(QFont)
        self.textEdit.setCurrentFont(font)

        self.actionClose.triggered.connect(self.close)
        self.actionExit.triggered.connect(QApplication.closeAllWindows)
        self.textEdit.textChanged.connect(self.documentModified)
        self.actionAboutQt.triggered.connect(QApplication.aboutQt)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        self.textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        self.textEdit.undoAvailable.connect(self.actionUndo.setEnabled)
        self.textEdit.redoAvailable.connect(self.actionRedo.setEnabled)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSaveAs.triggered.connect(self.saveFileAs)

        self.actionCopy.setEnabled(False)
        self.actionCut.setEnabled(False)
        self.actionUndo.setEnabled(False)
        self.actionRedo.setEnabled(False)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.loadFile(filename)

    def closeEvent(self, e: QCloseEvent):
        if self.isWindowModified():
            choice = QMessageBox.warning(
                self, "Документ изменен",
                "Документ был изменен. Хотите сохранить изменения?\nВсе несохраненные изменения будут потеряны.",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if choice == QMessageBox.Yes:
                if not self.saveFile():
                    e.ignore()
            elif choice == QMessageBox.No:
                e.accept()
            elif choice == QMessageBox.Cancel:
                e.ignore()
        else:
            e.accept()

    def documentModified(self):
        self.setWindowModified(True)

    def on_actionSelectFont_triggered(self):
        font = self.textEdit.font()
        status, newFont = QFontDialog.getFont(font)
        if status:
            self.textEdit.setCurrentFont(newFont)
            settings = QSettings()
            settings.setValue("viewFont", newFont)

    def on_actionAbout_triggered(self):
        QMessageBox.about(self, "О программе", "Что-то о этой удивительной программе")

    def loadFile(self, fileName):
        if not fileName:
            self.setFileName(None)
            return
        file = QFile(fileName)

        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            QMessageBox.warning(self, "Предупреждение", "Не удается открыть файл")
            self.setFileName(None)
            return

        in_stream = QTextStream(file)
        self.textEdit.setPlainText(in_stream.readAll())

        file.close()
        self.setFileName(fileName)
        self.setWindowModified(False)

    def setFileName(self, fileName):
        self.m_fileName = fileName
        self.setWindowTitle(
            f"{self.m_fileName if self.m_fileName else 'безымянный'}[*] - {QApplication.applicationName()}")

    def on_actionOpen_triggered(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Открыть документ", QDir.currentPath(), "Текстовые документы (*.txt)")
        if not fileName:
            return

        if not self.m_fileName and not self.isWindowModified():
            self.loadFile(fileName)
        else:
            new_window = TextEditor(fileName)
            new_window.show()

    def saveFileAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить документ",
                                                  self.m_fileName if self.m_fileName else QDir.currentPath(),
                                                  "Текстовые документы (*.txt)")
        if not fileName:
            return False
        self.setFileName(fileName)
        return self.saveFile()

    def saveFile(self):
        if not self.m_fileName:
            return self.saveFileAs()

        file = QFile(self.m_fileName)

        if not file.open(QIODevice.WriteOnly | QIODevice.Text):
            QMessageBox.warning(self, "Предупреждение", "Не удается сохранить файл")
            self.setFileName(None)
            return False

        out_stream = QTextStream(file)
        out_stream.write(self.textEdit.toPlainText())
        file.close()
        self.setWindowModified(False)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
