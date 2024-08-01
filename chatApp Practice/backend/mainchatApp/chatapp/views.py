from rest_framework import viewsets, permissions
from .models import ChatMessage
from .serializer import ChatMessageSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('-timestamp')
    serializer_class = ChatMessageSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
