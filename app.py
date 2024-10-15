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

# Checkbox for users who don't know who to share a room with
unsure_checkbox = st.checkbox("I don't know who to share a room with")

# If checkbox is selected, room selection is disabled
if unsure_checkbox:
    st.info("You will be assigned to a room later, and we will let you know soon.")
    room_selection = None
else:
    # Display room selection with status in the specified format
    room_selection = st.selectbox(
        "Choose a room: Rooms 1-51 are doubles, rooms 52-70 are triples",
        [get_room_status(room, details) for room, details in st.session_state.rooms.items() if len(details['occupants']) < details['capacity']]
    )

name_input = st.text_input("Enter your Name and Surname:")

# Adding hoodie size selection
hoodie_size = st.selectbox("Select your hoodie size:", ['S','L', 'XL', 'XXL'])

if st.button("Submit"):
    if name_input and hoodie_size:
        # Check if the user doesn't know who to share a room with
        if unsure_checkbox:
            selected_room = "Room 0"  # Assign to Room 0 if they are unsure
            st.success("We will assign you to a room and let you know soon.")
        else:
            # Get selected room (extracting room name before the status details in parentheses)
            selected_room = room_selection.split(',')[0]
            room_details = st.session_state.rooms[selected_room]
            
            # Check if the room is full
            if len(room_details['occupants']) < room_details['capacity']:
                # Add the user's name and hoodie size to the selected room by appending
                room_details['occupants'].append({"name": name_input, "hoodie_size": hoodie_size})
                save_rooms()  # Save updated room data
                st.success(f"Your name has been added to {selected_room} with hoodie size {hoodie_size}!")
            else:
                st.error(f"{selected_room} is full! Please choose another room.")
                st.stop()

        # Save the user's data to a separate file
        user_data = {"name": name_input, "hoodie_size": hoodie_size, "room": selected_room}
        save_user_data(user_data)  # Save the new user data
    else:
        st.error("Please enter your name and select a hoodie size before submitting.")

# Function to manually update rooms from the provided list
def update_rooms_from_list(manual_data):
    # Split by newlines and process each line
    for line in manual_data.strip().split('\n'):
        try:
            name, room, hoodie_size = line.split('\t')
            room_details = st.session_state.rooms.get(room)
            
            # If the room exists and has available capacity
            if room_details and len(room_details['occupants']) < room_details['capacity']:
                room_details['occupants'].append({"name": name, "hoodie_size": hoodie_size})
                
                # Save user data as well
                user_data = {"name": name, "hoodie_size": hoodie_size, "room": room}
                save_user_data(user_data)
            # Skip if the room is full or doesn't exist without raising any errors
        except ValueError:
            pass  # Ignore lines with incorrect formatting and continue

    # Save the updated room data after processing all entries
    save_rooms()



# Manual data from the user (your list)
manual_room_data = """
Ariel Ratzonel\t#1\tM
Hillel Balas\t#1\tM
Shirly Levi\t#2\tM
Alexandra Berman Benhamu\t#2\tM
Estrella Benzaquen\t#3\tS
Nogah Punturello\t#3\tS
Rebeca de Toro\t#4\tS
Raquel Bitan\t#4\tS
Shirel Assayag\t#5\tM
Myriam Anahory\t#5\tM
Nicole Benzaquen\t#6\tM
Sarah Belilty\t#6\tM
Sarah De Talavera\t#7\tM
Dafna Benhamu López-Bleda\t#7\tM
Nimrod Abraham\t#8\tL
Daniel Museyri\t#8\tL
Sol Eisenberg\t#9\tM
Debbie Scharf\t#9\tM
Guila Chocron\t#10\tM
Talia Chocron\t#10\tM
Gael Ankaoua\t#11\tM
Aryeh Yaacov Salama\t#11\tM
Ilan Israel\t#14\tM
Elie Halioua\t#14\tXL
Mena Nidam\t#15\tXXL
Jake Fereres\t#15\tXXL
Niso Abecasis\t#16\tXL
Armando Berros\t#16\tL
Moises Ayach\t#18\tL
Jacob Benchaya\t#18\tXL
Carlos Balas\t#19\tL
Isaac Eskenazi\t#19\tXXL
Rebeca Levy\t#20\tM
Yael Casquet Chocron\t#20\tM
Esther Benzaquen\t#21\tL
Yael Benhamu\t#21\tM
Arie Hassan\t#22\tS
Mark Vaisberg\t#22\tL
Dalit Taub\t#23\tL
Sofía Romano\t#23\tM
Joseph Bensusan Azulay\t#25\tM
Salomon Benhamu\t#25\tM
David Martin\t#29\tXL
Mena Gabizon\t#29\tM
Moises Bittan Aserraf\t#45\tM
Simon Salama Chocron\t#45\tS
Jonathan Sultan\t#46\tXL
Jack Israel\t#46\tL
Meir Bencheluch Aserraf\t#48\tM
Joseph Benhamu\t#48\tL
Isabella Sutton\t#49\tS
Isabella Fincheltub\t#49\tL
Martina Steimetz\t#50\tL
Nicole Steimetz Kerszberg\t#50\tL
Rebeca Levy\t#54\tM
Raquel Martin\t#54\tM
Michelle Titievsky\t#54\tM
Yaniv Salguero\t#55\tL
Yoav Salguero\t#55\tM
Abraham Amar\t#55\tL
Arie Benzadón\t#57\tM
Eyal Nahon\t#57\tS
Mijael Coen\t#57\tS
Valeria Benain\t#12\tM
Yamila Abraham\t#12\tM
Susan balas picciotto\t#51\tM
Valentina Bendiske Goldstein\t#51\tM
Tom Treiband\t#35\tL
Alexis Taub\t#35\tL
Federico Alberio\t#27\tM
Brandon Tub\t#27\tM
Moshe Bittan\t#17\tL
Yosef Benzaquen\t#17\tM
Alberto Elejalde\t#13\tL
Armando Benaim\t#13\tL
Taliah Lasry\t#26\tM
Noemi Benhamu\t#26\tM
Simon Sebban\t#52\tM

"""

# Call the update function with the manual data
update_rooms_from_list(manual_room_data)

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
