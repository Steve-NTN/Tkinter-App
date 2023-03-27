from tkinter import *
from tkinter import ttk, messagebox
from database.controller import getNamePrice, checkID, get_name_user
from .crud_product import CrudProductApplication, AddProduct
import sys
from .receipt import Reciept

class AddMultiWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.title("Thêm sỉ sản phẩm")
        positionRight = int(self.winfo_screenwidth()/2 - 320/2)
        positionDown = int(self.winfo_screenheight()/2 - 180/2)
        self.geometry(f"320x180+{positionRight}+{positionDown}")
        self.resizable(0, 0)

        # Phần "Tên SP"
        self.add_item_name = Label(self, text="Tên sản phẩm: ").grid(row=1, column=0, padx=10, pady=10)
        self.addName = StringVar()
        self.add_name_entry = Entry(self, textvariable=self.addName)
        self.add_name_entry.grid(row=1, column=1)
        self.add_name_entry.focus()

        # Phần "Mã Giá SP"
        self.addItemPrice = Label(self, text="Giá sỉ: *").grid(row=2, column=0, padx=10, pady=10)
        self.addPrice = StringVar()
        reg = self.register(self.callback)
        self.add_price_entry = Entry(self, textvariable=self.addPrice, validate ="key", validatecommand=(reg, '%S'))
        self.add_price_entry.grid(row=2, column=1)

        # Phần "Mô tả"
        self.qlt_multi_label = Label(self, text="Số lượng: *").grid(row=3, column=0, padx=10, pady=10)
        self.qlt_multi = StringVar()
        self.qlt_multi_entry = Spinbox(self, from_=1, to=200, textvariable=self.qlt_multi, width=19)
        self.qlt_multi_entry.grid(row=3, column=1)
        # OK
        self.addButtonCf = Button(self, text="Xác nhận", command=self.click_add_multi)
        self.addButtonCf.place(x=50, y=140)
        self.cancle = Button(self, text="Hủy bỏ", command=self.click_cancle)
        self.cancle.place(x=200, y=140)

    def callback(self, input):
        return input.isdigit()

    def click_add_multi(self):
        n = self.add_name_entry.get().strip()
        p = self.add_price_entry.get().strip()
        q = self.qlt_multi_entry.get().strip()

        # Kiểm tra "nhập mã + số lượng" khi thêm đồ vào hóa đơn
        if n == "" or p == "" or q == "":
            messagebox.showerror("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin sỉ.")
        else:
            self.original_frame.sum.delete(0, END)
            self.original_frame.total += int(q)*int(p)
            self.original_frame.tree_main.insert("", "end", text=self.original_frame.indexPro, values=(n,"{:,}".format(int(p))
                , q, "{:,}".format(int(p)*int(q))))
            self.original_frame.sum.insert(0, "{:,}".format(int(self.original_frame.total)))
            self.original_frame.indexPro += 1


    def click_cancle(self):
        self.destroy()
        self.original_frame.show()

