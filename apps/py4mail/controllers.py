
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
    return dict(get_emails_url = URL('get_emails'),
                trash_url = URL('move_to_trash'),
                delete_url = URL('delete'),
                star_url = URL('star'),)

@action("get_emails")
@action.uses(db, auth.user)
def get_emails():
    emails = db(db.emails.receiver_id == auth.user_id).select().as_list()

    # Retrieve sender names from auth_user table
    sender_ids = [email['sender_id'] for email in emails]
    sender_info = db(db.auth_user.id.belongs(sender_ids)).select()
    sender_names = {sender.id: f"{sender.first_name} {sender.last_name}" for sender in sender_info}

    # Retrieve receiver name from auth_user table
    receiver_info = db.auth_user[auth.user_id]
    receiver_name = f"{receiver_info.first_name} {receiver_info.last_name}"

    # Update emails list with sender and receiver names, and elapsed time
    for email in emails:
        email['sender_name'] = sender_names.get(email['sender_id'])
        email['receiver_name'] = receiver_name
        email['elapsed_time'] = get_elapsed_time(email['sent_at'])
    print(emails)
    return dict(emails=emails)

def get_elapsed_time(created_on):
    now = datetime.datetime.utcnow()

    # Calculate the time difference in seconds
    elapsed = now - created_on
    elapsed_seconds = elapsed.total_seconds()

    # Format the elapsed time based on different conditions
    if elapsed_seconds < 60:
        elapsed_time = "Just now"
    elif elapsed_seconds < 3600:
        minutes = int(elapsed_seconds / 60)
        elapsed_time = f"{minutes} min{'s' if minutes > 1 else ''} ago"
    elif created_on.year < now.year:
        elapsed_time = created_on.strftime("%m/%d/%Y")
    elif created_on.date() == now.date():
        elapsed_time = created_on.strftime("%I:%M %p")
    else:
        elapsed_time = created_on.strftime("%B %d")

    return elapsed_time

@action("move_to_trash", method="POST")
@action.uses(db, auth.user)
def move_to_trash():
    mail_id = request.json.get('id')
    email = db.emails(mail_id)
    email.update_record(isTrash=True)
    return dict(mail_id=mail_id,)


@action("delete", method="POST")
@action.uses(db, auth.user)
def delete():
    mail_id = request.json.get('id')
    db(db.emails.id == mail_id).delete()
    return dict(mail_id=mail_id,)

@action("star", method="POST")
@action.uses(db, auth.user)
def star():
    starred = False
    mail_id = request.json.get('id')
    email = db.emails(mail_id)
    if email.isStarred == True:
        email.update_record(isStarred=False)
    else:
        email.update_record(isStarred = True)
        starred = True
    return dict(mail_id = mail_id,
                starred = starred)

    
@action("blocked", method="POST")
@action.uses(db, auth.user)
def blocked():
    data = request.json
    user_id = data.get('id')
    block_user = db((db.blocked.created_by == auth.user_id) & (db.blocked.blocked_id == auth.user_id)).select().first()
    if block_user:
        block_user.delete_record(db.blocked[0]['id'])
    else:
        db.blocked.insert(created_by=auth.user_id, blocked_id=user_id)