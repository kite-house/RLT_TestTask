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
        self.resultData = {'dataset' : [], 'labels' : []}

    def group(self):
        '''Группируем данные по назначеному типу'''
        data = sorted(self.filter(), key = lambda x: x['dt']) #  сортировка данных по вермени.
        if self.group_type == 'month':
            return {month: list(group) for month, group in groupby(data, key=lambda x: f"{x['dt'].year}-{x['dt'].month}-1")}, '%Y-%m-01T00:00:00'
            
        elif self.group_type == 'day':
            return {day: list(group) for day, group in groupby(data, key=lambda x: f"{x['dt'].year}-{x['dt'].month}-{x['dt'].day}")}, '%Y-%m-%dT00:00:00'
        
        elif self.group_type == 'hour':
            return {hour: list(group) for hour, group in groupby(data, key=lambda x: f"{x['dt'].year}-{x['dt'].month}-{x['dt'].day}-{x['dt'].hour}")}, '%Y-%m-%dT%H:00:00'
    

    def filter(self):
        ''' Из всех обьектов фильтруем те которые подходят по данному диапозону времени '''
        data = [i for i in self.data if self.dt_from <= i['dt'] <= self.dt_upto]
        return data



group, formatTimeGroup = Agragation({
            "dt_from": "2022-09-01T00:00:00",
            "dt_upto": "2022-12-31T23:59:00",
            "group_type": "month"
            }).group()

for i in group:
    print(i)
