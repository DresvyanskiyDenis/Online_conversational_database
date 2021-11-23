import re
import datetime
def generate_pseudo_anonymization(name:str, surname:str, date_of_recording:str):

    date_of_recording=date_of_recording.strip()
    name=name.strip()
    surname=surname.strip()

    pattern = re.compile("\d\d\.\d\d\.\d\d\d\d")
    if not pattern.match(date_of_recording):
        raise Exception('THe format for passing the date is dd.mm.yyyy. You have passed: %s'%(date_of_recording))

    day, month, year = date_of_recording.split('.')
    return name[0].lower()+name[-1].lower() \
           + str(int(day)*int(month)*int(year)) \
           + surname[0].lower()+surname[-1].lower()

def generate_pseudoanonimization_time_room(room_name:str)->str:
    today = datetime.date.today()

    # dd/mm/YY
    date = today.strftime("%d%m%y")
    hour = datetime.datetime.now().hour
    return date+str(hour)+room_name
