import re
from dateutil import parser


POSSIBLE_DATE_KEYS_PARTS = ['date', 'дата']
RUSSIAN_MONTHS = {
    "января": "01", "февраля": "02", "марта": "03", "апреля": "04", 
    "мая": "05", "июня": "06", "июля": "07", "августа": "08", 
    "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"
}
POSSIBLE_TIME_PEDIOD_KEYS_PARTS = ['period', 'период', 'срок']


def convert_date_to_standard_format(date_str: str) -> str:
    clean_str = re.sub(r'[^\w\s\.]', '', date_str)
    clean_str = re.sub(r'\bгода\b|\bгод\b', '', clean_str)
    for ru_month, num_month in RUSSIAN_MONTHS.items():
        clean_str = clean_str.replace(ru_month, num_month)
    try:
        parsed_date = parser.parse(clean_str, dayfirst=True)
        return parsed_date.strftime("%d.%m.%Y")
    except ValueError:
        return "Invalid date"


def convert_time_period_to_format(time_str: str) -> str:
    text_numbers = {
        'один': 1, 'одна': 1, 'одного': 1,
        'два': 2, 'две': 2, 'двух': 2,
        'три': 3, 'трёх': 3, 'четыре': 4, 'пять': 5, 'шесть': 6,
        'семь': 7, 'восемь': 8,'девять': 9, 'десять': 10,
        'полгода': '6 месяцев'
    }

    cleaned_str = re.sub(r'[^\w\s]', '', time_str.lower())
    
    years, months, weeks, days = 0, 0, 0, 0

    for number, value in text_numbers.items():
        if number in cleaned_str:
            cleaned_str = cleaned_str.replace(number, str(value))
    
    if 'год' in cleaned_str or 'лет' in cleaned_str:
        years = int(re.findall(r'\d+', cleaned_str)[0])
    if 'месяц' in cleaned_str:
        months = int(re.findall(r'\d+', cleaned_str)[0])
    if 'недел' in cleaned_str:
        weeks = int(re.findall(r'\d+', cleaned_str)[0])
    if any((d in cleaned_str for d in ('день', 'дней', 'дня'))):
        days = int(re.findall(r'\d+', cleaned_str)[0])

    return f"{years}_{months}_{weeks}_{days}"
