# app_name = 'chat'
router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'chat-rooms', ChatRoomViewSet, basename='chat-rooms')


urlpatterns = [
    path('', include(router.urls))
  
]
