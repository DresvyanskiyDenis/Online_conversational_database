
def generate_pseudo_anonimization(name:str, surname:str, birth_date:str):
    day, month, year = birth_date.split('.')
    return name[0].lower()+name[-1].lower() \
           + str(int(day)*int(month)*int(year)) \
           + surname[0].lower()+surname[-1].lower()

