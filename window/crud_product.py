from tkinter import *
from tkinter import ttk, messagebox
from database.controller import *

class AddProduct(Toplevel):
    def __init__(self, parent, arg=None):
        super().__init__(parent)
        # Cửa số nhập thông tin thêm đồ
        self.original_frame = parent
        positionRight = int(self.winfo_screenwidth()/2 - 320/2)
        positionDown = int(self.winfo_screenheight()/2 - 230/2)
        self.geometry(f"320x230+{positionRight}+{positionDown}")
        self.resizable(0, 0)
        # Phần "Mã SP"
        self.title("Thêm đồ")
        self.addItemID = Label(self, text="Mã sản phẩm: *").grid(row=0, column=0, padx=10, pady=10)
        self.addId = StringVar()
        self.add_id_entry = Entry(self, textvariable=self.addId)
        self.add_id_entry.grid(row=0, column=1)
        # Phần "Tên SP"
        self.addItemName = Label(self, text="Tên sản phẩm: ").grid(row=1, column=0, padx=10, pady=10)
        self.addName = StringVar()
        self.add_name_entry = Entry(self, textvariable=self.addName)
        self.add_name_entry.grid(row=1, column=1)
        if arg:
            self.add_id_entry.insert(0, arg)
            self.add_name_entry.focus()
        else:
            self.add_id_entry.focus()
        # Phần "Mã Giá SP"
        self.addItemPrice = Label(self, text="Giá sản phẩm: *").grid(row=2, column=0, padx=10, pady=10)
        self.addPrice = StringVar()
        reg = self.register(self.callback)
        self.addPriceEntry = Entry(self, textvariable=self.addPrice, validate ="key", validatecommand=(reg, '%S'))
        self.addPriceEntry.grid(row=2, column=1)

        # Phần "Mô tả"
        self.addItemDesciption = Label(self, text="Mô tả: ").grid(row=3, column=0, padx=10, pady=10)
        self.addDesciption = StringVar()
        self.addDesciptionEntry = Entry(self, textvariable=self.addDesciption)
        self.addDesciptionEntry.grid(row=3, column=1)
        # OK
        self.addButtonCf = Button(self, text="Xác nhận", command=self.clickButtonAddCf)
        self.addButtonCf.place(x=50, y=180)
        self.cancle = Button(self, text="Hủy bỏ", command=self.click_cancle)
        self.cancle.place(x=200, y=180)

    def callback(self, input):
        return input.isdigit()

    # Kiểm tra khi thêm mới sản phẩm
    def checkAddProduct(self):
        try:
            id = self.add_id_entry.get().strip() 
            price = self.addPriceEntry.get().strip()

            if id != "" and price != "" :
                if checkID(self.add_id_entry.get()): 
                    return True
                else :
                    messagebox.showwarning("Thông báo", "Mã sp đã bị trùng")
            else:
                messagebox.showerror("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin sản phẩm")
        except ValueError:
            return False
        return False

    def click_cancle(self):
        self.destroy()
        self.original_frame.show()

    # Xử lí sự kiện khi "Xác nhận thêm mới SP"
    def clickButtonAddCf(self):
        if self.checkAddProduct():
            insertProduct(self.add_id_entry.get(), self.add_name_entry.get(), int(self.addPriceEntry.get()), self.addDesciptionEntry.get())
            messagebox.showinfo("Thông báo", "Bạn đã thêm sản phẩm thành công!")
            self.destroy()

# Cửa sổ (Xóa đồ)
class RemoveProduct(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 100/2)
        self.geometry(f"300x100+{positionRight}+{positionDown}")
        self.register(0, 0)
        self.title("Xóa đồ")
        # Phần "Mã SP"
        self.deleteLabelID = Label(self, text="Mã sản phẩm: *").grid(row=0, column=0, padx=10, pady=10)
        self.deleteId = StringVar()
        self.delete_id_entry = Entry(self, textvariable=self.deleteId)
        self.delete_id_entry.grid(row=0, column=1)
        self.delete_id_entry.focus()
        # OK
        self.deleteButtonCf = Button(self, text="Xác nhận", command=self.deleteProductWithID)
        self.deleteButtonCf.place(x=40, y=50)
        self.cancle = Button(self, text="Hủy bỏ", command=self.click_cancle)
        self.cancle.place(x=180, y=50)

    def click_cancle(self):
        self.destroy()
        self.original_frame.show()

    def deleteProductWithID(self): #
        if not checkID(self.delete_id_entry.get()): #
            messagebox.showwarning("Thông báo", "Chưa nhập hoặc mã sản phẩm không tồn tại.")
        else:
            i = self.delete_id_entry.get()
            n, p, d = getNamePrice(i) #
            m = messagebox.askokcancel("Cảnh báo", f"Bạn có muốn xóa sản phẩm (Mã: {i} | Tên: {n} | Giá: {p}) không?")
            if m: 
                deleteProduct(i) #
                messagebox.showinfo("Thông báo", "Sản phẩm đã được xóa.")
            self.destroy()


