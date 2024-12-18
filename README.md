# Password-Cracking-and-Protection-Toolkit

This is a locally hosted tool designed for educational purposes to demonstrate both offensive and defensive aspects of password security. The toolkit provides a GUI for executing dictionary and brute-force attacks and simulates a secure server to highlight best practices in password protection.

## Features
- **Attack Toolkit**: 
  - **Dictionary Attack:** Uses a predefined wordlist to test passwords.
  - **Brute Force Attack:** Generates all possible password combinations up to a specified length.
- **Attack Toolkit**: 
  - **Password Policies:** Enforces strong password requirements during user signup.
  - **Secure Password Storage:** Implements bcrypt for hashing and secure storage of user passwords.
  - **Flask-Based Authentication:** Simulates a login system to test attacks in a controlled environment.
- **GUI**: 
  - User-friendly interface to configure HTTP request details and select attack methods.


## Installation
### Prerequisites
Before setting up this tool, ensure you have the following installed:
- [Python 3](https://www.python.org/downloads/)
- [MySQL server](https://www.mysql.com/downloads/)


### Steps
1. **Clone the repository**:
    ```bash
    git clone https://github.com/Patel-Divya/Password-Cracking-and-Protection-Toolkit.git
    cd Password-Cracking-and-Protection-Toolkit
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure the MySQL database**:
   - Update settings.py with your database credentials:
    ```python
    HOST = 'your_host'  
    USER_NAME = 'your_user'  
    PASSWORD = 'your_password'  
    DB_NAME = 'your_database'  
    FOLDER_PATH = 'public_folder_path'  
    ```
    - Create the required table in your database:
    ```sql
    CREATE TABLE records (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    username VARCHAR(255) UNIQUE,  
    password VARCHAR(255)  
    );  
    ```

4. **Start the Flask server**:
    ```bash
    python server.py  
    ```
    
5. **Launch the GUI**:
    ```bash
    python attack.py   
    ```


## Usage
###Secure Server:
1. **Signup**:
   - Enter the target URL, HTTP method, headers, and payload.

3. **Login**:
   - Choose between Dictionary Attack (provide a wordlist path) or Brute Force Attack (define max password length).

5. **Simulate Attack**:
   - View real-time logs as the tool tests each password combination.

###Attacking Toolkit:
1. **Use Burp Suite to Intercept Requests**:
   - Use Burp Suite to intercept the HTTP request sent during the login process.
   - Capture the target URL, HTTP method, headers, and payload to configure the attacking toolkit.
   
2. **Configure HTTP Request**:
   - Enter the target URL, HTTP method, headers, and payload.

3. **Select Attack Type**:
   - Choose between Dictionary Attack (provide a wordlist path) or Brute Force Attack (define max password length).

4. **Execute and Monitor**:
   - View real-time logs as the tool tests each password combination.


## Files & Structure
  ```bash
  Project/
  ├── web-server/
  │   ├── public/
  │   │   ├── dashboard.html
  │   │   └── index.html
  │   ├── static/
  │   │   └── style.css
  │   ├── server.py
  │   └── settings.py
  ├── attacking-toolkit/
  │   ├── attack.py
  │   └── wordlist.txt
  ```

## Files Descriptions
### Web Server:
- **public/**:
  - **dashboard.html**: The user dashboard interface displayed after successful login.
  - **index.html**: The main page for login and signup functionalities.
- **static/**:
  - **style.css**: Stylesheet to define the visual layout and design of the web application.
- **server.py**: Python-based web server handling user authentication, dashboard rendering, and secure password management.
- **settings.py**: Contains configurations such as database credentials, file paths, and API keys used by the server.
  
### Attacking Toolkit:
- **attack.py**: Script for executing dictionary and brute force password attacks on the target URL. It includes GUI for request configuration.
- **wordlist.txt**: A pre-defined list of potential passwords used during dictionary attacks.
