from rest_framewok import serializers

# data models
# entities (or values objects in some cases)
# Data Transfer Ojbects


class EmailMessage:
    body: str
    subject: str
    recepient: str
    sender: str
