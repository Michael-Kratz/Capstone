from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from .models import Event, Service, TradePost, UserProfile, ServiceBooking, EventRegistration, ContactMessage


def home_view(request):
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now())[:3]
    context = {'upcoming_events': upcoming_events}
    return render(request, "pages/home.html", context)


def about_view(request):
    return render(request, "pages/about.html")


# Event Views
def events_list(request):
    """Display all events with filtering"""
    events = Event.objects.all()
    
    # Filter by event type
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)
    
    # Filter by date range
    upcoming_only = request.GET.get('upcoming')
    if upcoming_only:
        events = events.filter(start_date__gte=timezone.now())
    
    context = {
        'events': events,
        'event_type': event_type,
        'upcoming_only': upcoming_only,
    }
    return render(request, "pages/events_list.html", context)


def event_detail(request, pk):
    """Display event details"""
    event = get_object_or_404(Event, pk=pk)
    registrations = event.registrations.all().count()
    user_registered = False
    
    if request.user.is_authenticated:
        user_registered = event.registrations.filter(user=request.user).exists()
    
    context = {
        'event': event,
        'registrations': registrations,
        'user_registered': user_registered,
    }
    return render(request, "pages/event_detail.html", context)


@login_required
def register_for_event(request, pk):
    """Register user for an event"""
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user is already registered
    existing_registration = EventRegistration.objects.filter(event=event, user=request.user).first()
    
    if existing_registration:
        return redirect('event_detail', pk=pk)
    
    # Create registration
    registration = EventRegistration.objects.create(
        event=event,
        user=request.user,
        notes=request.POST.get('notes', '')
    )
    
    # Update event participants count
    event.participants_count += 1
    event.save()
    
    return redirect('event_detail', pk=pk)


@login_required
def cancel_event_registration(request, pk):
    """Cancel registration for an event"""
    event = get_object_or_404(Event, pk=pk)
    registration = get_object_or_404(EventRegistration, event=event, user=request.user)
    
    registration.delete()
    
    # Update event participants count
    event.participants_count -= 1
    event.save()
    
    return redirect('event_detail', pk=pk)


@login_required
def my_event_registrations(request):
    """View all user's event registrations"""
    registrations = EventRegistration.objects.filter(user=request.user).select_related('event').order_by('-registration_date')
    context = {'registrations': registrations}
    return render(request, "pages/my_event_registrations.html", context)


# Service Views
def services_list(request):
    """Display all services with filtering"""
    services = Service.objects.filter(available=True)
    
    # Filter by service type
    service_type = request.GET.get('type')
    if service_type:
        services = services.filter(service_type=service_type)
    
    # Filter by skill level
    skill_level = request.GET.get('skill')
    if skill_level:
        services = services.filter(skill_level=skill_level)
    
    context = {
        'services': services,
        'service_type': service_type,
        'skill_level': skill_level,
    }
    return render(request, "pages/services_list.html", context)


def service_detail(request, pk):
    """Display service details"""
    service = get_object_or_404(Service, pk=pk)
    context = {'service': service}
    return render(request, "pages/service_detail.html", context)


@login_required
def request_service_booking(request, pk):
    """Request a booking for a service"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        notes = request.POST.get('notes')
        
        # Create booking
        booking = ServiceBooking.objects.create(
            service=service,
            customer=request.user,
            booking_date=booking_date,
            notes=notes,
            status='pending'
        )
        
        # Redirect to booking confirmation
        return redirect('booking_confirmation', booking_id=booking.id)
    
    context = {'service': service}
    return render(request, "pages/request_booking.html", context)


@login_required
def booking_confirmation(request, booking_id):
    """Show booking confirmation"""
    booking = get_object_or_404(ServiceBooking, id=booking_id, customer=request.user)
    context = {'booking': booking}
    return render(request, "pages/booking_confirmation.html", context)


@login_required
def my_bookings(request):
    """View user's bookings"""
    bookings = ServiceBooking.objects.filter(customer=request.user).order_by('-created_at')
    context = {'bookings': bookings}
    return render(request, "pages/my_bookings.html", context)


