import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
from datetime import datetime, timedelta
from tkinter.font import Font


# pyinstaller --onefile --noconsole sales_with_return_data_generator.py


############################## if There is an icon ################################
# pyinstaller --onefile --noconsole --icon=path/to/icon.ico sales_with_return_data_generator.py

# The divider function
def divider(title):
    return (
        "\n\n\n"
        + "-- -----------------------------------------------------\n"
        + f"-- {title}\n"
        + "-- -----------------------------------------------------\n"
    )


# Function to generate SQL data based on inputs
def generate_random_sales_data_with_returns(
    num_records, sale_id_starting, sale_return_id_starting, customer_id_range, employee_id_range, date_range, 
    payment_method_id_range, payment_amount_range, sale_details_range, 
    product_unit_id_range, sale_price_range, quantity_range, unit_discount_range,
    sale_return_range, return_reason_list, return_details_range, return_payment_range,
    sale_return_chance
):
    sales_sql = "INSERT INTO `trade`.`sale` (`customer_id`, `employee_id`, `date`)\nVALUES\n"
    payments_sql = "INSERT INTO `trade`.`sale_payment` (`sale_id`, `employee_id`, `payment_method_id`, `amount`, `notes`, `payment_date`)\nVALUES\n"
    sale_details_sql = "INSERT INTO `trade`.`sale_detail` (`sale_id`, `product_unit_id`, `sale_price`, `quantity`, `unit_discount`)\nVALUES\n"
    sale_returns_sql = "INSERT INTO `trade`.`sale_return` (`sale_id`, `employee_id`, `customer_id`, `date`, `reason`)\nVALUES\n"
    sale_return_details_sql = "INSERT INTO `trade`.`sale_return_detail` (`sale_return_id`, `product_unit_id`, `sale_return_price`, `quantity`)\nVALUES\n"
    sale_return_payments_sql = "INSERT INTO `trade`.`sale_return_payment` (`sale_return_id`, `employee_id`, `payment_method_id`, `amount`, `notes`, `payment_date`)\nVALUES\n"
    
    sales_values = []
    payment_values = []
    sale_details_values = []
    sale_returns_values = []
    sale_return_details_values = []
    sale_return_payments_values = []
    
    start_date = datetime.strptime(date_range[0], '%Y-%m-%d')
    end_date = datetime.strptime(date_range[1], '%Y-%m-%d')
    
    sale_detail_map = {}
    sale_id_counter = sale_id_starting
    return_id_counter = sale_return_id_starting  # Initialize return_id_counter from parameter
    
    for sale_id in range(sale_id_starting, sale_id_starting + num_records):
        customer_id = random.randint(customer_id_range[0], customer_id_range[1])
        employee_id = random.randint(employee_id_range[0], employee_id_range[1])
        random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        sale_date_str = random_date.strftime('%Y-%m-%d %H:%M:%S')
        
        sales_values.append(f"({customer_id}, {employee_id}, '{sale_date_str}')")
        
        payment_method_id = random.randint(payment_method_id_range[0], payment_method_id_range[1])
        amount = round(random.uniform(payment_amount_range[0], payment_amount_range[1]), 2)
        payment_date_str = sale_date_str
        
        payment_values.append(f"({sale_id}, {employee_id}, {payment_method_id}, {amount}, 'Paid in full', '{payment_date_str}')")
        
        num_sale_details = random.randint(sale_details_range[0], sale_details_range[1])
        sale_detail_map[sale_id] = []
        for _ in range(num_sale_details):
            product_unit_id = random.randint(product_unit_id_range[0], product_unit_id_range[1])
            sale_price = round(random.uniform(sale_price_range[0], sale_price_range[1]), 2)
            quantity = random.randint(quantity_range[0], quantity_range[1])
            unit_discount = round(random.uniform(unit_discount_range[0], unit_discount_range[1]), 2)
            sale_details_values.append(f"({sale_id}, {product_unit_id}, {sale_price}, {quantity}, {unit_discount})")
            sale_detail_map[sale_id].append((product_unit_id, sale_price, quantity))
        
        # Determine if a sale return should be generated
        if random.randint(1, 100) <= sale_return_chance:  # Use percentage chance
            num_returns = random.randint(sale_return_range[0], sale_return_range[1])
            for _ in range(num_returns):
                return_reason = random.choice(return_reason_list)
                return_date = random_date + timedelta(days=random.randint(1, 30))
                return_date_str = return_date.strftime('%Y-%m-%d %H:%M:%S')
                
                sale_returns_values.append(f"({sale_id}, {employee_id}, {customer_id}, '{return_date_str}', '{return_reason}')")
                
                
                # Generate return details
                num_return_details = random.randint(return_details_range[0], return_details_range[1])
                for _ in range(num_return_details):
                    product_details = random.choice(sale_detail_map[sale_id])
                    product_unit_id, sale_price, max_quantity = product_details
                    return_quantity = random.randint(quantity_range[0], max_quantity)
                    sale_return_details_values.append(f"({return_id_counter}, {product_unit_id}, {sale_price}, {return_quantity})")
                
                # Generate return payment
                num_return_payments = random.randint(return_payment_range[0], return_payment_range[1])
                for _ in range(num_return_payments):
                    payment_method_id = random.randint(payment_method_id_range[0], payment_method_id_range[1])
                    return_amount = round(random.uniform(payment_amount_range[0], payment_amount_range[1]), 2)
                    sale_return_payments_values.append(f"({return_id_counter}, {employee_id}, {payment_method_id}, {return_amount}, 'Refund', '{return_date_str}')")
    
                return_id_counter += 1
    
    sales_sql += ",\n".join(sales_values) + ";"
    payments_sql += ",\n".join(payment_values) + ";"
    sale_details_sql += ",\n".join(sale_details_values) + ";"
    sale_returns_sql += ",\n".join(sale_returns_values) + ";"
    sale_return_details_sql += ",\n".join(sale_return_details_values) + ";"
    sale_return_payments_sql += ",\n".join(sale_return_payments_values) + ";"
    
    return (
        (
        divider(f"Insert {num_records} sales starting from sale_id {sale_id_starting}")
        + sales_sql
        + divider("Insert sale payments corresponding to the above sales")
        + payments_sql
        + divider("Insert sale details corresponding to the above sales")
        + sale_details_sql
       ),
( 
    divider("Insert sale returns")
        + sale_returns_sql
        + divider("Insert sale return payments")
        + sale_return_payments_sql
        + divider("Insert sale return details")
        + sale_return_details_sql
),
        )


