
import datetime
import random

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_username

# url_signer = URLSigner(session)

# Some constants.
MAX_RETURNED_USERS = 20 # Our searches do not return more than 20 users.
MAX_RESULTS = 20 # Maximum number of returned meows. 

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(get_emails_url = URL('get_emails'))

@action("get_emails")
@action.uses(db, auth.user)
def get_emails():
    emails = db(db.emails.receiver_id == auth.user_id).select().as_list() 
    print(emails)
    return dict(emails=emails
    )

@action("get_starred")
@action.uses(db, auth.user)
def get_starrred():
    emails = db(db.stared.receiver_id == auth.user_id).select().as_list() 
    return dict(emails=emails)



@action("get_trash")
@action.uses(db, auth.user)
def get_trash():
    emails = db(db.trash.receiver_id == auth.user_id).select().as_list()
    return dict(emails=emails)

# @action("set_follow", method="POST")
# @action.uses(db, auth.user)
# def set_follow():
#     # Implement.
#     return "ok"
