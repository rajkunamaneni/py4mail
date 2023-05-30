
import datetime
import random

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_username

# url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(get_emails_url = URL('get_emails'))

@action("get_emails")
@action.uses(db, auth.user)
def get_emails():
    all_emails = db(db.emails.receiver_id == auth.user_id).select().as_list()
    star_emails = db((db.emails.receiver_id == auth.user_id) & (db.emails.isStarred == True)).select().as_list()
    trash_emails = db((db.emails.receiver_id == auth.user_id) & (db.emails.isTrash == True)).select().as_list()
    return dict(emails=emails,
                star_emails=star_emails,
                trash_emails=trash_emails,
    )

@action("move_to_trash")
@action.uses(db, auth.user)
def move_to_trash():
    mail_id = request.json.get('id')
    email = db.emails(mail_id)
    email.update_record(isTrash=True)

@action("delete")
@action.uses(db, auth.user)
def delete():
    


    
    
@action("blocked")
@action.uses(db, auth.user)
def blocked():
    data = request.json
    user_id = data.get('id')
    block_user = db((db.blocked.created_by == auth.user_id) & (db.blocked.blocked_id == auth.user_id)).select().first()
    if block_user:
        block_user.delete_record(db.blocked[0]['id'])
    else:
        db.blocked.insert(created_by=auth.user_id, blocked_id=user_id)


## Delete later. Added for context of understanding blocked function
# db.define_table(
#     'blocked',
#     Field('created_by', 'reference auth_user', default=lambda: get_user_email()),
#     Field('blocked_id', 'reference auth_user'),
# )