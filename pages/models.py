from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Event Model - for store events/tournaments
class Event(models.Model):
    EVENT_TYPES = [
        ('tournament', 'Tournament'),
        ('league', 'League'),
        ('casual', 'Casual Play'),
        ('workshop', 'Workshop'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=300)
    max_participants = models.IntegerField(null=True, blank=True)
    participants_count = models.IntegerField(default=0)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.title} - {self.start_date.strftime('%m/%d/%Y')}"


# Service Model - for painting and coaching services
class Service(models.Model):
    SERVICE_TYPES = [
        ('painting', 'Painting Service'),
        ('coaching', 'Coaching'),
        ('commission', 'Commission Work'),
    ]
    
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.IntegerField(help_text="Estimated duration in hours")
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS)
    provider_name = models.CharField(max_length=200)
    provider_contact = models.CharField(max_length=200, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['service_type', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


# Trading Post Model - for buying/selling old models
class TradePost(models.Model):
    POST_TYPE = [
        ('selling', 'Selling'),
        ('buying', 'Buying'),
        ('trading', 'Trading'),
    ]
    
    CONDITION = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE)
    condition = models.CharField(max_length=20, choices=CONDITION)
    faction = models.CharField(max_length=200, help_text="e.g., Space Marines, Chaos, Necrons")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='trade_posts/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_post_type_display()}"

# UserProfile Model - for user ranks
class UserProfile(models.Model):
    RANK_CHOICES = [
        ('user', 'Regular User'),
        ('staff', 'Staff Member'),
        ('manager', 'Manager'),
        ('admin', 'Admin/Superuser'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_rank_display()}"
    
    def save(self, *args, **kwargs):
        """Sync rank with Django's is_staff and is_superuser flags"""
        if self.rank == 'admin':
            self.user.is_staff = True
            self.user.is_superuser = True
        elif self.rank == 'manager':
            self.user.is_staff = True
            self.user.is_superuser = False
        elif self.rank == 'staff':
            self.user.is_staff = True
            self.user.is_superuser = False
        else:  # user
            self.user.is_staff = False
            self.user.is_superuser = False
        self.user.save()
        super().save(*args, **kwargs)


# Booking Model - for service booking requests
class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Additional notes or requirements")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.username} - {self.service.title} ({self.status})"


# Event Registration Model - for tracking event participants
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Registration notes or comments")
    
    class Meta:
        ordering = ['-registration_date']
        unique_together = ['event', 'user']  # Prevent duplicate registrations
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


# Internal messaging for Trading Posts
class ContactMessage(models.Model):
    post = models.ForeignKey('TradePost', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} on {self.post.title}"
