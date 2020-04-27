from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import json
f=open('pipelined/gui_data.json','r+')
# f=open('gui_data.json','r+') #this one for testing, the above one for running from Master_runner.py
data=json.load(f)
print(data['pipreg'][0])
f.close()
nullout="---------------"
class Ui_Dialog(object):
    def setval(self):
        clk=self.clk
        if clk==0:
            self.textEdit.setText(data['commands'][data['pipreg'][0][0]['pc']])
            self.textEdit_2.setText(nullout)
            self.textEdit_3.setText(nullout)
            self.textEdit_4.setText(nullout)
            self.textEdit_5.setText(nullout)
            self.label_5.setText(str(clk))
            return
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
        self.textEdit_6.setText(str(data['btb_output'][clk])) 
        self.label_5.setText(str(clk))        
    def out_of_bound(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Clock cycle does not exist!!")
        msg.setWindowTitle("Out of bound error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    def find_clock_cycle(self):
        print(len(data['btb_output']))
        clk=int(self.textEdit_7.toPlainText())
        if(clk>len(data['btb_output'])):
            self.out_of_bound()
            return
        self.clk=clk
        self.setval()
    def next_clock_cycle(self):
        print(len(data['btb_output']))
        if self.clk==len(data['btb_output']):
            self.out_of_bound()
            return
        self.clk+=1
        self.setval()
    def prev_clock_cycle(self):
        print(self.clk)
        if self.clk==0:
            self.out_of_bound()
            return
        self.clk-=1
        self.setval()
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1515, 899)
        self.clk=0
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
        self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.textEdit_2 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setFont(font)
        self.verticalLayout_2.addWidget(self.textEdit_2)
        self.textEdit_3 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setFont(font)
        self.verticalLayout_2.addWidget(self.textEdit_3)
        self.textEdit_4 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_4.setObjectName("textEdit_4")
        self.textEdit_4.setFont(font)
        self.verticalLayout_2.addWidget(self.textEdit_4)
        self.textEdit_5 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_5.setObjectName("textEdit_5")
        self.textEdit_5.setFont(font)
        self.verticalLayout_2.addWidget(self.textEdit_5)
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
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 50, 511, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.textEdit_7 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_7.setGeometry(QtCore.QRect(720, 50, 361, 70))
        self.textEdit_7.setObjectName("textEdit_7")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(930, 160, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 810, 121, 81))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(546, 806, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_4.setFont(font)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(600, 850, 67, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(920, 810, 121, 81))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton.clicked.connect(self.find_clock_cycle)
        self.pushButton_2.clicked.connect(self.prev_clock_cycle)
        self.pushButton_3.clicked.connect(self.next_clock_cycle)
        self.setval()
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
        self.label_2.setText(_translate("Dialog", "BTB Output"))
        self.label_3.setText(_translate("Dialog", "Which clock cycle state would you like to see??"))
        self.pushButton.setText(_translate("Dialog", "Show"))
        self.pushButton_2.setText(_translate("Dialog", "Prev"))
        self.label_4.setText(_translate("Dialog", "Current Cycle"))
        self.label_5.setText(_translate("Dialog", "0"))
        self.pushButton_3.setText(_translate("Dialog", "Next"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RISCV_Simulator = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(RISCV_Simulator)
    RISCV_Simulator.show()
    sys.exit(app.exec_())
