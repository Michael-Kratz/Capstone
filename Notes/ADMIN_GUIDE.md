# Admin Quick Start Guide

## Creating Your Admin Account

Before you can access the admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

Enter:
- Username: (your choice)
- Email: (your email)
- Password: (secure password)

## Accessing Admin Panel

1. Start the development server: `python manage.py runserver`
2. Go to: http://localhost:8000/admin
3. Login with your superuser credentials

## Managing Events

### Add a New Event
1. Click **Events** in the sidebar
2. Click **Add Event**
3. Fill in:
   - **Title**: Event name (e.g., "February Tournament")
   - **Description**: Event details
   - **Event Type**: Choose tournament, league, casual, or workshop
   - **Start Date**: Date and time event begins
   - **End Date**: Date and time event ends
   - **Location**: Where the event is held
   - **Max Participants**: Maximum people allowed (optional)
   - **Entry Fee**: Cost to enter (if any)
4. Click **Save**

### Edit an Event
1. Click **Events** in the sidebar
2. Click on the event you want to edit
3. Make changes and click **Save**

### Delete an Event
1. Click **Events** in the sidebar
2. Select checkbox next to event
3. Select "Delete selected events" from Action dropdown
4. Click **Go**

## Managing Services

### Add a Painting or Coaching Service
1. Click **Services** in the sidebar
2. Click **Add Service**
3. Fill in:
   - **Title**: Service name (e.g., "Army Painting")
   - **Description**: What the service includes
   - **Service Type**: Painting, Coaching, or Commission
   - **Price**: Service cost
   - **Duration (hours)**: How long it takes
   - **Skill Level**: Beginner, Intermediate, or Advanced
   - **Provider Name**: Who's providing the service
   - **Provider Contact**: Phone/email/Discord
   - **Available**: Check if currently available
4. Click **Save**

### Manage Services
- **Change availability**: Edit service and toggle "Available" checkbox
- **Update prices**: Edit and change the price field
- **Remove service**: Select checkbox and delete

## Managing Trading Posts

### View All Posts
1. Click **Trade Posts** in the sidebar
2. See all posts with filter options
3. Search by title, description, faction, or author

### Filter Posts
- **Post Type**: Selling, Buying, or Trading
- **Condition**: New, Like New, Good, Fair, Poor
- **Faction**: Filter by Warhammer faction
- **Is Active**: Show active or inactive posts

### Moderate Posts
1. Click on a post to view details
2. Check the image and description
3. If inappropriate:
   - Uncheck **Is Active** to hide the post
   - Click **Save**

### Delete Inappropriate Posts
- Uncheck **Is Active** instead of fully deleting
- This keeps record but hides from public view

## Key Admin Features

### Bulk Actions
Select multiple items using checkboxes, then:
1. Choose action from dropdown at bottom
2. Click **Go**
3. Available actions: Delete (use cautiously)

### Search
Use the search box at top of each model list to quickly find:
- Events by title or location
- Services by provider or title
- Posts by title, faction, or author

### Filtering
Click filter categories on the right sidebar:
- **By Date**: Filter events by start date
- **By Type**: Filter by category
- **By Status**: Filter by active/available

### Sorting
Click column headers to sort:
- Events: By date, participants, entry fee
- Services: By type, price, skill level
- Posts: By date, condition, faction

## Pro Tips

### Best Practices
- **Always preview** - Click on items to preview how they appear to users
- **Keep descriptions clear** - Customers read these to decide
- **Update regularly** - Keep event dates and service availability current
- **Monitor posts** - Review trading posts regularly for quality
- **Respond quickly** - Users checking your site want current info

### Performance Tips
- Add 3-5 key events each month
- Keep 10-15 active services listed
- Review trading posts weekly
- Delete/archive very old events (>1 month past)

### Common Tasks

**Making an announcement?** 
- Add an event with type "Workshop" and description with news

**Staff out of town?**
- Uncheck "Available" on their services temporarily

**Special promotion?**
- Create a special event with description of offer

**Remove spam posts?**
- Find post, uncheck "Is Active", save

## Need Help?

Check the main README.md for:
- Full feature list
- Complete URL routes
- Troubleshooting guide
- Database model details

## Quick Links
- Admin Dashboard: http://localhost:8000/admin
- Main Site: http://localhost:8000
- Trading Post: http://localhost:8000/trading
- Services: http://localhost:8000/services
- Events: http://localhost:8000/events
