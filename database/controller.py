# import pymysql.cursors
# import mariadb
import pymysql
import sys

try:

    connection = pymysql.connect(host='localhost',
                                 port=3030,
                                 user='root',
                                 password='',
                                 db='shop_barcode'
                                 )
    # connection = mariadb.connect(
    #     user="root",
    #     password="nghia",
    #     host="localhost",
    #     port=3306,
    #     database="shop_tkinter"
    # )

except pymysql.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


# Lấy dữ liệu đăng nhập
# Trả ra True nếu đăng nhập thành công và False nếu thất bại
def can_login(user_name, user_password):
    cursor = connection.cursor()  # Kết nối CSDL
    query = "SELECT * FROM `login` WHERE user_id = %s AND user_pw = %s"
    val = (user_name, user_password)
    cursor.execute(query, val)
    return True if len(cursor.fetchall()) > 0 else False

# Trả ra tên người dùng khi đăng nhập


def get_name_user(user_id):
    cursor = connection.cursor()  # Kết nối CSDL
    query = "SELECT login.user_name FROM `login` WHERE user_id = %s"
    val = (user_id)
    cursor.execute(query, val)
    name_user = cursor.fetchall()
    return name_user[0][0]

# Kiểm tra mã admin đúng không


def check_admin_code(admin_code):
    list_code = ["abcxyz"]
    # cursor = connection.cursor()
    # query = "SELECT * FROM `admin_code` WHERE admin_code = '{}'".format(str(admin_code)))
    # cursor.execute(query)
    return True if admin_code in list_code else False


# Kiểm tra tài khoản đã có hay không để tiến hành đăng ký
def check_register(user_id):
    cursor = connection.cursor()
    query = "SELECT * FROM `login` WHERE user_id = '{}'".format(str(user_id))
    cursor.execute(query)
    return True if len(cursor.fetchall()) < 1 else False

# Đăng ký thông tin tài khoản người dùng


def register_acc(account):
    cursor = connection.cursor()
    query = "INSERT INTO `login` (`user_id`, `user_pw`, `user_name`, `user_phone`, `is_admin`) VALUES (%s, %s, %s, %s, 0)"
    val = (account['user_id'], account['user_pw'],
           account['user_name'], account['user_phone'])
    cursor.execute(query, val)
    connection.commit()


# Hiển thị tất cả trong mục products
def getProducts():
    cursor = connection.cursor()
    query = "SELECT * FROM `products`"
    cursor.execute(query)
    return cursor.fetchall()


# Kiểm tra mã sản phẩm tồn tại không
def checkID(id):
    cursor = connection.cursor()
    sql = "SELECT * FROM products WHERE products.product_id = " + id
    cursor.execute(sql)
    return True if cursor.fetchall() != () else False

# Lấy ra tên và giá sp theo id


def getNamePrice(id):
    cursor = connection.cursor()
    sql = "SELECT products.product_name, products.product_price, products.product_description FROM products WHERE products.product_id = " + id
    cursor.execute(sql)
    a = cursor.fetchall()
    if a:
        return [a[0][0], a[0][1], a[0][2]]
    return None

# Tổng tiền


def getTotal(index):
    cursor = connection.cursor()
    sql = "SELECT products.price * bill.number_of_prod FROM `bill` JOIN products WHERE products.id = bill.id_pro AND bill.id = %s"
    val = (index)
    cursor.execute(sql, val)
    return sum([i[0] for i in cursor.fetchall()])

# Thêm sản phẩm


def insertProduct(product_id, product_name, product_price, product_description):
    cursor = connection.cursor()
    sql = "INSERT INTO `products`(`product_id`, `product_name`, `product_price`, `product_description`) VALUES (%s,%s,%s, %s)"
    val = (product_id, product_name, product_price, product_description)
    cursor.execute(sql, val)
    connection.commit()

# Xóa sản phẩm


def deleteProduct(id):
    cursor = connection.cursor()
    sql = "DELETE FROM `products` WHERE product_id = " + id
    cursor.execute(sql)
    connection.commit()

# Sửa sản phẩm


def updateProduct(id, name, price):
    cursor = connection.cursor()
    sql = "UPDATE `products` SET `product_id`=%s,`product_name`=%s,`product_price`=%s WHERE `product_id`=%s"
    val = (id, name, price, id)
    cursor.execute(sql, val)
    connection.commit()