# Function to copy all the generated SQL to clipboard
def copy_all_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(result_text.get('1.0', tk.END))
    window.update()
    messagebox.showinfo("Copied", "All SQL has been copied to the clipboard.")

# Function to copy only sales SQL that generated to clipboard
def copy_only_sales_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(all_result[0])
    window.update()
    messagebox.showinfo("Copied", "Only Sales SQL has been copied to the clipboard.")

# Function to copy only sales returns SQL that generated to clipboard
def copy_only_sales_returns_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(all_result[1])
    window.update()
    messagebox.showinfo("Copied", "Only Sales Returns SQL has been copied to the clipboard.")

# Update the handle_generate function to include new fields
def handle_generate():
    global all_result

    try:
        num_records = int(num_records_entry.get())
        sale_id_starting = int(sale_id_starting_entry.get())
        sale_return_id_starting = int(sale_return_id_starting_entry.get())
        customer_id_range = (int(customer_id_min_entry.get()), int(customer_id_max_entry.get()))
        employee_id_range = (int(employee_id_min_entry.get()), int(employee_id_max_entry.get()))
        date_range = (date_start_entry.get(), date_end_entry.get())
        payment_method_id_range = (int(payment_method_min_entry.get()), int(payment_method_max_entry.get()))
        payment_amount_range = (float(payment_min_entry.get()), float(payment_max_entry.get()))
        sale_details_range = (int(sale_details_min_entry.get()), int(sale_details_max_entry.get()))
        product_unit_id_range = (int(product_unit_min_entry.get()), int(product_unit_max_entry.get()))
        sale_price_range = (float(sale_price_min_entry.get()), float(sale_price_max_entry.get()))
        quantity_range = (int(quantity_min_entry.get()), int(quantity_max_entry.get()))
        unit_discount_range = (float(unit_discount_min_entry.get()), float(unit_discount_max_entry.get()))
        
        sale_return_range = (int(sale_return_min_entry.get()), int(sale_return_max_entry.get()))
        return_details_range = (int(return_detail_min_entry.get()), int(return_detail_max_entry.get()))
        return_payment_range = (int(return_payment_min_entry.get()), int(return_payment_max_entry.get()))
        return_reason_list = return_reason_entry.get().split(',')
        sale_return_chance = int(sale_return_chance_entry.get())  # Get chance of sale return

        result = generate_random_sales_data_with_returns(
            num_records, sale_id_starting, sale_return_id_starting, customer_id_range, employee_id_range,
            date_range, payment_method_id_range, payment_amount_range,
            sale_details_range, product_unit_id_range, sale_price_range, quantity_range, unit_discount_range,
            sale_return_range, return_reason_list, return_details_range, return_payment_range, sale_return_chance
        )

        all_result = result
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, result)
    except ValueError as e:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"Invalid input: {e}. Please check your entries.")
        all_result = (f"Invalid input: {e}. Please check your entries.", f"Invalid input: {e}. Please check your entries.")


