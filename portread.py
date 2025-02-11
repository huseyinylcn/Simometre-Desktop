import multiprocessing
import serial
from db import dbWrite




class SerialPortRead:
    _instance = None 
    q = multiprocessing.Queue()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            p1 = multiprocessing.Process(target=self.read,args=(self.q,))
            p1.start()

        
    def read(self,q):
        db = dbWrite()
        dbİnfo = db.dbInfoGet()
        while True:
           try:
                self.serial_port = serial.Serial(f'/dev/{dbİnfo[2]}', int(dbİnfo[3]), timeout=3)
                print("bağlandı")
           except Exception as e:
            #    print("bağlanamadı")
            pass
               
           else:
               while True:
                    try:
                        q.put(self.serial_port.readline().decode().strip().split("*"))
                    except Exception as e:
                        self.serial_port.close()
                        break



seriport = SerialPortRead()




