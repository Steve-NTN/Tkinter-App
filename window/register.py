from tkinter import *
from tkinter import messagebox
from database.controller import check_register, register_acc, check_admin_code

class CheckAdmin(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.origin_frame = parent
        self.title("Mã xác nhận Admin")
        positionRight = int(self.winfo_screenwidth()/2 - 330/2)
        positionDown = int(self.winfo_screenheight()/2 - 100/2)
        self.geometry(f"330x100+{positionRight}+{positionDown}")
        self.resizable(0, 0)
        # Mã admin
        self.label_admin_code = Label(self, text="Mã Admin", font=("Arial", 10))
        self.entry_admin_code = Entry(self, width = 22) 
        self.label_admin_code.grid(row=1, column=0,  padx=20 ,pady=10)
        self.entry_admin_code.grid(row=1, column=1, padx=20 ,pady=10)
        self.entry_admin_code.focus()

        self.button_admin_code = Button(self, text="Xác nhận", command=lambda:self.click_cf_code(), width=10)
        self.button_cancle = Button(self, text="Hủy bỏ", command=lambda:self.click_cancle(), width=10) 
        self.button_admin_code.place(x=20, y=50)
        self.button_cancle.place(x=180, y=50)
    
    # Sự kiện xác nhận mã admin
    def click_cf_code(self):
        admin_code = self.entry_admin_code.get().strip() 
        if not check_admin_code(admin_code):
          messagebox.showerror("Mã admin không hợp lệ", "Mã admin không đúng hoặc không tồn tại.")
        else:
          messagebox.showinfo("Mã admin hợp lệ", "Mã admin được chấp nhận.")
          self.destroy() 
          self.origin_frame.show()
    
    #Sự kiện thoát đăng ký
    def click_cancle(self):
        self.destroy() 
        self.origin_frame.var_isadmin.set(0)
        self.origin_frame.show()

# Cửa sổ đăng ký
class RegisterApplication(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.origin_frame = parent
        self.title("Đăng ký")
        positionRight = int(self.winfo_screenwidth()/2 - 400/2)
        positionDown = int(self.winfo_screenheight()/2 - 310/2)
        self.geometry(f"400x310+{positionRight}+{positionDown}")
        self.resizable(0, 0)

        # Cấu hình thành phần màn đăng ký

        # Họ tên
        self.label_name = Label(self, text="Họ tên", font=("Arial", 10))
        self.entry_name = Entry(self, width = 30) 
        self.label_name.grid(row=1, column=0, pady=10)
        self.entry_name.grid(row=1, column=1, pady=10)
        self.entry_name.focus()

        # Số điện thoại
        self.label_phone = Label(self, text="SĐT", font=("Arial", 10))
        self.entry_phone = Entry(self, width = 30) 
        self.label_phone.grid(row=2, column=0, pady=10)
        self.entry_phone.grid(row=2, column=1, pady=10)

        # Tài khoản
        self.label_user = Label(self, text="Tài khoản", font=("Arial", 10))
        self.entry_user = Entry(self, width = 30) 
        self.label_user.grid(row=3, column=0, pady=10, padx=20)
        self.entry_user.grid(row=3, column=1, pady=10)

        # Mật khẩu
        self.label_password = Label(self, text="Mật khẩu", font=("Arial", 10))
        self.entry_password = Entry(self, width = 30)
        self.label_password.grid(row=4, column=0, pady=10)
        self.entry_password.grid(row=4, column=1, pady=10)

        # Nhập lại mật khẩu
        self.label_re_password = Label(self, text="Nhập lại", font=("Arial", 10))
        self.entry_re_password = Entry(self, width = 30)
        self.label_re_password.grid(row=5, column=0, pady=10)
        self.entry_re_password.grid(row=5, column=1, pady=10)

        # Là admin
        self.var_isadmin = IntVar()
        self.label_isadmin= Label(self, text="Là Admin", font=("Arial", 10))
        self.label_isadmin.grid(row=6, column=0, pady=10)
        self.checkbox_isadmin = Checkbutton(self, variable=self.var_isadmin, command=self.click_isadmin).place(x=100, y=220)

        # Các button đăng ký và thoát
        self.button_register = Button(self, text="Đăng ký", command=lambda:self.click_cf_register(), width=10)
        self.button_cancle = Button(self, text="Hủy bỏ", command=lambda:self.click_cancle(), width=10) 
        self.button_register.place(x=20, y=260)
        self.button_cancle.place(x=270, y=260)

    def click_isadmin(self):
        if self.var_isadmin.get() == 1:
            admin_code_window = CheckAdmin(self)
            admin_code_window.wait_visibility()
            admin_code_window.grab_set()

    # Xử lí sự kiện khi bấm đăng ký
    def click_cf_register(self):
    
        acc = {'user_id':self.entry_user.get().strip(), 'user_pw':self.entry_password.get().strip(), 'user_name': self.entry_name.get().strip(), 'user_phone': self.entry_phone.get().strip()}
        if acc['user_id'] == "" or acc['user_pw'] == "" or acc['user_name'] == "" or acc['user_phone'] == "" or self.entry_re_password.get().strip() == "":
            messagebox.showinfo("Thông báo","Cần phải nhập đầy đủ thông tin.")
        else:
            if acc['user_pw'] != self.entry_re_password.get():
                messagebox.showinfo("Thông báo","Mật khẩu nhập lại không trùng.")
            else:
                if check_register(acc['user_id']): 
                    register_acc(acc) 
                    msgbox = messagebox.showinfo("Thông báo","Tài khoản được đăng ký thành công.")
                    if msgbox:
                        self.click_cancle()
                else:
                    messagebox.showinfo("Thông báo","Tài khoản đã được sử dụng.")
       
    #Sự kiện thoát đăng ký
    def click_cancle(self):
        self.destroy() 
        self.origin_frame.show()

    def show(self):
        self.update()
        self.deiconify()