all_result = ("", "")

# Create the UI window
window = tk.Tk()
window.title("Random Sales Data Generator")
window.configure(bg="#f0f0f0")
window.geometry("1000x800")

# Create input fields frame
inputs_frame = ttk.Frame(window, padding="10")
inputs_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Row 1: num_records, sale_id_starting, sale_return_id_starting
tk.Label(inputs_frame, text="Number of Records", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=5, pady=5)
num_records_entry = tk.Entry(inputs_frame)
num_records_entry.insert(0, "60000")
num_records_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale ID Starting", bg="#f0f0f0").grid(row=0, column=2, sticky="w", padx=5, pady=5)
sale_id_starting_entry = tk.Entry(inputs_frame)
sale_id_starting_entry.insert(0, "13")
sale_id_starting_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale Return ID Starting", bg="#f0f0f0").grid(row=0, column=4, sticky="w", padx=5, pady=5)
sale_return_id_starting_entry = tk.Entry(inputs_frame)
sale_return_id_starting_entry.insert(0, "13")
sale_return_id_starting_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale Return Chance (%)", bg="#f0f0f0").grid(row=0, column=6, sticky="w", padx=5, pady=5)
sale_return_chance_entry = tk.Entry(inputs_frame)
sale_return_chance_entry.insert(0, "20")  # Default to 50%
sale_return_chance_entry.grid(row=0, column=7, padx=5, pady=5)