# Trading Post Views
def trading_list(request):
    """Display all active trade posts with filtering"""
    posts = TradePost.objects.filter(is_active=True)
    
    # Filter by post type
    post_type = request.GET.get('type')
    if post_type:
        posts = posts.filter(post_type=post_type)
    
    # Filter by faction
    faction = request.GET.get('faction')
    if faction:
        posts = posts.filter(faction__icontains=faction)
    
    # Search
    search = request.GET.get('search')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    context = {
        'posts': posts,
        'post_type': post_type,
        'faction': faction,
        'search': search,
    }
    return render(request, "pages/trading_list.html", context)


def trading_detail(request, pk):
    """Display trade post details"""
    post = get_object_or_404(TradePost, pk=pk, is_active=True)
    context = {'post': post}

    # If the post owner is viewing, provide their messages and mark as read
    if request.user.is_authenticated and request.user == post.author:
        owner_messages = post.messages.filter(recipient=post.author)
        # mark unread messages as read for the owner
        unread_qs = owner_messages.filter(read=False)
        if unread_qs.exists():
            unread_qs.update(read=True)
        context['owner_messages'] = owner_messages
    
    # If the user is authenticated but NOT the owner, show their conversation (sent messages + replies)
    elif request.user.is_authenticated:
        # Get messages they sent to this post's owner
        sent_messages = post.messages.filter(sender=request.user, recipient=post.author)
        # Get replies from the owner to this user
        received_replies = post.messages.filter(sender=post.author, recipient=request.user)
        # Combine and order by created_at
        conversation = (sent_messages | received_replies).order_by('created_at')
        context['buyer_messages'] = conversation

    return render(request, "pages/trading_detail.html", context)


@login_required
def send_message_to_post(request, pk):
    """Send an internal message to the post author"""
    post = get_object_or_404(TradePost, pk=pk, is_active=True)
    if request.method != 'POST':
        return redirect('trading_detail', pk=pk)

    message_text = request.POST.get('message', '').strip()
    subject = request.POST.get('subject', '').strip()

    if not message_text:
        messages.error(request, 'Message cannot be empty.')
        return redirect('trading_detail', pk=pk)

    # Prevent sending message to yourself
    if request.user == post.author:
        messages.error(request, "You cannot send a message to your own post.")
        return redirect('trading_detail', pk=pk)

    # Create internal message
    ContactMessage.objects.create(
        post=post,
        sender=request.user,
        recipient=post.author,
        subject=subject,
        message=message_text,
    )

    messages.success(request, 'Your message was sent to the seller.')
    return redirect('trading_detail', pk=pk)


@login_required
def reply_to_message(request, message_id):
    """Reply to a contact message (owner or buyer may reply to their conversation partner)"""
    original = get_object_or_404(ContactMessage, pk=message_id)
    post = original.post

    # Check authorization: either post owner or the original message recipient (buyer)
    is_owner = request.user == post.author
    is_recipient = request.user == original.recipient
    
    if not (is_owner or is_recipient):
        messages.error(request, 'You are not authorized to reply to this message.')
        return redirect('trading_detail', pk=post.pk)

    if request.method == 'POST':
        reply_text = request.POST.get('message', '').strip()
        if not reply_text:
            messages.error(request, 'Reply cannot be empty.')
            return redirect('reply_to_message', message_id=message_id)

        # Determine who the reply recipient is
        if is_owner:
            reply_recipient = original.sender
        else:
            reply_recipient = post.author

        # Create reply message directed to the other party
        ContactMessage.objects.create(
            post=post,
            sender=request.user,
            recipient=reply_recipient,
            subject=("Re: " + original.subject) if original.subject else "Re: (no subject)",
            message=reply_text,
        )

        messages.success(request, 'Reply sent.')
        return redirect('trading_detail', pk=post.pk)

    context = {'original': original}
    return render(request, 'pages/trading_message_reply.html', context)


