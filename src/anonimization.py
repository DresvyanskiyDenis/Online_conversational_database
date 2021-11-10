import re

def generate_pseudo_anonimization(name:str, surname:str, birth_date:str):

    birth_date=birth_date.strip()
    name=name.strip()
    surname=surname.strip()

    pattern = re.compile("\d\d\.\d\d\.\d\d\d\d")
    if not pattern.match(birth_date):
        raise Exception('THe format for passig the date is dd.mm.yyyy. You have passed: %s'%(birth_date))

    day, month, year = birth_date.split('.')
    return name[0].lower()+name[-1].lower() \
           + str(int(day)*int(month)*int(year)) \
           + surname[0].lower()+surname[-1].lower()