# Row 2: customer_id_range, employee_id_range, discount_range, date_range
tk.Label(inputs_frame, text="Customer ID Min", bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5, pady=5)
customer_id_min_entry = tk.Entry(inputs_frame)
customer_id_min_entry.insert(0, "1")
customer_id_min_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Customer ID Max", bg="#f0f0f0").grid(row=1, column=2, sticky="w", padx=5, pady=5)
customer_id_max_entry = tk.Entry(inputs_frame)
customer_id_max_entry.insert(0, "20")
customer_id_max_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Employee ID Min", bg="#f0f0f0").grid(row=1, column=4, sticky="w", padx=5, pady=5)
employee_id_min_entry = tk.Entry(inputs_frame)
employee_id_min_entry.insert(0, "1")
employee_id_min_entry.grid(row=1, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Employee ID Max", bg="#f0f0f0").grid(row=1, column=6, sticky="w", padx=5, pady=5)
employee_id_max_entry = tk.Entry(inputs_frame)
employee_id_max_entry.insert(0, "5")
employee_id_max_entry.grid(row=1, column=7, padx=5, pady=5)

tk.Label(inputs_frame, text="Date Start", bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=5, pady=5)
date_start_entry = tk.Entry(inputs_frame)
date_start_entry.insert(0, "2020-01-01")
date_start_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Date End", bg="#f0f0f0").grid(row=2, column=2, sticky="w", padx=5, pady=5)
date_end_entry = tk.Entry(inputs_frame)
date_end_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
date_end_entry.grid(row=2, column=3, padx=5, pady=5)

# Row 3: payment_method_id_range, payment_amount_range
tk.Label(inputs_frame, text="Payment Method ID Min", bg="#f0f0f0").grid(row=3, column=0, sticky="w", padx=5, pady=5)
payment_method_min_entry = tk.Entry(inputs_frame)
payment_method_min_entry.insert(0, "1")
payment_method_min_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Payment Method ID Max", bg="#f0f0f0").grid(row=3, column=2, sticky="w", padx=5, pady=5)
payment_method_max_entry = tk.Entry(inputs_frame)
payment_method_max_entry.insert(0, "3")
payment_method_max_entry.grid(row=3, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Payment Amount Min", bg="#f0f0f0").grid(row=3, column=4, sticky="w", padx=5, pady=5)
payment_min_entry = tk.Entry(inputs_frame)
payment_min_entry.insert(0, "200.00")
payment_min_entry.grid(row=3, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Payment Amount Max", bg="#f0f0f0").grid(row=3, column=6, sticky="w", padx=5, pady=5)
payment_max_entry = tk.Entry(inputs_frame)
payment_max_entry.insert(0, "1000.00")
payment_max_entry.grid(row=3, column=7, padx=5, pady=5)

# Row 4: sale_details_range, product_unit_id_range, sale_price_range, quantity_range
tk.Label(inputs_frame, text="Sale Details Min", bg="#f0f0f0").grid(row=4, column=0, sticky="w", padx=5, pady=5)
sale_details_min_entry = tk.Entry(inputs_frame)
sale_details_min_entry.insert(0, "3")
sale_details_min_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale Details Max", bg="#f0f0f0").grid(row=4, column=2, sticky="w", padx=5, pady=5)
sale_details_max_entry = tk.Entry(inputs_frame)
sale_details_max_entry.insert(0, "15")
sale_details_max_entry.grid(row=4, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Product Unit ID Min", bg="#f0f0f0").grid(row=4, column=4, sticky="w", padx=5, pady=5)
product_unit_min_entry = tk.Entry(inputs_frame)
product_unit_min_entry.insert(0, "1")
product_unit_min_entry.grid(row=4, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Product Unit ID Max", bg="#f0f0f0").grid(row=4, column=6, sticky="w", padx=5, pady=5)
product_unit_max_entry = tk.Entry(inputs_frame)
product_unit_max_entry.insert(0, "48")
product_unit_max_entry.grid(row=4, column=7, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale Price Min", bg="#f0f0f0").grid(row=5, column=0, sticky="w", padx=5, pady=5)
sale_price_min_entry = tk.Entry(inputs_frame)
sale_price_min_entry.insert(0, "30.00")
sale_price_min_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale Price Max", bg="#f0f0f0").grid(row=5, column=2, sticky="w", padx=5, pady=5)
sale_price_max_entry = tk.Entry(inputs_frame)
sale_price_max_entry.insert(0, "500.00")
sale_price_max_entry.grid(row=5, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Quantity Min", bg="#f0f0f0").grid(row=5, column=4, sticky="w", padx=5, pady=5)
quantity_min_entry = tk.Entry(inputs_frame)
quantity_min_entry.insert(0, "1")
quantity_min_entry.grid(row=5, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Quantity Max", bg="#f0f0f0").grid(row=5, column=6, sticky="w", padx=5, pady=5)
quantity_max_entry = tk.Entry(inputs_frame)
quantity_max_entry.insert(0, "5")
quantity_max_entry.grid(row=5, column=7, padx=5, pady=5)

# Additional input for unit discount range
tk.Label(inputs_frame, text="Unit Discount Min", bg="#f0f0f0").grid(row=6, column=0, sticky="w", padx=5, pady=5)
unit_discount_min_entry = tk.Entry(inputs_frame)
unit_discount_min_entry.insert(0, "5.00")
unit_discount_min_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Unit Discount Max", bg="#f0f0f0").grid(row=6, column=2, sticky="w", padx=5, pady=5)
unit_discount_max_entry = tk.Entry(inputs_frame)
unit_discount_max_entry.insert(0, "10.00")
unit_discount_max_entry.grid(row=6, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale Return Min", bg="#f0f0f0").grid(row=7, column=0, sticky="w", padx=5, pady=5)
sale_return_min_entry = tk.Entry(inputs_frame)
sale_return_min_entry.insert(0, "1")
sale_return_min_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale Return Max", bg="#f0f0f0").grid(row=7, column=2, sticky="w", padx=5, pady=5)
sale_return_max_entry = tk.Entry(inputs_frame)
sale_return_max_entry.insert(0, "2")
sale_return_max_entry.grid(row=7, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Detail Min", bg="#f0f0f0").grid(row=8, column=0, sticky="w", padx=5, pady=5)
return_detail_min_entry = tk.Entry(inputs_frame)
return_detail_min_entry.insert(0, "1")
return_detail_min_entry.grid(row=8, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Detail Max", bg="#f0f0f0").grid(row=8, column=2, sticky="w", padx=5, pady=5)
return_detail_max_entry = tk.Entry(inputs_frame)
return_detail_max_entry.insert(0, "5")
return_detail_max_entry.grid(row=8, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Payment Min", bg="#f0f0f0").grid(row=8, column=4, sticky="w", padx=5, pady=5)
return_payment_min_entry = tk.Entry(inputs_frame)
return_payment_min_entry.insert(0, "1")
return_payment_min_entry.grid(row=8, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Payment Max", bg="#f0f0f0").grid(row=8, column=6, sticky="w", padx=5, pady=5)
return_payment_max_entry = tk.Entry(inputs_frame)
return_payment_max_entry.insert(0, "1")
return_payment_max_entry.grid(row=8, column=7, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Reasons (comma-separated)", bg="#f0f0f0").grid(row=9, column=0, sticky="w", padx=5, pady=5)
return_reason_entry = tk.Entry(inputs_frame, width=50)
return_reason_entry.insert(0, "Defective,Wrong Item,Customer Change of Mind")
return_reason_entry.grid(row=9, column=1, columnspan=7, padx=5, pady=5)

# Button to generate SQL
generate_button = tk.Button(window, text="Generate SQL", command=handle_generate, bg="#007BFF", fg="white", font=("Arial", 12))
generate_button.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

# Result text area with a copy button
result_frame = ttk.Frame(window, padding="10")
result_frame.grid(row=11, column=0, sticky="nsew", padx=10, pady=5)

result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=120, height=15, font=("Consolas", 10))
result_text.grid(row=0, column=0, padx=5, pady=5)

copy_all_button = tk.Button(result_frame, text="📋 Copy All", command=copy_all_to_clipboard, bg="#28a745", fg="white", font=("Arial", 10))
copy_all_button.grid(row=0, column=1, padx=5, pady=5, sticky="n")

copy_only_sales_button = tk.Button(result_frame, text="📋 Copy Only Sales", command=copy_only_sales_to_clipboard, bg="#28a745", fg="white", font=("Arial", 10))
copy_only_sales_button.grid(row=0, column=2, padx=5, pady=5, sticky="n")

copy_only_sales_return_button = tk.Button(result_frame, text="📋 Copy Only Sales Return", command=copy_only_sales_returns_to_clipboard, bg="#28a745", fg="white", font=("Arial", 10))
copy_only_sales_return_button.grid(row=0, column=3, padx=5, pady=5, sticky="n")

# Start the main loop
window.mainloop()