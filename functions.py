from models import Users,Posts
import hashlib
import random
import string

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

#a good thought but bad if any user is deleted 
def author():
    username = Users.query.all()
    list_of_users = []
    for user in username:
        list_of_users.append(user.user)
        print(user.user)
    return list_of_users

def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])

def hash_pwd(password, salt=None):
    if not salt:
        salt = make_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash,salt)


def pw_validate_hash(hash,pw):
    salt = hash.split(',')[1]
    if hash_pwd(pw,salt) ==  hash:
        return True
    return False









