from datetime import datetime
#from dotenv import load_dotenv
import calendar
import os

#load_dotenv()


class InvoicePath(object):

    def __init__(self, patient, index):
        self.date = patient['date']
        self.medical = patient['medical']
        self.name = patient['name']
        self.index = index

    def convert(self):
        self.date  =  datetime.strptime(self.date, '%d.%m.%Y')
        return self.date

    def date_digits(self, date_component):
        if date_component == 'year':
            return self.date.year
        elif date_component == 'month':
            return self.date.month
        elif date_component == 'day':
            return self.date.day


    def generate(self):
       # date_component = self.date_digits(date_component)
        self.date = self.convert()
        self.path = os.getenv("OWNCLOUD_URL") +'/' + str(self.medical).upper() + '_' + os.getenv("USERNAME") + str(self.date_digits('year')) + '/' + str(self.date_digits('month')) + calendar.month_name[self.date_digits('month')] + str(self.date_digits('year')) + '/' + str(self.date_digits('month')) + '_' + str(self.index) + self.name


        return self.path
   # os.getenv("OWNCLOUD_URL") + 
   # os.getenv("SYSTEM_URL")
   # def patient(self, name):
   #     self.date 




#patient = {'case': 'asdfasdfa',
       #    'csrf_token':'ImU5NjFiYWEwN2Y1MGUyMmFiZDBkY2ZiYTQ5NDgxYzdiN2NlODQ2MDQi.XpVy6A.zOXe-xkr0gUZJroWUQHqVEoGxu0','date':
       #    '14.04.2020', 'medical': 'mva', 'name': 'lotharrrr hoo', 'po': '423423423'}
#date = InvoicePath(patient, 3)
#print(date)
#date_convert = date.generate()

#print(date_convert)


