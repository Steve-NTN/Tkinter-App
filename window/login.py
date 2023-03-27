from tkinter import *
from tkinter import messagebox
from database.controller import *
from .register import RegisterApplication
from .caculator import MainApplication
from .size_config import ENTRY_HEIGHT, FONT_SIZE, ENTRY_WIDTH, BUTTON_WIDTH

# Cửa sổ đăng nhập
class LoginApplication(Tk):
    def __init__(self):
        super().__init__()
        positionRight = int(self.winfo_screenwidth()/2)
        positionDown = int(self.winfo_screenheight()/2)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+{0}+{0}")
        print(self.winfo_screenwidth(), self.winfo_screenheight())
        self.bind("<Escape>", lambda event: self.destroy())
        self.title("Đăng nhập")  
        icon = PhotoImage(file = "images/icon.png")
        self.iconphoto(False, icon)
        self.resizable(0, 0)

        # Cấu hình thành phần màn đăng nhập
        self.label_user = Label(self, text="Tài khoản", font=("Arial", FONT_SIZE))
        self.label_user.place(x=positionRight / 2, y=positionDown / 3)

        self.entry_user = Entry(self, width=ENTRY_WIDTH, font=("Arial", ENTRY_HEIGHT)) 
        self.entry_user.focus()
        self.entry_user.place(x=3 * positionRight / 4, y=positionDown / 3, height=ENTRY_HEIGHT)

        self.label_password = Label(self, text="Mật khẩu", font=("Arial", FONT_SIZE))
        self.label_password.place(x=positionRight / 2, y=positionDown / 3 + 2 * ENTRY_HEIGHT)

        self.entry_password = Entry(self, show="*", width=ENTRY_WIDTH, font=("Arial", ENTRY_HEIGHT)) 
        self.entry_password.place(x=3 * positionRight / 4, y=positionDown + ENTRY_HEIGHT, height=ENTRY_HEIGHT)
        
        self.button_login = Button(self, text="Login", command=lambda:self.click_login(), width=BUTTON_WIDTH) 
        self.button_login.place(x=20, y=100)
        
        self.button_cancle = Button(self, text="Cancel", command=lambda:self.click_cancle(), width=BUTTON_WIDTH) 
        self.button_cancle.place(x=280, y=100)

        # self.button_login.grid(row=3, column=0, pady=10)
        self.button_register = Button(self, text="Register", command=lambda:self.click_register(), width=BUTTON_WIDTH) 
        self.button_register.place(x=150, y=100)
        self.bind("<Return>", self.click_login)

        # Xử lí sự kiện click đăng nhập
    def click_login(self, event=None):
        acc = {'user_id': self.entry_user.get().strip(), 'user_pw': self.entry_password.get().strip()}
        # Kiểm tra tài khoản, mật khẩu
        if acc['user_id'] == "" or acc['user_pw'] == "":
            messagebox.showinfo("Thông báo","Cần phải nhập đầy đủ thông tin.", icon = 'error')
        else:
            if can_login(self.entry_user.get(), self.entry_password.get()): 
                # messagebox.showinfo("Thông báo","Đăng nhập tài khoản {} thành công.".format(acc['user_id']))
                self.login_success()
            else:
                messagebox.showinfo("Thông báo","Tài khoản hoặc mật khẩu không đúng.", icon = 'error')

    # Xử lí sự kiện đăng ký
    def click_register(self):
        self.withdraw()
        register = RegisterApplication(self)
        register.grab_set()

    def login_success(self):
        self.withdraw()
        main = MainApplication(self)
        main.grab_set()

    def show(self):
        self.update()
        self.deiconify()

    # Xử lí sự kiến thoát
    def click_cancle(self): 
        msgbox = messagebox.askquestion('Đóng ứng dụng', 'Bạn có muốn đóng ứng dụng không?', icon = 'warning')  
        if msgbox == 'yes': 
            self.destroy()  
