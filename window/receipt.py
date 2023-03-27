from tkinter import *
from turtle import width
from fpdf import FPDF
from prettytable import PrettyTable 
from datetime import datetime, date

class Reciept(Toplevel):
    def __init__(self):
    # def __init__(self, parent):
        super().__init__()
        # super().__init__(parent)
        # self.original_frame = parent
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 100/2)
        self.geometry(f"300x500+{positionRight}+{positionDown}")

        self.big_title = Label(self, text='---------RECIEPT----------')
        self.big_title.pack()
        self.heading = Label(self, text='PRICE\tQTY\tTOTAL')
        self.heading.pack()

        self.export_button = Button(self, text="Xuất file", command=self.export_file).place(x=100, y=160)
        self.cancle_button = Button(self, text="Hủy bỏ", command=self.click_cancle).place(x=200, y=160)

        self.export_file()

    def click_cancle(self):
        self.destroy()
        # self.original_frame.show()

    def export_file(self):
        pdf = FPDF('P', 'mm', (80, 150))
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'static/font/DejaVuSansCondensed.ttf', uni=True)
        # pdf.add_font('DejaVu', '', 'static/font/DejaVuSansCondensed-Bold.ttf', uni=True)

        pdf.set_font("DejaVu", "", 5)
        pdf.cell(0, 0, "*"*(80), 0, 1, "C")

        pdf.set_font("DejaVu", "", 10)
        pdf.cell(0, 5, u"HÓA ĐƠN", 0, 1, "C")

        pdf.set_font("DejaVu", "", 5)
        now = datetime.now()
        current_date, current_time = now.strftime("%d/%m/%Y %H:%M:%S").split(" ")
        pdf.cell(0, 2, u"Ngày in hóa đơn: {}".format(current_date), 0, 1, "C")

        pdf.cell(0, 2, u"Giờ in hóa đơn: {}".format(current_time), 0, 1, "C")

        pdf.set_font("DejaVu", "", 5)
        pdf.cell(0, 5, "*"*80, 0, 1, "C")


        # items_in_bill = [
        #     self.original_frame.tree_main.item(item) for item in self.original_frame.tree_main.get_children()
        # ]

        effective_page_width = pdf.w - 2*pdf.l_margin

        header = [
            {"text": "STT", "width_rate": 0.1}, 
            {"text": "Sản phẩm", "width_rate": 0.3}, 
            {"text": "Giá", "width_rate": 0.2},
            {"text": "Số lượng", "width_rate": 0.2},
            {"text": "Thành tiền", "width_rate": 0.2}
        ]
        header_line = self.format_line(pdf, effective_page_width, header)
        pdf.cell(0, 2, header_line, 0, 1, "C")

        item_test = [
            {"values" : ['1', 'Gạo', '130,000', 4, '520,000']},
            {"values" : ['2', 'Nước mắm Nước mắm Nước mắm Nước mắm', '15,000', 6, '90,000']}
        ]

        width_rate = [0.1, 0.3, 0.2, 0.2, 0.2]

        for item in item_test:
            item_line = self.format_line(pdf, effective_page_width, [
                {
                    "text": str(part), "width_rate": width_rate[index]
                }
                for index, part in enumerate(item.get("values"))
            ])
            pdf.cell(0, 2, item_line, 0, 1, "C")


        return pdf.output("test.pdf", "F")

    def insert_items_to_pdf(self, pdf, items):
        
        # Specify the Column Names while initializing the Table 
        myTable = PrettyTable(["Student Name", "Class", "Section", "Percentage"]) 
        myTable.max_width = 20
            
        # Add rows
        for item in items:
            myTable.add_row(item) 

        string_x = str(myTable).split('\n')
        pdf.add_font("Arial", "", "static/font/arial.ttf", uni=True)
        pdf.set_font('Arial', '', 5)
        for index, item in enumerate(string_x):
            pdf.cell(200, 5, item, ln= 1)
            
        return pdf

    def format_line(self, pdf, page_width, parts):
        line = ""
        for part in parts:
            max_width = page_width * part["width_rate"]
            part_width = pdf.get_string_width(part["text"])

            test = ""
            if part_width > max_width:
                word_in_part = part["text"].split(" ")
                for w in word_in_part:
                    if pdf.get_string_width(test) > max_width:
                        # test += "\n"
                        pdf.cell(0, 2, "", 0, 1, "C")
                    
                    test += w + " "
            else:
                test = part["text"]

            spacing_width = max_width - part_width

            line += f"{test}{' '*int(spacing_width/ pdf.get_string_width(' '))}"
        # line += "\n"
        return line
