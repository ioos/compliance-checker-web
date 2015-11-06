#!/usr/bin/env python
'''
cchecker_web/email.py
'''

from flask.ext.mail import Message
from flask import render_template
from flask import current_app as app
from collections import defaultdict
from datetime import datetime, timedelta
from cchecker_web import mail
from collections import namedtuple

ImageAttachment = namedtuple('ImageAttachment', ['image_name', 'content_type', 'path', 'content_id'])



def send(subject, recipients, cc_recipients, text_body, html_body, image_attachments=None):
    image_attachments = image_attachments or []
    if not app.config['MAIL_ENABLED']:
        raise IOError("Mail is not enabled")
    msg = Message(subject, recipients=recipients, cc=cc_recipients)
    msg.body = text_body
    msg.html = html_body
    for attachment in image_attachments:
        if not isinstance(attachment, ImageAttachment):
            continue
        with open(attachment.path) as f:
            data = f.read()
        msg.attach(attachment.image_name, attachment.content_type, data, headers=[('Content-ID', attachment.content_id)])
    mail.send(msg)


