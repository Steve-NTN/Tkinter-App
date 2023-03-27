from sqlalchemy import ( 
    MetaData, create_engine
)

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'nghia'
host = '127.0.0.1'
port = 3306
database = 'shop_tkinter'

engine = create_engine(
    url=f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)


meta = MetaData(bind=engine)
MetaData.reflect(meta)