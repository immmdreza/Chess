from datetime import datetime

def dur_time(func):
    def wapper():
        s = datetime.utcnow()
        func()
        e = datetime.utcnow() - s
        print('Durection: ', e)
    return wapper