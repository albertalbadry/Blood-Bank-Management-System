import sys
import traceback
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import pyodbc
except ImportError:
    pyodbc = None


class Database:
    """Handles SQL Server connection and query execution."""

    def __init__(self):
        if pyodbc is None:
            messagebox.showerror(
                "Missing Dependency",
                "The pyodbc package is required. Install it with:\n"
                "pip install pyodbc",
            )
            raise RuntimeError("pyodbc is not installed")
        server = r"Albert\SQLEXPRESS"
        database = "bloodbank"
        driver = "ODBC Driver 18 for SQL Server"
        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )

        try:
            self.connection = pyodbc.connect(connection_string, autocommit=False)
            self.cursor = self.connection.cursor()
        except pyodbc.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Unable to connect to SQL Server.\nError: {error}",
            )
            raise

    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or [])
            columns = [column[0] for column in self.cursor.description]
            rows = self.cursor.fetchall()
            return columns, rows
        except pyodbc.Error as error:
            raise RuntimeError(f"Database query failed: {error}")

    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params or [])
            self.connection.commit()
        except pyodbc.Error as error:
            self.connection.rollback()
            raise RuntimeError(f"Database execution failed: {error}")

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except pyodbc.Error:
            pass


class BloodBankApp:
    """Main application class for the Blood Bank Management system."""

    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management System")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6fa")

        try:
            self.db = Database()
        except Exception:
            self.root.destroy()
            sys.exit(1)

        self.active_section = None
        self.sections = {
            "Bloodtype": self.bloodtype_fields,
            "hospital": self.hospital_fields,
            "Bloodunit": self.bloodunit_fields,
            "Bloodrequest": self.bloodrequest_fields,
            "Van": self.van_fields,
            "Delivery": self.delivery_fields,
        }

        self.build_layout()
        self.show_section("Bloodtype")

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg="#1f2937", width=220)
        self.sidebar.pack(side="left", fill="y")

        header = tk.Label(
            self.sidebar,
            text="Blood Bank",
            bg="#1f2937",
            fg="#ffffff",
            font=("Segoe UI", 18, "bold"),
            pady=20,
        )
        header.pack()

        self.sidebar_buttons = {}
        for section in ["Bloodtype", "hospital", "Bloodunit", "Bloodrequest", "Van", "Delivery"]:
            button = tk.Button(
                self.sidebar,
                text=section,
                bg="#111827",
                fg="#d1d5db",
                font=("Segoe UI", 11),
                relief="flat",
                activebackground="#374151",
                activeforeground="#ffffff",
                command=lambda s=section: self.show_section(s),
                padx=10,
                pady=12,
            )
            button.pack(fill="x", padx=10, pady=4)
            self.sidebar_buttons[section] = button

        spacer = tk.Frame(self.sidebar, bg="#1f2937")
        spacer.pack(expand=True, fill="both")

        exit_button = tk.Button(
            self.sidebar,
            text="Exit",
            bg="#dc2626",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            activebackground="#b91c1c",
            activeforeground="#ffffff",
            command=self.root.quit,
            padx=10,
            pady=12,
        )
        exit_button.pack(fill="x", padx=10, pady=20)

        self.content = tk.Frame(self.root, bg="#ffffff")
        self.content.pack(side="left", fill="both", expand=True)

        self.title_label = tk.Label(
            self.content,
            text="",
            bg="#ffffff",
            fg="#111827",
            font=("Segoe UI", 20, "bold"),
            pady=20,
        )
        self.title_label.pack()

        self.form_frame = tk.Frame(self.content, bg="#ffffff")
        self.form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        self.action_frame = tk.Frame(self.content, bg="#ffffff")
        self.action_frame.pack(padx=30, pady=20, fill="x")

        self.footer = tk.Label(
            self.content,
            text="Use the sidebar to switch between modules and manage blood bank data.",
            bg="#ffffff",
            fg="#6b7280",
            font=("Segoe UI", 10),
            pady=10,
        )
        self.footer.pack(side="bottom", fill="x")

    def reset_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        for widget in self.action_frame.winfo_children():
            widget.destroy()

    def show_section(self, section_name):
        self.active_section = section_name
        self.title_label.config(text=f"Manage {section_name}")
        self.reset_form()
        self.highlight_sidebar(section_name)

        if section_name in self.sections:
            self.sections[section_name]()

    def highlight_sidebar(self, section_name):
        for name, button in self.sidebar_buttons.items():
            if name == section_name:
                button.config(bg="#2563eb", fg="#ffffff")
            else:
                button.config(bg="#111827", fg="#d1d5db")

    def create_field(self, label_text, row, col, width=30):
        label = tk.Label(
            self.form_frame,
            text=label_text,
            anchor="w",
            bg="#ffffff",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
        )
        label.grid(row=row, column=col * 2, sticky="w", padx=(0, 10), pady=8)

        entry = tk.Entry(
            self.form_frame,
            width=width,
            font=("Segoe UI", 10),
            bd=1,
            relief="solid",
        )
        entry.grid(row=row, column=col * 2 + 1, sticky="w", pady=8)
        return entry

    def create_label_text(self, label_text, row, col, width=32):
        label = tk.Label(
            self.form_frame,
            text=label_text,
            anchor="w",
            bg="#ffffff",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
        )
        label.grid(row=row, column=col * 2, sticky="w", padx=(0, 10), pady=8)

        text_widget = tk.Text(
            self.form_frame,
            width=width,
            height=3,
            font=("Segoe UI", 10),
            bd=1,
            relief="solid",
        )
        text_widget.grid(row=row, column=col * 2 + 1, sticky="w", pady=8)
        return text_widget

    def create_action_buttons(self, insert_command, delete_command, update_command, view_command, search_command=None):
        insert_button = tk.Button(
            self.action_frame,
            text="Add Data",
            bg="#10b981",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10,
            command=insert_command,
        )
        insert_button.pack(side="left", padx=12)

        delete_button = tk.Button(
            self.action_frame,
            text="Delete Data",
            bg="#ef4444",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10,
            command=delete_command,
        )
        delete_button.pack(side="left", padx=12)

        update_button = tk.Button(
            self.action_frame,
            text="Update Data",
            bg="#6366f1",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10,
            command=update_command,
        )
        update_button.pack(side="left", padx=12)

        view_button = tk.Button(
            self.action_frame,
            text="View Data",
            bg="#2563eb",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10,
            command=view_command,
        )
        view_button.pack(side="left", padx=12)

        if search_command is not None:
            search_button = tk.Button(
                self.action_frame,
                text="Search",
                bg="#f59e0b",
                fg="#ffffff",
                font=("Segoe UI", 11, "bold"),
                relief="flat",
                padx=18,
                pady=10,
                command=search_command,
            )
            search_button.pack(side="left", padx=12)

    def normalize_value(self, value):
        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        if isinstance(value, str) and value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        return value

    def open_view_window(self, title, query, params=None, columns=None, rows=None):
        try:
            if columns is None or rows is None:
                columns, rows = self.db.fetch_all(query, params)
        except Exception as error:
            messagebox.showerror("View Error", str(error))
            return

        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("900x520")
        window.configure(bg="#f8fafc")

        title_label = tk.Label(
            window,
            text=title,
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 16, "bold"),
            pady=10,
        )
        title_label.pack(anchor="w", padx=20)

        frame = tk.Frame(window, bg="#f8fafc")
        frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center", width=120)

        normalized_rows = [
            tuple(self.normalize_value(value) for value in row)
            for row in rows
        ]

        for row in normalized_rows:
            tree.insert("", tk.END, values=row)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        if not rows:
            empty_label = tk.Label(
                frame,
                text="No records found. Click Refresh or add data to view results.",
                bg="#f8fafc",
                fg="#6b7280",
                font=("Segoe UI", 11),
                pady=10,
            )
            empty_label.pack(anchor="center", pady=20)

    def search_record(self, title, query, params):
        try:
            columns, rows = self.db.fetch_all(query, params)
            if not rows:
                messagebox.showinfo("No record found", "No record found")
                return
            self.open_view_window(title, query, params, columns=columns, rows=rows)
        except Exception as error:
            self.handle_error(error)

    def validate_text(self, value, field_name):
        if not value.strip():
            raise ValueError(f"{field_name} is required.")
        return value.strip()

    def validate_integer(self, value, field_name):
        text = self.validate_text(value, field_name)
        if not text.isdigit():
            raise ValueError(f"{field_name} must be a whole number.")
        return int(text)

    def parse_optional_integer(self, value):
        text = value.strip()
        if text == "":
            return None
        if not text.isdigit():
            raise ValueError("Optional numeric value must be a whole number or blank.")
        return int(text)

    def validate_date(self, value, field_name):
        text = self.validate_text(value, field_name)
        try:
            datetime.strptime(text, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"{field_name} must be in YYYY-MM-DD format.")
        return text

    def validate_choice(self, value, field_name, allowed_values):
        text = self.validate_text(value, field_name)
        if text not in allowed_values:
            raise ValueError(f"{field_name} must be one of: {', '.join(allowed_values)}")
        return text

    def parse_optional_text(self, value):
        text = value.strip()
        return text if text != "" else None

    def handle_error(self, error):
        messagebox.showerror("Operation Failed", str(error))
        traceback.print_exc()

    def bloodtype_fields(self):
        self.clear_vars()
        self.bloodtype_id_entry = self.create_field("Bloodtype ID", 0, 0)
        self.bloodgroup_entry = self.create_field("Bloodgroup", 1, 0)
        self.rhfactor_entry = self.create_field("RH Factor", 2, 0)
        self.unit_id_entry = self.create_field("Unit ID", 3, 0)

        self.create_action_buttons(
            self.insert_bloodtype,
            self.delete_bloodtype,
            self.update_bloodtype,
            self.view_bloodtype,
            self.search_bloodtype,
        )

    def insert_bloodtype(self):
        try:
            bloodtype_id = self.validate_integer(self.bloodtype_id_entry.get(), "Bloodtype ID")
            bloodgroup = self.validate_text(self.bloodgroup_entry.get(), "Bloodgroup")
            rhfactor = self.validate_text(self.rhfactor_entry.get(), "RH Factor")
            unit_id = self.parse_optional_integer(self.unit_id_entry.get())
            query = (
                "INSERT INTO bloodtype (Bloodtype_id, Bloodgroup, RHfactor, unit_id) "
                "VALUES (?, ?, ?, ?)"
            )
            self.db.execute(query, [bloodtype_id, bloodgroup, rhfactor, unit_id])
            messagebox.showinfo("Success", "Bloodtype record added successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def delete_bloodtype(self):
        try:
            bloodtype_id = self.validate_integer(self.bloodtype_id_entry.get(), "Bloodtype ID")
            if not messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete Bloodtype record {bloodtype_id}?",
            ):
                return
            query = "DELETE FROM bloodtype WHERE Bloodtype_id = ?"
            self.db.execute(query, [bloodtype_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Bloodtype record found with that ID.")
            else:
                messagebox.showinfo("Deleted", "Bloodtype record deleted successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def update_bloodtype(self):
        try:
            bloodtype_id = self.validate_integer(self.bloodtype_id_entry.get(), "Bloodtype ID")
            bloodgroup = self.validate_text(self.bloodgroup_entry.get(), "Bloodgroup")
            rhfactor = self.validate_text(self.rhfactor_entry.get(), "RH Factor")
            unit_id = self.parse_optional_integer(self.unit_id_entry.get())
            if not messagebox.askyesno(
                "Confirm Update",
                f"Are you sure you want to update Bloodtype record {bloodtype_id}?",
            ):
                return
            query = (
                "UPDATE bloodtype SET Bloodgroup = ?, RHfactor = ?, unit_id = ? "
                "WHERE Bloodtype_id = ?"
            )
            self.db.execute(query, [bloodgroup, rhfactor, unit_id, bloodtype_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Bloodtype record found with that ID.")
            else:
                messagebox.showinfo("Success", "Bloodtype record updated successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def view_bloodtype(self):
        self.open_view_window("Bloodtype Records", "SELECT Bloodtype_id, Bloodgroup, RHfactor, unit_id FROM bloodtype")

    def hospital_fields(self):
        self.clear_vars()
        self.hospital_id_entry = self.create_field("Hospital ID", 0, 0)
        self.hospital_name_entry = self.create_field("Hospital Name", 1, 0)
        self.location_entry = self.create_field("Location", 2, 0)
        self.phone_entry = self.create_field("Phone", 3, 0)
        self.request_id_entry = self.create_field("Request ID", 4, 0)

        self.create_action_buttons(
            self.insert_hospital,
            self.delete_hospital,
            self.update_hospital,
            self.view_hospital,
            self.search_hospital,
        )

    def insert_hospital(self):
        try:
            hospital_id = self.validate_integer(self.hospital_id_entry.get(), "Hospital ID")
            hospital_name = self.validate_text(self.hospital_name_entry.get(), "Hospital Name")
            location = self.validate_text(self.location_entry.get(), "Location")
            phone = self.validate_text(self.phone_entry.get(), "Phone")
            request_id = self.parse_optional_integer(self.request_id_entry.get())
            query = (
                "INSERT INTO hospital (hospital_id, hospital_name, location, phone, request_id) "
                "VALUES (?, ?, ?, ?, ?)"
            )
            self.db.execute(query, [hospital_id, hospital_name, location, phone, request_id])
            messagebox.showinfo("Success", "Hospital record added successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def delete_hospital(self):
        try:
            hospital_id = self.validate_integer(self.hospital_id_entry.get(), "Hospital ID")
            if not messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete Hospital record {hospital_id}?",
            ):
                return
            query = "DELETE FROM hospital WHERE hospital_id = ?"
            self.db.execute(query, [hospital_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Hospital record found with that ID.")
            else:
                messagebox.showinfo("Deleted", "Hospital record deleted successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def update_hospital(self):
        try:
            hospital_id = self.validate_integer(self.hospital_id_entry.get(), "Hospital ID")
            hospital_name = self.validate_text(self.hospital_name_entry.get(), "Hospital Name")
            location = self.validate_text(self.location_entry.get(), "Location")
            phone = self.validate_text(self.phone_entry.get(), "Phone")
            request_id = self.parse_optional_integer(self.request_id_entry.get())
            if not messagebox.askyesno(
                "Confirm Update",
                f"Are you sure you want to update Hospital record {hospital_id}?",
            ):
                return
            query = (
                "UPDATE hospital SET hospital_name = ?, location = ?, phone = ?, request_id = ? "
                "WHERE hospital_id = ?"
            )
            self.db.execute(query, [hospital_name, location, phone, request_id, hospital_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Hospital record found with that ID.")
            else:
                messagebox.showinfo("Success", "Hospital record updated successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def view_hospital(self):
        self.open_view_window(
            "Hospital Records",
            "SELECT hospital_id, hospital_name, location, phone, request_id FROM hospital",
        )

    def bloodunit_fields(self):
        self.clear_vars()
        self.unit_id_entry = self.create_field("Unit ID", 0, 0)
        self.collectiondate_entry = self.create_field("Collection Date", 1, 0)
        self.expirydate_entry = self.create_field("Expiry Date", 2, 0)
        self.status_entry = self.create_field("Status", 3, 0)
        self.delivery_fk_entry = self.create_field("Delivery ID", 4, 0)

        self.create_action_buttons(
            self.insert_bloodunit,
            self.delete_bloodunit,
            self.update_bloodunit,
            self.view_bloodunit,
            self.search_bloodunit,
        )

    def insert_bloodunit(self):
        try:
            unit_id = self.validate_integer(self.unit_id_entry.get(), "Unit ID")
            collectiondate = self.validate_date(self.collectiondate_entry.get(), "Collection Date")
            expirydate = self.validate_date(self.expirydate_entry.get(), "Expiry Date")
            status = self.validate_choice(self.status_entry.get(), "Status", ["available", "used", "expired"])
            delivery_id = self.parse_optional_integer(self.delivery_fk_entry.get())
            query = (
                "INSERT INTO Bloodunit (unit_id, collectiondate, expirydate, status, delivery_id) "
                "VALUES (?, ?, ?, ?, ?)"
            )
            self.db.execute(query, [unit_id, collectiondate, expirydate, status, delivery_id])
            messagebox.showinfo("Success", "Blood unit record added successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def delete_bloodunit(self):
        try:
            unit_id = self.validate_integer(self.unit_id_entry.get(), "Unit ID")
            if not messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete Bloodunit record {unit_id}?",
            ):
                return
            query = "DELETE FROM Bloodunit WHERE unit_id = ?"
            self.db.execute(query, [unit_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Bloodunit record found with that ID.")
            else:
                messagebox.showinfo("Deleted", "Blood unit record deleted successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def update_bloodunit(self):
        try:
            unit_id = self.validate_integer(self.unit_id_entry.get(), "Unit ID")
            collectiondate = self.validate_date(self.collectiondate_entry.get(), "Collection Date")
            expirydate = self.validate_date(self.expirydate_entry.get(), "Expiry Date")
            status = self.validate_choice(self.status_entry.get(), "Status", ["available", "used", "expired"])
            delivery_id = self.parse_optional_integer(self.delivery_fk_entry.get())
            if not messagebox.askyesno(
                "Confirm Update",
                f"Are you sure you want to update Bloodunit record {unit_id}?",
            ):
                return
            query = (
                "UPDATE Bloodunit SET collectiondate = ?, expirydate = ?, status = ?, delivery_id = ? "
                "WHERE unit_id = ?"
            )
            self.db.execute(query, [collectiondate, expirydate, status, delivery_id, unit_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Bloodunit record found with that ID.")
            else:
                messagebox.showinfo("Success", "Blood unit record updated successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def view_bloodunit(self):
        self.open_view_window(
            "Bloodunit Records",
            "SELECT unit_id, collectiondate, expirydate, status, delivery_id FROM Bloodunit",
        )

    def bloodrequest_fields(self):
        self.clear_vars()
        self.request_id_entry = self.create_field("Request ID", 0, 0)
        self.request_date_entry = self.create_field("Request Date", 1, 0)
        self.quantity_entry = self.create_field("Quantity", 2, 0)
        self.priority_entry = self.create_field("Priority", 3, 0)
        self.status_request_entry = self.create_field("Status", 4, 0)
        self.bloodtype_request_entry = self.create_field("Bloodtype ID", 5, 0)
        self.delivery_request_entry = self.create_field("Delivery ID", 6, 0)

        self.create_action_buttons(
            self.insert_bloodrequest,
            self.delete_bloodrequest,
            self.update_bloodrequest,
            self.view_bloodrequest,
            self.search_bloodrequest,
        )

    def insert_bloodrequest(self):
        try:
            request_id = self.validate_integer(self.request_id_entry.get(), "Request ID")
            request_date = self.validate_date(self.request_date_entry.get(), "Request Date")
            quantity = self.validate_integer(self.quantity_entry.get(), "Quantity")
            priority = self.validate_choice(self.priority_entry.get(), "Priority", ["Normal", "Urgent", "Emergency"])
            status = self.validate_choice(self.status_request_entry.get(), "Status", ["Pending", "Approved", "Rejected"])
            bloodtype_id = self.validate_integer(self.bloodtype_request_entry.get(), "Bloodtype ID")
            delivery_id = self.parse_optional_integer(self.delivery_request_entry.get())
            query = (
                "INSERT INTO Bloodrequest (request_id, request_date, quantity, Priority, status, bloodtype_id, delivery_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
            )
            self.db.execute(
                query,
                [request_id, request_date, quantity, priority, status, bloodtype_id, delivery_id],
            )
            messagebox.showinfo("Success", "Blood request record added successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def delete_bloodrequest(self):
        try:
            request_id = self.validate_integer(self.request_id_entry.get(), "Request ID")
            if not messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete Bloodrequest record {request_id}?",
            ):
                return
            query = "DELETE FROM Bloodrequest WHERE request_id = ?"
            self.db.execute(query, [request_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Bloodrequest record found with that ID.")
            else:
                messagebox.showinfo("Deleted", "Blood request record deleted successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def update_bloodrequest(self):
        try:
            request_id = self.validate_integer(self.request_id_entry.get(), "Request ID")
            request_date = self.validate_date(self.request_date_entry.get(), "Request Date")
            quantity = self.validate_integer(self.quantity_entry.get(), "Quantity")
            priority = self.validate_choice(self.priority_entry.get(), "Priority", ["Normal", "Urgent", "Emergency"])
            status = self.validate_choice(self.status_request_entry.get(), "Status", ["Pending", "Approved", "Rejected"])
            bloodtype_id = self.validate_integer(self.bloodtype_request_entry.get(), "Bloodtype ID")
            delivery_id = self.parse_optional_integer(self.delivery_request_entry.get())
            if not messagebox.askyesno(
                "Confirm Update",
                f"Are you sure you want to update Bloodrequest record {request_id}?",
            ):
                return
            query = (
                "UPDATE Bloodrequest SET request_date = ?, quantity = ?, Priority = ?, status = ?, bloodtype_id = ?, delivery_id = ? "
                "WHERE request_id = ?"
            )
            self.db.execute(
                query,
                [request_date, quantity, priority, status, bloodtype_id, delivery_id, request_id],
            )
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Bloodrequest record found with that ID.")
            else:
                messagebox.showinfo("Success", "Blood request record updated successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def view_bloodrequest(self):
        self.open_view_window(
            "Bloodrequest Records",
            "SELECT request_id, request_date, quantity, Priority, status, bloodtype_id, delivery_id FROM Bloodrequest",
        )

    def van_fields(self):
        self.clear_vars()
        self.van_id_entry = self.create_field("Van ID", 0, 0)
        self.plate_number_entry = self.create_field("Plate Number", 1, 0)
        self.capacity_entry = self.create_field("Capacity", 2, 0)
        self.status_van_entry = self.create_field("Status", 3, 0)
        self.current_location_entry = self.create_field("Current Location", 4, 0)
        self.delivery_fk_entry = self.create_field("Delivery ID", 5, 0)

        self.create_action_buttons(
            self.insert_van,
            self.delete_van,
            self.update_van,
            self.view_van,
            self.search_van,
        )

    def insert_van(self):
        try:
            van_id = self.validate_integer(self.van_id_entry.get(), "Van ID")
            plate_number = self.validate_text(self.plate_number_entry.get(), "Plate Number")
            capacity = self.validate_integer(self.capacity_entry.get(), "Capacity")
            status = self.validate_text(self.status_van_entry.get(), "Status")
            current_location = self.validate_text(self.current_location_entry.get(), "Current Location")
            delivery_id = self.parse_optional_integer(self.delivery_fk_entry.get())
            query = (
                "INSERT INTO Van (van_id, plate_number, capacity, status, current_location, delivery_id) "
                "VALUES (?, ?, ?, ?, ?, ?)"
            )
            self.db.execute(
                query,
                [van_id, plate_number, capacity, status, current_location, delivery_id],
            )
            messagebox.showinfo("Success", "Van record added successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def delete_van(self):
        try:
            van_id = self.validate_integer(self.van_id_entry.get(), "Van ID")
            if not messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete Van record {van_id}?",
            ):
                return
            query = "DELETE FROM Van WHERE van_id = ?"
            self.db.execute(query, [van_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Van record found with that ID.")
            else:
                messagebox.showinfo("Deleted", "Van record deleted successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def update_van(self):
        try:
            van_id = self.validate_integer(self.van_id_entry.get(), "Van ID")
            plate_number = self.validate_text(self.plate_number_entry.get(), "Plate Number")
            capacity = self.validate_integer(self.capacity_entry.get(), "Capacity")
            status = self.validate_text(self.status_van_entry.get(), "Status")
            current_location = self.validate_text(self.current_location_entry.get(), "Current Location")
            delivery_id = self.parse_optional_integer(self.delivery_fk_entry.get())
            if not messagebox.askyesno(
                "Confirm Update",
                f"Are you sure you want to update Van record {van_id}?",
            ):
                return
            query = (
                "UPDATE Van SET plate_number = ?, capacity = ?, status = ?, current_location = ?, delivery_id = ? "
                "WHERE van_id = ?"
            )
            self.db.execute(query, [plate_number, capacity, status, current_location, delivery_id, van_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Van record found with that ID.")
            else:
                messagebox.showinfo("Success", "Van record updated successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def view_van(self):
        self.open_view_window(
            "Van Records",
            "SELECT van_id, plate_number, capacity, status, current_location, delivery_id FROM Van",
        )

    def delivery_fields(self):
        self.clear_vars()
        self.delivery_id_entry = self.create_field("Delivery ID", 0, 0)
        self.departure_time_entry = self.create_field("Departure Time", 1, 0)
        self.arrival_time_entry = self.create_field("Arrival Time", 2, 0)
        self.status_delivery_entry = self.create_field("Status", 3, 0)

        self.create_action_buttons(
            self.insert_delivery,
            self.delete_delivery,
            self.update_delivery,
            self.view_delivery,
            self.search_delivery,
        )

    def insert_delivery(self):
        try:
            delivery_id = self.validate_integer(self.delivery_id_entry.get(), "Delivery ID")
            departure_time = self.validate_date(self.departure_time_entry.get(), "Departure Time")
            arrival_time = self.validate_date(self.arrival_time_entry.get(), "Arrival Time")
            status = self.validate_choice(self.status_delivery_entry.get(), "Status", ["Scheduled", "In Transit", "Completed", "Cancelled"])
            query = (
                "INSERT INTO Delivery (delivery_id, departure_time, arrival_time, status) "
                "VALUES (?, ?, ?, ?)"
            )
            self.db.execute(
                query,
                [delivery_id, departure_time, arrival_time, status],
            )
            messagebox.showinfo("Success", "Delivery record added successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def delete_delivery(self):
        try:
            delivery_id = self.validate_integer(self.delivery_id_entry.get(), "Delivery ID")
            if not messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete Delivery record {delivery_id}?",
            ):
                return
            query = "DELETE FROM Delivery WHERE delivery_id = ?"
            self.db.execute(query, [delivery_id])
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Delivery record found with that ID.")
            else:
                messagebox.showinfo("Deleted", "Delivery record deleted successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def update_delivery(self):
        try:
            delivery_id = self.validate_integer(self.delivery_id_entry.get(), "Delivery ID")
            departure_time = self.validate_date(self.departure_time_entry.get(), "Departure Time")
            arrival_time = self.validate_date(self.arrival_time_entry.get(), "Arrival Time")
            status = self.validate_choice(self.status_delivery_entry.get(), "Status", ["Scheduled", "In Transit", "Completed", "Cancelled"])
            if not messagebox.askyesno(
                "Confirm Update",
                f"Are you sure you want to update Delivery record {delivery_id}?",
            ):
                return
            query = (
                "UPDATE Delivery SET departure_time = ?, arrival_time = ?, status = ? "
                "WHERE delivery_id = ?"
            )
            self.db.execute(
                query,
                [departure_time, arrival_time, status, delivery_id],
            )
            if self.db.cursor.rowcount == 0:
                messagebox.showinfo("Not Found", "No Delivery record found with that ID.")
            else:
                messagebox.showinfo("Success", "Delivery record updated successfully.")
            self.clear_form_fields()
        except Exception as error:
            self.handle_error(error)

    def view_delivery(self):
        self.open_view_window(
            "Delivery Records",
            "SELECT delivery_id, departure_time, arrival_time, status FROM Delivery",
        )

    def search_bloodtype(self):
        try:
            bloodtype_id = self.validate_integer(self.bloodtype_id_entry.get(), "Bloodtype ID")
            self.search_record(
                "Bloodtype Search Result",
                "SELECT Bloodtype_id, Bloodgroup, RHfactor, unit_id FROM bloodtype WHERE Bloodtype_id = ?",
                [bloodtype_id],
            )
        except Exception as error:
            self.handle_error(error)

    def search_hospital(self):
        try:
            hospital_id = self.validate_integer(self.hospital_id_entry.get(), "Hospital ID")
            self.search_record(
                "Hospital Search Result",
                "SELECT hospital_id, hospital_name, location, phone, request_id FROM hospital WHERE hospital_id = ?",
                [hospital_id],
            )
        except Exception as error:
            self.handle_error(error)

    def search_bloodunit(self):
        try:
            unit_id = self.validate_integer(self.unit_id_entry.get(), "Unit ID")
            self.search_record(
                "Bloodunit Search Result",
                "SELECT unit_id, collectiondate, expirydate, status, delivery_id FROM Bloodunit WHERE unit_id = ?",
                [unit_id],
            )
        except Exception as error:
            self.handle_error(error)

    def search_bloodrequest(self):
        try:
            request_id = self.validate_integer(self.request_id_entry.get(), "Request ID")
            self.search_record(
                "Bloodrequest Search Result",
                "SELECT request_id, request_date, quantity, Priority, status, bloodtype_id, delivery_id FROM Bloodrequest WHERE request_id = ?",
                [request_id],
            )
        except Exception as error:
            self.handle_error(error)

    def search_van(self):
        try:
            van_id = self.validate_integer(self.van_id_entry.get(), "Van ID")
            self.search_record(
                "Van Search Result",
                "SELECT van_id, plate_number, capacity, status, current_location, delivery_id FROM Van WHERE van_id = ?",
                [van_id],
            )
        except Exception as error:
            self.handle_error(error)

    def search_delivery(self):
        try:
            delivery_id = self.validate_integer(self.delivery_id_entry.get(), "Delivery ID")
            self.search_record(
                "Delivery Search Result",
                "SELECT delivery_id, departure_time, arrival_time, status FROM Delivery WHERE delivery_id = ?",
                [delivery_id],
            )
        except Exception as error:
            self.handle_error(error)

    def clear_vars(self):
        self.form_entries = []

    def clear_form_fields(self):
        for widget in self.form_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = BloodBankApp(root)
        app.run()
    except Exception as app_error:
        messagebox.showerror("Application Error", f"A fatal error occurred:\n{app_error}")
        sys.exit(1)
