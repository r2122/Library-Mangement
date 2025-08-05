import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1100x650")
        self.root.config(bg="#f0f4f7")

        self.conn = None
        self.cursor = None
        self.connect_to_database()

        self.login_screen()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="library_db"
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to MySQL: {e}")
            self.root.destroy()

    def on_close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
        self.root.destroy()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()
        login_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.RIDGE)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=350)

        tk.Label(login_frame, text="Library Login", font=("Segoe UI", 20, "bold"), bg="white", fg="#004d99").pack(pady=20)

        tk.Label(login_frame, text="Username", font=("Segoe UI", 12), bg="white").pack(pady=5)
        self.username_entry = tk.Entry(login_frame, font=("Segoe UI", 12), bd=2)
        self.username_entry.pack(pady=5)

        tk.Label(login_frame, text="Password", font=("Segoe UI", 12), bg="white").pack(pady=5)
        self.password_entry = tk.Entry(login_frame, font=("Segoe UI", 12), bd=2, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(login_frame, text="Login", font=("Segoe UI", 12, "bold"), bg="#007acc", fg="white",
                  width=15, command=self.check_login).pack(pady=20)

    def check_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()

        try:
            self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
            result = self.cursor.fetchone()
            if result:
                self.main_menu()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Error as e:
            messagebox.showerror("Database Error", str(e))

    def main_menu(self):
        self.clear_screen()

        header = tk.Frame(self.root, bg="#003366", height=70)
        header.pack(fill=tk.X)
        tk.Label(header, text="Library Management System", bg="#003366", fg="white",
                 font=("Segoe UI", 24, "bold")).pack(pady=10)

        sidebar = tk.Frame(self.root, bg="#e6f2ff", width=250)
        sidebar.pack(fill=tk.Y, side=tk.LEFT)

        main = tk.Frame(self.root, bg="#f0f4f7")
        main.pack(expand=True, fill=tk.BOTH)

        features = [
            (" Add Book", self.add_book),
            (" Add Member", self.add_member),
            (" Issue Book", self.issue_book),
            (" Return Book", self.return_book),
            (" Search Book", self.search_book),
            (" Reports", self.reports),
            (" Logout", self.login_screen)
        ]

        for text, command in features:
            tk.Button(sidebar, text=text, font=("Segoe UI", 12), bg="#007acc", fg="white",
                      width=25, pady=10, bd=0, command=command).pack(pady=5)

        self.main_frame = main
        self.show_home_features()

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home_features(self):
        self.clear_main()
        card = tk.Frame(self.main_frame, bg="white", bd=2, relief=tk.RIDGE)
        card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=400)

        tk.Label(card, text="Features Overview", font=("Segoe UI", 18, "bold"), bg="white", fg="#003366").pack(pady=20)

        features = [
            "✓ Add New Books with Accession Number",
            "✓ Add New Members to Library",
            "✓ Issue and Return Book Features",
            "✓ Search Books by Details",
            "✓ Reports on Issued/Returned Books",
            "✓ Secure Login System"
        ]

        for f in features:
            tk.Label(card, text=f, font=("Segoe UI", 13), bg="white", fg="#333").pack(anchor="w", padx=30, pady=5)

    def add_book(self):
        self.clear_main()
        tk.Label(self.main_frame, text="Add Book", font=("Segoe UI", 18, "bold"), bg="#f0f4f7", fg="#333").pack(pady=20)

        form = tk.Frame(self.main_frame, bg="#f0f4f7")
        form.pack()

        labels = ["Accession Number", "Subject", "Title", "Author", "Publisher", "Price"]
        self.book_entries = {}
        for i, label in enumerate(labels):
            tk.Label(form, text=label, font=("Segoe UI", 12), bg="#f0f4f7").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(form, font=("Segoe UI", 12), width=30)
            entry.grid(row=i, column=1, pady=5)
            self.book_entries[label] = entry

        tk.Button(form, text="Save Book", font=("Segoe UI", 12), bg="#28a745", fg="white",
                  command=self.save_book).grid(row=len(labels), columnspan=2, pady=20)

    def save_book(self):
        data = [entry.get() for entry in self.book_entries.values()]
        if all(data):
            try:
                self.cursor.execute("""
                    INSERT INTO books (accession_no, subject, title, author, publisher, price)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, data)
                self.conn.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                self.clear_main()
            except Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", str(err))
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def add_member(self):
        self.clear_main()
        tk.Label(self.main_frame, text="Add Member", font=("Segoe UI", 18, "bold"), bg="#f0f4f7", fg="#333").pack(pady=20)

        form = tk.Frame(self.main_frame, bg="#f0f4f7")
        form.pack()

        labels = ["Member Code", "Name", "Address", "Phone"]
        self.member_entries = {}
        for i, label in enumerate(labels):
            tk.Label(form, text=label, font=("Segoe UI", 12), bg="#f0f4f7").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(form, font=("Segoe UI", 12), width=30)
            entry.grid(row=i, column=1, pady=5)
            self.member_entries[label] = entry

        tk.Button(form, text="Save Member", font=("Segoe UI", 12), bg="#28a745", fg="white",
                  command=self.save_member).grid(row=len(labels), columnspan=2, pady=20)

    def save_member(self):
        data = [entry.get() for entry in self.member_entries.values()]
        if all(data):
            try:
                self.cursor.execute("""
                    INSERT INTO members (member_code, name, address, phone, books_issued)
                    VALUES (%s, %s, %s, %s, 0)
                """, data)
                self.conn.commit()
                messagebox.showinfo("Success", "Member added successfully!")
                self.clear_main()
            except Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", str(err))
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def issue_book(self):
        self.clear_main()
        tk.Label(self.main_frame, text="Issue Book", font=("Segoe UI", 18, "bold"), bg="#f0f4f7", fg="#333").pack(
            pady=20)

        form = tk.Frame(self.main_frame, bg="#f0f4f7")
        form.pack()

        labels = ["Accession Number", "Member Code", "Issue Date (YYYY-MM-DD)"]
        self.issue_entries = {}
        for i, label in enumerate(labels):
            tk.Label(form, text=label, font=("Segoe UI", 12), bg="#f0f4f7").grid(row=i, column=0, padx=10, pady=5,
                                                                                 sticky="e")
            entry = tk.Entry(form, font=("Segoe UI", 12), width=30)
            entry.grid(row=i, column=1, pady=5)
            self.issue_entries[label] = entry

        tk.Button(form, text="Issue Book", font=("Segoe UI", 12), bg="#007acc", fg="white",
                  command=self.save_issue).grid(row=len(labels), columnspan=2, pady=20)

    def save_issue(self):
        data = [entry.get() for entry in self.issue_entries.values()]
        if all(data):
            try:
                self.cursor.execute("SELECT * FROM issued_books WHERE accession_no=%s AND return_date IS NULL",
                                    (data[0],))
                if self.cursor.fetchone():
                    messagebox.showwarning("Already Issued", "Book is already issued and not returned yet.")
                    return

                self.cursor.execute(
                    "INSERT INTO issued_books (accession_no, member_code, issue_date) VALUES (%s, %s, %s)", data)
                self.cursor.execute("UPDATE members SET books_issued = books_issued + 1 WHERE member_code=%s",
                                    (data[1],))
                self.conn.commit()
                messagebox.showinfo("Receipt", f"Book {data[0]} issued to Member {data[1]} on {data[2]}.")
                self.clear_main()
            except Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", str(err))
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def return_book(self):
        self.clear_main()
        tk.Label(self.main_frame, text="Return Book", font=("Segoe UI", 18, "bold"), bg="#f0f4f7", fg="#333").pack(
            pady=20)

        form = tk.Frame(self.main_frame, bg="#f0f4f7")
        form.pack()

        labels = ["Accession Number", "Return Date (YYYY-MM-DD)"]
        self.return_entries = {}
        for i, label in enumerate(labels):
            tk.Label(form, text=label, font=("Segoe UI", 12), bg="#f0f4f7").grid(row=i, column=0, padx=10, pady=5,
                                                                                 sticky="e")
            entry = tk.Entry(form, font=("Segoe UI", 12), width=30)
            entry.grid(row=i, column=1, pady=5)
            self.return_entries[label] = entry

        tk.Button(form, text="Return Book", font=("Segoe UI", 12), bg="#007acc", fg="white",
                  command=self.save_return).grid(row=len(labels), columnspan=2, pady=20)

    def save_return(self):
        accession_no = self.return_entries["Accession Number"].get()
        return_date = self.return_entries["Return Date (YYYY-MM-DD)"].get()
        if accession_no and return_date:
            try:
                self.cursor.execute("""
                    UPDATE issued_books 
                    SET return_date=%s 
                    WHERE accession_no=%s AND return_date IS NULL
                """, (return_date, accession_no))
                if self.cursor.rowcount == 0:
                    messagebox.showwarning("Not Found", "No issued record found for this book.")
                    return
                self.cursor.execute("""
                    UPDATE members 
                    SET books_issued = books_issued - 1 
                    WHERE member_code = (
                        SELECT member_code FROM issued_books 
                        WHERE accession_no=%s ORDER BY issue_id DESC LIMIT 1
                    )
                """, (accession_no,))
                self.conn.commit()
                messagebox.showinfo("Receipt", f"Book {accession_no} returned on {return_date}.")
                self.clear_main()
            except Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", str(err))
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def search_book(self):
        self.clear_main()
        tk.Label(self.main_frame, text="Search Book", font=("Segoe UI", 18, "bold"), bg="#f0f4f7", fg="#333").pack(
            pady=20)

        search_frame = tk.Frame(self.main_frame, bg="#f0f4f7")
        search_frame.pack()

        tk.Label(search_frame, text="Search by Title or Author", font=("Segoe UI", 12), bg="#f0f4f7").pack(pady=10)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 12), width=40)
        self.search_entry.pack(pady=5)
        tk.Button(search_frame, text="Search", font=("Segoe UI", 12), bg="#007acc", fg="white",
                  command=self.perform_search).pack(pady=10)

        self.search_result = tk.Text(self.main_frame, width=100, height=15, font=("Consolas", 11))
        self.search_result.pack(pady=10)

    def perform_search(self):
        key = self.search_entry.get()
        if key:
            try:
                query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
                self.cursor.execute(query, (f"%{key}%", f"%{key}%"))
                results = self.cursor.fetchall()
                self.search_result.delete(1.0, tk.END)
                if results:
                    for book in results:
                        self.search_result.insert(tk.END, f"Book: {book[2]} by {book[3]} | Acc #: {book[0]}\n")
                else:
                    self.search_result.insert(tk.END, "No books found.")
            except Error as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter a title or author.")

    def reports(self):
        self.clear_main()
        tk.Label(self.main_frame, text="Reports", font=("Segoe UI", 18, "bold"), bg="#f0f4f7", fg="#333").pack(pady=20)

        report_frame = tk.Frame(self.main_frame, bg="#f0f4f7")
        report_frame.pack()

        tk.Label(report_frame, text="Issued Books Report", font=("Segoe UI", 14, "bold"), bg="#f0f4f7",
                 fg="#004d99").pack(pady=10)

        report_text = tk.Text(report_frame, width=100, height=20, font=("Consolas", 11))
        report_text.pack()

        try:
            self.cursor.execute("""
                SELECT i.accession_no, b.title, m.name, i.issue_date, i.return_date
                FROM issued_books i
                JOIN books b ON i.accession_no = b.accession_no
                JOIN members m ON i.member_code = m.member_code
                ORDER BY i.issue_date DESC
            """)
            rows = self.cursor.fetchall()

            if rows:
                for row in rows:
                    acc, title, member, issue_date, return_date = row
                    return_info = return_date if return_date else "Not Returned"
                    report_text.insert(tk.END,
                                       f"{acc} | {title} | Issued to: {member} | Issue Date: {issue_date} | Return: {return_info}\n")
            else:
                report_text.insert(tk.END, "No issued books found.")
        except Error as err:
            messagebox.showerror("Error", str(err))

    def display_main(self, frame, text, color="#004080"):
        self.clear_main()
        tk.Label(frame, text=text, font=("Segoe UI", 18, "bold"), fg=color, bg=frame["bg"]).pack(pady=100)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
