import customtkinter as ctk
from database import database
from UserAction import UserAction

class LoginFrame (ctk.CTkFrame):
    def __init__(self,master,switch_callback,user_action):
        super().__init__(master)
        self.UserAction = user_action

        self.label = ctk.CTkLabel(self, text="Logowanie",font=("Arial",20))
        self.label.pack(pady=20)

        self.email_entry = ctk.CTkEntry(self,placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self,placeholder_text="Hasło",show="*")
        self.password_entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Zaloguj",command=self.login_event)
        self.button.pack(pady=20)

        self.register_button = ctk.CTkButton(self,text="Zarejestruj się",fg_color="transparent",font=("Arial",10),command=switch_callback)
        self.register_button.pack(pady=5)
    def login_event(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        result, message = self.UserAction.Login(email,password)
        if result:
            print(f"{message}")
            #dodam przekierowanie do menu
        else:
            print(f"{message}")
class RegisterFrame(ctk.CTkFrame):
    def __init__(self,master,switch_callback,user_action):
        super().__init__(master)
        self.UserAction = user_action

        self.label = ctk.CTkLabel(self,text="Zarejestruj się", font=("Arial",20))
        self.label.pack(pady=20)

        self.entry_name = ctk.CTkEntry(self,placeholder_text="Imię")
        self.entry_name.pack(pady=10)

        self.entry_lastname = ctk.CTkEntry(self, placeholder_text="Nazwisko")
        self.entry_lastname.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self,placeholder_text="E-mail")
        self.entry_email.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self,placeholder_text="Hasło", show="*")
        self.entry_password.pack(pady=10)

        self.register_button = ctk.CTkButton(self,text="Zarejestruj się",command=self.register_event)
        self.register_button.pack(pady=5)

        self.register_button = ctk.CTkButton(self, text="Zaloguj się", fg_color="transparent", font=("Arial", 10),command=switch_callback)
        self.register_button.pack(pady=5)
    def register_event(self):
        name = self.entry_name.get()
        lastname = self.entry_lastname.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        success,message = self.UserAction.AddUser(name,lastname,email,password,"ADMIN")

        if success:
            print(f"{message}")
        else:
            print(f"{message}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x1000")
        self.title("Domowa biblioteczka")

        self.db = database()
        self.db.InitDb()
        self.user_action = UserAction(self.db)

        self.frame = None
        self.show_login_frame()
    def clear_screen(self):
        if self.frame is not None:
            self.frame.destroy()
    def show_login_frame(self):
        self.clear_screen()
        self.frame = LoginFrame(self,self.show_register,self.user_action)
        self.frame.pack(pady=20,padx=20,fill="both",expand=True)
    def show_register(self):
        self.clear_screen()
        self.frame = RegisterFrame(self,self.show_login_frame,self.user_action)
        self.frame.pack(pady=20,padx=20,fill="both",expand =True)




if __name__ == "__main__":
    app = App()
    app.mainloop()