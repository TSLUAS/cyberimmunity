import pandas as pd 
import time 

def get_log_data() -> pd.DataFrame:
    data = pd.read_excel("./log.xlsx")
    return data

def send_single_frame() -> None:
    df = get_log_data()
    for index, row in df.iterrows():

        # точка выхода из программы отправки телеметрии
        print(row)

        time.sleep(1)
    return 

if __name__ == '__main__':
    send_single_frame()