from django.contrib import admin

from .models import Thread, ThreadParticipant, Message, SupportTicket, TicketMessage


admin.site.register(Thread)
admin.site.register(ThreadParticipant)
admin.site.register(Message)
admin.site.register(SupportTicket)
admin.site.register(TicketMessage)
