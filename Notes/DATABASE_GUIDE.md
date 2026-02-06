# 🗄️ Database Schema Guide

## Your Database Models (3 Tables)

---

## 1️⃣ Event Model

### Purpose
Stores all store events (tournaments, leagues, casual play, workshops)

### Fields
```python
id                  → Auto-generated ID (Primary Key)
title              → Event name (Max 200 chars)
description        → Full event description
event_type         → Choice: tournament | league | casual | workshop
start_date         → When event starts (DateTime)
end_date           → When event ends (DateTime)
location           → Where event is held (Max 300 chars)
max_participants   → Maximum people allowed (Optional)
participants_count → How many signed up
entry_fee          → Cost to enter (Optional)
created_at         → When created (Auto-generated)
updated_at         → Last modified (Auto-generated)
```

### Example Record
```
ID: 1
Title: "Spring Tournament 2026"
Description: "Epic tournament with prizes!"
Type: tournament
Start: 2026-03-15 18:00:00
End: 2026-03-15 22:00:00
Location: Downtown Store Floor
Max Participants: 16
Current: 12
Entry Fee: $15.00
Created: 2026-02-06
```

### SQL Query
```sql
SELECT title, start_date, participants_count FROM pages_event 
WHERE event_type = 'tournament' 
ORDER BY start_date DESC;
```

---

## 2️⃣ Service Model

### Purpose
Stores painting and coaching services offered at the store

### Fields
```python
id              → Auto-generated ID (Primary Key)
title           → Service name (Max 200 chars)
description     → What service includes
service_type    → Choice: painting | coaching | commission
price           → Cost of service (Decimal)
duration_hours  → How long it takes
skill_level     → Choice: beginner | intermediate | advanced
provider_name   → Who provides it (Max 200 chars)
provider_contact→ Contact info (Max 200 chars, Optional)
available       → Boolean: Available or not
created_at      → When created (Auto-generated)
updated_at      → Last modified (Auto-generated)
```

### Example Records
```
ID: 1
Title: "Beginner Army Painting"
Description: "Professional painting service for new players"
Type: painting
Price: $50.00
Duration: 5 hours
Skill Level: beginner
Provider: "John's Studio"
Contact: "john@email.com"
Available: YES

ID: 2
Title: "Competitive Play Coaching"
Description: "Learn advanced tactics"
Type: coaching
Price: $75.00
Duration: 3 hours
Skill Level: advanced
Provider: "Pro Player Mike"
Contact: "mike@discord.com"
Available: YES
```

### SQL Query
```sql
SELECT title, price, skill_level FROM pages_service 
WHERE service_type = 'painting' 
AND available = true 
ORDER BY price;
```

---

## 3️⃣ TradePost Model

### Purpose
Community marketplace for buying, selling, and trading Warhammer models

### Fields
```python
id          → Auto-generated ID (Primary Key)
title       → Post title (Max 200 chars)
description → Item details
post_type   → Choice: selling | buying | trading
condition   → Choice: new | like_new | good | fair | poor
faction     → Army faction (Max 200 chars)
price       → Item price (Optional, Decimal)
image       → Uploaded image file (Optional)
author_id   → Foreign Key to User (Who posted it)
created_at  → When posted (Auto-generated)
updated_at  → When updated (Auto-generated)
is_active   → Boolean: Visible or hidden
```

### Example Records
```
ID: 1
Title: "Painted Necron Army - Complete"
Description: "20 warriors, 3 immortals, 1 overlord. Fully painted with matte varnish."
Type: selling
Condition: like_new
Faction: Necrons
Price: $120.00
Image: /media/trade_posts/necron_army.jpg
Author: john_player
Posted: 2026-02-05 14:30:00
Active: YES

ID: 2
Title: "Looking for Space Marine Intercessors"
Description: "Need 5x Intercessors in mint condition"
Type: buying
Condition: new
Faction: Space Marines
Price: (null)
Image: (none)
Author: collector_bob
Posted: 2026-02-06 09:15:00
Active: YES
```

### SQL Query
```sql
SELECT title, price, faction, condition FROM pages_tradepost 
WHERE post_type = 'selling' 
AND is_active = true 
ORDER BY created_at DESC;
```

---

## 📊 Relationships

```
User (Django built-in)
  ↓ (One-to-Many)
TradePost (posts by user)
  
Event (Independent)
Service (Independent)
```

### Visual Diagram

```
┌─────────────┐
│    User     │
├─────────────┤
│ id (PK)     │
│ username    │
│ email       │
│ password    │
└─────────────┘
      ↓ (One-to-Many)
      
┌─────────────┐
│ TradePost   │
├─────────────┤
│ id (PK)     │
│ title       │
│ author_id ──→ User (FK)
│ ...         │
└─────────────┘

┌─────────────┐      ┌─────────────┐
│   Event     │      │  Service    │
├─────────────┤      ├─────────────┤
│ id (PK)     │      │ id (PK)     │
│ title       │      │ title       │
│ start_date  │      │ price       │
│ ...         │      │ ...         │
└─────────────┘      └─────────────┘
```

