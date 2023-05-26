from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os

def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "coach" and password == "password":
        #messagebox.showinfo("Login Successful", "You have logged in successfully!")
        os.system("sudo python3 uwb.py")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Create the main window
window = Tk()
window.title("SmartTag")

# Expand the window to fit the screen
window.attributes("-zoomed", True)

window.configure(bg='#272727')

# Load and display logo
logo_image = Image.open("logo.png")
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(window, image=logo_photo, bg='#272727')
logo_label.pack(pady=20)

# Create the username label and entry
label_username = Label(window, text="Username", font=("Arial", 14), bg='#272727' , fg="white")
label_username.pack()
entry_username = Entry(window, font=("Arial", 14))
entry_username.pack(pady=5)

# Create the password label and entry
label_password = Label(window, text="Password", font=("Arial", 14), bg='#272727', fg="white")
label_password.pack()
entry_password = Entry(window, show="*", font=("Arial", 14))
entry_password.pack(pady=5)

# Create the login button
login_button = Button(window, text="Login", font=("Arial", 14), command=validate_login, bg="#ED1B76", fg="white")
login_button.pack(pady=20, ipadx=10, ipady=5)

# Run the main event loop
window.mainloop()

