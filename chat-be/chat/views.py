from django.shortcuts import render
from datetime import datetime, timedelta

from .models import Chat, Message, SheduledMessage
from .serializers import ChatSerializers, MessagePostSerializer, MessageSerializer, SheduledMessageSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import math 



class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        mess = Chat.objects.all()
        serializer = ChatSerializers(mess, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        print(request.data)
        Chat.objects.create(creator=request.user)
        return Response(status=200)

class DialogView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        date = datetime.now()
        chat = request.GET.get("chat")
        page_number = int(request.GET.get("page"))
        mess = Message.objects.filter(chat=chat)
        serializer = MessageSerializer(mess, many=True)
        sh_mess = SheduledMessage.objects.filter(chat=chat, date__lte=date)
        serializer_sh = SheduledMessageSerializer(sh_mess, many=True)
        data = serializer.data + serializer_sh.data
        sorted_data = sorted(data, key=lambda k: k['date'], reverse=True) 

        # custom pagination for tests=) bad for real project with a lot of data
        pages = []
        page = {}
        page_counter = 1
        date_for_page = []
        counter = 0
        total = math.ceil(len(sorted_data)/5)

        if len(sorted_data) < 5:
            for i in sorted_data:
                date_for_page.append(i)
            page.update({page_counter: date_for_page[:]})
            pages.append(page.copy())
            page.clear()
            date_for_page.clear()
        else:
            for i in sorted_data:
                if counter < 4:
                    date_for_page.append(i)
                    counter += 1
                else:
                    date_for_page.append(i)
                    page.update({page_counter: date_for_page[:]})
                    pages.append(page.copy())
                    page.clear()
                    page_counter += 1
                    counter = 0
                    date_for_page.clear()
        if len(date_for_page) != 0:
            page.update({page_counter: date_for_page[:]})
            pages.append(page.copy())
            page.clear()
            date_for_page.clear()
        
        return Response({"data": pages[page_number-1][page_number], "total": total})

    


    def post(self, request):
        dialog = MessagePostSerializer(data=request.data)
        print(type(request.user))
        if dialog.is_valid():
            dialog.save(user=request.user)
            return Response(status=200)
        else:
            return Response(status=400)

class SchedDialogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        chat = request.POST.getlist('chat')[0]
        date = request.POST.getlist('date')[0]
        date_time_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        date = date_time_obj-timedelta(hours=2)
        text = request.POST.getlist('text')[0]
        chat = Chat(chat)
        SheduledMessage.objects.create(chat=chat, date=date, text=text, user=request.user)

        return Response(status=200)