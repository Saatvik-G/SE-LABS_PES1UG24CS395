"""Event management system for organizing meetups and tracking guest attendance."""

import json
import secrets
from datetime import date

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create a new event with venue, capacity, and an isolated guest list."""
    if guests is None:
        guests = []
    events[event_name] = {"venue": venue, "capacity": capacity,
                          "guests": guests}
    return events[event_name]


def register_guest(event_name, guest):
    """Register a guest for a specified event if capacity permits."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Calculate the remaining seat capacity for an event."""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Determine whether an event is upcoming or completed based on current date."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order="name"):
    """Generate a sorted comma-separated string of registered guest names."""
    is_descending = sort_order == "desc"
    names = sorted(events[event_name]["guests"], reverse=is_descending)
    return ", ".join(names)


def save_events(file_name="events.json"):
    """Persist all events dictionary into a structured JSON file."""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)


def load_events(file_name="events.json"):
    """Load and restore events data from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def print_badges(event_name):
    """Generate printable text badges for registered guests."""
    filename = f"badges_{event_name}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for guest in events.get(event_name, {}).get("guests", []):
            f.write(f"Badge: {guest} | Event: {event_name}\n")


def main():
    """Run demonstration workflow for event creation, registration, and persistence."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop",2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left=seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup", "name"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    winner = secrets.choice(events["Tech Meetup"]["guests"])
    print("Lucky draw winner:", winner)
    save_events()
    restored = load_events() # reload to confirm the save worked
    print("Events restored from file:", len(restored))
    print("Venues:", [e["venue"] for e in restored.values()])

main()
