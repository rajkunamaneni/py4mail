"""
This file defines the database models
"""

import datetime
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
    Field('sent_at', 'datetime', default=get_time()),
    Field('isStarred', 'boolean', default=False),
    Field('isTrash', 'boolean', default=False),
)

db.define_table(
    'blocked',
    Field('created_by', 'reference auth_user', default=lambda: get_user_email()),
    Field('blocked_id', 'reference auth_user'),
)

db.commit()

# UNCOMMENT THIS TO DELETE ALL ENTRIES IN THE EMAILS TABLE
table = db.emails
db(table.id > 0).delete()
db.commit()