@login_required
def trading_create(request):
    """Create a new trade post"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        post_type = request.POST.get('post_type')
        condition = request.POST.get('condition')
        faction = request.POST.get('faction')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        
        post = TradePost.objects.create(
            title=title,
            description=description,
            post_type=post_type,
            condition=condition,
            faction=faction,
            price=price if price else None,
            image=image,
            author=request.user
        )
        return redirect('trading_detail', pk=post.pk)
    
    context = {}
    return render(request, "pages/trading_create.html", context)


@login_required
def trading_edit(request, pk):
    """Edit a trade post (only by owner)"""
    post = get_object_or_404(TradePost, pk=pk)
    
    if post.author != request.user:
        return redirect('trading_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.description = request.POST.get('description', post.description)
        post.condition = request.POST.get('condition', post.condition)
        post.faction = request.POST.get('faction', post.faction)
        post.price = request.POST.get('price', post.price)
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.save()
        return redirect('trading_detail', pk=post.pk)
    
    context = {'post': post}
    return render(request, "pages/trading_edit.html", context)


@login_required
@require_http_methods(["POST"])
def trading_delete(request, pk):
    """Delete a trade post (only by owner)"""
    post = get_object_or_404(TradePost, pk=pk)
    
    if post.author != request.user:
        return redirect('trading_detail', pk=post.pk)
    
    post.is_active = False
    post.save()
    return redirect('trading_list')


# Authentication Views
def signup_view(request):
    """Register a new user account"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            context = {'error': 'All fields are required'}
            return render(request, "pages/signup.html", context)
        
        if password != password_confirm:
            context = {'error': 'Passwords do not match'}
            return render(request, "pages/signup.html", context)
        
        if User.objects.filter(username=username).exists():
            context = {'error': 'Username already taken'}
            return render(request, "pages/signup.html", context)
        
        if User.objects.filter(email=email).exists():
            context = {'error': 'Email already registered'}
            return render(request, "pages/signup.html", context)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Auto-login the user
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Get the next page from referrer or default to trading_list
            next_page = request.GET.get('next', 'trading_list')
            return redirect(next_page)
        
        # If auto-login fails, redirect to login page
        return redirect('login')
    
    context = {}
    return render(request, "pages/signup.html", context)


def login_view(request):
    """Login page with form"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to 'next' page if provided, otherwise go to trading_list
            next_page = request.POST.get('next', request.GET.get('next', 'trading_list'))
            return redirect(next_page)
        else:
            context = {'error': 'Invalid username or password', 'next': request.POST.get('next', request.GET.get('next', ''))}
            return render(request, "pages/login.html", context)
    
    next_page = request.GET.get('next', '')
    context = {'next': next_page}
    return render(request, "pages/login.html", context)


def logout_view(request):
    """Logout user"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')


# Staff Management Views
def staff_required(view_func):
    """Decorator to check if user is staff"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def manager_or_superuser_required(view_func):
    """Decorator to check if user is manager or superuser"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        
        # Check if superuser (legacy support for existing admins)
        if request.user.is_superuser:
            # Create profile if doesn't exist
            UserProfile.objects.get_or_create(user=request.user, defaults={'rank': 'admin'})
            return view_func(request, *args, **kwargs)
        
        # Check profile rank
        try:
            profile = request.user.profile
            if profile.rank in ['manager', 'admin']:
                return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            pass
        
        return redirect('home')
    return wrapper


@staff_required
def staff_dashboard(request):
    """Staff management dashboard"""
    events_count = Event.objects.count()
    services_count = Service.objects.count()
    trading_posts_count = TradePost.objects.filter(is_active=True).count()
    pending_bookings_count = ServiceBooking.objects.filter(status='pending').count()
    all_bookings_count = ServiceBooking.objects.count()
    total_registrations = EventRegistration.objects.count()
    
    context = {
        'events_count': events_count,
        'services_count': services_count,
        'trading_posts_count': trading_posts_count,
        'pending_bookings_count': pending_bookings_count,
        'all_bookings_count': all_bookings_count,
        'total_registrations': total_registrations,
    }
    return render(request, "pages/staff_dashboard.html", context)


