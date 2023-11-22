"""
Aplikacja do połączenia z bazą danych MySQL
Autor: Piotr Frydman
"""
import tkinter as tk
from tkinter import messagebox
import mysql.connector as mysql
from mysql.connector import Error

class DatabaseConnector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Połączenie z bazą danych")
        self.geometry("350x150+500+250")
        self.resizable(False, False)
        
        #położenie elementów w oknie
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.create_widgets()

    def create_widgets(self):
        #wczytywanie elementów interfejsu użytkownika
        self.ipaddress = tk.Label(self, text="Adres IP")
        self.ipaddress.grid(row=0, column=0)
        self.host = tk.Entry(self, bd=2)
        self.host.grid(row=0, column=1)
        self.username = tk.Label(self, text="Login")
        self.username.grid(row=1, column=0)
        self.login = tk.Entry(self, bd=2)
        self.login.grid(row=1, column=1)
        self.password = tk.Label(self, text="Hasło")
        self.password.grid(row=2, column=0)
        self.passwd = tk.Entry(self, bd=2)
        self.passwd.grid(row=2, column=1)
        
        self.connect = tk.Button(self, text="Połącz",
                                 command=self.connect_to_database, width=10)
        self.connect.grid(row=2, column=2)

    def connect_to_database(self):
        try:
            #pobiera dane od użytkownika
            connection = mysql.connect(
                host=self.host.get(),
                user=self.login.get(),
                password=self.passwd.get()
            )
            if connection.is_connected():
                messagebox.showinfo("Info","Połączono z bazą danych MySQL.")
                connection.close()
            else:
                messagebox.showerror("Błąd", "Nie udało połączyć się z bazą danych")
        except Error as e:
            messagebox.showerror("Błąd", f"Błąd: {e}")
        finally:
            #zamyka okno po próbie połączenia
            self.destroy()

db_connect = DatabaseConnector()
db_connect.mainloop()
