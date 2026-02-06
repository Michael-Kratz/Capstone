# Warhammer 40K Store Management System

A Django-based web application for managing a local Warhammer 40K store with events, services, and a trading marketplace.

## Features

### 🎮 Public Features
- **Event Calendar** - Browse tournaments, leagues, casual play sessions, and workshops
- **Painting & Coaching Services** - Browse professional painting services and expert coaching
- **Trading Post** - Buy, sell, and trade Warhammer 40K models with other players

### 👨‍💼 Admin Features
- **Store Management** - Add, edit, and delete events, services, and items
- **Trading Post Management** - Moderate trading posts and manage listings
- **User Permissions** - Control who can post items and manage services

## Project Structure

```
Capstone/
├── config/                 # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── pages/                 # Main app
│   ├── models.py          # Event, Service, TradePost models
│   ├── views.py           # View logic
│   ├── admin.py           # Admin interface configuration
│   ├── urls.py            # App URL routing
│   └── migrations/        # Database migrations
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── navbar.html        # Navigation bar
│   └── pages/             # Page templates
│       ├── home.html
│       ├── events_list.html
│       ├── event_detail.html
│       ├── services_list.html
│       ├── service_detail.html
│       ├── trading_list.html
│       ├── trading_detail.html
│       ├── trading_create.html
│       └── trading_edit.html
├── static/                # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── imgs/
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database
└── venv/                  # Virtual environment
```

## Database Models

### Event
- Title, description, type (tournament/league/casual/workshop)
- Start/end dates, location
- Max participants, entry fee
- Automatically ordered by date

### Service
- Title, description, type (painting/coaching/commission)
- Price, duration (hours)
- Skill level (beginner/intermediate/advanced)
- Provider information
- Availability status

### TradePost
- Title, description, item image
- Post type (selling/buying/trading)
- Item condition (new/like new/good/fair/poor)
- Faction (e.g., Space Marines, Chaos)
- Price (optional)
- Author (linked to User)
- Active/inactive status

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 6.0+
- Pillow (for image handling)

### Installation

1. **Activate Virtual Environment**
```bash
cd "c:\path\to\Capstone"
.\venv\Scripts\Activate.ps1
```

2. **Install Dependencies** (if needed)
```bash
pip install django pillow
```

3. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create Superuser** (Admin account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

5. **Start Development Server**
```bash
python manage.py runserver
```

6. **Access the Application**
- Main site: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## URL Routes

### Public Routes
- `/` - Home page
- `/about/` - About page
- `/events/` - Events list (with filtering)
- `/events/<id>/` - Event details
- `/services/` - Services list (with filtering)
- `/services/<id>/` - Service details
- `/trading/` - Trading posts (with search/filter)
- `/trading/<id>/` - Trading post details

### Admin Routes (Requires Login)
- `/admin/` - Admin dashboard
- `/trading/create/` - Create new trading post
- `/trading/<id>/edit/` - Edit trading post
- `/trading/<id>/delete/` - Delete trading post

## Using the Admin Panel

1. Navigate to http://localhost:8000/admin
2. Login with your superuser credentials
3. You can now:
   - **Add Events** - Create tournaments, leagues, workshops
   - **Add Services** - Post painting and coaching services
   - **Manage Trading Posts** - View, approve, or delete listings
   - **Manage Users** - Create accounts for store staff

## Features in Detail

### Event Management
- Create various types of events (tournaments, leagues, casual, workshops)
- Track participant count vs max capacity
- Set entry fees
- Filter events by type
- View full event details

### Service Management
- List painting and coaching services
- Filter by skill level and service type
- View provider information and contact details
- Track service availability

### Trading Post System
- Users can post items for sale, buying, or trading
- Upload images for listings
- Filter by condition, faction, and type
- Search for specific items
- Only item owners can edit/delete their posts
- Admin can manage all posts

## Future Enhancements

- User messaging system
- Event registration system
- Service booking calendar
- User ratings/reviews
- Advanced search filters
- Email notifications
- User profile pages
- Community forums

## Admin Tips

### Managing Events
1. Go to Admin > Events
2. Click "Add Event"
3. Fill in event details (tournament type, date, location, etc.)
4. Update participant count as people register

### Managing Services
1. Go to Admin > Services
2. Click "Add Service"
3. Set pricing and skill level
4. Mark as available/unavailable

### Managing Trading Posts
1. Go to Admin > Trade Posts
2. View all listings
3. Mark as inactive to remove problematic posts
4. See author information for each post

## Development Notes

- The project uses Bootstrap 5 for styling
- Font Awesome icons are used throughout
- Images are stored in `media/trade_posts/`
- All times are in UTC (configurable in settings.py)
- Authentication uses Django's built-in User model

## Troubleshooting

**"ModuleNotFoundError: No module named 'django'"**
- Activate your virtual environment: `.\venv\Scripts\Activate.ps1`

**Images not displaying**
- Ensure DEBUG=True in settings.py
- Check that media files are in the correct directory

**Admin not accessible**
- Create a superuser: `python manage.py createsuperuser`
- Make sure you're logged in

**Database errors**
- Reset database: `python manage.py flush` (WARNING: deletes all data)
- Recreate migrations: `python manage.py makemigrations && python manage.py migrate`

## License

This project is for educational purposes.
