import streamlit as st
import json
import os

# Define the file to store room data
ROOM_DATA_FILE = 'room_data.json'

# Initialize room data if not available
if not os.path.exists(ROOM_DATA_FILE):
    rooms = {f"Room {i}": {"capacity": 2 if i <= 20 else 3, "occupants": []} for i in range(1, 41)}
    with open(ROOM_DATA_FILE, 'w') as f:
        json.dump(rooms, f)
else:
    with open(ROOM_DATA_FILE, 'r') as f:
        rooms = json.load(f)

st.title("Camp Room Assignment")

# Display available rooms
st.write("Select a room and enter your name:")

room_selection = st.selectbox("Choose a room:", [room for room, details in rooms.items() if len(details['occupants']) < details['capacity']])

name_input = st.text_input("Enter your name:")

if st.button("Submit"):
    if name_input:
        rooms[room_selection]['occupants'].append(name_input)
        
        # Save the updated data
        with open(ROOM_DATA_FILE, 'w') as f:
            json.dump(rooms, f)

        st.success(f"Your name has been added to {room_selection}!")
    else:
        st.error("Please enter your name before submitting.")

# Display the current room status
st.write("Current Room Status:")
for room, details in rooms.items():
    st.write(f"{room} (Capacity: {details['capacity']}): {', '.join(details['occupants']) if details['occupants'] else 'Available'}")
