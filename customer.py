class Customer:
    def __init__(
        self,
        customer_id,
        cccd,
        customer_name,
        phone="",
        email="",
        balance=0.0,
        status="active"
    ):
        self.customer_id = customer_id
        self.cccd = cccd
        self.customer_name = customer_name
        self.phone = phone
        self.email = email
        self.balance = float(balance)
        self.status = status

    def __str__(self):
        return (
            f"{self.customer_id} | {self.customer_name} | CCCD: {self.cccd} | "
            f"Phone: {self.phone} | Email: {self.email} | "
            f"Balance: {self.balance:,.0f} VND | Status: {self.status}"
        )
