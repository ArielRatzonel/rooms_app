import streamlit as st
import json
import os

# Define the file to store room data
ROOM_DATA_FILE = 'room_data.json'

# Function to load room data once and store it in session state
def load_rooms():
    if 'rooms' not in st.session_state:
        if os.path.exists(ROOM_DATA_FILE):
            with open(ROOM_DATA_FILE, 'r') as f:
                st.session_state.rooms = json.load(f)
        else:
            # Initialize room data if not available
            rooms = {f"Room {i}": {"capacity": 2 if i <= 20 else 3, "occupants": []} for i in range(1, 41)}
            with open(ROOM_DATA_FILE, 'w') as f:
                json.dump(rooms, f)
            st.session_state.rooms = rooms

# Function to save room data
def save_rooms():
    with open(ROOM_DATA_FILE, 'w') as f:
        json.dump(st.session_state.rooms, f)

# Load rooms once (cached in session state for faster interaction)
load_rooms()

st.title("Camp Room Assignment")

# Display available rooms
st.write("Select a room and enter your name:")

room_selection = st.selectbox("Choose a room:", [room for room, details in st.session_state.rooms.items() if len(details['occupants']) < details['capacity']])
name_input = st.text_input("Enter your name:")

if st.button("Submit"):
    if name_input:
        # Add the user's name to the selected room
        st.session_state.rooms[room_selection]['occupants'].append(name_input)
        save_rooms()  # Save updated data
        st.success(f"Your name has been added to {room_selection}!")
    else:
        st.error("Please enter your name before submitting.")

# Display all rooms in a grid layout (no pagination)
def display_rooms(rooms, cols=3):
    col_list = st.columns(cols)  # Split the page into columns

    for i, (room, details) in enumerate(rooms.items()):
        with col_list[i % cols]:  # Distribute rooms across columns
            st.subheader(room)  # Room title
            st.write(f"Capacity: {details['capacity']}")
            occupants = ", ".join(details['occupants']) if details['occupants'] else "Available"
            st.write(f"Occupants: {occupants}")
            if len(details['occupants']) < details['capacity']:
                st.write("Status: 🟢 Available")
            else:
                st.write("Status: 🔴 Full")

# Display all rooms in a grid (3 rooms per row)
st.write("### Current Room Status:")
display_rooms(st.session_state.rooms)
