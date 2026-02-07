from django.contrib import admin
from .models import Event, Service, TradePost, UserProfile, ServiceBooking, EventRegistration, ContactMessage


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'participants_count', 'max_participants']
    list_filter = ['event_type', 'start_date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Event Info', {
            'fields': ('title', 'description', 'event_type')
        }),
        ('Date & Location', {
            'fields': ('start_date', 'end_date', 'location')
        }),
        ('Participation', {
            'fields': ('max_participants', 'participants_count', 'entry_fee')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'skill_level', 'price', 'available']
    list_filter = ['service_type', 'skill_level', 'available']
    search_fields = ['title', 'description', 'provider_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Service Info', {
            'fields': ('title', 'description', 'service_type')
        }),
        ('Details', {
            'fields': ('skill_level', 'duration_hours', 'price', 'available')
        }),
        ('Provider', {
            'fields': ('provider_name', 'provider_contact')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TradePost)
class TradePostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'faction', 'condition', 'author', 'is_active']
    list_filter = ['post_type', 'condition', 'faction', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'faction', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'author']
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'description', 'image')
        }),
        ('Details', {
            'fields': ('post_type', 'condition', 'faction', 'price')
        }),
        ('Status', {
            'fields': ('author', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'rank', 'created_at']
    list_filter = ['rank']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'booking_date', 'status', 'created_at']
    list_filter = ['status', 'service', 'booking_date']
    search_fields = ['customer__username', 'service__title', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Booking Info', {
            'fields': ('service', 'customer', 'booking_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'registration_date', 'attended']
    list_filter = ['event', 'attended', 'registration_date']
    search_fields = ['user__username', 'event__title', 'notes']
    readonly_fields = ['registration_date']
    fieldsets = (
        ('Registration Info', {
            'fields': ('event', 'user', 'registration_date')
        }),
        ('Attendance', {
            'fields': ('attended',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'post', 'created_at', 'read']
    list_filter = ['read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'post__title', 'message']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Message Info', {
            'fields': ('post', 'sender', 'recipient', 'created_at')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('read',)
        }),
    )
