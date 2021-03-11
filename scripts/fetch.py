import requests
import json
from scripts import models


def data():
    data = requests.get('https://www.gov.je/Datasets/ListOpenData?ListName=COVID19CasesChart&type=json')
    data = json.loads(data.content)
    return models.DailyData(
        data['COVID19CasesChart'][0]['DateTime'],
    data['COVID19CasesChart'][0]['KnownActiveCases'],
    data['COVID19CasesChart'][0]['Newcasesreported'])
