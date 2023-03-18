import tkinter as tk
import os
import time
from FaceRecognition import recog_n_save
from emailData import sendMail
from dt import dat
from tkinter import messagebox, simpledialog
import re
# Create the main window and set its size and title
root = tk.Tk()
root.geometry("600x400")
root.title("Face Recognition System")
root.configure(bg="#b3e6ff")
# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(expand=True, padx=50, pady=20)
PASSWORD = "admin123"
TOKEN_EXPIRY = 20
access_token = None
def validate_password(password):
    return password == PASSWORD
def is_access_token_valid():
    global access_token
    if access_token is None:
        return False
    timestamp, token = access_token
    return time.time() - timestamp < TOKEN_EXPIRY


def validate_email(emailText):
    """
    Validate the syntax of an email address.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, emailText) is not None
# Define a function to be called when button 1 is clicked
def button1_clicked():
    global access_token
    # Check if the user has valid access
    if not is_access_token_valid():
        password = simpledialog.askstring("Admin Password", "Enter admin password:", show="*")
        if not validate_password(password):
            messagebox.showerror("Access Denied", "Incorrect password.")
            return
        # Create a new access token
        access_token = (time.time(), "button1")
    
    face_id = simpledialog.askstring("Enter Unique Number", "Enter Roll Number:", show="*")
    dat(face_id)

def button2_clicked():
    global access_token
    # Check if the user has valid access
    if not is_access_token_valid():
        password = simpledialog.askstring("Admin Password", "Enter admin password:", show="*")
        if not validate_password(password):
            messagebox.showerror("Access Denied", "Incorrect password.")
            return
        # Create a new access token
        access_token = (time.time(), "button2")
    os.system('python Trainer.py')

# Define a function to be called when button 3 is clicked
def button3_clicked():
    SUBJECT = simpledialog.askstring("Subject", "Enter subject name")
    if not SUBJECT == '':
        recog_n_save(SUBJECT)
    #os.system('python FaceRecognition.py')

# Define a function to be called when button 4 is clicked
def button4_clicked():
    EMAIL = simpledialog.askstring("Email Attendance", "Enter email address")
    sendMail(email = EMAIL)
    # Call the emailData.py script with the email address as an argument
    #os.system(f'python emailData.py "{email}"')
    #os.system('python emailData.py')

# Create the buttons and set their size and style
button1 = tk.Button(button_frame, text="New Data", command=button1_clicked, width=15, height=3, bg="#ff9999", fg="white", font=("Arial", 12), bd=0)
button2 = tk.Button(button_frame, text="Train Data", command=button2_clicked, width=15, height=3, bg="#ff9999", fg="white", font=("Arial", 12), bd=0)
button3 = tk.Button(button_frame, text="Face Recognition", command=button3_clicked, width=15, height=3, bg="#0099cc", fg="white", font=("Arial", 12), bd=0)
button4 = tk.Button(button_frame, text="Email Attendance", command=button4_clicked, width=15, height=3, bg="#0099cc", fg="white", font=("Arial", 12), bd=0)

# Add the buttons to the frame using a grid layout
button1.grid(row=0, column=0, padx=20, pady=10)
button2.grid(row=0, column=1, padx=20, pady=10)
button3.grid(row=1, column=0, padx=20, pady=10)
button4.grid(row=1, column=1, padx=20, pady=10)


root.mainloop()
