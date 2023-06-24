from .models import *
import datetime
from dateutil import tz

special_table = {'!', '@', '#', '$', '%', '^', '&' , '*', '(' , ')'}  

# local time as datetime object
def get_current_time():
    return datetime.datetime.now(datetime.timezone.utc)

# converts a datetime object into local time and returns a string
def convert_datetime(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    old_time= time.replace(tzinfo=from_zone)
    new_time = old_time.astimezone(to_zone)
    return new_time.strftime('%#m-%#d-%Y %#I:%M %p')

# determines valid passwords
def check_valid_password(password):
    if (' ' in password):
        return False
    special_character_checker = False
    uppercase_characters = 0
    lowercase_characters = 0
    for character in password:
        if character.isupper() and uppercase_characters == 0:
            uppercase_characters += 1
        if character.islower() and lowercase_characters == 0:
            lowercase_characters += 1
        if character in special_table:
            special_character_checker = True
            break
    check_digit = any(char.isdigit for char in password)
    if check_digit == False or len(password) < 12 or uppercase_characters < 1 or lowercase_characters < 1 or special_character_checker == False: 
        return False
    return True
