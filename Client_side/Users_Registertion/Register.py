from tkinter import *


class Register:
    def __init__(self, window, status, client):
        self.status = status
        self.window = window
        self.client = client
        self.loop()

    def loop(self):
        """Main function to display and manage the registration page."""

        # Background image
        self.background_image = PhotoImage(file="../assets/register.png")
        bg_image_reg = Label(self.window, image=self.background_image)
        bg_image_reg.place(x=-2, y=-2)

        # Already Have an Account Text
        self.already_account_text = Label(
            bg_image_reg,
            text="?כבר רשום",
            fg="#000000",
            font=("Ariel", 12, "bold"),
            bg="#FFFFFF"
        )
        self.already_account_text.place(x=310, y=200)

        # Login Button
        self.login_button = Button(
            bg_image_reg,
            text="התחבר",
            fg="#1D4063",
            font=("Ariel", 12, "bold"),
            bg="#FFFFFF",
            bd=0,
            cursor="hand2",
            activebackground="#FFFFFF",
            activeforeground="#1D4063",
            command=self.LogIn_page
        )
        self.login_button.place(x=260, y=195, width=50, height=35)

        # First Name Section
        self.create_first_name_section(bg_image_reg)

        # Last Name Section
        self.create_last_name_section(bg_image_reg)

        # Username Section
        self.create_username_section(bg_image_reg)

        # Password Section
        self.create_password_section(bg_image_reg)

        # Confirm Password Section
        self.create_confirm_password_section(bg_image_reg)

        # Submit Button
        self.create_submit_button(bg_image_reg)

        # Bind Return key for submission
        self.window.bind("<Return>", lambda event: self.submit(self.username_entry, self.password_entry))

        self.window.mainloop()

    def create_first_name_section(self, parent):
        """Create the first name input section."""
        self.first_name_image = PhotoImage(file="../assets/short_input.png")
        first_name_input_frame = Label(parent, image=self.first_name_image, bg="#FFFFFF")
        first_name_input_frame.place(x=125, y=242)

        first_name_input_frame.bind("<Enter>", self.on_enter)
        first_name_input_frame.bind("<Leave>", self.on_leave)

        self.first_name_entry = Entry(
            first_name_input_frame,
            bd=0, bg="#FFFFFF", fg="#1D4063", highlightthickness=0,
            font=("Ariel", 12, "bold")
        )
        self.first_name_entry.place(x=11, y=10, width=175, height=34)

        first_name_label = Label(
            first_name_input_frame, text="*שם פרטי", fg="#1D4063", font=("Ariel", 10, "bold"), bg="#FFFFFF"
        )
        first_name_label.place(x=125, y=5, width=70, height=13)

    def create_last_name_section(self, parent):
        """Create the last name input section."""
        self.last_name_image = PhotoImage(file="../assets/short_input.png")
        last_name_input_frame = Label(parent, image=self.last_name_image, bg="#FFFFFF")
        last_name_input_frame.place(x=340, y=242)

        last_name_input_frame.bind("<Enter>", self.on_enter)
        last_name_input_frame.bind("<Leave>", self.on_leave)

        self.last_name_entry = Entry(
            last_name_input_frame,
            bd=0, bg="#FFFFFF", fg="#1D4063", highlightthickness=0,
            font=("Ariel", 12, "bold")
        )
        self.last_name_entry.place(x=11, y=10, width=175, height=34)

        last_name_label = Label(
            last_name_input_frame, text="*שם משפחה", fg="#1D4063", font=("Ariel", 10, "bold"), bg="#FFFFFF"
        )
        last_name_label.place(x=115, y=5, width=70, height=13)

    def create_username_section(self, parent):
        """Create the username input section."""
        self.username_image = PhotoImage(file="../assets/email.png")
        username_input_frame = Label(parent, image=self.username_image, bg="#FFFFFF")
        username_input_frame.place(x=125, y=310)

        username_input_frame.bind("<Enter>", self.on_enter)
        username_input_frame.bind("<Leave>", self.on_leave)

        self.username_entry = Entry(
            username_input_frame,
            bd=0, bg="#FFFFFF", fg="#1D4063", highlightthickness=0,
            font=("Ariel", 12, "bold")
        )
        self.username_entry.place(x=10, y=9, width=390, height=36)

        username_label = Label(
            username_input_frame, text="*שם משתמש", fg="#1D4063", font=("Ariel", 10, "bold"), bg="#FFFFFF"
        )
        username_label.place(x=320, y=5, width=85, height=13)

    def create_password_section(self, parent):
        """Create the password input section."""
        self.password_image = PhotoImage(file="../assets/short_input.png")
        password_input_frame = Label(parent, image=self.password_image, bg="#FFFFFF")
        password_input_frame.place(x=125, y=380)

        password_input_frame.bind("<Enter>", self.on_enter)
        password_input_frame.bind("<Leave>", self.on_leave)

        self.password_entry = Entry(
            password_input_frame,
            bd=0, bg="#FFFFFF", fg="#1D4063", show="•", highlightthickness=0,
            font=("Ariel", 12, "bold")
        )
        self.password_entry.place(x=11, y=10, width=175, height=34)

        password_label = Label(
            password_input_frame, text="*סיסמה", fg="#1D4063", font=("Ariel", 10, "bold"), bg="#FFFFFF"
        )
        password_label.place(x=135, y=5, width=60, height=13)

    def create_confirm_password_section(self, parent):
        """Create the confirm password input section."""
        self.confirm_password_image = PhotoImage(file="../assets/short_input.png")
        confirm_password_input_frame = Label(parent, image=self.confirm_password_image, bg="#FFFFFF")
        confirm_password_input_frame.place(x=340, y=380)

        confirm_password_input_frame.bind("<Enter>", self.on_enter)
        confirm_password_input_frame.bind("<Leave>", self.on_leave)

        self.confirm_password_entry = Entry(
            confirm_password_input_frame,
            bd=0, bg="#FFFFFF", fg="#1D4063", show="•", highlightthickness=0,
            font=("Ariel", 12, "bold")
        )
        self.confirm_password_entry.place(x=11, y=10, width=175, height=34)

        confirm_password_label = Label(
            confirm_password_input_frame, text="*אימות סיסמה", fg="#1D4063", font=("Ariel", 10, "bold"), bg="#FFFFFF"
        )
        confirm_password_label.place(x=105, y=5, width=85, height=13)

    def create_submit_button(self, parent):
        """Create the submit button."""
        self.submit_button_image = PhotoImage(file="../assets/reg_button.png")
        submit_button = Button(
            parent, image=self.submit_button_image, borderwidth=0, highlightthickness=0, relief="flat",
            bg="#ffffff", activebackground="#272A37", cursor="hand2",
            command=lambda: self.submit(self.first_name_entry, self.username_entry, self.password_entry,
                                        self.confirm_password_entry)
        )
        submit_button.place(x=157, y=500, width=333, height=65)


    def submit(self, first_name_entry, username_entry, password_entry, confirm_password_entry):
        """Submit the registration details."""
        if password_entry.get() == confirm_password_entry.get():
            self.client.register(first_name_entry.get(), username_entry.get(), password_entry.get())
            self.status[0] = "Log_In"
            self.window.quit()
        else:
            error_label = Label(
                text="עליך להזין את אותה הסיסמה",
                fg="#FF0000", font=("Ariel", 12), bg="#ffffff"
            )
            error_label.place(x=230, y=460)

    def LogIn_page(self):
        """Redirect to the login page."""
        self.status[0] = "Log_In"
        self.window.quit()

    def on_enter(self, event):
        """Highlight the entry when mouse enters the widget."""
        event.widget.winfo_children()[1].config(fg="#7D91A4")  # Glowing effect for text
        for child in event.widget.winfo_children():
            child.lift()

    def on_leave(self, event):
        """Revert to default colors when mouse leaves."""
        event.widget.winfo_children()[1].config(fg="#1D4063")  # Default text color
        for child in event.widget.winfo_children():
            child.lift()