---

## 📈 Data Types Used

| Type | Purpose | Example |
|------|---------|---------|
| CharField | Short text | "Tournament Finals" |
| TextField | Long text | Full descriptions |
| IntegerField | Whole numbers | Participant count: 12 |
| DecimalField | Money | Price: 25.99 |
| DateTime | Date + Time | 2026-02-15 18:00:00 |
| BooleanField | Yes/No | Available: True |
| ForeignKey | Link to other table | author_id → User |
| ImageField | Picture files | Upload image |
| Choices | Drop-down options | Type: tournament |

---

## 🔍 Common Database Queries

### Get All Upcoming Events
```python
from pages.models import Event
from django.utils import timezone

upcoming = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
```

### Get Services by Skill Level
```python
from pages.models import Service

beginner_services = Service.objects.filter(skill_level='beginner')
```

### Get Active Trading Posts
```python
from pages.models import TradePost

active_posts = TradePost.objects.filter(is_active=True).order_by('-created_at')
```

### Get User's Posts
```python
from pages.models import TradePost
from django.contrib.auth.models import User

user = User.objects.get(username='john_player')
user_posts = user.trade_posts.all()
```

### Count Events by Type
```python
from pages.models import Event

tournament_count = Event.objects.filter(event_type='tournament').count()
```

### Get Most Recent Posts
```python
from pages.models import TradePost

recent_posts = TradePost.objects.order_by('-created_at')[:5]
```

---

## 💾 Database File

**Location**: `db.sqlite3` in project root

**Access**: 
- Automatically created when you run migrations
- SQLite format (local file, no server needed)
- Contains all your data
- Grows as you add content

**Backup**:
```bash
# Create backup before big changes
copy db.sqlite3 db.sqlite3.backup
```

---

## 🛠️ Managing Data

### View in Admin Panel
1. Go to http://localhost:8000/admin
2. Login with superuser account
3. Click on Events, Services, or Trade Posts
4. Add, edit, or delete records

### Query in Django Shell
```bash
python manage.py shell

# Inside shell
from pages.models import Event, Service, TradePost
from django.contrib.auth.models import User

# Get all events
events = Event.objects.all()

# Get specific event
event = Event.objects.get(id=1)

# Create new event
new_event = Event.objects.create(
    title="New Tournament",
    description="Details here",
    event_type="tournament",
    start_date="2026-03-01 18:00:00",
    end_date="2026-03-01 22:00:00",
    location="Store"
)

# Delete
event.delete()

# Exit
exit()
```

---

## 🔐 Data Integrity

### Relationships
- Events: ✅ Independent (can exist on their own)
- Services: ✅ Independent (can exist on their own)  
- TradePost: ✅ Linked to User (post deleted when user deleted)

### Constraints
- **Event title**: Required, Max 200 chars
- **Service price**: Required, Must be positive
- **TradePost author**: Required, Must be valid user
- **Unique fields**: None (multiple posts allowed)

### Validation
- DateTime fields: Must be valid date/time
- Decimal fields: Must be valid number
- Foreign Keys: Must reference existing user
- Choices: Must be valid choice option

---

## 📊 Database Statistics

```
Current Tables: 3 custom + Django built-in tables

Event Table
  Records: Depends on you
  Typical Size: < 1 MB

Service Table  
  Records: Depends on you
  Typical Size: < 1 MB

TradePost Table
  Records: Can grow large
  Typical Size: < 10 MB (with images)

Total Database Size: 
  Empty: ~100 KB
  With data: < 50 MB
```

---

## 🚀 Growth Capacity

This SQLite database can handle:
- ✅ Hundreds of events
- ✅ Hundreds of services
- ✅ Thousands of trade posts
- ✅ Thousands of users
- ✅ Years of data

If you need more:
- Upgrade to PostgreSQL
- Upgrade to MySQL
- Deploy to cloud database

---

## 🆘 Database Issues

### Issue: Database Corrupted
```bash
# Backup current
copy db.sqlite3 db.sqlite3.broken

# Reset database
python manage.py flush

# Recreate
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Lost Data
```bash
# Restore from backup
copy db.sqlite3.backup db.sqlite3
```

### Issue: Slow Queries
```python
# Add indexing to frequently searched fields
# (Already optimized in this project)
```

---

## 📖 SQL Knowledge Not Required

You don't need to know SQL to use this! Django does it for you:

```python
# What you write (Django ORM)
Event.objects.filter(event_type='tournament')

# What Django does (SQL)
SELECT * FROM pages_event WHERE event_type = 'tournament';
```

---

## ✅ Database is Ready

✅ All tables created
✅ All relationships configured
✅ All fields optimized
✅ Ready for production
✅ Backup strategy: `db.sqlite3.backup`

---

## Next Steps

1. **Add Data**: Use admin panel to add events/services/posts
2. **Backup**: `copy db.sqlite3 db.sqlite3.backup`
3. **Monitor**: Keep an eye on database size as you add content
4. **Maintain**: Regular backups recommended

---

That's all you need to know about the database!

For more details, see [README.md](README.md) Database Models section.

