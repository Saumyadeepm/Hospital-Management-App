# Hospital Management App
This is a Hospital Management App implemented using Streamlit and MongoDB. The app allows users to perform various tasks such as booking appointments, managing patient records, generating reports, and user management.

## Prerequisites
Before running the application, make sure you have the following prerequisites installed:

Python 3.x
Streamlit
pandas
pymongo

## Installation
1. Clone the repository:
```python
git clone <repository_url>
```
2. Change to the project directory:
```python
cd hospital-management-app
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Set up MongoDB:

- Create a MongoDB Atlas account and set up a cluster.
- Update the uri variable in the code with your MongoDB connection URI.

## Usage
To run the Hospital Management App, execute the following command in the project directory:
```python
streamlit run app.py
```
The application will be launched in your web browser. If you are not logged in, you will be prompted to enter your credentials. Once authenticated, you will have access to various features of the app based on your user role.

## Features
### Appointment Booking
- Book appointments with doctors by providing the doctor's name, date, and time.
### Patient Records
- Add patient records by entering the patient's name, age, gender, and medical history.
### Viewing Records
- View patient records and appointment details in separate tables.
- Display doctor schedules and invoices.
## Billing and Payments
- View invoices and their details.
- Make payments for unpaid invoices.
### Reports and Analytics
- Generate appointment and patient reports.
- Display generated reports.
### User Management (Admin Only)
- Manage users, including adding and removing users.
- View and delete user records.
## Contributing
Contributions to the Hospital Management App are welcome. If you find any issues or want to add new features, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

Contact
If you have any questions or suggestions, please feel free to contact me at [saumyadeepmitra.12@gmail.com].
