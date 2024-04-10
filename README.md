### Vulnerable APP

This is a vulnerable app that is used to demonstrate SQL injection attacks. The app is a simple web application to save TODOs. The app is written in Python using Flask and SQLite.

### Setup

1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Run the app using `python app.py`

### Usage

1. Open the app in your browser
2. Redirect to Burp Suite and intercept the request
3. Edit a task 
4. Use the sqlmap to dump the database

