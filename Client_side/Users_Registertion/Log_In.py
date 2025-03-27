from tkinter import *


class LogIn:
    def __init__(self, window, status, client):
        self.status = status
        self.window = window
        self.client = client
        self.initialize_ui()

    def initialize_ui(self):
        """Main function to display and manage the login page."""

        # Background image
        self.background_image = PhotoImage(file="../assets/log_in.png")
        bg_image_login = Label(self.window, image=self.background_image)
        bg_image_login.place(x=-2, y=-2)

        # Username Section
        self.create_username_section(bg_image_login)

        # Password Section
        self.create_password_section(bg_image_login)

        # Sign-Up Redirect
        self.create_signup_redirect(bg_image_login)

        # Submit Button
        self.create_submit_button(bg_image_login)

        # Bind Return key for submission
        self.window.bind("<Return>", lambda event: self.submit(self.username_entry, self.password_entry))

        # Start main loop
        self.window.mainloop()

    def create_username_section(self, parent):
        """Create the username input section."""
        self.username_image = PhotoImage(file="../assets/email.png")
        username_input_frame = Label(parent, image=self.username_image, bg="#FFFFFF")
        username_input_frame.place(x=117, y=252)

        # Mouse enter/leave events
        username_input_frame.bind("<Enter>", self.on_enter)
        username_input_frame.bind("<Leave>", self.on_leave)

        # Username entry field
        self.username_entry = Entry(
            username_input_frame,
            bd=0, bg="#FFFFFF", fg="#1D4063", highlightthickness=0,
            font=("Ariel", 12, "bold")
        )
        self.username_entry.place(x=40, y=9, width=360, height=36)

        # Username label
        username_label = Label(
            username_input_frame, text="*שם משתמש", fg="#1D4063", font=("Ariel", 12, "bold"), bg="#FFFFFF"
        )
        username_label.place(x=305, y=5, width=85, height=13)

        # Username icon
        self.username_icon = PhotoImage(file="../assets/email-icon.png")
        username_icon_label = Label(image=self.username_icon, bg="#FFFFFF")
        username_icon_label.place(x=125, y=267)

    def create_password_section(self, parent):
        """Create the password input section."""
        self.password_image = PhotoImage(file="../assets/email.png")
        password_input_frame = Label(parent, image=self.password_image, bg="#FFFFFF")
        password_input_frame.place(x=117, y=330)

        # Mouse enter/leave events
        password_input_frame.bind("<Enter>", self.on_enter)
        password_input_frame.bind("<Leave>", self.on_leave)

        # Password entry field
        self.password_entry = Entry(
            password_input_frame,
            bd=0, bg="#FFFFFF", fg="#1D4063", highlightthickness=0,
            show="•", font=("Ariel", 12, "bold")
        )
        self.password_entry.place(x=40, y=9, width=360, height=36)

        # Password label
        password_label = Label(
            password_input_frame, text="*סיסמה", fg="#1D4063", font=("Ariel", 12, "bold"), bg="#FFFFFF"
        )
        password_label.place(x=325, y=5, width=82, height=13)

        # Password icon
        self.password_icon = PhotoImage(file="../assets/pass-icon.png")
        password_icon_label = Label(image=self.password_icon, bg="#FFFFFF")
        password_icon_label.place(x=125, y=345)

    def create_signup_redirect(self, parent):
        """Create the sign-up redirect text and button."""
        sign_up_text = Label(
            parent, text="?אין לי משתמש", fg="#000000", font=("Ariel", 12, "bold"), bg="#FFFFFF"
        )
        sign_up_text.place(x=290, y=400)

        redirect_signup_button = Button(
            parent, text="הרשמה", fg="#1D4063", font=("Ariel", 12, "bold"), bg="#FFFFFF", bd=0,
            cursor="hand2", activebackground="#FFFFFF", activeforeground="#1D4063",
            command=self.register_page
        )
        redirect_signup_button.place(x=240, y=395, width=50, height=35)

    def create_submit_button(self, parent):
        """Create the submit button."""
        self.submit_button_image = PhotoImage(file="../assets/button.png")
        submit_button = Button(
            parent, image=self.submit_button_image, borderwidth=0, highlightthickness=0, relief="flat",
            bg="#ffffff", activebackground="#272A37", cursor="hand2",
            command=lambda: self.submit(self.username_entry, self.password_entry)
        )
        submit_button.place(x=157, y=445, width=333, height=65)

    def register_page(self):
        """Redirect to the register page."""
        self.status[0] = "Register"
        self.window.quit()

    def submit(self, username_entry, password_entry):
        """Submit the login credentials."""
        if self.status[0] == "Log_In":
            if self.client.log_in(username_entry.get(), password_entry.get()):
                self.status[0] = "App"
                self.window.quit()
            else:
                error_label = Label(
                    text="שם משתמש או הסיסמה שגויה", fg="#FF0000", font=("Ariel", 12), bg="#ffffff"
                )
                error_label.place(x=230, y=420)

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
