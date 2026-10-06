import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
from datetime import datetime
import re

# ==========================================
# 1. ENTITY CLASS (DATA MODEL)
# ==========================================
class MemberData:
    """Class representing the affiliate entity stored in memory."""
    def __init__(self, doc_type: str, doc_num: str, full_name: str, 
                 current_income: float, desired_service: str, 
                 employment_type: str, affiliation_fee: float, affiliation_date: str):
        self.doc_type = doc_type
        self.doc_num = doc_num
        self.full_name = full_name
        self.current_income = current_income
        self.desired_service = desired_service
        self.employment_type = employment_type
        self.affiliation_fee = affiliation_fee
        self.affiliation_date = affiliation_date


# ==========================================
# 2. MAIN APPLICATION (DATA MANAGEMENT)
# ==========================================
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compensandote Compensation Fund - Affiliate Management")
        self.geometry("980x670")
        self.minsize(750, 520)
        self.configure(bg="#FDEDEC")  # Soft pastel pink background

        # Linear Data Structures in Memory
        self.stack_data = deque()  # Stack (LIFO)
        self.queue_data = deque()  # Queue (FIFO)
        self.list_data = []        # List (Sequential)

        self._configure_pastel_pink_styles()
        self._build_responsive_interface()

    def _configure_pastel_pink_styles(self):
        """Configuration of the pastel pink color palette and custom button styles."""
        style = ttk.Style()
        style.theme_use("clam")

        # Pastel Pink Palette Constants
        COLOR_BACKGROUND = "#FDEDEC"      # Very soft pastel pink
        COLOR_PANEL = "#FFFFFF"           # Clean white for containers
        COLOR_PRIMARY_PINK = "#FADBD8"    # Base pastel pink for buttons
        COLOR_BUTTON_HOVER = "#F5B7B1"    # Darker pastel pink on hover
        COLOR_TEXT = "#4A235A"            # Dark plum/purple for high contrast text
        COLOR_HEADER = "#E8DAEF"          # Soft lilac/pink for table header

        style.configure(".", background=COLOR_BACKGROUND, foreground=COLOR_TEXT, font=("Segoe UI", 9))
        style.configure("TLabelframe", background=COLOR_PANEL, relief="flat", borderwidth=1)
        style.configure("TLabelframe.Label", background=COLOR_PANEL, foreground="#7D3C98", font=("Segoe UI", 10, "bold"))
        style.configure("TFrame", background=COLOR_PANEL)
        
        style.configure("TLabel", background=COLOR_PANEL, foreground=COLOR_TEXT)
        style.configure("TRadiobutton", background=COLOR_PANEL, foreground=COLOR_TEXT)
        
        # Explicit Button Styling fixing white background issue
        style.configure("Pink.TButton", 
                        background=COLOR_PRIMARY_PINK, 
                        foreground="#512E5F",
                        borderwidth=1, 
                        relief="flat",
                        focuscolor="none", 
                        font=("Segoe UI", 9, "bold"), 
                        padding=6)
        
        style.map("Pink.TButton", 
                  background=[("active", COLOR_BUTTON_HOVER), ("pressed", "#E6B0AA")],
                  foreground=[("active", "#4A235A"), ("pressed", "#4A235A")])

        # Table (Treeview) Styling
        style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF", foreground=COLOR_TEXT, rowheight=25)
        style.configure("Treeview.Heading", background=COLOR_HEADER, foreground="#512E5F", font=("Segoe UI", 9, "bold"))
        style.map("Treeview.Heading", background=[("active", "#D2B4DE")])

    def _build_responsive_interface(self):
        """Constructs a scrollable container to adapt elements when resizing the window."""
        self.main_canvas = tk.Canvas(self, bg="#FDEDEC", highlightthickness=0)
        self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.main_canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar_v.set)
        self.main_canvas.bind('<Configure>', self._on_canvas_configure)

        self.scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # -------------------------------------------------------------
        # LEFT PANEL - REGISTRATION FORM
        # -------------------------------------------------------------
        left_panel = ttk.LabelFrame(self.scrollable_frame, text=" Affiliate Registration ", padding=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        ttk.Label(left_panel, text="Document Type:").pack(anchor=tk.W, pady=(2,0))
        self.cb_doc_type = ttk.Combobox(left_panel, values=["CC", "CE", "NUIP", "PAS"], state="readonly")
        self.cb_doc_type.current(0)
        self.cb_doc_type.pack(fill=tk.X, pady=2)

        ttk.Label(left_panel, text="Document Number:").pack(anchor=tk.W, pady=(4,0))
        self.txt_doc_num = ttk.Entry(left_panel)
        self.txt_doc_num.insert(0, "e.g., 1012345678")
        self.txt_doc_num.bind("<FocusIn>", lambda e: self._clear_placeholder(self.txt_doc_num, "e.g., 1012345678"))
        self.txt_doc_num.pack(fill=tk.X, pady=2)

        ttk.Label(left_panel, text="Full Name:").pack(anchor=tk.W, pady=(4,0))
        self.txt_name = ttk.Entry(left_panel)
        self.txt_name.insert(0, "e.g., Jane Doe")
        self.txt_name.bind("<FocusIn>", lambda e: self._clear_placeholder(self.txt_name, "e.g., Jane Doe"))
        self.txt_name.pack(fill=tk.X, pady=2)

        ttk.Label(left_panel, text="Monthly Income ($):").pack(anchor=tk.W, pady=(4,0))
        self.txt_income = ttk.Entry(left_panel)
        self.txt_income.insert(0, "e.g., 2500000")
        self.txt_income.bind("<FocusIn>", lambda e: self._clear_placeholder(self.txt_income, "e.g., 2500000"))
        self.txt_income.bind("<FocusOut>", lambda e: self.calculate_fee())
        self.txt_income.pack(fill=tk.X, pady=2)

        ttk.Label(left_panel, text="Employment Type:").pack(anchor=tk.W, pady=(4,0))
        self.var_employment = tk.StringVar(value="Employee")
        frame_rb = ttk.Frame(left_panel)
        frame_rb.pack(fill=tk.X)
        ttk.Radiobutton(frame_rb, text="Employee", value="Employee", variable=self.var_employment, command=self.calculate_fee).pack(side=tk.LEFT)
        ttk.Radiobutton(frame_rb, text="Independent", value="Independent", variable=self.var_employment, command=self.calculate_fee).pack(side=tk.LEFT, padx=10)

        ttk.Label(left_panel, text="Desired Service:").pack(anchor=tk.W, pady=(4,0))
        services = ["Unemployment Allowance", "Park Access", "Training Course", "Travel Package", "Preventive Medicine"]
        self.cb_service = ttk.Combobox(left_panel, values=services, state="readonly")
        self.cb_service.current(0)
        self.cb_service.pack(fill=tk.X, pady=2)
        self.cb_service.bind("<<ComboboxSelected>>", lambda e: self.calculate_fee())

        ttk.Label(left_panel, text="Calculated Affiliation Fee ($):").pack(anchor=tk.W, pady=(4,0))
        self.txt_fee = ttk.Entry(left_panel, state="readonly")
        self.txt_fee.pack(fill=tk.X, pady=2)

        ttk.Label(left_panel, text="Date (Day / Month / Year):").pack(anchor=tk.W, pady=(4,0))
        frame_date = ttk.Frame(left_panel)
        frame_date.pack(fill=tk.X)
        
        now = datetime.now()
        self.sp_day = ttk.Spinbox(frame_date, from_=1, to=31, width=3, format="%02.0f")
        self.sp_month = ttk.Spinbox(frame_date, from_=1, to=12, width=3, format="%02.0f")
        self.sp_year = ttk.Spinbox(frame_date, from_=2020, to=2030, width=5)
        
        self.sp_day.set(f"{now.day:02d}")
        self.sp_month.set(f"{now.month:02d}")
        self.sp_year.set(str(now.year))
        
        self.sp_day.pack(side=tk.LEFT); ttk.Label(frame_date, text="/").pack(side=tk.LEFT)
        self.sp_month.pack(side=tk.LEFT); ttk.Label(frame_date, text="/").pack(side=tk.LEFT)
        self.sp_year.pack(side=tk.LEFT)

        ttk.Label(left_panel, text="Target Data Structure:").pack(anchor=tk.W, pady=(10,0))
        self.cb_structure = ttk.Combobox(left_panel, values=["Stack (LIFO)", "Queue (FIFO)", "List (Sequential)"], state="readonly")
        self.cb_structure.current(0)
        self.cb_structure.pack(fill=tk.X, pady=2)
        self.cb_structure.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        ttk.Label(left_panel, text="Report Result:").pack(anchor=tk.W, pady=(6,0))
        self.txt_report = ttk.Entry(left_panel, state="readonly")
        self.txt_report.pack(fill=tk.X, pady=2)

        # -------------------------------------------------------------
        # RIGHT PANEL - DATA TABLE
        # -------------------------------------------------------------
        right_panel = ttk.Frame(self.scrollable_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

        columns = ("Doc Type", "Doc Number", "Name", "Income", "Service", "Employment", "Fee", "Date")
        self.table = ttk.Treeview(right_panel, columns=columns, show="headings", height=15)
        
        tree_scroll_y = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.table.yview)
        tree_scroll_x = ttk.Scrollbar(right_panel, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=105, anchor=tk.CENTER)

        self.table.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")

        right_panel.rowconfigure(0, weight=1)
        right_panel.columnconfigure(0, weight=1)

        # -------------------------------------------------------------
        # BOTTOM PANEL - ACTION BUTTONS
        # -------------------------------------------------------------
        frame_buttons = ttk.Frame(self.scrollable_frame)
        frame_buttons.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))

        ttk.Button(frame_buttons, text="Register", style="Pink.TButton", command=self.register_member).pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_buttons, text="Clear", style="Pink.TButton", command=self.clear_fields).pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_buttons, text="Report", style="Pink.TButton", command=self.show_report).pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_buttons, text="Delete", style="Pink.TButton", command=self.delete_record).pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_buttons, text="Exit", style="Pink.TButton", command=self.destroy).pack(side=tk.RIGHT, padx=4)

        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=2)
        self.scrollable_frame.rowconfigure(0, weight=1)

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _clear_placeholder(self, entry, placeholder_text):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)

    def get_current_structure(self):
        val = self.cb_structure.get()
        if "Stack" in val: return "Stack"
        if "Queue" in val: return "Queue"
        return "List"

    def calculate_fee(self):
        """Calculates the fee dynamically based on income, employment, and service."""
        income_str = self.txt_income.get().strip()
        try:
            income = float(income_str)
        except ValueError:
            return

        emp_type = self.var_employment.get()
        base_fee = 0.0

        if income < 1000000:
            base_fee = 0.0
        elif emp_type == "Employee":
            if 1000000 <= income <= 2000000: base_fee = 45000
            elif income <= 3000000: base_fee = 60000
            elif income <= 4000000: base_fee = 75000
            elif income <= 5000000: base_fee = 90000
            elif income > 5000000: base_fee = 150000
        else:  # Independent
            if 1000000 <= income <= 2000000: base_fee = 10000
            elif income <= 3000000: base_fee = 20000
            elif income <= 4000000: base_fee = 30000
            elif income <= 5000000: base_fee = 40000
            elif income > 5000000: base_fee = 80000

        service = self.cb_service.get()
        surcharge = 0.0
        if service == "Park Access": surcharge = 2500
        elif service == "Training Course": surcharge = 7500
        elif service == "Travel Package": surcharge = 10000
        elif service == "Preventive Medicine": surcharge = income * 0.10

        total_fee = base_fee + surcharge
        self.txt_fee.config(state="normal")
        self.txt_fee.delete(0, tk.END)
        self.txt_fee.insert(0, f"{total_fee:.2f}")
        self.txt_fee.config(state="readonly")

    def register_member(self):
        """Validates and registers the affiliate into the active data structure."""
        doc_num = self.txt_doc_num.get().strip()
        name = self.txt_name.get().strip()
        income_str = self.txt_income.get().strip()

        if not doc_num.isdigit():
            messagebox.showerror("Validation Error", "Document number must contain digits only.")
            return
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", name) or name.startswith("e.g."):
            messagebox.showerror("Validation Error", "Full name must contain letters only.")
            return
        try:
            income = float(income_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Income must be a valid numeric value.")
            return

        if income < 1000000:
            messagebox.showwarning("Warning", "The minimum income required for the fee table is $1,000,000.")
            return

        self.calculate_fee()
        fee = float(self.txt_fee.get())
        date_str = f"{self.sp_day.get()}/{self.sp_month.get()}/{self.sp_year.get()}"

        member = MemberData(
            self.cb_doc_type.get(), doc_num, name, income, 
            self.cb_service.get(), self.var_employment.get(), fee, date_str
        )

        struct_name = self.get_current_structure()
        if struct_name == "Stack":
            self.stack_data.append(member)
        elif struct_name == "Queue":
            self.queue_data.append(member)
        elif struct_name == "List":
            self.list_data.append(member)

        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Success", f"Affiliate successfully registered in the {struct_name}.")

    def refresh_table(self):
        """Refreshes the table view according to the active structure."""
        for item in self.table.get_children():
            self.table.delete(item)

        struct_name = self.get_current_structure()
        dataset = []
        if struct_name == "Stack": dataset = list(reversed(self.stack_data))
        elif struct_name == "Queue": dataset = list(self.queue_data)
        elif struct_name == "List": dataset = self.list_data

        for m in dataset:
            self.table.insert("", tk.END, values=(
                m.doc_type, m.doc_num, m.full_name, 
                f"${m.current_income:,.2f}", m.desired_service, 
                m.employment_type, f"${m.affiliation_fee:,.2f}", m.affiliation_date
            ))

    def show_report(self):
        """Generates a summary report based on the active structure."""
        struct_name = self.get_current_structure()
        res = ""

        if struct_name == "Stack":
            total_sum = sum(m.affiliation_fee for m in self.stack_data)
            res = f"Total Fees Sum: ${total_sum:,.2f}"
        elif struct_name == "Queue":
            count = len(self.queue_data)
            res = f"Total Records: {count}"
        elif struct_name == "List":
            if self.list_data:
                avg = sum(m.current_income for m in self.list_data) / len(self.list_data)
                res = f"Average Income: ${avg:,.2f}"
            else:
                res = "Average Income: $0.00"

        self.txt_report.config(state="normal")
        self.txt_report.delete(0, tk.END)
        self.txt_report.insert(0, res)
        self.txt_report.config(state="readonly")

    def delete_record(self):
        """Deletes items honoring LIFO (Stack), FIFO (Queue), or ID Search (List)."""
        struct_name = self.get_current_structure()

        if struct_name == "Stack":
            if not self.stack_data:
                messagebox.showwarning("Warning", "The Stack is empty.")
                return
            if messagebox.askyesno("Confirm", "Do you want to pop the last registered affiliate?"):
                self.stack_data.pop()
                self.refresh_table()

        elif struct_name == "Queue":
            if not self.queue_data:
                messagebox.showwarning("Warning", "The Queue is empty.")
                return
            if messagebox.askyesno("Confirm", "Do you want to dequeue the first registered affiliate?"):
                self.queue_data.popleft()
                self.refresh_table()

        elif struct_name == "List":
            if not self.list_data:
                messagebox.showwarning("Warning", "The List is empty.")
                return
            doc_num = self.txt_doc_num.get().strip()
            if not doc_num or doc_num.startswith("e.g."):
                messagebox.showerror("Error", "Please enter the Document Number to search and delete from the List.")
                return
            
            target = next((x for x in self.list_data if x.doc_num == doc_num), None)
            if target and messagebox.askyesno("Confirm", f"Delete {target.full_name} from the list?"):
                self.list_data.remove(target)
                self.refresh_table()
            elif not target:
                messagebox.showerror("Error", "Document number not found in the List.")

    def clear_fields(self):
        """Resets the input fields."""
        self.txt_doc_num.delete(0, tk.END)
        self.txt_doc_num.insert(0, "e.g., 1012345678")
        self.txt_name.delete(0, tk.END)
        self.txt_name.insert(0, "e.g., Jane Doe")
        self.txt_income.delete(0, tk.END)
        self.txt_income.insert(0, "e.g., 2500000")
        
        self.txt_fee.config(state="normal")
        self.txt_fee.delete(0, tk.END)
        self.txt_fee.config(state="readonly")


# ==========================================
# 3. LOGIN INTERFACE (ENTRY POINT)
# ==========================================
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Compensation Fund Compensandote")
        self.geometry("480x390")
        self.resizable(False, False)
        self.configure(bg="#FDEDEC")  # Soft pastel pink

        # Menu Bar Configuration
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        menu_bar.add_command(label="About", command=self.show_about_info)

        # Header Titles in English
        tk.Label(self, text="Compensation Fund Compensandote", font=("Segoe UI", 14, "bold"), bg="#FDEDEC", fg="#512E5F").pack(pady=(18, 2))
        tk.Label(self, text="Application: Phase 3", font=("Segoe UI", 11, "bold"), bg="#FDEDEC", fg="#7D3C98").pack(pady=1)
        tk.Label(self, text="Student: Angie Nathaly Gonzalez", font=("Segoe UI", 10), bg="#FDEDEC", fg="#4A235A").pack(pady=1)
        
        # Execution Date Display
        current_date_str = datetime.now().strftime("%d/%m/%Y")
        tk.Label(self, text=f"Execution Date: {current_date_str}", font=("Segoe UI", 9, "italic"), bg="#FDEDEC", fg="#6C3483").pack(pady=(1, 12))

        # Password Input Field
        tk.Label(self, text="Access Password:", font=("Segoe UI", 10, "bold"), bg="#FDEDEC", fg="#4A235A").pack(pady=(5, 3))
        
        self.txt_password = ttk.Entry(self, show="*", font=("Segoe UI", 10))
        self.txt_password.pack(pady=4)
        self.txt_password.focus()

        # Action Buttons Frame with Custom Pink Buttons
        frame_btn = tk.Frame(self, bg="#FDEDEC")
        frame_btn.pack(pady=20)
        
        # Custom Tkinter buttons for full color compatibility
        btn_enter = tk.Button(frame_btn, text="Enter", font=("Segoe UI", 9, "bold"), 
                              bg="#F1948A", fg="#FFFFFF", activebackground="#E6B0AA", activeforeground="#FFFFFF",
                              bd=0, padx=15, pady=5, command=self.validate_login)
        btn_enter.pack(side=tk.LEFT, padx=8)

        btn_exit = tk.Button(frame_btn, text="Exit", font=("Segoe UI", 9, "bold"), 
                             bg="#F1948A", fg="#FFFFFF", activebackground="#E6B0AA", activeforeground="#FFFFFF",
                             bd=0, padx=15, pady=5, command=self.destroy)
        btn_exit.pack(side=tk.LEFT, padx=8)

    def show_about_info(self):
        """Displays modal window with updated developer & academic details in English."""
        info = (
            "Student: Angie Nathaly Gonzalez Carrillo\n"
            "UNAD ECBTI - Systems Engineering\n"
            "Course: Data Structures - 301305A\n"
            "Group: 301305A_2204\n"
            "Year: 2026"
        )
        messagebox.showinfo("About Developer", info)

    def validate_login(self):
        """Validates that the password is strictly 'Caja'."""
        if self.txt_password.get() == "Caja":
            self.destroy()
            app = MainApplication()
            app.mainloop()
        else:
            messagebox.showerror("Access Denied", "Incorrect password. Please try again.")


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()