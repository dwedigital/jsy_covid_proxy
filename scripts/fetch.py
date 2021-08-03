import requests
import json
from scripts import models
from datetime import datetime, date

def checkUpdate():
    data = requests.get('https://www.gov.je/datasets/listopendata?listname=COVID19&type=json&refresh=yes')
    data = json.loads(data.content)
    if (datetime.strptime(data['COVID19'][0]['Date'],"%Y-%m-%d").weekday()==6 or datetime.strptime(data['COVID19'][0]['Date'],"%Y-%m-%d").weekday()==5):
        return {"today":False}
    else:
        #convert string to date time
        current = datetime.strptime(data['COVID19'][0]['Date'],"%Y-%m-%d")
        #convert the date time object to just a date to compare against today
        current = current.date()
        #get today's dat as a standard date object
        today = date.today()
        return {"today":current==today}


def data():
    print("fetching")
    data = requests.get('https://www.gov.je/datasets/listopendata?listname=COVID19&type=json&refresh=yes')
    data = json.loads(data.content)

    # used to find the right index of data as weekends get no data so skip weekend data
    first = 0
    last = 1
    weekend = False

    # if latest day is a Sunday then make it Friday and make previous day Thursday
    if (datetime.strptime(data['COVID19'][0]['Date'],"%Y-%m-%d").weekday()==6):
        first = 2
        last=3
        weekend= True

    #if first day is Saturday then make latest day Friday and make previous day Thursday
    elif (datetime.strptime(data['COVID19'][0]['Date'],"%Y-%m-%d").weekday()==5):
        first = 1
        last = 2
        weekend = True

    # if first day is Monday then get Friday as the previous day
    elif (datetime.strptime(data['COVID19'][0]['Date'],"%Y-%m-%d").weekday()==0):
        last = 3
        weekend = True


    previousDay = models.DailyData(
    data['COVID19'][last]['DateTime'],
    data['COVID19'][last]['CasesCurrentKnownActiveCases'],
    data['COVID19'][last]['CasesSymptomatic'],
    data['COVID19'][last]['CasesNumberOfKnownDirectContactsOfCurrentActiveCases'],
    data['COVID19'][last]['CasesKnownCasesInHospital'],
    datetime.strptime(data['COVID19'][last]['Date'],"%Y-%m-%d").weekday()
    ).__dict__  

    latestDay = models.DailyData(
 data['COVID19'][first]['DateTime'],
    data['COVID19'][first]['CasesCurrentKnownActiveCases'],
    data['COVID19'][first]['CasesSymptomatic'],
    data['COVID19'][first]['CasesNumberOfKnownDirectContactsOfCurrentActiveCases'],
    data['COVID19'][first]['CasesKnownCasesInHospital'],
    datetime.strptime(data['COVID19'][first]['Date'],"%Y-%m-%d").weekday()
    
    ).__dict__



    chart = {
        "dates":[],
        "activeCases":[],
        "symptomaticCases":[],
        "hospitalCases":[],
    }
    dates = []
    active_cases = []


    for day in data['COVID19']:
        if (datetime.strptime(day['Date'],"%Y-%m-%d").weekday()==5 or datetime.strptime(day['Date'],"%Y-%m-%d").weekday()==6):
            pass
        else:
            
            chart['dates'].append(day['Date'])
            try:
                chart['activeCases'].append(int(day['CasesCurrentKnownActiveCases']) - int(day['CasesSymptomatic']))
                chart['symptomaticCases'].append(int(day['CasesSymptomatic']))
                chart['hospitalCases'].append(int(day['CasesKnownCasesInHospital']))
            except:
                chart['activeCases'].append(0)
                chart['symptomaticCases'].append(0)
                chart['hospitalCases'].append(0)


    return ([previousDay,latestDay,{"weekend":weekend}, chart])
