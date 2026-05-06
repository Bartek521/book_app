import customtkinter as ctk
from database import database
from UserAction import UserAction

class LoginFrame (ctk.CTkFrame):
    def __init__(self,master,switch_callback,user_action):
        super().__init__(master)
        self.main_app = master
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
            user_id = result[0][0]
            self.master.show_user_frame(user_id)
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

        self.entry_password = ctk.CTkEntry(self,placeholder_text="Hasło min 7 znaków", show="*")
        self.entry_password.pack(pady=10)

        self.register_button = ctk.CTkButton(self,text="Zarejestruj się",command=self.register_event)
        self.register_button.pack(pady=5)

        self.register_button = ctk.CTkButton(self, text="Zaloguj się", fg_color="transparent", font=("Arial", 10),command=switch_callback)
        self.register_button.pack(pady=5)

        self.error_info = ctk.CTkLabel(self,text="",bg_color="transparent")
        self.error_info.pack(pady=5)
    def register_event(self):
        name = self.entry_name.get()
        lastname = self.entry_lastname.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        success,message = self.UserAction.AddUser(name,lastname,email,password,"USER")

        if success:
            print(f"SUKCES :{message}")

        else:
            print(f"{message}")
            self.error_info.configure(text=f"{message}", text_color="red")
class UserFrame(ctk.CTkFrame):
    def __init__(self, master, user_id,user_actions,logout_callback):
        super().__init__(master)
        self.user_id = user_id
        self.UserAction = user_actions
        self.logout_callback = logout_callback

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.grid(row=0,column=0,sticky="ew",padx=20,pady=10)

        self.title_label = ctk.CTkLabel(self.top_bar, text="Do przeczytania", font=("Arial",24,"bold"))
        self.title_label.pack(side="left")

        self.menu_options = ctk.CTkOptionMenu(self.top_bar,
                                              values=["Menu","Dodaj książkę do listy","Statystyki","Wyloguj"],command=self.menu_callback)
        self.menu_options.pack(side="right")
        self.menu_options.set("Opcje")

        self.scrol_frame = ctk.CTkScrollableFrame(self,label_text="Moje książki do przeczytania")
        self.scrol_frame.grid(row=1,column=0,sticky="nsew",padx=20,pady=(0,20))

        self.to_read_list()
    def menu_callback(self,choice):
        if choice== "Wyloguj":
            self.logout_callback()
        elif choice == "Dodaj książkę do listy":
            self.add_book_window()
        elif choice == "Statystyki":
            print("Tu będą statystyki")

        self.menu_options.set("Opcje")
    def to_read_list(self):
        for element in self.scrol_frame.winfo_children():
            element.destroy()

        books = self.UserAction.DownloadList(self.user_id,"DO PRZECZYTANIA")

        if not books:
            msg = ctk.CTkLabel(self.scrol_frame,text = "Brak książek do przeczytania")
            msg.pack(pady=20)
            return
        for book in books:
            book_item = ctk.CTkFrame(self.scrol_frame)
            book_item.pack(fill="x", pady=5,padx=5)

            book_info = ctk.CTkLabel(book_item,text = f"{book[2]}-{book[3]}",font=("Arial",14))
            book_info.pack(side="left",padx=10,pady=5)

            status_menu =ctk.CTkOptionMenu(book_item, values=["Zmień status","W TRAKCIE CZYTANIA", "PRZECZYTANE", "USUŃ"],
                                           width=140,command=lambda choice ,b=book[1]:self.change_status(choice, b))
            status_menu.pack(side="right",padx=10)
            status_menu.set("Zmień status")
    def change_status(self,new_status,barcode):
        if new_status == "Zmień status":
            return
        success, message = self.UserAction.UpdateStatus(self.user_id,barcode,new_status)

        if success:
            self.to_read_list()
        elif new_status == "Usuń":
            print("Metoda do usuń")
        else:
            self.to_read_list()



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
    def show_user_frame(self,user_id):
        self.clear_screen()
        self.frame = UserFrame(self,user_id,self.user_action,self.show_login_frame)
        self.frame.pack(pady=20,padx=20,fill="both",expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()