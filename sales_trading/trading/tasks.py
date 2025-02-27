from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_trade_notification(email, trade_id, price, quantity):
    subject = "Ваша сделка исполнена!"
    message = f"Ваша сделка #{trade_id} исполнена:\nЦена: {price}\nКоличество: {quantity}"
    send_mail(subject, message, 'to7zhan@gmail.com', [email])