@staff_required
def staff_add_event(request):
    """Add a new event"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_type = request.POST.get('event_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        max_participants = request.POST.get('max_participants')
        entry_fee = request.POST.get('entry_fee')
        
        if not all([title, description, event_type, start_date, end_date, location]):
            context = {'error': 'All fields are required'}
            return render(request, "pages/staff_add_event.html", context)
        
        event = Event.objects.create(
            title=title,
            description=description,
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            location=location,
            max_participants=int(max_participants) if max_participants else None,
            entry_fee=float(entry_fee) if entry_fee else None,
        )
        
        return redirect('staff_events_list')
    
    context = {'event_types': Event._meta.get_field('event_type').choices}
    return render(request, "pages/staff_add_event.html", context)


@staff_required
def staff_events_list(request):
    """View all events for staff management"""
    events = Event.objects.all().order_by('-created_at')
    context = {'events': events}
    return render(request, "pages/staff_events_list.html", context)


@staff_required
def staff_delete_event(request, pk):
    """Delete an event"""
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('staff_events_list')


@manager_or_superuser_required
def staff_add_service(request):
    """Add a new service"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        service_type = request.POST.get('service_type')
        price = request.POST.get('price')
        duration_hours = request.POST.get('duration_hours')
        skill_level = request.POST.get('skill_level')
        provider_name = request.POST.get('provider_name')
        provider_contact = request.POST.get('provider_contact')
        available = request.POST.get('available') == 'on'
        
        if not all([title, description, service_type, price, provider_name]):
            context = {'error': 'Required fields are missing'}
            return render(request, "pages/staff_add_service.html", context)
        
        service = Service.objects.create(
            title=title,
            description=description,
            service_type=service_type,
            price=float(price),
            duration_hours=int(duration_hours) if duration_hours else None,
            skill_level=skill_level,
            provider_name=provider_name,
            provider_contact=provider_contact,
            available=available,
        )
        
        return redirect('staff_services_list')
    
    context = {
        'service_types': Service._meta.get_field('service_type').choices,
        'skill_levels': Service._meta.get_field('skill_level').choices,
    }
    return render(request, "pages/staff_add_service.html", context)


@staff_required
def staff_services_list(request):
    """View all services for staff management"""
    services = Service.objects.all().order_by('-created_at')
    context = {'services': services}
    return render(request, "pages/staff_services_list.html", context)


@manager_or_superuser_required
def staff_delete_service(request, pk):
    """Delete a service"""
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('staff_services_list')


@staff_required
def staff_trading_posts(request):
    """View all trading posts for staff management"""
    posts = TradePost.objects.all().order_by('-created_at')
    context = {'posts': posts}
    return render(request, "pages/staff_trading_posts.html", context)


@staff_required
def staff_delete_trading_post(request, pk):
    """Delete/deactivate a trading post"""
    post = get_object_or_404(TradePost, pk=pk)
    post.is_active = False
    post.save()
    return redirect('staff_trading_posts')


@manager_or_superuser_required
def staff_users(request):
    """Manage staff members and their ranks"""
    # Ensure current user has a profile
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.user.is_superuser and user_profile.rank != 'admin':
        user_profile.rank = 'admin'
        user_profile.save()
    
    users = User.objects.all().prefetch_related('profile').order_by('-date_joined')
    
    # Count by rank - create profiles for users without them
    for user in users:
        if not hasattr(user, 'profile') or user.profile is None:
            UserProfile.objects.get_or_create(user=user)
    
    user_count = UserProfile.objects.filter(rank='user').count()
    staff_count = UserProfile.objects.filter(rank='staff').count()
    manager_count = UserProfile.objects.filter(rank='manager').count()
    admin_count = UserProfile.objects.filter(rank='admin').count()
    
    context = {
        'users': users,
        'user_count': user_count,
        'staff_count': staff_count,
        'manager_count': manager_count,
        'admin_count': admin_count,
    }
    return render(request, "pages/staff_users.html", context)


