import imaplib
import email


def login_mail(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    return mail


def get_mail_ids_from_inbox(connection):
    connection.select('inbox')
    # search and return uids instead
    # result, data = connection.uid('search', None, "ALL")
    result, data = connection.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    return [first_email_id, latest_email_id]


def read_raw_email(raw_email):
    msg = email.message_from_bytes(raw_email[0][1])
    email_subject = msg['subject']
    email_from = msg['from']
    print('From : ' + email_from + '\n')
    print('Subject : ' + email_subject + '\n')
    body = get_first_text_block(msg)
    print(body)

# note that if you want to get text content (body) and the email contains
# multiple payloads (plaintext/ html), you must parse each message separately.
# use something like the following: (taken from a stackoverflow post)


def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()


def iterate_all_emails(connection, first_id, last_id):
    for i in range(last_id, first_id, -1):
        result, data = connection.fetch(str(i), '(RFC822)')
        read_raw_email(data)


def run():
    connection = login_mail('testest@gmail.com', 'abcdefghijklmnop')
    email_ids = get_mail_ids_from_inbox(connection)
    first_email_id, latest_email_id = email_ids
    iterate_all_emails(connection, first_email_id, latest_email_id)


run()