# Cửa sổ "Sửa thông tin SP"
class EditProduct(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 100/2)
        self.geometry(f"300x100+{positionRight}+{positionDown}")
        self.register(0, 0)
        self.title("Sửa thông tin sản phẩm")
        # Phần mã sản phẩm
        self.UpdateLabelID = Label(self, text="Mã sản phẩm: *").grid(row=0, column=0, padx=10, pady=10)
        self.updateId = StringVar()
        reg = self.register(self.callback)
        self.update_id_entry = Entry(self, textvariable=self.updateId, validate ="key", validatecommand=(reg, '%S'))
        self.update_id_entry.grid(row=0, column=1)
        self.update_id_entry.focus()
        # OK
        self.updateButtonCf = Button(self, text="Xác nhận", command=self.updateProductWithID)
        self.updateButtonCf.place(x=40, y=50)
        self.cancle = Button(self, text="Hủy bỏ", command=self.click_cancle)
        self.cancle.place(x=180, y=50)

    def callback(self, input):
        return input.isdigit()

    def click_cancle(self):
        self.destroy()
        self.original_frame.show()

    # Xử lí sự kiện trong mục "Sửa SP"
    def updateProductWithID(self): #
        if not checkID(self.update_id_entry.get()): #
            messagebox.showwarning("Thông báo", "Chưa nhập hoặc mã sản phẩm không tồn tại.")
        else:
            i = self.update_id_entry.get()
            n, p, d = getNamePrice(i)
            positionRight = int(self.winfo_screenwidth()/2 - 330/2)
            positionDown = int(self.winfo_screenheight()/2 - 200/2)
            self.geometry(f"330x200+{positionRight}+{positionDown}")

            #Phần tên SP
            self.updateItemName = Label(self, text="Tên sản phẩm: *").grid(row=1, column=0, padx=10, pady=10)
            self.updateName = StringVar()
            self.updateNameEntry = Entry(self, textvariable=self.updateName)
            self.updateNameEntry.insert(0, f"{n}")
            self.updateNameEntry.grid(row=1, column=1)
            # Phần giá
            self.updateItemPrice = Label(self, text="Giá sản phẩm: *").grid(row=2, column=0, padx=10, pady=10)
            self.updatePrice = StringVar()
            self.updatePriceEntry = Entry(self, textvariable=self.updatePrice)
            self.updatePriceEntry.insert(0, "{:,}".format(p))
            self.updatePriceEntry.grid(row=2, column=1)
            # Phần mô tả
            self.updateItemPrice = Label(self, text="Mô tả sản phẩm: *").grid(row=3, column=0, padx=10, pady=10)
            self.update_des = StringVar()
            self.update_des_entry = Entry(self, textvariable=self.update_des)
            self.update_des_entry.insert(0, f"{d}")
            self.update_des_entry.grid(row=3, column=1)
            self.updateButtonCf.destroy()
            self.cancle.destroy()
            self.updateButtonCf = Button(self, text="Xác nhận", command=self.updateProductCf)
            self.updateButtonCf.place(x=50, y=160)
            self.cancle = Button(self, text="Hủy bỏ", command=self.click_cancle)
            self.cancle.place(x=200, y=160)
            
    #Xác nhận lại xem có muốn đổi thông tin sản phẩm hay không
    def updateProductCf(self): 
        i = self.update_id_entry.get()
        n, p, d = getNamePrice(i) 
        nn = self.updateNameEntry.get()
        pp = self.updatePriceEntry.get()
        m = messagebox.askokcancel("Cảnh báo", f"Bạn có muốn thay đổi thông tin sản phẩm từ *Tên: {n} | Giá: {int(p)})* thành *Tên: {nn} | Giá: {pp}* không?")
        if m:
            updateProduct(i, nn, int(pp.replace(',', ''))) 
            messagebox.showinfo("Thông báo", "Thông tin sản phẩm đã được cập nhập.")

