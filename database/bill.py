import random
import string
from datetime import datetime
from sqlalchemy import insert
from .models import meta

# create bill
def create_bill(bill_file, creater, customer=None):

    random_id = "".join(random.choice(string.digits + string.ascii_lowercase) for _ in range(10))
    new_bill = insert(meta.tables["bill"])
    new_bill = new_bill.values({
        "bill_id": random_id,
        "create_time": datetime.now(),
        "bill_file": bill_file,
        "create_by": creater,
        "custermer": customer
    })
    new_bill.execute()