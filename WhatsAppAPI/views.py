from django.views.generic import TemplateView
# from chat.entities.chat_rooms import ChatRoom

class HomePageView(TemplateView):
    template_name = '/home/tinsae/Desktop/projects/WhatsAppAPI/chat/templates/chat/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_rooms'] = ChatRoom.objects.all()
        context['id'] = 1
        return context