class ListProduct(Toplevel):
    def __init__(self, parent, products):
        super().__init__(parent)
        self.original_frame = parent
        positionRight = int(self.winfo_screenwidth()/2 - 620/2)
        positionDown = int(self.winfo_screenheight()/2 - 500/2)
        self.geometry(f"620x500+{positionRight}+{positionDown}")
        self.resizable(0, 0)
        self.title("Danh sách sản phẩm")

        self.index = 1
        
        # cửa sổ xem thông tin sản phẩm 
        self.tree_product = ttk.Treeview(self, columns=("1", "2", "3","4"), height=20)
        self.tree_product.heading("#0", text="STT")
        self.tree_product.column("#0", width = 50)
        self.tree_product.heading("1", text = "ID")
        self.tree_product.column("1", anchor="center", minwidth=50, width=130)
        self.tree_product.heading("2", text = "Tên")
        self.tree_product.column("2", anchor="center", minwidth=100, width=150)
        self.tree_product.heading("3", text = "Giá")
        self.tree_product.column("3", anchor="center", minwidth=100, width=100)
        self.tree_product.heading("4", text = "Mô tả sản phẩm")
        self.tree_product.column("4", anchor="center", minwidth=150, width=150)
        self.tree_product.grid(row=1, column=0, columnspan=3, padx= 10)
        
         # ScrollBar
        self.scrollProduct = Scrollbar(self, orient="vertical",command=self.tree_product.yview)
        self.scrollProduct.grid(row=1, column=4, sticky="NSE")
        self.tree_product.configure(yscrollcommand=self.scrollProduct.set)
        # Button
        self.button_load = Button(self, text="Tìm kiếm", command=self.find_product, width=15, height=2)
        self.button_load.place(x=100, y=440)
        self.cancle = Button(self, text="Hủy bỏ", command=self.click_cancle, width=15, height=2)
        self.cancle.place(x=370, y=440)

        listItem = self.tree_product.get_children()
        for i in listItem:
            self.tree_product.delete(i)
        for product in products: 
            self.tree_product.insert("", "end", text=self.index, values=(product[0], product[1], "{:,}".format(product[2]), product[3]))
            self.index += 1

       #Sự kiện khi click vào "Tải lại" trong mục "Danh sách sản phẩm"
    def find_product(self):
        messagebox.showinfo("Thông báo", "Chức năng tìm kiếm đang được nâng cấp.")
        pass
        

    def click_cancle(self):
        self.destroy()
        self.original_frame.show()


class CrudProductApplication(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        positionRight = int(self.winfo_screenwidth()/2 - 650/2)
        positionDown = int(self.winfo_screenheight()/2 - 70/2)
        self.geometry(f"650x70+{positionRight}+{positionDown}")
        self.title("Cài đặt sản phẩm")
        self.resizable(0, 0)
        self.addItem = Button(self, text="Thêm", width=15, height=2, command=self.add_product).grid(row=0, column=0, padx=10, pady=10)
        self.addItem = Button(self, text = "Xóa", width=15, height=2, command=self.remove_product).grid(row=0, column=1, pady=10)
        self.addItem = Button(self, text = "Sửa", width=15, height=2, command=self.edit_product).grid(row=0, column=2, padx=10, pady=10)
        self.addItem = Button(self, text = "D.sách s.phẩm", width=15, height=2, command=self.list_product).grid(row=0, column=3, pady=10)
    
    def add_product(self):
        add_window = AddProduct(self)
        add_window.grab_set()

    def remove_product(self):
        remove_window = RemoveProduct(self)
        remove_window.grab_set()

    def edit_product(self):
        edit_window = EditProduct(self)
        edit_window.grab_set()

    def list_product(self):
        products = getProducts()
        products_window = ListProduct(self, products)
        products_window.grab_set()

    def show(self):
        self.update()
        self.deiconify()


    


   
            

