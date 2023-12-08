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
        self.create_widgets()

    def create_widgets(self):        
        #wczytywanie elementów interfejsu użytkownika
        self.ipaddress = tk.Label(self, text="Adres IP")
        self.ipaddress.grid(row=0, column=0)
        self.host = tk.Entry(self, justify="right",width=30, bd=2)
        self.host.grid(row=0, column=1)
        self.host.focus()
        self.username = tk.Label(self, text="Login")
        self.username.grid(row=1, column=0)
        self.login = tk.Entry(self, justify="right", width=30, bd=2)
        self.login.grid(row=1, column=1)
        self.password = tk.Label(self, text="Hasło")
        self.password.grid(row=2, column=0)
        self.passwd = tk.Entry(self, show="*",justify="right",width=30, bd=2)
        self.passwd.grid(row=2, column=1)
        
        self.conn_btn = tk.Button(self, text="Połącz",
                                 command=self.connect_to_server, width=10)
        self.conn_btn.place(x=150, y=63)
            
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
                messagebox.showerror("Błąd", "Nie udało połączyć się z"\
                                     "bazą danych")
                
        except mysql.Error as e:
            messagebox.showerror("Błąd", f"Błąd: {e}")

    def show_login_win(self):
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
            if "SELECT" in operation:
                table ={'columns':[i[0] for i in cursor.description],
                        'records':records}
                return table
            if records is not None:
                return records
            cursor.close()
        else:
            messagebox.showinfo("Info", "Nie połączono z serwerem")
        
    def display_databases(self):
        db = tk.Toplevel()
        db.title("Bazy danych")
        db.geometry("260x200+500+250")
        db.resizable(False, False)
        db.focus()
    
        db_list = tk.Listbox(db, width=40)
        for databases in self.db_operations("SHOW DATABASES"):
            db_list.insert(tk.END, databases[0])
        db_list.grid(column=0, row=0)        

        connect_btn = tk.Button(db, text="Połącz",
                                command=lambda:self.show_tables(db_list))
        connect_btn.place(x=3, y=170)
        #zamknięcie połączenia z bazą danych
        disconnect_btn = tk.Button(db, text="Rozłącz", command=lambda:
            (self.connect.close(),db.destroy(),self.show_login_win()), width=8)
        disconnect_btn.place(x=50,y=170)
        db.mainloop()

    def show_tables(self, db_list):
        try:
            db_tables = tk.Toplevel()
            db_tables.geometry("260x200+540+220")
            db_tables.resizable(False, False)
            db_tables.focus()
        
            for i in db_list.curselection():
                select_db = db_list.get(i)
            db_tables.title(f"Baza danych: {select_db}")

            table_list = tk.Listbox(db_tables, width=40)
            table_list.grid(row=0, column=0)

            self.db_operations(f"USE {select_db}")
            # wyświetlanie tabeli w bazie danych
            for table in self.db_operations("SHOW TABLES;"):
                table_list.insert(tk.END, table[0])
           
            open_btn = tk.Button(db_tables, text="Otwórz", command=lambda:
                                 self.read_table(table_list), width=8)
            open_btn.place(x=3, y=170)

            disconnect_btn = tk.Button(db_tables, text="Zamknij",
                                       command=db_tables.destroy, width=8)
            disconnect_btn.place(x=63,y=170)
            db_tables.mainloop()

        except UnboundLocalError:
            db_tables.destroy()
            messagebox.showinfo("Info", "Proszę wybrać bazę danych")

    def read_table(self, table_list):
        try:
            selected_table = tk.Toplevel()
            selected_table.geometry("280x250+500+250")
            selected_table.resizable(False, False)
            selected_table.focus()
            
            for i in table_list.curselection():
                select_tab = table_list.get(i)
            selected_table.title(f"Tabela: {select_tab}")

            tree = ttk.Treeview(selected_table)
            tab = self.db_operations(f"SELECT * FROM {select_tab}")
            #pobiera nazwy kolumn
            tree["show"] = "headings"
            tree["columns"] = tuple(tab['columns'])
            for col_name in tab['columns']:
                tree.heading(col_name, text=col_name)
       
            #wyświetla zawartość tabeli
            for record in tab['records']:
                tree.insert("", tk.END, values=record)
            for column in tree["columns"]:
                tree.column(column,width=100)
                tree.heading(column,anchor="w")
            tree.column("id",width=20)
            tree.grid(row=0, column=0, sticky="nsew")
                               
            # Scrollbars
            vsb = ttk.Scrollbar(selected_table, orient="vertical",
                                command=tree.yview)
            vsb.grid(row=0, column=1, sticky="ns")
            tree.configure(yscrollcommand=vsb.set)
            selected_table.mainloop()
            
        except UnboundLocalError:
            selected_table.destroy()
            messagebox.showinfo("Info", "Proszę wybrać tabelę")
            
db_connect = DatabaseConnector()
db_connect.mainloop()
