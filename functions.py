from models import Users,Posts
from app import app , db, request, redirect, render_template, session, flash

#functions to validate length, spaces, empty field, and '@' and '.' in email
def length(field):
    if len(field) > 4 and len(field) < 120:
        return True
    return False

def spaces(field):
    space = ' '
    if space in field:
        return False
    return True

def empty(field):
    emp = ''
    if field == emp:
        return False
    return True

def atdot_check(email):
    at = '@'
    dot = '.'
    if at in email and dot in email:
        return True
    return False

def use_pass(field):
    error = empty(field)
    if error == False:
        return False
    error = length(field)
    if error == False:
        return False
    error = spaces(field)
    if error == False:
        return False
    return True

def eml(field):
    error = length(field)
    if error == False:
        return False
    error = spaces(field)
    if error == False:
        return False
    error = atdot_check(field)
    if error == False:
        return False
    return True


def author():
    username = Users.query.all()
    list_of_users = []
    for user in username:
        list_of_users.append(user.user)
        print(user.user)
    return list_of_users














