import streamlit as st
import pandas as pd
from pymongo.mongo_client import MongoClient
from src.agstyler import PINLEFT, PRECISION_TWO, draw_grid

uri = "mongodb+srv://saumya:helloworld@mycluster101.keorneq.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)

db = client["hospital_management"]
appointments_collection = db["appointments"]
patients_collection = db["patients"]
doctors_collection = db["doctors"]
invoices_collection = db["invoices"]
reports_collection = db["reports"]
users_collection = db["users"]


# Create Streamlit app and define layout
st.set_page_config(page_title="Hospital Management App", layout="wide")

# User authentication
def authenticate(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == password:
        return user
    return None

# Main function
def main():
    # Authentication
    # Check if user is logged in
    if "user" not in st.session_state:
        st.error("Authentication failed. Please log in.")
        st.stop()

    user = st.session_state["user"]
    logout_button = """
        <style>
        .logout-button {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 999;
        }
        </style>
        <button class="logout-button" onclick="logout()">Logout</button>
        <script>
        function logout() {
            fetch('/_logout', { method: 'POST' });
            location.reload();
        }
        </script>
    """

    st.markdown(logout_button, unsafe_allow_html=True)
    

    # Appointment Booking
    st.sidebar.subheader("Appointment Booking")
    doctor_name = st.sidebar.text_input("Doctor's Name", key="doctor_name")
    appointment_date = st.sidebar.date_input("Appointment Date", key="appointment_date")
    appointment_time = st.sidebar.time_input("Appointment Time", key="appointment_time")
    book_appointment = st.sidebar.button("Book Appointment", key="book_appointment")
    
    if book_appointment:
        if doctor_name and appointment_date and appointment_time:
            appointment = {
                "doctor_name": doctor_name,
                "date": str(appointment_date),
                "time": str(appointment_time),
                "user_id": str(user["_id"])
            }
            appointments_collection.insert_one(appointment)
            st.sidebar.success("Appointment booked successfully!")
        else:
            st.sidebar.error("Please fill in all the appointment details!")
   
    st.sidebar.divider()
    # Patient Records
    st.sidebar.subheader("Patient Records")
    patient_name = st.sidebar.text_input("Patient Name")
    patient_age = st.sidebar.number_input("Patient Age", min_value=0, max_value=150)
    patient_gender = st.sidebar.selectbox("Patient Gender", ["Male", "Female", "Other"])
    patient_history = st.sidebar.text_area("Medical History")
    add_patient = st.sidebar.button("Add Patient")
    

    if add_patient:
        if patient_name and patient_age and patient_gender:
            patient = {
                "name": patient_name,
                "age": patient_age,
                "gender": patient_gender,
                "medical_history": patient_history,
                "user_id": user["_id"]
            }
            patients_collection.insert_one(patient)
            st.sidebar.success("Patient added successfully!")
        else:
            st.sidebar.error("Please fill in all the patient details!")
    
    st.sidebar.divider()
    
    row_number = st.number_input('Number of rows', min_value=0, value=20)
    
    

    # Retrieve patient records from MongoDB and convert Cursor to DataFrame
    patient_cursor = patients_collection.find({"user_id": user["_id"]}).limit(row_number)
   
    # Retrieve appointments data from MongoDB and convert Cursor to DataFrame
    appointment_cursor = appointments_collection.find({"user_id": user["_id"]}).limit(row_number)
    
    # Divide the screen into two columns
    col1, col2 = st.beta_columns(2)
    
    with col1:
        # Display Patient Records
        st.subheader("Patient Records")
        patient_records = []
        for patient in patient_cursor:
            patient_records.append({
                "Patient Name": patient["name"],
                "Age": patient["age"],
                "Gender": patient["gender"],
                "Medical History": patient["medical_history"]
            })
        if len(patient_records) > 0:
            col1.table(patient_records)
        else:
            col1.info("No patient records found.")
            
    with col2:
        # Display Appointments Records
        st.subheader("Appointments")
        appointment_records = []
        for appointment in appointment_cursor:
            appointment_records.append({
                "Doctor Name": patient["doctor_name"],
                "Appointment Date": patient["date"],
                "Appointment Time": patient["time"]
            })
        if len(appointment_records) > 0:
            col2.table(appointment_records)
        else:
            col2.info("No appointment records found.")
        
        
    st.sidebar.divider()
    # Doctor's Schedule
    if user["is_admin"]:
        st.sidebar.subheader("Doctor's Schedule")
        doctor_name = st.sidebar.text_input("Doctor's Name")
        doctor_schedule = st.sidebar.text_area("Doctor's Schedule")
        update_schedule = st.sidebar.button("Update Schedule")

        if update_schedule:
            if doctor_name and doctor_schedule:
                doctor = doctors_collection.find_one({"name": doctor_name})
                if doctor:
                    doctors_collection.update_one(
                        {"name": doctor_name},
                        {"$set": {"schedule": doctor_schedule}}
                    )
                    st.sidebar.success("Doctor's schedule updated successfully!")
                else:
                    st.sidebar.error("Doctor not found!")
            else:
                st.sidebar.error("Please fill in all the doctor schedule details!")
    
    st.sidebar.divider()
    # Billing and Payments
    st.sidebar.subheader("Billing and Payments")
    view_invoices = st.sidebar.button("View Invoices")
    make_payment = st.sidebar.button("Make Payment")

    if view_invoices:
        st.subheader("Invoices")
        invoices_cursor = invoices_collection.find({"user_id": user["_id"]})
        for invoice in invoices_cursor:
            st.write(f"Invoice ID: {invoice['_id']}")
            st.write(f"Amount: {invoice['amount']}")
            st.write(f"Status: {invoice['status']}")
            st.write("-------------------------")
    
   
    
    # Retrieve patient records from MongoDB and convert Cursor to DataFrame
    doctor_cursor = doctors_collection.find({"user_id": user["_id"]}).limit(row_number)
   
    # Retrieve appointments data from MongoDB and convert Cursor to DataFrame
    invoice_cursor = invoices_collection.find({"user_id": user["_id"]}).limit(row_number)
    
    # Divide the screen into two columns
    col1, col2 = st.beta_columns(2)
    
    with col1:
        # Display Patient Records
        st.subheader("Doctors Schedule")
        doctor_schedules = []
        for doctor in doctor_cursor:
            doctor_schedules.append({
                "Doctor Name": doctor["name"],
                "Schedule": doctor["schedule"]
        })
        if len(doctor_schedules) > 0:
            col1.table(doctor_schedules)
        else:
            col1.info("No doctor schedules found.")
            
    with col2:
        # Display Invoices
        st.subheader("Invoices")
        invoice_records = []
        for invoice in invoice_cursor:
            invoice_records.append({
                "Invoice ID": invoice["_id"],
                "Amount": invoice["amount"],
                "Status": invoice["status"]
            })
        if len(invoice_records) > 0:
            col2.table(invoice_records)
        else:
            col2.info("No invoices found.")   
            
    if make_payment:
        st.subheader("Make Payment")
        invoice_id = st.text_input("Invoice ID")
        payment_amount = st.number_input("Payment Amount")
        submit_payment = st.button("Submit Payment")

        if submit_payment:
            if invoice_id and payment_amount > 0:
                invoice = invoices_collection.find_one({"_id": invoice_id})
                if invoice:
                    if invoice["status"] == "unpaid":
                        # Update the invoice status and payment amount
                        invoices_collection.update_one(
                            {"_id": invoice_id},
                            {"$set": {"status": "paid", "payment_amount": payment_amount}}
                        )
                        st.success("Payment successful!")
                    else:
                        st.warning("Invoice is already paid.")
                else:
                    st.error("Invoice not found.")
            else:
                st.error("Please provide a valid invoice ID and payment amount.")
    
    st.sidebar.divider()
    # Reports and Analytics
    st.sidebar.subheader("Reports and Analytics")
    generate_report = st.sidebar.button("Generate Report")

    if generate_report:
        st.subheader("Generate Report")
        report_type = st.selectbox("Select Report Type", ["Appointment", "Patient"])
        generate_button = st.button("Generate")

        if generate_button:
            if report_type == "Appointment":
                # Generate appointment report
                report_data = []
                appointment_cursor = appointments_collection.find({})
                for appointment in appointment_cursor:
                    report_data.append(appointment)
                reports_collection.insert_one({"report_type": "Appointment", "data": report_data})
                st.success("Appointment report generated!")
            elif report_type == "Patient":
                # Generate patient report
                report_data = []
                patient_cursor = patients_collection.find({})
                for patient in patient_cursor:
                    report_data.append(patient)
                reports_collection.insert_one({"report_type": "Patient", "data": report_data})
                st.success("Patient report generated!")
    st.divider()
    # Divide the screen into two columns
    col1, col2 = st.beta_columns(2)
    with col1:
        #Display Appointment Report
        st.subheader("Appointment Report")
        report_data = []
        appointment_cursor = appointments_collection.find({},{"_id":0}).limit(row_number)
        for appointment in appointment_cursor:
            report_data.append(appointment)
        if len(report_data) > 0:
            col1.table(report_data)
        else:
            col1.info("No appointment records found.")
        reports_collection.insert_one({"report_type": "Appointment", "data": report_data})
        st.success("Appointment report generated!")

    with col2:
    # Display Patient Report
        st.subheader("Patient Report")
        report_data = []
        patient_cursor = patients_collection.find({},{"_id":0}).limit(row_number)
        for patient in patient_cursor:
            report_data.append(patient)
        if len(report_data) > 0:
            col2.table(report_data)
        else:
            col2.info("No patient records found.")
        reports_collection.insert_one({"report_type": "Patient", "data": report_data})
        st.success("Patient report generated!")
    
    # User Management
    if user["is_admin"]:
        st.sidebar.subheader("User Management")
        manage_users = st.sidebar.button("Manage Users")

        if manage_users:
            st.subheader("Manage Users")
            all_users = users_collection.find({})
            user_records = []
            for user in all_users:
                user_records.append({
                    "User ID": user["_id"],
                    "Name": user["name"],
                    "Email": user["email"],
                    "Is Admin": user["is_admin"]
                })

            if len(user_records) > 0:
                st.table(user_records)
            else:
                st.info("No user records found.")
            # Add Users
            st.subheader("Add Users")
            new_user_name = st.text_input("Name")
            new_user_email = st.text_input("Email")
            new_user_password = st.text_input("Password", type="password")
            is_admin = st.checkbox("Is Admin")

            add_user = st.button("Add User")

            if add_user:
                if new_user_name and new_user_email and new_user_password:
                    new_user = {
                        "name": new_user_name,
                        "email": new_user_email,
                        "password": new_user_password,
                        "is_admin": is_admin
                    }
                    users_collection.insert_one(new_user)
                    st.success("User added successfully!")
                else:
                    st.error("Please fill in all the user details!")
    if manage_users:
            st.subheader("Manage Users")
            all_users = users_collection.find({})
            user_records = []
            for user in all_users:
                user_records.append({
                    "User ID": user["_id"],
                    "Name": user["name"],
                    "Email": user["email"],
                    "Is Admin": user["is_admin"],
                    "Action": st.button(f"Remove##{user['_id']}")
                })

            if len(user_records) > 0:
                df = pd.DataFrame(user_records)
                df.set_index("User ID", inplace=True)
                st.dataframe(df)
            else:
                st.info("No user records found.")

            for user_record in user_records:
                if user_record["Action"]:
                    user_id = user_record.name
                    users_collection.delete_one({"_id": user_id})
                    st.success("User removed successfully!")            
        
    
    
# User login
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Log In")

    if login_button:
        user = authenticate(username, password)
        if user:
            st.success("Authentication successful!")
            st.session_state["user"] = user
        else:
            st.error("Authentication failed. Please try again.")

# Run the app
if __name__ == "__main__":
    if "user" not in st.session_state:
        login()
    else:
        main()
