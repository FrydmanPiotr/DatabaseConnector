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
        self.geometry("350x120+500+250")
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
        self.host = tk.Entry(self, justify="right", bd=2)
        self.host.grid(row=0, column=1)
        self.host.focus()
        self.username = tk.Label(self, text="Login")
        self.username.grid(row=1, column=0)
        self.login = tk.Entry(self, justify="right", bd=2)
        self.login.grid(row=1, column=1)
        self.password = tk.Label(self, text="Hasło")
        self.password.grid(row=2, column=0)
        self.passwd = tk.Entry(self, justify="right", bd=2)
        self.passwd.grid(row=2, column=1)
        
        self.connect = tk.Button(self, text="Połącz",
                                 command=self.connect_to_database, width=10)
        self.connect.grid(row=2, column=2)

    def connect_to_database(self):
        try:
            #pobiera dane od użytkownika
            connect = mysql.connect(
                host=self.host.get(),
                user=self.login.get(),
                password=self.passwd.get()
            )
            if connect.is_connected():
                self.withdraw() #ukrywa okno logowania
                self.display_databases(connect) 
            else:
                messagebox.showerror("Błąd", "Nie udało połączyć się z bazą danych")
                
        except Error as e:
            messagebox.showerror("Błąd", f"Błąd: {e}")

    def show_login_window(self):
        self.deiconify()  #wyświetla okno logowania
        self.host.delete(0, tk.END) #usuwa dane logowania
        self.login.delete(0, tk.END)
        self.passwd.delete(0, tk.END)
        
    def display_databases(self, connect):
        top = tk.Toplevel()
        top.title("Bazy danych")
        top.geometry("300x300+500+250")
        self.resizable(False, False)
        top.focus()
        
        databases = []
        try:
            #wyszukiwanie bazy danych
            if connect.is_connected():
                cursor = connect.cursor()
                cursor.execute("SHOW DATABASES;")
                databases = cursor.fetchall()
        
            if databases:
                self.listbox = tk.Listbox(top)
                for db in databases:
                    self.listbox.insert(tk.END, db[0])
                self.listbox.grid(column=0, row=0)
            else:
                messagebox.showinfo("Błąd", "Brak baz danych.")
        finally:
            if cursor:
                cursor.close()

        #zamknięcie połączenia z bazą danych
        open_btn = tk.Button(top, text="Otwórz", command=lambda: self.show_tables(connect))
        open_btn.grid(column=0,row=1)
        disconnect_btn = tk.Button(top, text="Rozłącz", command=lambda: (connect.close(),
                                        top.destroy(), self.show_login_window()), width=8)
        disconnect_btn.grid(column=1, row=1)
        top.mainloop()

    def show_tables(self,connect):
        for i in self.listbox.curselection():
            select_db = self.listbox.get(i)
        
        db_tables = tk.Toplevel()
        db_tables.title(f"{select_db}")
        db_tables.geometry("300x300+500+250")
        self.resizable(False, False)
        db_tables.focus()

        table_listbox = tk.Listbox(db_tables)
        table_listbox.grid(row=0, column=0)

        if connect.is_connected():
            cursor = connect.cursor()
            cursor.execute(f"USE {select_db}")
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()

            #wyświetlanie tabeli w bazie danych
            if tables:
                for table in tables:
                    table_listbox.insert(tk.END, table[0])
            else:
                messagebox.showinfo("Info", "Brak tabeli w tej bazie danych.")
        else:
            messagebox.showinfo("Błąd", "Wystąpił błąd podczas połączenia z bazą danych.")
                
        disconnect_btn = tk.Button(db_tables, text="Zamknij", command=db_tables.destroy, width=8)
        disconnect_btn.grid(column=0, row=1)
            
        db_tables.mainloop()
        
db_connect = DatabaseConnector()
db_connect.mainloop()
