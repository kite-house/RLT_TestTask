from pymongo import MongoClient
from datetime import datetime, timedelta
from itertools import groupby
class Agrigation:
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
    
        else:
            raise Exception('group does not match')

    def filter(self):
        ''' Из всех обьектов фильтруем те которые подходят по данному диапозону времени '''
        data = [i for i in self.data if self.dt_from <= i['dt'] <= self.dt_upto]
        return data

    def omissions(self):
        ''' Исправление пропусков дат, которых нету в бд '''
        start_date = self.dt_from
        range_time = []

        while start_date <= self.dt_upto: # Диапозон времени
            if self.group_type == 'day':
                range_time.append(f'{start_date.year}-{start_date.month}-{start_date.day}')
                start_date += timedelta(days=1)
            if self.group_type == 'hour':
                range_time.append(f'{start_date.year}-{start_date.month}-{start_date.day}-{start_date.hour}')
                start_date += timedelta(hours=1)
            if self.group_type == 'month':
                range_time.append(f'{start_date.year}-{start_date.month}-1')
                start_date += timedelta(days=1)

        sorted_data = {}
        groupData, self.formatTime = self.group()
        if range_time != list(groupData.values()): 
            for time in range_time:
                try:
                    sorted_data[time] = groupData[time] # Пересоздаем список, для сортировки его данных
                except Exception: # Если обьект не обнаружен, добавляем 0 значение
                    if self.group_type == 'day':
                        sorted_data[time] = [{'__id': 'Objectid(None)','value': 0, 'dt': datetime(int(time.split('-')[0]), int(time.split('-')[1]), int(time.split('-')[2]))}]
                    if self.group_type == 'hour':
                        sorted_data[time] = [{'__id': 'Objectid(None)','value': 0, 'dt': datetime(int(time.split('-')[0]), int(time.split('-')[1]), int(time.split('-')[2]), int(time.split('-')[3]),)}]
                    if self.group_type == 'month':
                        sorted_data[time] = [{'__id': 'Objectid(None)','value': 0, 'dt': datetime(int(time.split('-')[0]), int(time.split('-')[1]), int(time.split('-')[2]))}]

        return sorted_data

    def dataset(self):
        '''Создание готового датасета'''
        sortedData = self.omissions()
        for time in sortedData: # Получаем группы по времени(ключи от словаря)
            value = 0
            for data in sortedData[time]: # получаем данные в этой группе
                value += data['value']

            self.resultData['labels'].append(datetime.strftime(sortedData[time][0]['dt'], self.formatTime))
            self.resultData['dataset'].append(value)

        return str(self.resultData) # исправить ошибку с пропусками