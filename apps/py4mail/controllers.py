
import datetime
import random

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_username
from py4web.utils.form import Form, FormStyleBulma

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(get_emails_url = URL('get_emails'), get_sent_url = URL('get_sent'))

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
    return dict(emails=emails)

#still under works
@action("get_sent")
@action.uses(db, auth.user)
def get_sent():
    emails = db(db.emails.sender_id == auth.user_id).select().as_list()
    # Retrieve sender names from auth_user table
    receiver_ids = [email['receiver_id'] for email in emails]
    receiver_info = db(db.auth_user.id.belongs(receiver_ids)).select()
    receiver_names = {receiver.id: f"{receiver.first_name} {receiver.last_name}" for receiver in receiver_info}

    # Retrieve receiver name from auth_user table
    sender_info = db.auth_user[auth.user_id]
    sender_name = f"{sender_info.first_name} {sender_info.last_name}"

    # Update emails list with sender and receiver names, and elapsed time
    for email in emails:
        email['receiver_name'] = receiver_names.get(email['receiver_id'])
        email['sender_name'] = sender_name
        email['elapsed_time'] = get_elapsed_time(email['sent_at'])
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

@action("move_to_trash")
@action.uses(db, auth.user)
def move_to_trash():
    mail_id = request.json.get('id')
    email = db.emails(mail_id)
    email.update_record(isTrash=True)

@action("delete")
@action.uses(db, auth.user)
def delete():
    pass
    
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

@action('compose_mail', method=['GET', 'POST'])
@action.uses('compose_mail.html', url_signer, db, session, auth.user)
def compose_mail():
    form = Form(db.emails, csrf_session = session, formstyle = FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)   
