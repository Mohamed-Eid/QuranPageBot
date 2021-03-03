from datetime import datetime
from datetime import date

def days_between():
    first = datetime.strptime("2021-2-26", "%Y-%m-%d")
    today = datetime.strptime(str(date.today()), "%Y-%m-%d")
    return abs((first - today).days)
