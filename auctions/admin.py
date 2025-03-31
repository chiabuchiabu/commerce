from django.contrib import admin
from .models import User,auction_list,Bid,Comment,Active
# Register your models here.

class User_listAdmin(admin.ModelAdmin):
    filter_horizontal=("watchitem",)


admin.site.register(User,User_listAdmin)
admin.site.register(auction_list)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Active)
