import mysql.connector as sql
import pandas as pd

"""
function definitions start here
"""
def create_database():
    try:
        conn = sql.connect(host="localhost", user="root", passwd="Shree123")
        c = conn.cursor()
        c.execute("CREATE DATABASE IF NOT EXISTS dbms_miniproj")
        print("Database created successfully")
        conn.close()
    except Exception as e:
        print("Error creating database:", e)

def drop_database():
    try:
        conn = sql.connect(host="localhost", user="root", passwd="Shree123")
        c = conn.cursor()
        c.execute("DROP DATABASE IF EXISTS dbms_miniproj")
        print("Database dropped successfully")
        conn.close()
    except Exception as e:
        print("Error dropping database:", e)

def create_tables():
    #create table if not exist
    try:
        c1.execute("""CREATE TABLE IF NOT EXISTS customers (
            custid INT(6) PRIMARY KEY AUTO_INCREMENT,
            fname VARCHAR(30) NOT NULL,
            lname VARCHAR(30) NOT NULL,
            phn_num BIGINT(10) NOT NULL,
            email VARCHAR(60) NOT NULL,
            address_line1 VARCHAR(40) NOT NULL,
            address_line2 VARCHAR(40),
            city VARCHAR(40) NOT NULL,
            state VARCHAR(40) NOT NULL,
            country VARCHAR(40) NOT NULL DEFAULT "India",
            pin_code INT(6) NOT NULL,
            dom DATE DEFAULT (CURDATE()))
            AUTO_INCREMENT=100001""")

        c1.execute("""CREATE TABLE IF NOT EXISTS employees (
            empid INT(3) PRIMARY KEY AUTO_INCREMENT,
            fname VARCHAR(30) NOT NULL,
            lname VARCHAR(30) NOT NULL,
            phn_num BIGINT(10) NOT NULL,
            email VARCHAR(60),
            department VARCHAR(30) NOT NULL,
            post VARCHAR(30) NOT NULL,
            doj DATE DEFAULT (CURDATE()),
            salary FLOAT(6) NOT NULL,
            employed varchar(10) NOT NULL DEFAULT "Active",
            address_line1 VARCHAR(40) NOT NULL,
            address_line2 VARCHAR(40),
            city VARCHAR(40) NOT NULL,
            country VARCHAR(40) NOT NULL DEFAULT "India",
            pin_code INT(6) NOT NULL)
            AUTO_INCREMENT=1001""")

        c1.execute("""CREATE TABLE IF NOT EXISTS products (
            prodid INT(4) PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(60) NOT NULL,
            category VARCHAR(30) NOT NULL,
            price FLOAT(7) NOT NULL,
            brand VARCHAR(30) NOT NULL,
            qty_avlbl INT(4) NOT NULL)
            AUTO_INCREMENT=1001""")

        c1.execute("""CREATE TABLE IF NOT EXISTS billing (
            billid INT(8) PRIMARY KEY AUTO_INCREMENT,
            prodid INT(4),
            custid INT(6),
            empid INT(3),
            billdate date default (curdate()),
            qty int(4) NOT NULL,
            gst float(6) NOT NULL,
            subtotal float(7) NOT NULL,
            paid varchar(3) NOT NULL default 'No',        
            FOREIGN KEY (custid) REFERENCES customers(custid),
            FOREIGN KEY (empid) REFERENCES employees(empid),
            FOREIGN KEY (prodid) REFERENCES products(prodid))""")

        conn.commit()
        print("Tables created successfully")
    except Exception as e:
        print("Error creating tables:", e)

