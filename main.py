from customer_manager import CustomerManager

# Thành viên 2 thêm sau:
# from wallet_manager import WalletManager
# from transaction_manager import TransactionManager

# Thành viên 3 thêm sau:
# from expense_manager import ExpenseManager

# Thành viên 4 thêm sau:
# from report_manager import ReportManager

# Thành viên chatbot thêm sau:
# from ai_chatbot_manager import AIChatbotManager


def main():
    CustomerManager.initialize_database()

    while True:
        print("\n===== MOMO MINI APP =====")
        print("1. Quản lý khách hàng")
        print("2. Quản lý ví")
        print("3. Quản lý chi tiêu")
        print("4. Báo cáo - thống kê")
        print("5. Chatbot AI")
        print("6. Thoát")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            customer_menu()
        elif choice == "2":
            wallet_menu()
        elif choice == "3":
            expense_menu()
        elif choice == "4":
            report_menu()
        elif choice == "5":
            ai_chatbot_menu()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Lựa chọn không hợp lệ.")


def customer_menu():
    while True:
        print("\n===== CUSTOMER MANAGEMENT =====")
        print("1. Tìm / tạo khách hàng bằng CCCD")
        print("2. Xem toàn bộ khách hàng")
        print("3. Tìm khách hàng theo CCCD")
        print("4. Cập nhật thông tin khách hàng theo CCCD")
        print("5. Quay lại")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            CustomerManager.get_or_create_customer_by_cccd()

        elif choice == "2":
            CustomerManager.display_all_customers()

        elif choice == "3":
            cccd = input("Nhập CCCD: ").strip()
            customer = CustomerManager.find_customer_by_cccd(cccd)

            if customer is None:
                print("Không tìm thấy khách hàng.")
            else:
                print("\nThông tin khách hàng:")
                print(customer)

        elif choice == "4":
            cccd = input("Nhập CCCD khách hàng cần cập nhật: ").strip()
            customer = CustomerManager.find_customer_by_cccd(cccd)

            if customer is None:
                print("Không tìm thấy khách hàng.")
            else:
                print("\nĐể trống nếu không muốn đổi.")
                new_name = input("Tên mới: ")
                new_phone = input("SĐT mới: ")
                new_email = input("Email mới: ")
                new_status = input("Trạng thái mới (active/locked): ")

                updated = CustomerManager.update_customer_by_cccd(
                    cccd=cccd,
                    new_name=new_name if new_name.strip() else None,
                    new_phone=new_phone,
                    new_email=new_email,
                    new_status=new_status if new_status.strip() else None
                )

                if updated:
                    print("Cập nhật thành công.")
                else:
                    print("Cập nhật thất bại.")

        elif choice == "5":
            break

        else:
            print("Lựa chọn không hợp lệ.")


def wallet_menu():
    pass


def expense_menu():
    pass


def report_menu():
    pass


def ai_chatbot_menu():
    pass


if __name__ == "__main__":
    main()