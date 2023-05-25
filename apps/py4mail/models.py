"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_username():
    return auth.current_user.get('username') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


db.define_table(
    'emails',
    
    Field('sender_id', 'reference auth_user'),
    Field('receiver_id', 'reference auth_user'),
    Field('title', 'text'),
    Field('message', 'text'),
    Field('sent_at', 'datetime', default=get_time())
)
    
stared = db.define_table(
    'stared',
    Field('r_username', 'reference auth_user'),
    Field('s_username', 'reference auth_user'), 
    Field('email_id', 'reference auth_user'),
    Field('receiver_id', 'reference auth_user'),
    Field('title', 'text'),
    Field('message', 'text'),
    Field('sent_at', 'datetime', default=get_time()),
    Field('starred', 'boolean')
)

trash = db.define_table(
    'trash',
    Field('r_username', 'reference auth_user'),
    Field('s_username', 'reference auth_user'), 
    Field('sender_id', 'reference auth_user'),
    Field('receiver_id', 'reference auth_user'),
    Field('sender_email', 'text'),
    Field('receiver_email', 'text'),
    Field('title', 'text'),
    Field('message', 'text'),
    Field('sent_at', 'datetime', default=get_time()),
)
db.commit()

def add_emails_for_testing():
    db.emails.insert(
                    sender_id=17,
                    receiver_id=16,
                    title='helllllllo',
                    message='just saying hi!!! :)',
                    )
    db.emails.insert(
                    sender_id=17,
                    receiver_id=16,
                    title='whats up',
                    message='just saying hi again!!! :)',
                    )
    db.commit()

add_emails_for_testing()




