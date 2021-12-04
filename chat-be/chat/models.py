from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    creator = models.ForeignKey(User, verbose_name="Chat Creator", on_delete=models.CASCADE)
    chat_name = models.CharField(max_length=20, verbose_name="Chat name", default="Chat")


    class Meta:
        verbose_name = "Chat"

    
    def __str__(self):
        return f"{self.chat_name}(ID={self.id})"


class Message(models.Model):
    chat = models.ForeignKey(Chat,verbose_name='Chat ID', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="The date the message was created", auto_now=True, editable=False)
    text = models.CharField(max_length=250, verbose_name="Message")
    
    class Meta:
        verbose_name = "Message"

    
    def __str__(self):
        return f"{self.id}"



class SheduledMessage(models.Model):
    chat = models.ForeignKey(Chat,verbose_name='Chat ID', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="The date of the scheduled message")
    text = models.CharField(max_length=250, verbose_name="Message")
    
    class Meta:
        verbose_name = "Sheduled Message"

    
    def __str__(self):
        return f"{self.id}"