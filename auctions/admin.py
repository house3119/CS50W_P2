from django.contrib import admin
from .models import User, Listing, Bid, Comment

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "active", "poster", "category", "created",)
    filter_horizontal = ("watchers",)


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bidder", "relatedListing", "bid", "created",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "commenter", "commentedListing", "created",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "date_joined",)


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)