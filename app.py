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
            rooms = {f"#{i}": {"capacity": 2 if i <= 51 else 3, "occupants": []} for i in range(1, 71)}
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

# Function to load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# Load rooms once (cached in session state for faster interaction)
load_rooms()

st.title("Shabbaton")

# Function to get room status in the specified format
def get_room_status(room, details):
    occupants = details['occupants']
    capacity = details['capacity']
    num_occupants = len(occupants)
    
    if num_occupants == 0:
        occupant_status = "Empty"
    else:
        occupant_status = ", ".join([occupant["name"] for occupant in occupants])

    available_spots = capacity - num_occupants

    return f"{room}, {occupant_status}"

# Display room selection with status in the specified format
room_selection = st.selectbox(
    "Choose a room: Rooms 1-51 are doubles, rooms 52-70 are triples",
    [get_room_status(room, details) for room, details in st.session_state.rooms.items() if len(details['occupants']) < details['capacity']]
)

name_input = st.text_input("Enter your Name and Surname:")

# Adding hoodie size selection
hoodie_size = st.selectbox("Select your hoodie size:", ['XS', 'S', 'M', 'L', 'XL', 'XXL'])

if st.button("Submit"):
    if name_input and hoodie_size:
        # Get selected room (extracting room name before the status details in parentheses)
        selected_room = room_selection.split(',')[0]
        room_details = st.session_state.rooms[selected_room]
        
        # Check if the room is full
        if len(room_details['occupants']) < room_details['capacity']:
            # Add the user's name and hoodie size to the selected room by appending
            room_details['occupants'].append({"name": name_input, "hoodie_size": hoodie_size})
            save_rooms()  # Save updated room data
            
            # Save the user's data to a separate file
            user_data = {"name": name_input, "hoodie_size": hoodie_size, "room": selected_room}
            save_user_data(user_data)  # Save the new user data
            
            st.success(f"Your name has been added to {selected_room} with hoodie size {hoodie_size}!")
        else:
            st.error(f"{selected_room} is full! Please choose another room.")
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

# Section to display the list of users (admin link)
st.write("---")
st.write("### Admin Section")

# Password input and direct display of user data if correct
password = st.text_input("Enter access code to view the user list:", type="password")

if password == "1111":
    st.success("Access granted.")
    
    # Load and display user data
    user_data = load_user_data()
    
    if user_data:
        st.write("### Full List of Users:")
        for user in user_data:
            st.write(f"Name: {user['name']}, Room: {user['room']}, Hoodie Size: {user['hoodie_size']}")
    else:
        st.write("No user data available.")
elif password:
    st.error("Incorrect access code!")
