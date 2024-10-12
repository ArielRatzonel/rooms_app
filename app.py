import streamlit as st
import json
import os

# Define the file to store room data and user data
ROOM_DATA_FILE = 'room_data.json'
USER_DATA_FILE = 'user_data.json'  # New file for user information

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

# Function to save user data to file
def save_user_data(user_data):
    if os.path.exists(USER_DATA_FILE):
        try:
            # Load existing user data
            with open(USER_DATA_FILE, 'r') as f:
                users = json.load(f)
        except json.JSONDecodeError:
            # Handle the case where the file is empty or corrupted
            users = []
    else:
        users = []
    
    # Append the new user data
    users.append(user_data)
    
    # Save back to the file
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

# Load rooms once (cached in session state for faster interaction)
load_rooms()

st.title("Rooms assignment ")

# Display available rooms
st.write("Select a room, enter your name, and choose your hoodie size:")

room_selection = st.selectbox("Choose a room:", 
                              [room for room, details in st.session_state.rooms.items() if len(details['occupants']) < details['capacity']])

name_input = st.text_input("Enter your name:")

# Adding hoodie size selection
hoodie_size = st.selectbox("Select your hoodie size:", ['XS', 'S', 'M', 'L', 'XL', 'XXL'])

if st.button("Submit"):
    if name_input and hoodie_size:
        room_details = st.session_state.rooms[room_selection]
        # Check if the room is full
        if len(room_details['occupants']) < room_details['capacity']:
            # Add the user's name and hoodie size to the selected room by appending
            room_details['occupants'].append({"name": name_input, "hoodie_size": hoodie_size})
            save_rooms()  # Save updated room data
            
            # Save the user's data to a separate file
            user_data = {"name": name_input, "hoodie_size": hoodie_size, "room": room_selection}
            save_user_data(user_data)  # Save the new user data
            
            st.success(f"Your name has been added to {room_selection} with hoodie size {hoodie_size}!")
        else:
            st.error(f"{room_selection} is full! Please choose another room.")
    else:
        st.error("Please enter your name and select a hoodie size before submitting.")

# Display all rooms in a grid layout (in rows)
def display_rooms(rooms, cols=3):
    row_count = (len(rooms) + cols - 1) // cols  # Calculate how many rows we need
    for row in range(row_count):
        col_list = st.columns(cols)  # Create a new row of columns
        for col in range(cols):
            index = row * cols + col
            if index < len(rooms):
                room, details = list(rooms.items())[index]  # Get the room and its details
                with col_list[col]:  # Place the room details in the correct column
                    st.subheader(room)  # Room title
                    st.write(f"Capacity: {details['capacity']}")
                    
                    # Handle both strings and dictionaries for occupants
                    occupants = ", ".join([occupant["name"] for occupant in details['occupants']]) if details['occupants'] else "Available"
                    
                    st.write(f"Occupants: {occupants}")
                    if len(details['occupants']) < details['capacity']:
                        st.write("Status: 🟢 Available")
                    else:
                        st.write("Status: 🔴 Full")

# Display all rooms in a grid (3 rooms per row)
st.write("### Current Room Status:")
display_rooms(st.session_state.rooms)
