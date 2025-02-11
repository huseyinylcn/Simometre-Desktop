from PyQt5.QtWidgets import QApplication,QComboBox,QLineEdit,QFrame,QLabel,QVBoxLayout,QHBoxLayout,QWidget,QMainWindow,QPushButton,QMessageBox,QTextEdit
import sys
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from time import sleep

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from db import dbWrite
import threading
import multiprocessing




from portread  import seriport
#import write


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, axes = plt.subplots(3, 1)
        self.ax1, self.ax2, self.ax3 = axes 
        self.fig.patch.set_alpha(0)

        plt.tight_layout()  # Elemanları optimize et
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Marginleri sıfırla

        super().__init__(self.fig)



class SismometreDesktop(QMainWindow):
    def __init__(self):
        super().__init__()

    
        p1 = threading.Thread(target=self.graphicDraw,args=())
        p1.start()






        self.db = dbWrite()
        
        self.initUINavbar()
        self.y_data = np.zeros(1000)
        self.x_data = np.arange(len(self.y_data))
    



 
        self.y_data2 = np.zeros(1000)
        self.x_data2 = np.arange(len(self.y_data2))



        self.y_data3 = np.zeros(1000)
        self.x_data3 = np.arange(len(self.y_data3))
        self.GrapicPage()
        
        self.show()

    def initUINavbar(self):

        self.setWindowTitle("Sismometre Desktop ")
        self.setGeometry(700,100,1200,700)
        self.setStyleSheet("background-color:#252526 ;")

        self.main_wiget = QWidget(self)
        self.setCentralWidget(self.main_wiget)


        
        self.dikey = QVBoxLayout()


        self.frameTop = QFrame(self)
        self.frameTop.setFrameShape(QFrame.Box)
        self.frameTop.setContentsMargins(0,0,0,0)
        self.frameTop.setStyleSheet("background-color:#1E1E1E;")
        self.frameTop.setMinimumHeight(70)
        self.frameTop.setMaximumHeight(70)

        self.frameBottom = QFrame(self)
        self.frameBottom.setFrameShape(QFrame.StyledPanel)
        self.frameBottom.setStyleSheet("background-color:#252526 ;")


        self.dikey.addWidget(self.frameTop)
        self.dikey.addWidget(self.frameBottom)
        self.main_wiget.setLayout(self.dikey)

        layout = QHBoxLayout(self.frameTop)


        rightGroup = QHBoxLayout()
        rightGroup.setContentsMargins(0,0,50,0)

        leftGroup = QHBoxLayout()
        leftGroup.setAlignment(Qt.AlignLeft)
        leftGroup.setContentsMargins(50,0,0,0)

        self.logo = QLabel(self)
        logo = QPixmap('public/img/logo.png')
        xlogo = logo.scaled(70,100,Qt.KeepAspectRatio)
        self.logo.setPixmap(xlogo)
        leftGroup.addWidget(self.logo)
       
        self.main_btn = QPushButton("Ana Sayfa 🌍",self)
        self.main_btn.setFixedHeight(40)
        self.main_btn.setFixedWidth(110)
        self.main_btn.setStyleSheet("""font-weight: 400; font-size: 13px; color:#FFFFFF; background-color:#007ACC; """)
        self.main_btn.clicked.connect(self.GrapicPage)

        rightGroup.addWidget(self.main_btn)
        rightGroup.addSpacing(10)

        self.setting_btn = QPushButton("Ayarlar 🛠️🔧",self)
        self.setting_btn.setFixedHeight(40)
        self.setting_btn.setFixedWidth(120)
        self.setting_btn.setStyleSheet("""font-weight: 400; font-size: 13px; color:#FFFFFF; background-color:#007ACC; """)
        self.setting_btn.clicked.connect(self.settingPage)
        rightGroup.addWidget(self.setting_btn)
        rightGroup.addSpacing(10)


        self.report_btn = QPushButton("Raporlar 📋",self)
        self.report_btn.setFixedHeight(40)
        self.report_btn.setFixedWidth(120)
        self.report_btn.setStyleSheet("""font-weight: 400; font-size: 13px; color:#FFFFFF; background-color:#007ACC; """)
        self.report_btn.clicked.connect(self.reportPage)
        rightGroup.addWidget(self.report_btn)
        rightGroup.addSpacing(10)


        layout.addLayout(leftGroup)
        layout.addLayout(rightGroup)

    def GrapicPage(self):
        self.clearFrame()

        self.MotherLayout = QVBoxLayout(self.frameBottom)

        self.grapic = MplCanvas(self)
        self.MotherLayout.addWidget(self.grapic)


        self.gr1, = self.grapic.ax1.plot(self.x_data,self.y_data, linewidth=0.5,color="green")
        self.grapic.ax1.axis("off")

        self.gr2, = self.grapic.ax2.plot(self.x_data2,self.y_data2,color="red",linewidth=0.5)
        self.grapic.ax2.axis("off")

        self.gr3, =  self.grapic.ax3.plot(self.x_data3,self.y_data3,color="orange",linewidth=0.5)
        self.grapic.ax3.axis("off")






    
    def settingPage(self):
        self.clearFrame()
        self.data = self.db.dbInfoGet()

        self.MotherLayout = QVBoxLayout(self.frameBottom)
        
        

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        self.MotherLayout.addLayout(layout)

        settinBoxLeftİnfoBox = QFrame(self.frameBottom)
        settinBoxLeftİnfoBox.setMaximumWidth(700)
        settinBoxLeftİnfoBox.setMinimumWidth(250)

        settinBoxLeftİnfoBox.setStyleSheet("border: 1px solid #383737; background-color: ; border-radius:10px;")
        layout.addWidget(settinBoxLeftİnfoBox)
        leftLayout = QVBoxLayout(settinBoxLeftİnfoBox)
        leftLayout.setAlignment(Qt.AlignTop)


        infoLabel = QTextEdit()
        infoLabel.setStyleSheet("border:none")
        infoLabel.setReadOnly(True)
        infoLabel.setText("""            <h3 style="color: white; font-family: sans-serif; padding: 10px 10px 0px 10px; font-weight: 300; font-size: 53px;"> <b> What is Authentication ? </b> </h3>
            <p style="line-height: 19px; color: #d4d4d4; font-family: sans-serif; font-weight: 300;padding-left: 10px; font-size: 16px;" >Lorem ipsum dolor sit amet consectetur adipisicing elit. Et laboriosam excepturi perspiciatis sapiente quidem! Necessitatibus voluptatibus fuga dolorem quas totam fugiat ab corporis. Nihil nostrum dignissimos fugiat quae sequi cupiditate.</p>
            <p  style="line-height: 19px; color: #d4d4d4; font-family: sans-serif; font-weight: 300;padding-left: 10px; font-size: 16px;" >Lorem ipsum dolor sit amet consectetur adipisicing elit. Quasi odio, similique, reiciendis at possimus reprehenderit consequatur facilis voluptas nihil veritatis beatae, voluptate impedit cupiditate vero. Delectus eos itaque laudantium? Ducimus corporis nisi velit maxime illo aliquid quod, quisquam molestias animi totam exercitationem, deleniti assumenda placeat amet earum tempore facere adipisci qui voluptates sequi doloremque. Hic.</p>
    
            
    
            <h3 style="color: white; font-family: sans-serif; padding: 10px 10px 0px 10px; font-weight: 300; font-size: 23px;">What is Serial Port Configuration?</h3>
            <p style="line-height: 19px; color: #d4d4d4; font-family: sans-serif; font-weight: 300;padding-left: 10px; font-size: 16px;" >Lorem ipsum dolor sit amet consectetur adipisicing elit. Et laboriosam excepturi perspiciatis sapiente quidem! Necessitatibus voluptatibus fuga dolorem quas totam fugiat ab corporis. Nihil nostrum dignissimos fugiat quae sequi cupiditate.</p>
            <p style="line-height: 19px; color: #d4d4d4; font-family: sans-serif; font-weight: 300;padding-left: 10px; font-size: 16px;" >Lorem ipsum dolor sit amet consectetur adipisicing elit. Et laboriosam excepturi perspiciatis sapiente quidem! Necessitatibus voluptatibus fuga dolorem quas totam fugiat ab corporis. Nihil nostrum dignissimos fugiat quae sequi cupiditate.</p>

            <h3 style="color: white; font-family: sans-serif; padding: 10px 10px 0px 10px; font-weight: 300; font-size: 23px;">Important</h3>
            <p style="line-height: 19px; color: #d4d4d4; font-family: sans-serif; font-weight: 300;padding-left: 10px; font-size: 16px;" >Lorem ipsum dolor sit amet consectetur adipisicing elit. Et laboriosam excepturi perspiciatis sapiente quidem! Necessitatibus voluptatibus fuga dolorem quas totam fugiat ab corporis. Nihil nostrum dignissimos fugiat quae sequi cupiditate.</p>
            <p style="line-height: 19px; color: #d4d4d4; font-family: sans-serif; font-weight: 300;padding-left: 10px; font-size: 16px;" >Lorem ipsum dolor sit amet consectetur adipisicing elit. Et laboriosam excepturi perspiciatis sapiente quidem! Necessitatibus voluptatibus fuga dolorem quas totam fugiat ab corporis. Nihil nostrum dignissimos fugiat quae sequi cupiditate.</p>

    """)
        leftLayout.addWidget(infoLabel)
        

        # Kullanıcı Ayar Kutusu
        settingBox = QFrame(self.frameBottom)
        settingBox.setMaximumWidth(700)
        settingBox.setStyleSheet("border: 1px solid #383737; background-color: ; border-radius:10px;")
        layout.addWidget(settingBox)

        mainlayout = QVBoxLayout(settingBox)
        mainlayout.setAlignment(Qt.AlignTop)
      
        
        mainlayout.setSpacing(10)

        horizontal0 = QHBoxLayout()
        # horizontal.setAlignment(Qt.AlignLeft)
        horizontal0.setSpacing(10)
        horizontal0.setContentsMargins(10,10,0,0)

        horizontal = QHBoxLayout()
        # horizontal.setAlignment(Qt.AlignLeft)
        horizontal.setSpacing(10)
        horizontal.setContentsMargins(10,10,0,0)


        horizontal2 = QHBoxLayout()
        # horizontal2.setAlignment(Qt.AlignLeft)
        horizontal2.setSpacing(10)
        horizontal2.setContentsMargins(10,20,0,0)


        horizontal3 = QHBoxLayout()
        horizontal3.setSpacing(10)
        horizontal3.setContentsMargins(10,20,0,0)



        titleGroup = QVBoxLayout()
        titleLabel = QLabel("Settings 🛠️")
        titleLabel.setMinimumHeight(40)
        titleLabel.setStyleSheet("border-bottom:2px solid #c3c3c3; color:white;border-top:0px; border-left:0px;border-right:0px; border-radius:0px; font-size:19px; ")

        titleGroup.addWidget(titleLabel)


        userGroup = QVBoxLayout()
        userGroup.setAlignment(Qt.AlignTop)

        labelUser = QLabel("Username:")
        labelUser.setStyleSheet("color: white; font-size: 13px; font-weight: 100;border:none;")
        userGroup.addWidget(labelUser)


        self.username = QLineEdit()
        self.username.setStyleSheet("font-weight: 100; font-size:12px; padding: 3px; border-radius: 3px; background-color: #303031; border: 1px solid #383737; color: whitesmoke;")
        self.username.setPlaceholderText("Kullanıcı adınız..")
        self.username.setMaximumWidth(200)
        self.username.setMinimumHeight(30)
        self.username.setText(self.data[0])
        userGroup.addWidget(self.username)


        
       


        passGroup = QVBoxLayout()
        passGroup.setAlignment(Qt.AlignTop)

        labelPass = QLabel("Password:")
        labelPass.setStyleSheet("color: white; font-size: 13px; font-weight: 100;border:none;")
        passGroup.addWidget(labelPass)

        self.passw = QLineEdit()
        self.passw.setStyleSheet("font-weight: 100; padding: 3px; border-radius: 3px; background-color: #303031; border: 1px solid #383737; color: whitesmoke;")
        self.passw.setPlaceholderText(" Şifreniz..")
        self.passw.setEchoMode(QLineEdit.Password)
        self.passw.setText(self.data[1])
        self.passw.setMaximumWidth(200)
        self.passw.setMinimumHeight(30)
        passGroup.addWidget(self.passw)


        usernameBtnGroup = QVBoxLayout()


        labelusernamebtn =  QLabel()
        labelusernamebtn.setStyleSheet("border:none")
        usernameBtnGroup.addWidget(labelusernamebtn)

        self.usernameBtn = QPushButton("Save")
        self.usernameBtn.setStyleSheet("font-weight: 400; font-size: 13px; color:#FFFFFF; background-color:#007ACC; border-radius:2px;")
        self.usernameBtn.setMinimumHeight(30)
        self.usernameBtn.setMaximumWidth(100)
        self.usernameBtn.setMinimumWidth(90)
        self.usernameBtn.clicked.connect(lambda : self.db.dbuserPasw(username=self.username.text(), password=self.passw.text()))

        usernameBtnGroup.addWidget(self.usernameBtn)






        serialportgroup = QVBoxLayout()

    

        labelSerialPort = QLabel("Seri Port :")
        labelSerialPort.setStyleSheet("color: white; font-size: 13px; font-weight: 100;border:none;")
        serialportgroup.addWidget(labelSerialPort)

        
        self.serialport = QComboBox()
        self.serialport.setStyleSheet("""     
        QComboBox {
        font-weight: 100; 
        padding: 3px; 
        border-radius: 3px;  
        border: 1px solid #383737; 
      
        color: whitesmoke;
        background-color: #383737; /* Ana kutu arka planı */
     
        padding:0;
        padding-left:5px;
    }
   
    QComboBox QAbstractItemView {
        background-color: #383737; /* Açılır menü arka planı */
        color: whitesmoke;         /* Açılır menü metin rengi */
        border: 1px solid #383737; /* Açılır menü çerçevesi */
       
    
    }
    """)
        

        self.serialport.setCurrentText(self.data[2])
        self.serialport.setMinimumWidth(200)
        self.serialport.setMinimumHeight(30)
        serialportgroup.addWidget(self.serialport)
        self.serialnameFunc()


        boundSpeedGroup = QVBoxLayout()



        labelBoundSpeed = QLabel("Bound Speed : ")
        labelBoundSpeed.setStyleSheet("color: white; font-size: 13px; font-weight: 100;border:none;")
        boundSpeedGroup.addWidget(labelBoundSpeed)



        self.boundSpeed = QComboBox()
        self.boundSpeed.addItems(["300","1200","2400","48000","9600","19200","38400","57600","74880","115200","230400","250000","500000","1000000"])
        self.boundSpeed.setStyleSheet("""     
        QComboBox {
        font-weight: 100; 
        padding: 3px; 
        border-radius: 3px;  
        border: 1px solid #383737; 
      
        color: whitesmoke;
        background-color: #383737; /* Ana kutu arka planı */
     
        padding:0;
        padding-left:5px;
    }
   
    QComboBox QAbstractItemView {
        background-color: #383737; /* Açılır menü arka planı */
        color: whitesmoke;         /* Açılır menü metin rengi */
        border: 1px solid #383737; /* Açılır menü çerçevesi */
       
    
    }
    """)
        self.boundSpeed.setCurrentText(self.data[3])

        self.boundSpeed.setMinimumWidth(200)
        self.boundSpeed.setMinimumHeight(30)

        boundSpeedGroup.addWidget(self.boundSpeed)
        


        serialBtnGroup = QVBoxLayout()


        labelserialbtn =  QLabel()
        labelserialbtn.setStyleSheet("border:none")
        serialBtnGroup.addWidget(labelserialbtn)

        self.serialBtn = QPushButton("Save")
        self.serialBtn.setStyleSheet("font-weight: 400; font-size: 13px; color:#FFFFFF; background-color:#007ACC; border-radius:2px;")
        self.serialBtn.setMinimumHeight(30)
        self.serialBtn.setMaximumWidth(100)
        self.serialBtn.setMinimumWidth(90)
        self.serialBtn.clicked.connect(lambda : self.db.serialinfoSave(port=self.serialport.currentText() ,bound=self.boundSpeed.currentText() ))


        serialBtnGroup.addWidget(self.serialBtn)



        urlGroup = QVBoxLayout()
        urlLabel = QLabel("Url")
        urlLabel.setStyleSheet("color: white; font-size: 13px; font-weight: 100;border:none;")
        urlGroup.addWidget(urlLabel)



        self.urlInput = QLineEdit()
        self.urlInput.setStyleSheet("font-weight: 100; font-size:12px; padding: 3px; border-radius: 3px; background-color: #303031; border: 1px solid #383737; color: whitesmoke;")
        self.urlInput.setPlaceholderText("Example:http://www.example.com")
        self.urlInput.setMaximumWidth(400)
        self.urlInput.setMinimumHeight(30)
        self.urlInput.setText(self.data[5])
        urlGroup.addWidget(self.urlInput)



        urllBtnGroup = QVBoxLayout()
        urlBtnLabel = QLabel()
        urllBtnGroup.addWidget(urlBtnLabel)
        urlBtnLabel.setStyleSheet("border:none")


        self.urlBtn = QPushButton("Save")
        self.urlBtn.setStyleSheet("font-weight: 400; font-size: 13px; color:#FFFFFF; background-color:#007ACC; border-radius:2px;")
        self.urlBtn.setMinimumHeight(30)
        self.urlBtn.setMaximumWidth(100)
        self.urlBtn.setMinimumWidth(90)
        self.urlBtn.clicked.connect(lambda :  self.db.dbUrlSave(url=self.urlInput.text()) )

        urllBtnGroup.addWidget(self.urlBtn)









        
        
        horizontal0.addLayout(titleGroup)

        horizontal.addLayout(userGroup)
        horizontal.addLayout(passGroup)
        horizontal.addLayout(usernameBtnGroup)


        horizontal2.addLayout(serialportgroup)
        horizontal2.addLayout(boundSpeedGroup)
        horizontal2.addLayout(serialBtnGroup)

        horizontal3.addLayout(urlGroup)
        horizontal3.addLayout(urllBtnGroup)





        mainlayout.addLayout(horizontal0)

        mainlayout.addLayout(horizontal)
        mainlayout.addLayout(horizontal2)
        mainlayout.addLayout(horizontal3)

    
    def reportPage(self):
        self.clearFrame()
        reportMainLayout = QVBoxLayout(self.frameBottom)
        tt = QLabel("test")
        reportMainLayout.addWidget(tt)

    def serialnameFunc(self):
        portinfo = QSerialPortInfo.availablePorts()
        potrlist = []
        for i in portinfo:
            if not(i.description() in 'USB'):
         
                potrlist.append(i.portName())

        if len(potrlist) == 0:
            print("seri port yok")
            potrlist.append("seri port yok")
        self.serialport.addItems(potrlist)
    

    def clearFrame(self):
        self.frameBottom.deleteLater()
        self.frameBottom = QFrame(self)
        self.frameBottom.setFrameShape(QFrame.StyledPanel)
        self.frameBottom.setStyleSheet("background-color:#252526 ;")
        self.dikey.addWidget(self.frameBottom)
    
    
    def graphicDraw(self):
       
        while True:
            try:
                data = seriport.q.get()
                print(data)
                
                self.y_data = np.roll(self.y_data, -1)  
                self.y_data[-1] = float(data[0]) 
                self.y_data2 = np.roll(self.y_data2, -1)  
                self.y_data2[-1] = int(data[1]) 

                self.y_data3 = np.roll(self.y_data3, -1)  
                self.y_data3[-1] = int(data[2]) 


                self.gr1.set_ydata(self.y_data)
                self.gr2.set_ydata(self.y_data2)
                self.gr3.set_ydata(self.y_data3)


                self.grapic.ax1.set_ylim(min(self.y_data) , max(self.y_data)  )
                self.grapic.ax2.set_ylim(min(self.y_data2) - 5, max(self.y_data2) + 5)
                self.grapic.ax3.set_ylim(min(self.y_data3) - 5, max(self.y_data3) + 5)




                # self.grapic.fig.canvas.draw_idle()
                self.grapic.draw_idle()
            except Exception as  e:
                print(e)
                


        



if __name__ == '__main__':
    app  = QApplication(sys.argv)
    window = SismometreDesktop()


    sys.exit(app.exec())