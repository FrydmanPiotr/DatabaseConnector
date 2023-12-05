"""
Aplikacja do połączenia z bazą danych MySQL
Autor: Piotr Frydman
"""
import tkinter as tk
from tkinter import messagebox,ttk
import mysql.connector as mysql
from mysql.connector import Error

class DatabaseConnector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Połączenie z serwerem MySQL")
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
        self.passwd = tk.Entry(self, show="*",justify="right", bd=2)
        self.passwd.grid(row=2, column=1)
        
        self.conn_btn = tk.Button(self, text="Połącz",
                                 command=self.connect_to_server, width=10)
        self.conn_btn.grid(row=2, column=2)
            
    def connect_to_server(self):
        try:
            #pobiera dane od użytkownika
            self.connect = mysql.connect(
                host=self.host.get(),
                user=self.login.get(),
                password=self.passwd.get()
            )
            if self.connect.is_connected():
                self.withdraw() #ukrywa okno logowania
                self.display_databases()
            else:
                messagebox.showerror("Błąd", "Nie udało połączyć się z bazą danych")
                
        except mysql.Error as e:
            messagebox.showerror("Błąd", f"Błąd: {e}")

    def show_login_window(self):
        self.deiconify()  #wyświetla okno logowania
        self.host.delete(0, tk.END) #usuwa dane logowania
        self.login.delete(0, tk.END)
        self.passwd.delete(0, tk.END)

    #wykonywanie operacji na bazach danych
    def db_operations(self, operation):
        records = []
        if self.connect.is_connected():
            cursor = self.connect.cursor()
            cursor.execute(operation)
            records = cursor.fetchall()
            if records is not None:
                return records
        else:
            messagebox.showinfo("Info", "Nie połączono z serwerem")
        
    def display_databases(self):
        top = tk.Toplevel()
        top.title("Bazy danych")
        top.geometry("300x300+500+250")
        top.resizable(False, False)
        top.focus()
    
        db_list = tk.Listbox(top)
        for db in self.db_operations("SHOW DATABASES"):
            db_list.insert(tk.END, db[0])
        db_list.grid(column=0, row=0)        

        connect_btn = tk.Button(top, text="Połącz", command=lambda: self.show_tables(db_list))
        connect_btn.grid(column=0,row=1)
        #zamknięcie połączenia z bazą danych
        disconnect_btn = tk.Button(top, text="Rozłącz", command=lambda: (connect.close(),
                                        top.destroy(), self.show_login_window()), width=8)
        disconnect_btn.grid(column=1, row=1)
        top.mainloop()

    def show_tables(self, db_list):
        for i in db_list.curselection():
            select_db = db_list.get(i)
                    
        db_tables = tk.Toplevel()
        db_tables.title(f"Baza danych: {select_db}")
        db_tables.geometry("300x300+540+220")
        db_tables.resizable(False, False)
        db_tables.focus()

        table_list = tk.Listbox(db_tables)
        table_list.grid(row=0, column=0)

        self.db_operations(f"USE {select_db}")

        # wyświetlanie tabeli w bazie danych
        for table in self.db_operations("SHOW TABLES;"):
            table_list.insert(tk.END, table[0])
       
        open_btn = tk.Button(db_tables, text="Otwórz", command=lambda:
                             self.read_table(table_list), width=8)
        open_btn.grid(column=0, row=1)

        disconnect_btn = tk.Button(db_tables, text="Zamknij", command=db_tables.destroy, width=8)
        disconnect_btn.grid(column=1, row=1)
        db_tables.mainloop()

    def read_table(self, table_list):
        for i in table_list.curselection():
            select_tab = table_list.get(i)
            
        selected_table = tk.Toplevel()
        selected_table.geometry("280x250+500+250")
        selected_table.title(f"Tabela: {select_tab}")
        selected_table.resizable(False, False)
        selected_table.focus()

        tree = ttk.Treeview(selected_table)
        columns = []

        try:
            if self.connect.is_connected():
                cursor = self.connect.cursor()
                cursor.execute(f"SELECT * FROM {select_tab}")

                #pobiera nazwy kolumn
                columns = [i[0] for i in cursor.description]
                tree["show"] = "headings"
                tree["columns"] = tuple(columns)
                for col_name in columns:
                    tree.heading(col_name, text=col_name)

                records = cursor.fetchall()

                #wyświetla tabelę w oknie
                for record in records:
                    tree.insert("", tk.END, values=record)
                cursor.close()
                column_width = 100
                for column in tree["columns"]:
                    tree.column(column,width=column_width)
                    tree.heading(column,anchor="w")
                tree.column("id",width=20)
                tree.grid(row=0, column=0, sticky="nsew")
                
            else:
                messagebox.showinfo("Info", "Wystąpił błąd podczas pobierania danych.")
        except mysql.Error as e:
            messagebox.showinfo("Error", f"Błąd {e}")

        finally:
            if cursor:
                cursor.close()
                
        # Scrollbars
        vsb = ttk.Scrollbar(selected_table, orient="vertical", command=tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=vsb.set)

        selected_table.mainloop()

        
db_connect = DatabaseConnector()
db_connect.mainloop()
