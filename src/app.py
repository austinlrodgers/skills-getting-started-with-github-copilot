"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team for practices and games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "nina@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim laps and improve technique with the school swim club",
        "schedule": "Mondays, Wednesdays, 5:00 PM - 6:00 PM",
        "max_participants": 16,
        "participants": ["liam@mergington.edu", "emma@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 4:45 PM",
        "max_participants": 14,
        "participants": ["maya@mergington.edu", "zoe@mergington.edu"]
    },
    "Drama Society": {
        "description": "Practice acting, scenes, and stage production for school plays",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["liya@mergington.edu", "ethan@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation skills and compete in debate tournaments",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "hannah@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for science competitions and explore STEM challenges",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
# Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
