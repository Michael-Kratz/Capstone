# Testing & Demo Guide

This guide helps you test all features of the Warhammer 40K Store application.

## Getting Started

1. **Start the server**
```bash
cd "c:\path\to\Capstone"
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

2. **Open browser**
   - Main site: http://localhost:8000
   - Admin: http://localhost:8000/admin

3. **Create admin account** (if not done yet)
```bash
python manage.py createsuperuser
```

## Test Cases

### Test 1: Homepage Navigation

**Goal**: Verify homepage displays all main features

**Steps**:
1. Go to http://localhost:8000
2. Verify you see:
   - ✓ Hero section with "Warhammer 40K Store Hub"
   - ✓ Three feature cards (Events, Services, Trading)
   - ✓ Buttons linking to each section
3. Click "Browse Events" button
4. Click back, then "Trading Post" button
5. Verify pages load correctly

### Test 2: Event Management

**Goal**: Test creating, viewing, and filtering events

**Steps**:
1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Click **Events** → **Add Event**
4. Create a test event:
   - Title: "Tournament Finals"
   - Type: Tournament
   - Start Date: Feb 15, 2026 6:00 PM
   - End Date: Feb 15, 2026 9:00 PM
   - Location: Store Floor
   - Max Participants: 8
   - Entry Fee: 10.00
5. Click **Save**
6. Go to http://localhost:8000/events/
7. Verify event appears in list
8. Click on event to view details
9. Test filter by type:
   - Select "Tournament" from dropdown
   - Click Filter
   - Verify only tournament shows
10. Test upcoming filter:
   - Check "Upcoming only"
   - Verify events in future show

### Test 3: Service Management

**Goal**: Test adding and viewing services

**Steps**:
1. Go to http://localhost:8000/admin
2. Click **Services** → **Add Service**
3. Create a test service:
   - Title: "Beginner Army Painting"
   - Type: Painting Service
   - Skill Level: Beginner
   - Price: 50.00
   - Duration: 5 hours
   - Provider: "John's Painting Studio"
   - Contact: john@email.com
   - Available: ✓ (checked)
4. Click **Save**
5. Go to http://localhost:8000/services/
6. Verify service appears
7. Filter by skill level "Beginner"
8. Click on service to view full details
9. Verify all information displays correctly

### Test 4: Trading Post - Public View

**Goal**: Test viewing trading posts without login

**Steps**:
1. Go to http://localhost:8000/trading/
2. Verify page loads
3. Note: "Post New Item" button shows "Login to Post"
4. Try search functionality:
   - Enter search term like "marines"
   - Verify search works

### Test 5: Trading Post - Create as Logged-In User

**Goal**: Test posting a new item

**Setup**:
1. Create a non-admin user account (via admin panel):
   - Go to Admin → Users → Add User
   - Username: testuser
   - Password: testpass123

**Steps**:
1. Go to http://localhost:8000/admin
2. Login as testuser (logout first if needed)
3. Go to http://localhost:8000/trading/
4. Click **Post New Item**
5. Fill out form:
   - Title: "Unpainted Space Marines"
   - Type: Selling
   - Faction: Space Marines
   - Condition: Good
   - Price: 35.00
   - Description: "Includes 10 tactical marines, 1 sergeant, 2 heavy weapons"
6. Upload an image (optional)
7. Click **Post Item**
8. Verify:
   - ✓ Redirects to item detail page
   - ✓ Your username shows as author
   - ✓ Post appears in trading list

### Test 6: Trading Post - Edit & Delete

**Goal**: Test modifying your own posts

**Prerequisites**: Must have a trading post created (Test 5)

**Steps**:
1. Go to http://localhost:8000/trading/
2. Click on the post you created
3. Click **Edit**
4. Change:
   - Title to "Painted Space Marines"
   - Price to "45.00"
5. Click **Save Changes**
6. Verify changes appear on detail page
7. Click **Edit** again
8. Change condition to "Like New"
9. Click **Save Changes**
10. Go back to trading list
11. On your post, click **Delete**
12. Confirm deletion
13. Verify post no longer shows (but may still be searchable by admin)

### Test 7: Filtering & Search

**Goal**: Test search and filter functionality

**Prerequisites**: Add multiple trading posts with different factions

**Steps**:
1. Create 3+ posts with different factions (Chaos, Necrons, etc.)
2. Go to http://localhost:8000/trading/
3. Test faction filter:
   - Enter "Chaos" in faction field
   - Click Search
   - Verify only Chaos items show
4. Test type filter:
   - Select "Selling" from dropdown
   - Click Search
   - Verify only selling posts show
5. Test combined filters:
   - Type: Selling
   - Faction: Space Marines
   - Search: "painted"
   - Click Search

### Test 8: Admin Moderation

**Goal**: Test admin ability to manage all posts

**Steps**:
1. Go to http://localhost:8000/admin
2. Login as superuser
3. Click **Trade Posts**
4. Verify you see all posts including others'
5. Click on a post
6. Uncheck **Is Active**
7. Click **Save**
8. Go to http://localhost:8000/trading/
9. Verify that post no longer appears publicly
10. Go back to admin, re-check **Is Active**
11. Verify post reappears on public site

### Test 9: Navigation Bar

**Goal**: Test navigation across all pages

**Steps**:
1. Click navbar **Events** → Goes to events list
2. Click navbar **Services** → Goes to services list
3. Click navbar **Trading Post** → Goes to trading list
4. When logged in:
   - Navbar shows your username
   - Click dropdown
   - Verify "Admin Panel" link (if staff)
   - Click "Logout" to test logout
5. When logged out:
   - See "Login" button
   - Click to go to admin login

### Test 10: Mobile Responsiveness

**Goal**: Verify mobile layout works

**Steps**:
1. Open Chrome DevTools (F12)
2. Click device toggle (Ctrl+Shift+M)
3. Test different sizes:
   - iPhone (375px)
   - iPad (768px)
   - Desktop (1440px)
4. Verify:
   - ✓ Navigation collapses to hamburger menu on mobile
   - ✓ Cards stack properly
   - ✓ Images scale correctly
   - ✓ Forms are readable

## Data for Testing

### Sample Event
```
Title: "Spring Tournament"
Type: Tournament
Location: Downtown Store
Participants: 12/16
Entry Fee: $15
Date: Mar 1, 2026 6:00 PM
Description: "Win prizes and glory! $100 first place prize."
```

### Sample Service
```
Title: "Expert Competitive Coaching"
Type: Coaching
Provider: "Mike the Mentor"
Price: $75/session
Duration: 3 hours
Skill: Advanced
Contact: mike@store.com
```

### Sample Trading Post
```
Title: "Beautiful Painted Necrons Army"
Type: Selling
Faction: Necrons
Condition: Like New
Price: $120
Description: "Fully painted, sealed with matte varnish. Includes 20 warriors, 3 immortals, 1 overlord, 2 annihilation barges."
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Can't upload images | Make sure media folder exists. Run: `mkdir media media/trade_posts` |
| Posts not showing | Check if "Is Active" is checked. Admin can hide posts. |
| Can't edit someone else's post | This is correct behavior - only post author or admin can edit |
| Server not starting | Activate venv, run migrations: `python manage.py migrate` |
| CSS/Icons not loading | Make sure to run: `python manage.py collectstatic` |

## Performance Testing

### Load Multiple Items
1. Admin panel
2. Go to Events
3. Create 10+ events
4. Go to http://localhost:8000/events/
5. Page should load smoothly
6. Filter and search should be fast

### Test with Images
1. Add trading posts with various image sizes
2. Verify images display correctly
3. Check that pages load reasonably fast

## Final Checklist

Before deployment:
- [ ] All 3 models (Events, Services, Posts) working
- [ ] Admin can CRUD all models
- [ ] Users can view all public pages
- [ ] Logged-in users can create posts
- [ ] Only post authors can edit/delete their posts
- [ ] Admin can moderate all posts
- [ ] Navigation works across all pages
- [ ] Mobile responsive layout works
- [ ] Images upload and display correctly
- [ ] Filtering and search functional
- [ ] Admin guide written and clear

## Next Steps

1. **Populate with real data** - Add actual events, services, and posts
2. **Customize styling** - Edit CSS in `static/css/`
3. **Add user accounts** - Create accounts for staff members
4. **Set up messaging** (future) - Let users contact each other
5. **Backup database** - Regularly backup `db.sqlite3`

Great! Your Warhammer 40K store management system is ready to use!
