#############################################Note####################################################################
# RFID Reader:
# Created On: 20-09-2020  Version V1.0
# Author: Aditya Shrivastava
# GitHub ID: AdityaShrivastava03
# Run command "pip install pyserial"  to install serial
# Run command "pip install pyqt5" to install pyqt5
# Application tested successfully on EM-18 RFID Module (Hardware)
########################################################################################################################

import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from threading import Thread
import time

#####################################################################
class RFID_reader(QDialog):
    def __init__(self):
        super().__init__()

        print("========================================")
        print("|            RFID READER               |")
        print("|    ------------------------------    |")
        print("|   1) Scan available com ports        |")
        print("|   2) Read and decode raw RFID data   |")
        print("|                                      |")
        print("|                                      |")
        print("|           Author: Aditya Shrivastava |")
        print("|       GitHub ID: AdityaShrivastava03 |")
        print("|https://github.com/AdityaShrivastava03|")
        print("========================================\n")

        # Thread running flag
        self.flag = 0
        # Kill thread on exit
        global exit
        exit = 0
        dlg.pushButton_connect.clicked.connect(self.Connect_port)
        dlg.pushButton_scan.clicked.connect(self.Available_comport)
        dlg.pushButton_clear.clicked.connect(self.Clear)
        dlg.pushButton_disconnect.clicked.connect(self.Disconnect_port)
        dlg.pushButton_exit.clicked.connect(self.Exit)
        self.urlLink = "<a href=\"https://github.com/AdityaShrivastava03\">Author</a>"
        dlg.label_link.setOpenExternalLinks(True)
        dlg.label_link.setText(self.urlLink)
        # Call method on start up to print available com port
        self.Available_comport()

    # Clear All data
    def Clear(self):
        print("Clear Data")
        dlg.textEdit_output.clear()

    # Scan for available com ports
    def Available_comport(self):
        ports = list(serial.tools.list_ports.comports())
        print("List of available com ports:-")
        if ports != []:
            for self.p in ports:
                print(self.p)
                dlg.textEdit_output.append("Available com port: " + str(self.p))
        else:
            print("Com port not available please check drivers or cable connection")
            dlg.textEdit_output.append("Com port not available")

    # Connect with selected com port
    def Connect_port(self):
        global ser
        global read
        self.com_port = dlg.comboBox_com.currentText()
        self.baud_rate = dlg.comboBox_baud.currentText()
        try:
            # Com Port Disconnected
            if self.flag == 1:
                read = 0
                ser.close()
                print('Serial port closed')
            ser = serial.Serial(self.com_port, self.baud_rate,
                                bytesize=8, timeout=0.1, stopbits=serial.STOPBITS_ONE)
            time.sleep(1)
            read = 1
            dlg.textEdit_output.append("Connected:")
            if self.flag == 0:
                self.flag = 1
                serialThread.start()
            else:
                print('serialThread running')
        except (OSError, serial.SerialException):
            QMessageBox.information(
                None, "Warning", "Selected com port not available ")
            dlg.textEdit_output.append("Disconnected:")

    # Disconnect with serial com port
    def Disconnect_port(self):
        global ser
        global read
        if self.flag == 1:
            read = 0
            ser.close()
            dlg.textEdit_output.append("Disconnected:")

    # Exit application
    def Exit(self):
        global exit
        # Kill thread
        exit = 1
        print('Exit')
        time.sleep(0.5)
        dlg.close()
#######################################################################################
# Thread Class
class SerialThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.data_r = ""
    # RUN Thread
    def run(self):
        global ser
        global read
        global exit
        try:
            print("Thread Started!\n")
            while True:
                time.sleep(0.1)
                if exit == 1:
                    print('Thread Kill')
                    break
                if read == 1:
                    self.data_r = ser.readline()
                    if len(self.data_r) >= 1:
                        print("Raw Data: " + self.data_r.decode('Ascii'))
                        # Filter and decode RFID data
                        try:
                            self.x = self.data_r.decode('Ascii')
                            self.y = self.x[4] + self.x[5] + self.x[6] + \
                                self.x[7] + self.x[8] + self.x[9]
                            # Convert string hex to decimal
                            print('RFID:  ' +str(int(self.y, 16)))
                            dlg.textEdit_output.append(
                                'RFID:  ' + str(int(self.y, 16)))
                        except:
                            print("Garbage Data")
                            dlg.textEdit_output.append("Garbage Data: ")
        except (OSError, serial.SerialException):
            print("Com Port Disconnected")
            # Update read variable
            read = 0
            # Close communication
            ser.close()
            print('Serial port closed')
            dlg.textEdit_output.append("Com Port Disconnected:")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dlg = uic.loadUi("RFID_serial_read.ui")
    serialThread = SerialThread()
    RFID = RFID_reader()
    dlg.show()
    app.exec()
