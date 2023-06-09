
import datetime
import random

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_username




@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(get_emails_url = URL('get_emails'),
                trash_url = URL('move_to_trash'),
                delete_url = URL('delete'),
                star_url = URL('star'),
                get_sent_url = URL('get_sent'),
                get_compose_url = URL('compose_mail'),
                get_users_url = URL('get_users'),
                blocked_url = URL('blocked'),
                cant_send_url = URL('cant_send'),)

@action("get_emails")
@action.uses(db, auth.user)
def get_emails():
    emails = db(db.emails.receiver_id == auth.user_id).select().as_list()
    blocked_list = db(db.blocked.blocked_id == auth.user_id).select().as_list()

    # Retrieve sender names from auth_user table
    sender_ids = [email['sender_id'] for email in emails]
    sender_info = db(db.auth_user.id.belongs(sender_ids)).select()
    sender_names = {sender.id: f"{sender.first_name} {sender.last_name}" for sender in sender_info}
    sender_emails = {sender.id: sender.email for sender in sender_info}

    # Retrieve receiver name from auth_user table
    receiver_info = db.auth_user[auth.user_id]
    receiver_name = f"{receiver_info.first_name} {receiver_info.last_name}"

    # Add sender, receiver names, and elapsed time to the list
    for email in emails:
        email['sender_name'] = sender_names.get(email['sender_id'])
        email['sender_email'] = sender_emails.get(email['sender_id'])
        email['receiver_name'] = receiver_name
        email['receiver_email'] = receiver_info.email
        email['elapsed_time'] = get_elapsed_time(email['sent_at'])
    return dict(emails=emails,
                blocked_list=blocked_list,)

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

@action("get_sent")
@action.uses(db, auth.user)
def get_sent():
    emails = db(db.emails.sender_id == auth.user_id).select().as_list()
    # Retrieve sender names from auth_user table
    receiver_ids = [email['receiver_id'] for email in emails]
    receiver_info = db(db.auth_user.id.belongs(receiver_ids)).select()
    receiver_names = {receiver.id: f"{receiver.first_name} {receiver.last_name}" for receiver in receiver_info}
    receiver_emails = {receiver.id: receiver.email for receiver in receiver_info}

    # Retrieve receiver name from auth_user table
    sender_info = db.auth_user[auth.user_id]
    sender_name = f"{sender_info.first_name} {sender_info.last_name}"

    # Add sender, receiver names, and elapsed time to the list
    for email in emails:
        email['receiver_name'] = receiver_names.get(email['receiver_id'])
        email['receiver_email'] = receiver_emails.get(email['receiver_id'])
        email['sender_name'] = sender_name
        email['sender_email'] = sender_info.email
        email['elapsed_time'] = get_elapsed_time(email['sent_at'])
    return dict(emails=emails)

@action("move_to_trash", method="POST")
@action.uses(db, auth.user)
def move_to_trash():
    mail_id = request.json.get('id')
    email = db.emails(mail_id)
    email.update_record(isTrash=True)
    email.updated_record(isStarred=False)
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
    block_user = db.blocked.insert(created_by=auth.user_id, blocked_id=user_id)
    blocked_list = db(db.blocked.blocked_id == auth.user_id).select().as_list()
    return dict(blocked_list = blocked_list,)


@action('compose_mail', method=['POST'])
@action.uses(db, session, auth.user)
def compose_mail():
    email = request.json

    if email is None:
        return "Failure"
    # # Extract email fields
    receiver_mail = email.get('receiver_mail')
    title = email.get('title')
    content = email.get('content')

    # Get sender and receiver user objects
    sender = auth.get_user()
    sender_id = sender["id"] if sender else None

    receiver = db(db.auth_user.email == receiver_mail).select().first()
    receiver_id = receiver["id"] if receiver else None

    # Insert the email data into the database
    db.emails.insert(
        sender_id=sender_id,
        receiver_id=receiver_id,
        title=title,
        message=content,
        sent_at=datetime.datetime.utcnow(),
        isStarred=False,
        isTrash=False
    )
    return "Mail sent successfully"

@action("get_users")
@action.uses(db, auth.user)
def get_users():
    # Implement. Lists all the users 
    rows = db(db.auth_user).select().as_list()
    return dict(users=rows)

@action("cant_send")
@action.uses(db, auth.user)
def cant_send():
    i_blocked = db(db.blocked.created_by == auth.user_id).select().as_list()
    blocked_me = db(db.blocked.blocked_id == auth.user_id).select().as_list()
    return dict(i_blocked=i_blocked,
                blocked_me=blocked_me)
