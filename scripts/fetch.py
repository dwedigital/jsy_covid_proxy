import requests
import json
from scripts import models


def data():
    data = requests.get('https://www.gov.je/datasets/listopendata?listname=COVID19&type=json&refresh=yes')
    data = json.loads(data.content)

    return models.DailyData(
        data['COVID19'][0]['DateTime'],
    data['COVID19'][0]['CasesCurrentKnownActiveCases'],
    data['COVID19'][0]['CasesDailyNewConfirmedCases'])
