import sqlite3
from pathlib import Path
from customer import Customer


class CustomerManager:
    DB_NAME = "momo_mini.db"

    @staticmethod
    def get_database_path():
        return Path(__file__).resolve().parent / CustomerManager.DB_NAME

    @staticmethod
    def get_connection():
        db_path = CustomerManager.get_database_path()
        return sqlite3.connect(db_path)

    @staticmethod
    def initialize_database():
        conn = CustomerManager.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                cccd TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                balance REAL DEFAULT 0,
                status TEXT DEFAULT 'active'
            )
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def generate_next_customer_id():
        CustomerManager.initialize_database()

        conn = CustomerManager.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_id
            FROM customers
            WHERE customer_id LIKE 'C%'
        """)

        rows = cursor.fetchall()
        conn.close()

        max_id = 0
        for row in rows:
            customer_id = row[0]
            number_part = customer_id[1:] if customer_id.startswith("C") else ""
            if number_part.isdigit():
                max_id = max(max_id, int(number_part))

        return f"C{max_id + 1:03d}"

    @staticmethod
    def find_customer_by_cccd(cccd):
        CustomerManager.initialize_database()

        conn = CustomerManager.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_id, cccd, customer_name, phone, email, balance, status
            FROM customers
            WHERE cccd = ?
        """, (cccd,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return Customer(*row)

    @staticmethod
    def find_customer_by_id(customer_id):
        CustomerManager.initialize_database()

        conn = CustomerManager.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_id, cccd, customer_name, phone, email, balance, status
            FROM customers
            WHERE customer_id = ?
        """, (customer_id,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return Customer(*row)

    @staticmethod
    def create_customer(cccd, customer_name, phone="", email=""):
        CustomerManager.initialize_database()

        existing_customer = CustomerManager.find_customer_by_cccd(cccd)
        if existing_customer is not None:
            return existing_customer, False

        new_customer_id = CustomerManager.generate_next_customer_id()

        conn = CustomerManager.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO customers (
                    customer_id, cccd, customer_name, phone, email, balance, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                new_customer_id,
                cccd,
                customer_name,
                phone,
                email,
                0.0,
                "active"
            ))

            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            existing_customer = CustomerManager.find_customer_by_cccd(cccd)
            if existing_customer is not None:
                return existing_customer, False
            raise

        conn.close()
        return CustomerManager.find_customer_by_id(new_customer_id), True

    @staticmethod
    def get_or_create_customer_by_cccd():
        cccd = input("Nhập CCCD: ").strip()
        while not cccd:
            print("CCCD không được để trống.")
            cccd = input("Nhập CCCD: ").strip()

        existing_customer = CustomerManager.find_customer_by_cccd(cccd)
        if existing_customer is not None:
            print("\nKhách hàng đã tồn tại:")
            print(existing_customer)
            return existing_customer

        print("\nCCCD chưa tồn tại. Tạo khách hàng mới.")
        customer_name = input("Nhập tên khách hàng: ").strip()
        while not customer_name:
            print("Tên khách hàng không được để trống.")
            customer_name = input("Nhập tên khách hàng: ").strip()

        phone = input("Nhập số điện thoại: ").strip()
        email = input("Nhập email: ").strip()

        new_customer, _ = CustomerManager.create_customer(
            cccd=cccd,
            customer_name=customer_name,
            phone=phone,
            email=email
        )

        print("\nTạo khách hàng thành công:")
        print(new_customer)
        return new_customer

    @staticmethod
    def display_all_customers():
        CustomerManager.initialize_database()

        conn = CustomerManager.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_id, cccd, customer_name, phone, email, balance, status
            FROM customers
            ORDER BY customer_id
        """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("Chưa có khách hàng nào.")
            return

        print("\n===== DANH SÁCH KHÁCH HÀNG =====")
        for index, row in enumerate(rows, start=1):
            customer = Customer(*row)
            print(f"{index}. {customer}")

    @staticmethod
    def update_customer_by_cccd(cccd, new_name=None, new_phone=None, new_email=None, new_status=None):
        CustomerManager.initialize_database()

        customer = CustomerManager.find_customer_by_cccd(cccd)
        if customer is None:
            return False

        updated_name = new_name.strip() if new_name is not None and new_name.strip() else customer.customer_name
        updated_phone = new_phone.strip() if new_phone is not None else customer.phone
        updated_email = new_email.strip() if new_email is not None else customer.email
        updated_status = new_status.strip() if new_status is not None and new_status.strip() else customer.status

        conn = CustomerManager.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE customers
            SET customer_name = ?, phone = ?, email = ?, status = ?
            WHERE cccd = ?
        """, (
            updated_name,
            updated_phone,
            updated_email,
            updated_status,
            cccd
        ))

        conn.commit()
        conn.close()
        return True

    @staticmethod
    def update_balance(customer_id, amount_change):
        CustomerManager.initialize_database()

        customer = CustomerManager.find_customer_by_id(customer_id)
        if customer is None:
            return False, "Không tìm thấy khách hàng."

        new_balance = customer.balance + float(amount_change)
        if new_balance < 0:
            return False, "Số dư không đủ."

        conn = CustomerManager.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE customers
            SET balance = ?
            WHERE customer_id = ?
        """, (new_balance, customer_id))

        conn.commit()
        conn.close()

        return True, new_balance
