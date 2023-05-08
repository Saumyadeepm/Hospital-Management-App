import streamlit as st
from pymongo.mongo_client import MongoClient

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
                "date": appointment_date,
                "time": appointment_time,
                "user_id": user["_id"]
            }
            appointments_collection.insert_one(appointment)
            st.sidebar.success("Appointment booked successfully!")
        else:
            st.sidebar.error("Please fill in all the appointment details!")

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

    # User Management
    if user["is_admin"]:
        st.sidebar.subheader("User Management")
        manage_users = st.sidebar.button("Manage Users")

        if manage_users:
            st.subheader("Manage Users")
            all_users = users_collection.find({})
            for user in all_users:
                st.write(f"User ID: {user['_id']}")
                st.write(f"Name: {user['name']}")
                st.write(f"Email: {user['email']}")
                st.write(f"Is Admin: {user['is_admin']}")
                st.write("-------------------------")

    # Display Appointments
    st.subheader("Appointments")
    appointment_cursor = appointments_collection.find({"user_id": user["_id"]})
    for appointment in appointment_cursor:
        st.write(f"Appointment ID: {appointment['_id']}")
        st.write(f"Doctor: {appointment['doctor_name']}")
        st.write(f"Date: {appointment['date']}")
        st.write(f"Time: {appointment['time']}")
        st.write("-------------------------")
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
