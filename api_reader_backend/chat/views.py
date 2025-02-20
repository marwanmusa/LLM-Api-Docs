from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatHistory
from .serializers import ChatHistorySerializer

class ChatHistoryView(APIView):
    def get(self, request):
        """Retrieve all chat history."""
        chat_histories = ChatHistory.objects.all()
        serializer = ChatHistorySerializer(chat_histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a new chat message to an existing chat session or create a new one."""
        data = request.data
        chat_id = data.get("chat_id")  # Optional, for updating existing chats
        topic = data.get("topic", "New Chat")

        if "message" not in data or "sender" not in data:
            return Response(
                {"error": "Both 'message' and 'sender' fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if chat_id:
            try:
                chat_history = ChatHistory.objects.get(id=chat_id)
            except ChatHistory.DoesNotExist:
                return Response({"error": "Chat ID not found."}, status=status.HTTP_404_NOT_FOUND)

            chat_history.chat_data.append({
                "sender": data["sender"],
                "message": data["message"],
            })
            chat_history.save()
            return Response(ChatHistorySerializer(chat_history).data, status=status.HTTP_200_OK)

        # If no chat_id is provided, create a new chat history
        new_chat = ChatHistory.objects.create(
            topic=topic,
            chat_data=[{"sender": data["sender"], "message": data["message"]}]
        )
        return Response(ChatHistorySerializer(new_chat).data, status=status.HTTP_201_CREATED)


class ClearChatHistoryView(APIView):
    def delete(self, request):
        """Clear all chat history from the database."""
        ChatHistory.objects.all().delete()
        return Response({"message": "Chat history cleared."}, status=status.HTTP_200_OK)