def add_record(table_name):
    try:
        if table_name == 'customers':
            #add record customers
            fname = input("Enter first name: ")
            lname = input("Enter last name: ")
            phn_num = input("Enter phone number: ")
            email = input("Enter email (optional): ")
            address_line1 = input("Enter address line 1: ")
            address_line2 = input("Enter address line 2 (optional): ")
            city = input("Enter city: ")
            state = input("Enter state: ")
            country = input("Enter country (default India): ")
            pin_code = input("Enter PIN code: ")

            customer_exists=check_existing_customer(phn_num)
            if customer_exists==True:
                print("This customer is already a member of our store. You can continue purchasing with same contact no. or create new customer.")
                answer = input("Would you like to try using another phone number? (Y/N)")
                if answer.lower() == 'Y':
                    new_phn_num = input ("Enter phone number: ")
                    c1.execute("""INSERT INTO customers (fname, lname, phn_num, email, address_line1, address_line2, city, state, country, pin_code)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (fname, lname, new_phn_num, email, address_line1, address_line2, city, state, country, pin_code))
                    conn.commit()
                    print("Customer record added successfully")            
                else:
                    pass
            elif customer_exists==False:
                c1.execute("""INSERT INTO customers (fname, lname, phn_num, email, address_line1, address_line2, city, state, country, pin_code)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (fname, lname, phn_num, email, address_line1, address_line2, city, state, country, pin_code))
                conn.commit()
                print("Customer record added successfully")

        elif table_name == 'employees':
            #add record emp
            fname = input("Enter first name: ")
            lname = input("Enter last name: ")
            phn_num = input("Enter phone number: ")
            email = input("Enter email: ")
            department = input("Enter department: ")
            post = input("Enter post: ")
            doj = input("Enter date of joining (YYYY-MM-DD): ")
            salary = input ("Enter salary: ")
            employed=input("Enter employment status (Active/Inactive):")
            address_line1 = input("Enter address line 1: ")
            address_line2 = input("Enter address line 2 (optional): ")
            city = input("Enter city: ")
            country = input("Enter country (default India): ")
            pin_code = input("Enter PIN code: ")

            c1.execute("""INSERT INTO employees (fname, lname, phn_num, email, department, post, doj, salary, employed, address_line1, address_line2, city, country, pin_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (fname, lname, phn_num, email, department, post, doj, salary, employed, address_line1, address_line2, city, country, pin_code))
            conn.commit()
            print("Employee record added successfully")

        elif table_name == 'billing':
            #add record bill
            prodid = input("Enter product ID: ")
            custid = input("Enter customer ID: ")
            empid = input("Enter employee ID: ")
            qty = int(input("Enter quantity: "))

            #display price
            c1.execute("SELECT price FROM products WHERE prodid = %s", (prodid,))
            price = c1.fetchone()[0]

            # Calculate subtotal and gst in SQL query
            c1.execute("""
                INSERT INTO billing (prodid, custid, empid, qty, gst, subtotal, paid)
                SELECT %s, %s, %s, %s, (%s * 0.18), (%s * %s) + ((%s * %s) * 0.18), 'No'
                FROM products
                WHERE prodid = %s
            """, (prodid, custid, empid, qty, price, qty, price, qty, price, prodid))
            conn.commit()
            print("Billing record added successfully.")


        elif table_name == 'products':
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            price = input("Enter product price: ")
            brand = input("Enter product brand: ")
            qty_avlbl = input("Enter product quantity available: ")

            c1.execute("INSERT INTO products(name, category, price, brand, qty_avlbl) VALUES (%s, %s, %s, %s, %s)",
                    (name, category, price, brand, qty_avlbl))
            conn.commit()
            print("Product record added successfully")

        else:
            print("Invalid table name. Please provide 'customers', 'employees', 'products' or 'billing'.")
    except Exception as e:
        print("Error adding record:", e)

def delete_record(table_name):
    try:
        if table_name == 'customers':
            # Code to delete customer record
            custid = input("Enter customer ID to delete: ")
            c1.execute("DELETE FROM customers WHERE custid = %s", (custid,))
            conn.commit()
            print("Customer record deleted successfully")

        elif table_name == 'employees':
            # Code to delete employee record
            empid = input("Enter employee ID to delete: ")
            c1.execute("DELETE FROM employees WHERE empid = %s", (empid,))
            conn.commit()
            print("Employee record deleted successfully")

        elif table_name == 'billing':
            # Code to delete billing record
            billid = input("Enter billing ID to delete: ")
            c1.execute("DELETE FROM billing WHERE billid = %s", (billid,))
            conn.commit()
            print("Billing record deleted successfully")

        elif table_name == 'products':
            prodid = input("Enter product ID to delete: ")
            c1.execute("DELETE FROM products WHERE prodid = %s", (prodid,))
            conn.commit()
            print("Product record deleted successfully")

        else:
            print("Invalid table name. Please provide 'customers', 'employees', 'products' or 'billing'.")
    except Exception as e:
        print("Error deleting record:", e)

def retrieve_records(table_name):
    try:
        if table_name == 'customers':
            choice = input("Enter 'all' to retrieve all records or enter customer ID to retrieve specific record: ")
            if choice.lower() == 'all':
                c1.execute("SELECT * FROM customers")
                records = c1.fetchall()
                df = pd.DataFrame(records, columns=[desc[0] for desc in c1.description])
                print("Customer Records:")
                print(df)
            else:
                c1.execute("SELECT * FROM customers WHERE custid = %s", (choice,))
                record = c1.fetchone()
                if record:
                    df = pd.DataFrame(records, columns=[desc[0] for desc in c1.description])
                    print("Customer Records:")
                    print(df)
                else:
                    print("Customer not found.")

        elif table_name == 'employees':
            choice = input("Enter 'all' to retrieve all records or enter employee ID to retrieve specific record: ")
            if choice.lower() == 'all':
                c1.execute("SELECT * FROM employees")
                records = c1.fetchall()
                df = pd.DataFrame(records, columns=[desc[0] for desc in c1.description])
                print("Employee Records:")
                print(df)
            else:
                c1.execute("SELECT * FROM employees WHERE empid = %s", (choice,))
                record = c1.fetchone()
                if record:
                    df = pd.DataFrame(records, columns=[desc[0] for desc in c1.description])
                    print("Employee Records:")
                    print(df)
                else:
                    print("Employee not found.")

        elif table_name == 'billing':
            choice = input("Enter 'all' to retrieve all records or enter billing ID to retrieve specific record: ")
            if choice.lower() == 'all':
                c1.execute("SELECT * FROM billing")
                records = c1.fetchall()
                df = pd.DataFrame(records, columns=[desc[0] for desc in c1.description])
                print("Billing Records:")
                print(df)            
            else:
                c1.execute("SELECT * FROM billing WHERE billid = %s", (choice,))
                record = c1.fetchone()
                if record:
                    df = pd.DataFrame(records, columns=[desc[0] for desc in c1.description])
                    print("Billing Records:")
                    print(df)
                else:
                    print("Billing record not found.")

        elif table_name == 'products':
            choice = input("Enter 'all' to retrieve all records or enter product ID to retrieve specific record: ")
            if choice.lower() == 'all':
                c1.execute("SELECT * FROM products")
                records = c1.fetchall()
                df = pd.DataFrame(records, columns=[desc[0] for desc in c1.description])
                print("Product Records:")
                print(df)
            else:
                c1.execute("SELECT * FROM products WHERE prodid = %s", (choice,))
                record = c1.fetchone()
                if record:
                    df = pd.DataFrame(records, columns=[desc[0] for desc in c1.description])
                    print("Product Records:")
                    print(df)
                else:
                    print("Product not found.")

        else:
            print("Invalid table name. Please provide 'customers', 'employees', 'products' or 'billing'.")
    except Exception as e:
        print("Error retrieving record:", e)

def update_record(table_name):
    try:
        if table_name == 'customers':
            # Code to update customer record
            custid = input("Enter customer ID to update: ")
            attribute = input("Enter attribute to update (fname, lname, phn_num, email, address_line1, address_line2, city, state, country, pin_code, dom): ")
            new_value = input(f"Enter new value for {attribute}: ")

            update_query = f"UPDATE customers SET {attribute} = %s WHERE custid = %s"
            c1.execute(update_query, (new_value, custid))
            conn.commit()
            print("Customer record updated successfully")

        elif table_name == 'employees':
            # Code to update employee record
            empid = input("Enter employee ID to update: ")
            attribute = input("Enter attribute to update (fname, lname, phn_num, email, department, post, doj, salary, employed, address_line1, address_line2, city, country, pin_code): ")
            new_value = input(f"Enter new value for {attribute}: ")

            update_query = f"UPDATE employees SET {attribute} = %s WHERE empid = %s"
            c1.execute(update_query, (new_value, empid))
            conn.commit()
            print("Employee record updated successfully")

        elif table_name == 'billing':
            # Code to update billing record
            billid = input("Enter billing ID to update: ")
            attribute = input("Enter attribute to update (prodid, custid, empid, qty, paid): ")
            new_value = input(f"Enter new value for {attribute}: ")

            update_query = f"UPDATE billing SET {attribute} = %s WHERE billid = %s"
            c1.execute(update_query, (new_value, billid))
            conn.commit()
            print("Billing record updated successfully")

        elif table_name == 'products':
            prodid = input("Enter product ID to update: ")
            attribute = input("Enter attribute to update (name, category, price, brand, qty_avlbl): ")
            new_value = input(f"Enter new value for {attribute}: ")

            update_query = f"UPDATE products SET {attribute} = %s WHERE prodid = %s"
            c1.execute(update_query, (new_value, prodid))
            conn.commit()
            print("Product record updated successfully")

        else:
            print("Invalid table name. Please provide 'customers', 'employees', 'products' or 'billing'.")
    except Exception as e:
        print("Error updating record:", e)

def search_record(table_name):
    try:
        if table_name == 'customers':
            # Code to search customer record
            attribute = input("Enter attribute to search by (fname, lname, phn_num, email, city, state, country, pin_code, dom): ")
            search_value = input(f"Enter value to search for {attribute}: ")

            search_query = f"SELECT * FROM customers WHERE {attribute} LIKE %s"
            c1.execute(search_query, (search_value,))
            customer_records = c1.fetchall()
            df = pd.DataFrame(customer_records, columns=[desc[0] for desc in c1.description])
            print("Customer Records:")
            print(df)                

        elif table_name == 'employees':
            #search employee record
            attribute = input("Enter attribute to search by (fname, lname, phn_num, email, department, post, doj, salary, employed, city, country, pin_code): ")
            search_value = input(f"Enter value to search for {attribute}: ")

            search_query = f"SELECT * FROM employees WHERE {attribute} LIKE %s"
            c1.execute(search_query, (search_value,))
            employee_records = c1.fetchall()
            df = pd.DataFrame(employee_records, columns=[desc[0] for desc in c1.description])
            print("Customer Records:")
            print(df)

        elif table_name == 'billing':
            #search billing record
            attribute = input("Enter attribute to search by (prodid, custid, empid, qty, subtotal, paid): ")
            search_value = input(f"Enter value to search for {attribute}: ")

            search_query = f"SELECT * FROM billing WHERE {attribute} LIKE %s"
            c1.execute(search_query, (search_value,))
            billing_records = c1.fetchall()
            df = pd.DataFrame(billing_records, columns=[desc[0] for desc in c1.description])
            print("Customer Records:")
            print(df)

        elif table_name == 'products':
            #search products record
            attribute = input("Enter attribute to search by (name, category, price, brand, qty_avlbl): ")
            search_value = input(f"Enter value to search for {attribute}: ")

            search_query = f"SELECT * FROM products WHERE {attribute} LIKE %s"
            c1.execute(search_query, (search_value,))
            product_records = c1.fetchall()
            df = pd.DataFrame(product_records, columns=[desc[0] for desc in c1.description])
            print("Customer Records:")
            print(df)

        else:
            print("Invalid table name. Please provide 'customers', 'employees', 'products' or 'billing'.")
    except Exception as e:
        print("Error searching customer:", e)

def customer_history(cust_id, start_date, end_date):
    try:
        c1.execute("""
            SELECT billing.*, customers.fname, customers.lname
            FROM billing
            INNER JOIN customers ON billing.custid = customers.custid
            WHERE billing.custid = %s AND billing.billdate BETWEEN %s AND %s
        """, (cust_id, start_date, end_date))
        billing_records = c1.fetchall()
        df = pd.DataFrame(billing_records, columns=[desc[0] for desc in c1.description])
        print("Customer Records:")
        print(df)

    except Exception as e:
        print("Error fetching customer history:", e)

def check_product_stock(prod_id):
    try:
        c1.execute("SELECT qty_avlbl FROM products WHERE prodid = %s", (prod_id,))
        stock = c1.fetchone()
        if stock:
            print("Available Stock:", stock[0])
        else:
            print("Product not found.")
    except Exception as e:
        print("Error checking product stock:", e)

def sales_by_date(empid, start_date, end_date):
    try:
        c1.execute("""
            SELECT SUM(billing.subtotal), employees.fname, employees.lname
            FROM billing
            INNER JOIN employees ON billing.empid = employees.empid
            WHERE billing.empid = %s AND billing.billdate BETWEEN %s AND %s
            GROUP BY employees.empid
        """, (empid, start_date, end_date))
        total_sales = c1.fetchone()[0]
        print(f"Total sales for employee {empid} from {start_date} to {end_date} : {total_sales}")
    except Exception as e:
        print("Error fetching total sales:", e)

def total_bill(cust_id):
    try:
        c1.execute("SELECT SUM(subtotal) FROM billing WHERE paid = %s AND custid = %s", ("No", cust_id))
        total_bill = c1.fetchone()[0]
        print(f"Total bill for customer {cust_id} : {total_bill}")
    except Exception as e:
        print("Error fetching total bill:", e)

def reduce_stock(bill_id):
    try:
        # Fetch the product ID and quantity from the billing table using the bill ID
        c1.execute("SELECT prodid, qty FROM billing WHERE billid = %s", (bill_id,))
        bill_data = c1.fetchone()
        
        if bill_data:
            prod_id, qty = bill_data
            
            # Update the product table to reduce the quantity available
            c1.execute("UPDATE product SET qty_avlbl = qty_avlbl - %s WHERE prodid = %s", (qty, prod_id))
            conn.commit()
            print("Stock reduced successfully")
        else:
            print("Billing record not found")
    except Exception as e:
        print("Error reducing stock:", e)

def update_paid_status():
    try:
        # Update paid status
        billid = input("Enter billing ID to update payment status: ")
        paid_status = input("Enter new payment status (Yes/No): ")

        c1.execute("UPDATE billing SET paid = %s WHERE billid = %s", (paid_status, billid))
        conn.commit()
        print("Billing record updated successfully")

        #if payment reduce stock
        if paid_status.lower() == 'yes':
            reduce_stock(billid)
    except Exception as e:
        print("Error updating paid status:", e)

def check_existing_customer(phone_num):
    try:
        c1.execute("SELECT * FROM customers WHERE phn_num = %s", (phone_num,))
        existing_customer = c1.fetchone()
        if existing_customer:
            return True
        else:
            return False
    except Exception as e:
        print("Error checking existing customer:", e)
        return None

def main_menu():
    print("\nMain Menu")
    print("1. Admin Login")
    print("2. Danger Zone: Drop Database")
    print("3. Exit")

def handle_admin_actions():
    while(True):
        print("\nAdmin Actions Menu")
        print("1. Basic Operations")
        print("2. Special Functions")
        print("3. Back to Main Menu")

        super_choice = input ("Enter your choice: ")
        #basic operations
        if super_choice=='1':
            print("\nBasic Operations")
            print("1. Add Record")
            print("2. Delete Record")
            print("3. Retrieve Records")
            print("4. Update Records")
            print("5. Search Records")
            choice1 = input("Enter your choice: ")
            if choice1 == '1':
                print("Select table to ADD record to")
                print("1. Customer")
                print("2. Employee")
                print("3. Product")
                print("4. Billing")
                table_choice = int(input("Enter your choice: "))
                table_name=""
                if table_choice==1:
                    table_name="customers"
                elif table_choice==2:
                    table_name="employees"
                elif table_choice==3:
                    table_name="products"
                elif table_choice==4:
                    table_name="billing"
                else:
                    print("Wrong choice")
                add_record(table_name)
            elif choice1 == '2':
                print("Select table to DELETE record from")
                print("1. Customer")
                print("2. Employee")
                print("3. Product")
                print("4. Billing")
                table_choice = int(input("Enter your choice: "))
                table_name=""
                if table_choice==1:
                    table_name="customers"
                elif table_choice==2:
                    table_name="employees"
                elif table_choice==3:
                    table_name="products"
                elif table_choice==4:
                    table_name="billing"
                else:
                    print("Wrong choice")
                delete_record(table_name)
            elif choice1 == '3':
                print("Select table to RETRIEVE record from")
                print("1. Customer")
                print("2. Employee")
                print("3. Product")
                print("4. Billing")
                table_choice = int(input("Enter your choice: "))
                table_name=""
                if table_choice==1:
                    table_name="customers"
                elif table_choice==2:
                    table_name="employees"
                elif table_choice==3:
                    table_name="products"
                elif table_choice==4:
                    table_name="billing"
                else:
                    print("Wrong choice")
                retrieve_records(table_name)
            elif choice1 == '4':
                print("Select table to UPDATE record from")
                print("1. Customer")
                print("2. Employee")
                print("3. Product")
                print("4. Billing")
                table_choice = int(input("Enter your choice: "))
                table_name=""
                if table_choice==1:
                    table_name="customers"
                elif table_choice==2:
                    table_name="employees"
                elif table_choice==3:
                    table_name="products"
                elif table_choice==4:
                    table_name="billing"
                else:
                    print("Wrong choice")
                update_record(table_name)
            elif choice1 == '5':
                print("Select table to SEARCH record from")
                print("1. Customer")
                print("2. Employee")
                print("3. Product")
                print("4. Billing")
                table_choice = int(input("Enter your choice: "))
                table_name=""
                if table_choice==1:
                    table_name="customers"
                elif table_choice==2:
                    table_name="employees"
                elif table_choice==3:
                    table_name="products"
                elif table_choice==4:
                    table_name="billing"
                else:
                    print("Wrong choice")
                search_record(table_name)

            else:
                print("Invalid choice")
        
        #special functions
        elif super_choice=='2':
            print("Special Operations")
            print("1. Bill Payment Status Updation")
            print("2. Total Employee Sales by Date")
            print("3. Customer Bill Generation")
            print("4. Check customer history by date")
            print("5. Check Stock of Product")
            choice2 = input("Enter your choice: ")
            if choice2 == '1':
                update_paid_status()
            elif choice2 == '2':
                empid = input("Enter Employee ID: ")
                date = input("Enter Date (YYYY-MM-DD): ")
                sales_by_date(empid, date)
            elif choice2 == '3':
                cust_id = input("Enter Customer ID: ")
                total_bill(cust_id)
            elif choice2 == '4':
                check_cust_id=input("Enter Customer ID : ")
                start_date=input("Enter start date (YYYY-MM-DD): ")
                end_date=input("Enter start date (YYYY-MM-DD): ")
                customer_history(check_cust_id, start_date, end_date)
            elif choice2 == '5':
                check_emp_id=input("Enter Employee ID : ")
                start_date=input("Enter start date (YYYY-MM-DD): ")
                end_date=input("Enter start date (YYYY-MM-DD): ")
                sales_by_date(check_emp_id, start_date, end_date)                
            else:
                print("Invalid choice")
        elif super_choice == '3':
            return
        else:
            print("Invalid choice")




"""
main code execution starts here
"""
#display whole table using pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

#MySQL connection
create_database()

#connect to db
try:
    conn = sql.connect(host="localhost", user="root", passwd="Shree123", database="dbms_miniproj")
    if conn.is_connected():
        print("Connected to MySQL database")
except Exception as e:
    print("Error connecting to database:", e)

#create cursor
try:
    c1 = conn.cursor()
except Exception as e:
    print("Error creating cursor:", e)


create_tables()

print("----------Electronics Store Management System----------")
while True:
    main_menu()
    choice = input("Enter your choice: ")

    if choice == '1':
        password = input("Enter Admin Password: ")
        if password == 'admin123':
            handle_admin_actions()
        else:
            print("Invalid admin credentials")
    elif choice == '2':
        answer = input("Are you sure you wanna drop database? (Y/N): ")
        if answer.lower() == 'y':
            pwd = input ("Enter admin password: ")
            if pwd == "admin123":
                drop_database()
                break
            else:
                print("Invalid admin credentials")
    elif choice == '3':
        print("Exiting...")
        break
    else:
        print("Invalid choice")

#finally close connection to mysql
try:
    print("Closing connection....")
    conn.close()
    print("Connection closed successfully")
except Exception as close_err:
    print("Error closing connection:", close_err)