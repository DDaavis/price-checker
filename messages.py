from tkinter import messagebox

def wrong_input():
    messagebox.showwarning("Bad input!", "You need to fill out all fields!")

def product_uploaded():
    messagebox.showinfo("Success!", "Product saved.")

def product_deleted():
    messagebox.showinfo("Success!", "Product(s) deleted.")