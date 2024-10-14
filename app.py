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
            try:
                with open(ROOM_DATA_FILE, 'r') as f:
                    st.session_state.rooms = json.load(f)
            except json.JSONDecodeError:
                st.session_state.rooms = initialize_rooms()
        else:
            st.session_state.rooms = initialize_rooms()

# Function to initialize rooms if room data file doesn't exist
def initialize_rooms():
    rooms = {"Suite Presidential": {"capacity": 2, "occupants": []}}  # Rename Room 1
    rooms.update({f"#{i}": {"capacity": 2 if i <= 51 else 3, "occupants": []} for i in range(2, 71)})
    with open(ROOM_DATA_FILE, 'w') as f:
        json.dump(rooms, f)
    return rooms

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

# Function to manually update rooms from a list
def update_rooms_from_list(manual_data):
    # Split by newlines and process each line
    for line in manual_data.strip().split('\n'):
        name, room, hoodie_size = line.split('\t')
        room_details = st.session_state.rooms.get(room)
        
        # If the room exists and isn't full
        if room_details and len(room_details['occupants']) < room_details['capacity']:
            room_details['occupants'].append({"name": name, "hoodie_size": hoodie_size})
            
            # Save user data as well
            user_data = {"name": name, "hoodie_size": hoodie_size, "room": room}
            save_user_data(user_data)
        else:
            st.warning(f"Room {room} is full or does not exist.")
    
    save_rooms()  # Save the updated room data after all entries

# Manual data from the user (your list)
manual_room_data = """
Ariel Ratzonel	#1	M
Hillel Balas	#1	M
Rebeca de Toro	#4	S
Raquel Bitan	#4	S
Shirel Assayag	#5	M
Myriam Anahory	#5	M
Nicole Benzaquen	#6	M
Sarah Belilty	#6	M
Sarah De Talavera	#7	M
Dafna Benhamu López-Bleda	#7	M
Nimrod Abraham	#8	L
Daniel Museyri	#8	L
Sol Eisenberg	#9	M
Debbie Scharf	#9	M
Guila Chocron	#10	M
Talia Chocron	#10	M
Gael Ankaoua	#11	M
Aryeh Yaacov Salama	#11	M
Ilan Israel	#14	M
Elie Halioua	#14	XL
Mena Nidam	#15	XXL
Jake Fereres	#15	XXL
Niso Abecasis	#16	XL
Armando Berros	#16	L
Niso Abecasis	#17	XL
Armando Berros Melul	#17	L
Moises Ayach	#18	L
Jacob Benchaya	#18	XL
Carlos Balas	#19	L
Isaac Eskenazi	#19	XXL
Rebeca Levy	#20	M
Yael Casquet Chocron	#20	M
Esther Benzaquen	#21	L
Yael Benhamu	#21	M
Arie Hassan	#22	S
Mark Vaisberg	#22	L
Dalit Taub	#23	L
Sofía Romano	#23	M
Joseph Bensusan Azulay	#25	M
Salomon Benhamu	#25	M
David Martin	#29	XL
Mena Gabizon	#29	M
Jonathan Sultan	#45	XL
Moises Bittan Aserraf	#45	M
Simon Salama Chocron	#45	S
Jack Israel	#45	L
Meir Bencheluch Aserraf	#48	M
Joseph Benhamu	#48	L
Isabella Sutton	#49	S
Isabella Fincheltub	#49	L
Martina Steimetz	#50	L
Nicole Steimetz Kerszberg	#50	L
Shirly Levi	#52	M
Alexandra Berman Benhamu	#52	M
Estrella Benzaquen	#53	S
Nogah Punturello	#53	S
Rebeca Levy	#54	M
Raquel Martin	#54	M
Michelle Titievsky	#54	M
Yaniv Salguero	#55	L
Yoav Salguero	#55	M
Abraham Amar	#55	L
"""

# Call function to update rooms from the list
update_rooms_from_list(manual_room_data)

st.title("Shabbaton")

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