#Xây dựng MainApplication
class MainApplication(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.total, self.indexPro = 0, 1 
        self.title("Tính tiền")
        self.resizable(0, 0)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        positionRight = int(self.winfo_screenwidth()/2 - 720/2)
        positionDown = int(self.winfo_screenheight()/2 - 700/2)
        self.geometry(f"720x700+{positionRight}+{positionDown}")

        self.text_main = Label(self, text="Hóa Đơn", font=("Arial Bold", 30))
        self.text_main.grid(row=0, column=0, columnspan=3, pady=10)
    
        # Giao diện chính hóa đơn
        self.tree_main = ttk.Treeview(self , columns=("1", "2", "3","4"), height=20)
        self.tree_main.heading("#0", text="STT")
        self.tree_main.column("#0", width = 30)
        self.tree_main.heading("1", text = "Tên")
        self.tree_main.column("1", anchor="center", minwidth=150, width=250)
        self.tree_main.heading("2", text = "Giá")
        self.tree_main.column("2", anchor="center", minwidth=100, width=100)
        self.tree_main.heading("3", text = "Số lượng")
        self.tree_main.column("3", anchor="center", minwidth=100, width=100)
        self.tree_main.heading("4", text = "Thành tiền")
        self.tree_main.column("4", anchor="center", minwidth=150, width=180)
        self.tree_main.grid(row=1, column=0, columnspan=3, padx= 25)
        
        # ScrollBar
        self.scrollBar = Scrollbar(self, orient="vertical",command=self.tree_main.yview)
        self.scrollBar.grid(row=1, column=2, sticky="NSE")
        self.tree_main.configure(yscrollcommand=self.scrollBar.set)
        
        # Text
        self.pressID = Label(self, text="Nhập mã: *").place(x=20, y=510)
        self.pressQlt = Label(self, text="Nhập số lượng: *").place(x=20, y=550)
    

        self.id_pro = StringVar()
        self.entry_id = Entry(self, textvariable=self.id_pro)
        self.entry_id.focus()
        self.entry_id.place(x=140, y=510)
        self.qlt = StringVar()
        reg = self.register(self.callback)
        self.entry_qlt = Spinbox(self, from_=1, to=200, textvariable=self.qlt, width=19, validate ="key", validatecommand=(reg, '%S'))
        self.entry_qlt.place(x=140, y=550)


        # Button
        self.button_logout = Button(self, text="Đăng xuất", command=self.click_logout, width=15, height=2).place(x=340, y=610)
        self.button_add = Button(self, text="Thêm lẻ", command=self.click_add, width=8, height=2).place(x=20, y=610)
        self.button_add_multi = Button(self, text="Sỉ", command=self.click_add_multi, width=3, height=2).place(x=115, y=610)
        self.button_del = Button(self, text="Xóa đồ", command=self.deleteProduct, width=15, height=2).place(x=180, y=610)
        self.button_setting = Button(self, text="Cài đặt", command=self.newWindow, height=5, width=20).place(x=510, y=580)
        self.button_back = Button(self, text="Tạo mới", command=self.refresh, width=5, height=2).place(x=320, y=510)
        self.button_print_bill = Button(self, text="In hóa đơn", command=self.print_bill, width=5, height=2).place(x=350, y=510)
        
        # Tổng tiền
        self.labelSum = Label(self, text="Tổng tiền cần thanh toán: *").place(x=500, y=510)
        self.sum = Entry(self, width = 25)
        self.sum.place(x=490, y=530)
        self.sum.bind("<Key>", lambda e: "break")
        self.sum.insert(0, "0")
        
        
    def callback(self, input):
        return input.isdigit()

    def on_closing(self):
        msgbox = messagebox.askokcancel("Cảnh báo", "Bạn có muốn đóng ứng dụng không?")
        if msgbox:
            sys.exit()

    # Click ra màn đăng nhập
    def click_logout(self):
        msgbox = messagebox.askokcancel("Cảnh báo", f"Bạn có muốn đăng xuất tài khoản {self.original_frame.entry_user.get()} không?")
        if msgbox:
            self.destroy()
            self.original_frame.show()

    # Click thêm đồ sỉ
    def click_add_multi(self):
        add_multi = AddMultiWindow(self)
        add_multi.grab_set()

    # Click thêm đồ lẻ
    def click_add(self):
        i = self.id_pro.get().strip()
        q = self.qlt.get().strip()

        # Kiểm tra "nhập mã + số lượng" khi thêm đồ vào hóa đơn
        if i == "" or q == "":
            messagebox.showerror("Thiếu thông tin", "Vui lòng nhập đầy đủ mã sản phẩm và số lượng.")
        else:
            if not checkID(i):
                self.messageToAdd()
            else: 
                self.sum.delete(0, END)
                name_price = getNamePrice(i)
                if not name_price:
                    self.messageToAdd()
                    return
                self.total += int(q)*name_price[1] 
                self.tree_main.insert("", "end", text=self.indexPro, values=(getNamePrice(i)[0], 
                                    "{:,}".format(getNamePrice(i)[1]), q, "{:,}".format(int(q)*getNamePrice(i)[1])))

                self.sum.insert(0, "{:,}".format(int(self.total)))
                self.indexPro += 1
                self.deleteInput() 
                
    # Thông báo sản phẩm không tồn tại trong csdl khi "thêm đồ" 
    def messageToAdd(self):
        m = messagebox.askokcancel("Thông báo","Mã sản phẩm chưa có. Thêm vào?")
        if m: 
            add_window = AddProduct(parent=self, arg=self.entry_id.get())
            add_window.focus_get()

    # tông tiền của hóa đơn
    def getSum(self):
        self.sum.delete(0, END)
        self.sum.insert(0, "{:,}".format(int(self.total)))

    # Xóa input "Nhập mã + số lượng " khi bấm vào thêm đồ thành công
    def deleteInput(self):
        self.entry_id.delete(0, END)
        self.entry_qlt.delete(0, END)
        self.entry_qlt.insert(0, 1)

    # Xử lí sự kiện khi click vào "Tạo mới"   
    def refresh(self):     
        listItem = self.tree_main.get_children()
        for i in listItem:
            self.tree_main.delete(i)
        self.total = 0
        self.sum.delete(0, END)
        self.sum.insert(0, 0)
        self.indexPro = 1

    # Xử lí sự kiện khi click vào "In hoa đơn"   
    def print_bill(self):     
        m = messagebox.askokcancel("Thông báo","Bạn có muốn xuất hóa đơn không?")
        if m: 
            reciept = Reciept(self)
            reciept.grab_set()

    # Sự kiện khi click xóa sản phẩm
    def deleteProduct(self): #
        select = self.tree_main.selection()
        if select != ():
            f = self.tree_main.focus()
            self.total -= int(self.tree_main.item(f)['values'][3].replace(',', ''))
            self.tree_main.delete(select)
            self.getSum()
        else:
            messagebox.showerror("Chưa chọn sản phẩm", "Vui lòng chọn vào sản phẩm muốn xóa.")

    # Sự kiện khi click vào cài đặt
    def newWindow(self):
        crud_product = CrudProductApplication(self)
        crud_product.grab_set()

    def show(self):
        self.update()
        self.deiconify()