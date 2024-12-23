import streamlit as st
from locate_donor import LocationService  # Assuming this is your location processing logic module

class BloodSeaApp:
    def __init__(self):
        self.blood_groups = [
            "A RhD positive (A+",
            "A RhD negative (A-)",
            "B RhD positive (B+)",
            "B RhD negative (B-)",
            "O RhD positive (O+)",
            "O RhD negative (O-)",
            "AB RhD positive (AB+)",
            "AB RhD negative (AB-)"
        ]

    def render_form(self):
        # Display an image as a header
        st.image("https://via.placeholder.com/800x200.png?text=BloodSea", use_container_width=True)

        # Create a column layout for better alignment
        col1, col2 = st.columns([1, 2])
        
        # Name field
        name = col1.text_input("Name:", key="name", placeholder="Enter your name", help="Please enter your name")

        # Pincode field
        pincode = col2.text_input("Pincode:", key="pincode", placeholder="Enter your pincode", help="Please enter your pincode")

        # Blood group dropdown
        selected_blood_group = st.selectbox(
            "Blood Group:", options=self.blood_groups, key="blood_group", 
            help="Please select your blood group."
        )

        # Search button with icon
        if st.button("🔍 Search"):
            # Retrieve data from session state
            st.success("Details have been stored!")
            st.write(f"Name: {name}")
            st.write(f"Pincode: {pincode}")
            st.write(f"Blood Group: {selected_blood_group}")

            # Call LocationService to handle calculations and data filtering
            location_service = LocationService(pincode, selected_blood_group)
            donors_data = location_service.process_data()  # Processing data

            # Display results in a table
            if donors_data:
                st.write("Top 5 Closest Donors:")
                st.table(donors_data)  # Display the filtered data in a table
                # location_service.clear_output_csv()  # Clear the output CSV after processing
                st.markdown(
                    """
                    <a href="pages/donor_locations_map.html" target="_blank">
                        <button style="background-color:blue; color:white; padding:10px; border:none; border-radius:5px; cursor:pointer;">
                            View All Donors
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("No matching data found.")

        st.markdown("<hr>", unsafe_allow_html=True)

    def run(self):
        self.render_form()


# Run the application
if __name__ == "__main__":
    app = BloodSeaApp()
    app.run()
