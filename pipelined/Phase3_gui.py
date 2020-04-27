from PyQt5 import QtCore, QtGui, QtWidgets
import json
f=open('pipelined/gui_data.json','r+')
# f=open('gui_data.json','r+') #this one for testing, the above one for running from Master_runner.py
data=json.load(f)
print(data['pipreg'][0])
f.close()
nullout="---------------"
class Ui_Dialog(object):
    def find_clock_cycle(self):
        clk=int(self.textEdit_7.toPlainText())
        if clk==0:
            self.textEdit.setText(data['commands'][0])
            self.textEdit_2.setText(nullout)
            self.textEdit_3.setText(nullout)
            self.textEdit_4.setText(nullout)
            self.textEdit_5.setText(nullout)
            return
        clk-=1
        print()
        #fetch
        if data['pipreg'][clk][0]['isnull']==True:
            self.textEdit.setText(nullout)
        else:
            self.textEdit.setText(data['commands'][data['pipreg'][clk][0]['pc']])
        #decode
        if data['pipreg'][clk][1]['isnull']==True:
            self.textEdit_2.setText(nullout)
        else:
            self.textEdit_2.setText(data['commands'][data['pipreg'][clk][1]['pc']])

        #execute
        if data['pipreg'][clk][2]['isnull']==True:
            self.textEdit_3.setText(nullout)
        else:
            self.textEdit_3.setText(data['commands'][data['pipreg'][clk][2]['pc']])

        #Memory_read_write
        if data['pipreg'][clk][3]['isnull']==True:
            self.textEdit_4.setText(nullout)
        else:
            self.textEdit_4.setText(data['commands'][data['pipreg'][clk][3]['pc']])

        #reg_write
        if data['pipreg'][clk][4]['isnull']==True:
            self.textEdit_5.setText(nullout)
        else:
            self.textEdit_5.setText(data['commands'][data['pipreg'][clk][4]['pc']])
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        self.clk=0
        Dialog.resize(1188, 899)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(200, 170, 205, 621))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(450, 170, 391, 621))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_3.setObjectName("textEdit_3")
        self.verticalLayout_2.addWidget(self.textEdit_3)
        self.textEdit_2 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_2.addWidget(self.textEdit_2)
        self.textEdit_4 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_4.setObjectName("textEdit_4")
        self.verticalLayout_2.addWidget(self.textEdit_4)
        self.textEdit_5 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_5.setObjectName("textEdit_5")
        self.verticalLayout_2.addWidget(self.textEdit_5)
        self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(480, 50, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.next_clock_cycle)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(899, 390, 211, 121))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.textEdit_6 = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.textEdit_6.setObjectName("textEdit_6")
        self.verticalLayout_3.addWidget(self.textEdit_6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Fetch"))
        self.label_6.setText(_translate("Dialog", "Decode"))
        self.label_8.setText(_translate("Dialog", "Execute"))
        self.label_7.setText(_translate("Dialog", "Memory Read"))
        self.label_9.setText(_translate("Dialog", "Register Write"))
        self.textEdit_3.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_2.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Start"))
        self.label_2.setText(_translate("Dialog", "BTB Output"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RISCV_Simulator = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(RISCV_Simulator)
    RISCV_Simulator.show()
    sys.exit(app.exec_())

