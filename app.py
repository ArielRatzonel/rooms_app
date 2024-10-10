import streamlit as st
import json
import os

# Define the file to store room data
ROOM_DATA_FILE = 'room_data.json'

# Load room data once and cache it for performance
@st.cache_data
def load_rooms():
    if os.path.exists(ROOM_DATA_FILE):
        with open(ROOM_DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        # Initialize room data if not available
        rooms = {f"Room {i}": {"capacity": 2 if i <= 20 else 3, "occupants": []} for i in range(1, 41)}
        with open(ROOM_DATA_FILE, 'w') as f:
            json.dump(rooms, f)
        return rooms

# Save room data
def save_rooms(rooms):
    with open(ROOM_DATA_FILE, 'w') as f:
        json.dump(rooms, f)

# Load rooms from file (cached)
rooms = load_rooms()

st.title("Camp Room Assignment")

# Allow user to select a room and enter name
st.write("Select a room and enter your name:")

room_selection = st.selectbox("Choose a room:", [room for room, details in rooms.items() if len(details['occupants']) < details['capacity']])
name_input = st.text_input("Enter your name:")

if st.button("Submit"):
    if name_input:
        rooms[room_selection]['occupants'].append(name_input)
        save_rooms(rooms)  # Save updated data
        st.success(f"Your name has been added to {room_selection}!")
    else:
        st.error("Please enter your name before submitting.")

# Display all rooms in a simplified grid layout using expander
st.write("### Current Room Status:")
for room, details in rooms.items():
    with st.expander(room, expanded=False):  # Collapsible section for mobile
        st.write(f"Capacity: {details['capacity']}")
        occupants = ", ".join(details['occupants']) if details['occupants'] else "Available"
        st.write(f"Occupants: {occupants}")
        st.write("Status: 🟢 Available" if len(details['occupants']) < details['capacity'] else "Status: 🔴 Full")
