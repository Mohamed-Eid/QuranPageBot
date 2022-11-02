from datetime import datetime
from datetime import date

def days_between():
    first = datetime.strptime("2022-11-1", "%Y-%m-%d")
    today = datetime.strptime(str(date.today()), "%Y-%m-%d")
    return abs((first - today).days)
