from pymongo import MongoClient
from datetime import datetime
from itertools import groupby
class Agragation:
    def __init__(self, request):
        client = MongoClient('mongodb://localhost:27017/')
        self.data = client['TestWork'].get_collection('sampleDB').find()
        self.dt_from = datetime.strptime(request['dt_from'].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        self.dt_upto = datetime.strptime(request['dt_upto'].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        self.group_type = request['group_type']

    def filter(self):
        ''' Из всех обьектов фильтруем те которые подходят по данному диапозону времени '''
        data = [i for i in self.data if self.dt_from <= i['dt'] <= self.dt_upto]
        return data

filter = Agragation({
            "dt_from": "2022-09-01T00:00:00",
            "dt_upto": "2022-12-31T23:59:00",
            "group_type": "month"
            }).filter()

for i in filter:
    print(i)
