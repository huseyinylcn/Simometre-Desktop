from  portread import seriport
import multiprocessing

import pandas as pd 
import time
import os
import csv




class Write:
    def __init__(self):
        self.yesterday = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}.csv"
        p1 = multiprocessing.Process(target=self.write)
        p1.start()

    def write(self):
        while True:
            if not  os.path.exists(self.yesterday):
                self.yesterday = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}.csv"
                open(self.yesterday,"x")
                default_data = {
                    "date": [],
                    "x": [],
                    "y": [],
                    "z": []
                }
                default_df = pd.DataFrame(default_data)
                default_df.to_csv(self.yesterday,index=False)

            with open(self.yesterday,mode="a",encoding="utf-8",newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["date", "x", "y", "z"])
                while True:
                    try:
                        data = seriport.q.get()
                        if self.yesterday != f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}.csv":
                            break

                        writer.writerow({"date":f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}.{int((time.time() % 1) * 1000)}","x":data[0],"y":data[1],"z":data[2]})
                    except:
                        pass
                    
            





wrt = Write()

