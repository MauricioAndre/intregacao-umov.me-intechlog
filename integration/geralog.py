from datetime import datetime
def salvalog(result):
    arquivo=open('log.txt','a')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    arquivo.write(dt_string)
    arquivo.write(result)
    arquivo.write('\n')
    arquivo.close()