@manager_or_superuser_required
def staff_update_user_rank(request, pk):
    """Update a user's staff rank"""
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        new_rank = request.POST.get('rank')
        
        # Get current user's profile
        current_user_profile = UserProfile.objects.get(user=request.user)
        target_user_profile, _ = UserProfile.objects.get_or_create(user=user)
        
        # Only admins can change admin ranks or make someone admin
        if current_user_profile.rank == 'manager':
            # Managers cannot touch admins
            if target_user_profile.rank == 'admin':
                user_count = UserProfile.objects.filter(rank='user').count()
                staff_count = UserProfile.objects.filter(rank='staff').count()
                manager_count = UserProfile.objects.filter(rank='manager').count()
                admin_count = UserProfile.objects.filter(rank='admin').count()
                context = {
                    'error': 'Managers cannot modify admin accounts',
                    'users': User.objects.all().prefetch_related('profile').order_by('-date_joined'),
                    'user_count': user_count,
                    'staff_count': staff_count,
                    'manager_count': manager_count,
                    'admin_count': admin_count,
                }
                return render(request, "pages/staff_users.html", context)
            
            # Managers cannot promote anyone to admin
            if new_rank == 'admin':
                user_count = UserProfile.objects.filter(rank='user').count()
                staff_count = UserProfile.objects.filter(rank='staff').count()
                manager_count = UserProfile.objects.filter(rank='manager').count()
                admin_count = UserProfile.objects.filter(rank='admin').count()
                context = {
                    'error': 'Managers cannot promote users to admin rank',
                    'users': User.objects.all().prefetch_related('profile').order_by('-date_joined'),
                    'user_count': user_count,
                    'staff_count': staff_count,
                    'manager_count': manager_count,
                    'admin_count': admin_count,
                }
                return render(request, "pages/staff_users.html", context)
            
            # Managers cannot make themselves admin
            if request.user.pk == user.pk and new_rank == 'admin':
                user_count = UserProfile.objects.filter(rank='user').count()
                staff_count = UserProfile.objects.filter(rank='staff').count()
                manager_count = UserProfile.objects.filter(rank='manager').count()
                admin_count = UserProfile.objects.filter(rank='admin').count()
                context = {
                    'error': 'Managers cannot promote themselves to admin',
                    'users': User.objects.all().prefetch_related('profile').order_by('-date_joined'),
                    'user_count': user_count,
                    'staff_count': staff_count,
                    'manager_count': manager_count,
                    'admin_count': admin_count,
                }
                return render(request, "pages/staff_users.html", context)
        
        # Prevent admins from removing themselves
        if request.user.pk == user.pk and current_user_profile.rank == 'admin' and new_rank != 'admin':
            user_count = UserProfile.objects.filter(rank='user').count()
            staff_count = UserProfile.objects.filter(rank='staff').count()
            manager_count = UserProfile.objects.filter(rank='manager').count()
            admin_count = UserProfile.objects.filter(rank='admin').count()
            context = {
                'error': 'Cannot remove yourself as admin',
                'users': User.objects.all().prefetch_related('profile').order_by('-date_joined'),
                'user_count': user_count,
                'staff_count': staff_count,
                'manager_count': manager_count,
                'admin_count': admin_count,
            }
            return render(request, "pages/staff_users.html", context)
        
        # Update profile
        target_user_profile.rank = new_rank
        target_user_profile.save()
    
    return redirect('staff_users')


# Service Booking Views for Staff
@staff_required
def staff_bookings(request):
    """View all service bookings"""
    status_filter = request.GET.get('status')
    bookings = ServiceBooking.objects.select_related('customer', 'service').order_by('-created_at')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
    }
    return render(request, "pages/staff_bookings.html", context)


@staff_required
def staff_update_booking_status(request, booking_id):
    """Update booking status"""
    if request.method == 'POST':
        booking = get_object_or_404(ServiceBooking, pk=booking_id)
        new_status = request.POST.get('status')
        
        if new_status in ['pending', 'confirmed', 'completed', 'cancelled']:
            booking.status = new_status
            booking.save()
        
        return redirect('staff_bookings')
    
    booking = get_object_or_404(ServiceBooking, pk=booking_id)
    context = {'booking': booking}
    return render(request, "pages/staff_booking_detail.html", context)


# Staff Event Registration Views
@staff_required
def staff_event_registrations(request):
    """View all event registrations"""
    event_filter = request.GET.get('event')
    registrations = EventRegistration.objects.select_related('event', 'user').order_by('-registration_date')
    
    if event_filter:
        registrations = registrations.filter(event_id=event_filter)
    
    events = Event.objects.all()
    
    context = {
        'registrations': registrations,
        'events': events,
        'event_filter': event_filter,
    }
    return render(request, "pages/staff_event_registrations.html", context)


@staff_required
def staff_event_registration_detail(request, registration_id):
    """View event registration details"""
    registration = get_object_or_404(EventRegistration, pk=registration_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'attended':
            registration.attended = True
            registration.save()
        elif action == 'not_attended':
            registration.attended = False
            registration.save()
    
    context = {'registration': registration}
    return render(request, "pages/staff_event_registration_detail.html", context)
