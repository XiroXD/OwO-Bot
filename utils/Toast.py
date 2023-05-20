from notifypy import Notify

def send(title, message):
    notification = Notify()
    notification.title = title
    notification.message = message
    notification.application_name = "OwO Bot"
    notification.send(block=False)