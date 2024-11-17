import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
from datetime import datetime, timedelta
from tkinter.font import Font
from datetime import datetime


# pyinstaller --onefile --noconsole purchases_with_return_data_generator.py


############################## if There is an icon ################################
# pyinstaller --onefile --noconsole --icon=path/to/icon.ico purchases_with_return_data_generator.py

# The divider function
def divider(title):
    return (
        "\n\n\n"
        + "-- -----------------------------------------------------\n"
        + f"-- {title}\n"
        + "-- -----------------------------------------------------\n"
    )

def generate_random_purchase_data_with_returns(
    num_records, purchase_id_starting, return_id_starting, supplier_id_range, employee_id_range,
    date_range, payment_method_id_range, payment_amount_range, purchase_details_range,
    product_unit_id_range, purchase_price_range, quantity_range, return_range,
    return_reason_list, return_details_range, return_payment_range, return_chance
):
    purchases_sql = divider(f"Insert {num_records} Purchases starting from purchase_id {purchase_id_starting}") + "INSERT INTO `trade`.`purchase` (`supplier_id`, `employee_id`, `date`)\nVALUES\n"
    payments_sql = divider("Insert Purchase Payments") + "INSERT INTO `trade`.`purchase_payment` (`purchase_id`, `employee_id`, `payment_method_id`, `amount`, `notes`, `payment_date`)\nVALUES\n"
    purchase_details_sql = divider("Insert Purchase Details") + "INSERT INTO `trade`.`purchase_detail` (`purchase_id`, `product_unit_id`, `purchase_price`, `quantity`)\nVALUES\n"
    returns_sql = divider("Insert Purchase Returns") + "INSERT INTO `trade`.`purchase_return` (`purchase_id`, `employee_id`, `supplier_id`, `date`, `reason`)\nVALUES\n"
    return_details_sql = divider("Insert Purchase Return Details") + "INSERT INTO `trade`.`purchase_return_detail` (`purchase_return_id`, `product_unit_id`, `purchase_return_price`, `quantity`)\nVALUES\n"
    return_payments_sql = divider("Insert Purchase Return Payments") + "INSERT INTO `trade`.`purchase_return_payment` (`purchase_return_id`, `employee_id`, `payment_method_id`, `amount`, `notes`, `payment_date`)\nVALUES\n"
    
    purchases_values, payment_values, purchase_details_values = [], [], []
    returns_values, return_details_values, return_payments_values = [], [], []
    purchase_detail_map = {}
    
    start_date = datetime.strptime(date_range[0], '%Y-%m-%d')
    end_date = datetime.strptime(date_range[1], '%Y-%m-%d')
    
    return_id_counter = return_id_starting
    for purchase_id in range(purchase_id_starting, purchase_id_starting + num_records):
        supplier_id = random.randint(supplier_id_range[0], supplier_id_range[1])
        employee_id = random.randint(employee_id_range[0], employee_id_range[1])
        random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        purchase_date_str = random_date.strftime('%Y-%m-%d %H:%M:%S')
        
        purchases_values.append(f"({supplier_id}, {employee_id}, '{purchase_date_str}')")
        
        payment_method_id = random.randint(payment_method_id_range[0], payment_method_id_range[1])
        amount = round(random.uniform(payment_amount_range[0], payment_amount_range[1]), 2)
        payment_values.append(f"({purchase_id}, {employee_id}, {payment_method_id}, {amount}, 'Paid', '{purchase_date_str}')")
        
        num_purchase_details = random.randint(purchase_details_range[0], purchase_details_range[1])
        purchase_detail_map[purchase_id] = []
        for _ in range(num_purchase_details):
            product_unit_id = random.randint(product_unit_id_range[0], product_unit_id_range[1])
            purchase_price = round(random.uniform(purchase_price_range[0], purchase_price_range[1]), 2)
            quantity = random.randint(quantity_range[0], quantity_range[1])
            purchase_details_values.append(f"({purchase_id}, {product_unit_id}, {purchase_price}, {quantity})")
            purchase_detail_map[purchase_id].append((product_unit_id, purchase_price, quantity))
        
        if random.randint(1, 100) <= return_chance:
            return_reason = random.choice(return_reason_list)
            return_date = random_date + timedelta(days=random.randint(1, 30))
            return_date_str = return_date.strftime('%Y-%m-%d %H:%M:%S')
            
            returns_values.append(f"({purchase_id}, {employee_id}, {supplier_id}, '{return_date_str}', '{return_reason}')")
            
            num_return_details = random.randint(return_details_range[0], return_details_range[1])
            for _ in range(num_return_details):
                product_details = random.choice(purchase_detail_map[purchase_id])
                product_unit_id, purchase_price, max_quantity = product_details
                return_quantity = random.randint(quantity_range[0], max_quantity)
                return_details_values.append(f"({return_id_counter}, {product_unit_id}, {purchase_price}, {return_quantity})")
            
            num_return_payments = random.randint(return_payment_range[0], return_payment_range[1])
            for _ in range(num_return_payments):
                return_amount = round(random.uniform(payment_amount_range[0], payment_amount_range[1]), 2)
                return_payments_values.append(f"({return_id_counter}, {employee_id}, {payment_method_id}, {return_amount}, 'Refund', '{return_date_str}')")
            
            return_id_counter += 1
    
    return (
        (
        purchases_sql + ",\n".join(purchases_values) + ";"
        + payments_sql + ",\n".join(payment_values) + ";"
        + purchase_details_sql + ",\n".join(purchase_details_values) + ";"
        ),
        (
          returns_sql + ",\n".join(returns_values) + ";"
        + return_payments_sql + ",\n".join(return_payments_values) + ";"
        + return_details_sql + ",\n".join(return_details_values) + ";"
        )
    )

# Function to copy all the generated SQL to clipboard
def copy_all_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(result_text.get('1.0', tk.END))
    window.update()
    messagebox.showinfo("Copied", "All SQL has been copied to the clipboard.")

# Function to copy only purchases SQL that generated to clipboard
def copy_only_purchases_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(all_result[0])
    window.update()
    messagebox.showinfo("Copied", "Only purchases SQL has been copied to the clipboard.")

# Function to copy only purchases returns SQL that generated to clipboard
def copy_only_purchases_returns_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(all_result[1])
    window.update()
    messagebox.showinfo("Copied", "Only purchases Returns SQL has been copied to the clipboard.")

# Update the handle_generate function for purchases
def handle_generate():
    global all_result

    try:
        num_records = int(num_records_entry.get())
        purchase_id_starting = int(purchase_id_starting_entry.get())
        return_id_starting = int(return_id_starting_entry.get())
        supplier_id_range = (int(supplier_id_min_entry.get()), int(supplier_id_max_entry.get()))
        employee_id_range = (int(employee_id_min_entry.get()), int(employee_id_max_entry.get()))
        date_range = (date_start_entry.get(), date_end_entry.get())
        payment_method_id_range = (int(payment_method_min_entry.get()), int(payment_method_max_entry.get()))
        payment_amount_range = (float(payment_min_entry.get()), float(payment_max_entry.get()))
        purchase_details_range = (int(purchase_details_min_entry.get()), int(purchase_details_max_entry.get()))
        product_unit_id_range = (int(product_unit_min_entry.get()), int(product_unit_max_entry.get()))
        purchase_price_range = (float(purchase_price_min_entry.get()), float(purchase_price_max_entry.get()))
        quantity_range = (int(quantity_min_entry.get()), int(quantity_max_entry.get()))
        
        return_range = (int(return_min_entry.get()), int(return_max_entry.get()))
        return_details_range = (int(return_detail_min_entry.get()), int(return_detail_max_entry.get()))
        return_payment_range = (int(return_payment_min_entry.get()), int(return_payment_max_entry.get()))
        return_reason_list = return_reason_entry.get().split(',')
        return_chance = int(return_chance_entry.get())  # Get chance of purchase return

        result = generate_random_purchase_data_with_returns(
            num_records, purchase_id_starting, return_id_starting, supplier_id_range, employee_id_range,
            date_range, payment_method_id_range, payment_amount_range,
            purchase_details_range, product_unit_id_range, purchase_price_range, quantity_range,
            return_range, return_reason_list, return_details_range, return_payment_range, return_chance
        )

        all_result = result
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, result[0] + result[1])
    except ValueError as e:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"Invalid input: {e}. Please check your entries.")
        all_result = (f"Invalid input: {e}. Please check your entries.", f"Invalid input: {e}. Please check your entries.")


all_result = ("", "")

# Create the UI window
window = tk.Tk()
window.title("Random Purchase Data Generator")
window.configure(bg="#f0f0f0")
window.geometry("1000x800")

# Create input fields frame
inputs_frame = ttk.Frame(window, padding="10")
inputs_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Row 1: num_records, purchase_id_starting, purchase_return_id_starting
tk.Label(inputs_frame, text="Number of Records", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=5, pady=5)
num_records_entry = tk.Entry(inputs_frame)
num_records_entry.insert(0, "100000")
num_records_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Purchase ID Starting", bg="#f0f0f0").grid(row=0, column=2, sticky="w", padx=5, pady=5)
purchase_id_starting_entry = tk.Entry(inputs_frame)
purchase_id_starting_entry.insert(0, "61")
purchase_id_starting_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Purchase Return ID Starting", bg="#f0f0f0").grid(row=0, column=4, sticky="w", padx=5, pady=5)
return_id_starting_entry = tk.Entry(inputs_frame)
return_id_starting_entry.insert(0, "13")
return_id_starting_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Chance (%)", bg="#f0f0f0").grid(row=0, column=6, sticky="w", padx=5, pady=5)
return_chance_entry = tk.Entry(inputs_frame)
return_chance_entry.insert(0, "20")
return_chance_entry.grid(row=0, column=7, padx=5, pady=5)

# Row 2: supplier_id_range, employee_id_range, date_range
tk.Label(inputs_frame, text="Supplier ID Min", bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5, pady=5)
supplier_id_min_entry = tk.Entry(inputs_frame)
supplier_id_min_entry.insert(0, "1")
supplier_id_min_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Supplier ID Max", bg="#f0f0f0").grid(row=1, column=2, sticky="w", padx=5, pady=5)
supplier_id_max_entry = tk.Entry(inputs_frame)
supplier_id_max_entry.insert(0, "7")
supplier_id_max_entry.grid(row=1, column=3, padx=5, pady=5)

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

# Row 4: purchase_details_range, product_unit_id_range, purchase_price_range, quantity_range
tk.Label(inputs_frame, text="Purchase Details Min", bg="#f0f0f0").grid(row=4, column=0, sticky="w", padx=5, pady=5)
purchase_details_min_entry = tk.Entry(inputs_frame)
purchase_details_min_entry.insert(0, "3")
purchase_details_min_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Purchase Details Max", bg="#f0f0f0").grid(row=4, column=2, sticky="w", padx=5, pady=5)
purchase_details_max_entry = tk.Entry(inputs_frame)
purchase_details_max_entry.insert(0, "15")
purchase_details_max_entry.grid(row=4, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Product Unit ID Min", bg="#f0f0f0").grid(row=4, column=4, sticky="w", padx=5, pady=5)
product_unit_min_entry = tk.Entry(inputs_frame)
product_unit_min_entry.insert(0, "1")
product_unit_min_entry.grid(row=4, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Product Unit ID Max", bg="#f0f0f0").grid(row=4, column=6, sticky="w", padx=5, pady=5)
product_unit_max_entry = tk.Entry(inputs_frame)
product_unit_max_entry.insert(0, "48")
product_unit_max_entry.grid(row=4, column=7, padx=5, pady=5)

tk.Label(inputs_frame, text="Purchase Price Min", bg="#f0f0f0").grid(row=5, column=0, sticky="w", padx=5, pady=5)
purchase_price_min_entry = tk.Entry(inputs_frame)
purchase_price_min_entry.insert(0, "20.00")
purchase_price_min_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Purchase Price Max", bg="#f0f0f0").grid(row=5, column=2, sticky="w", padx=5, pady=5)
purchase_price_max_entry = tk.Entry(inputs_frame)
purchase_price_max_entry.insert(0, "300.00")
purchase_price_max_entry.grid(row=5, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Quantity Min", bg="#f0f0f0").grid(row=5, column=4, sticky="w", padx=5, pady=5)
quantity_min_entry = tk.Entry(inputs_frame)
quantity_min_entry.insert(0, "20")
quantity_min_entry.grid(row=5, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Quantity Max", bg="#f0f0f0").grid(row=5, column=6, sticky="w", padx=5, pady=5)
quantity_max_entry = tk.Entry(inputs_frame)
quantity_max_entry.insert(0, "30")
quantity_max_entry.grid(row=5, column=7, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Min", bg="#f0f0f0").grid(row=6, column=0, sticky="w", padx=5, pady=5)
return_min_entry = tk.Entry(inputs_frame)
return_min_entry.insert(0, "1")
return_min_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Max", bg="#f0f0f0").grid(row=6, column=2, sticky="w", padx=5, pady=5)
return_max_entry = tk.Entry(inputs_frame)
return_max_entry.insert(0, "2")
return_max_entry.grid(row=6, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Details Min", bg="#f0f0f0").grid(row=7, column=0, sticky="w", padx=5, pady=5)
return_detail_min_entry = tk.Entry(inputs_frame)
return_detail_min_entry.insert(0, "1")
return_detail_min_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Details Max", bg="#f0f0f0").grid(row=7, column=2, sticky="w", padx=5, pady=5)
return_detail_max_entry = tk.Entry(inputs_frame)
return_detail_max_entry.insert(0, "5")
return_detail_max_entry.grid(row=7, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Payment Min", bg="#f0f0f0").grid(row=7, column=4, sticky="w", padx=5, pady=5)
return_payment_min_entry = tk.Entry(inputs_frame)
return_payment_min_entry.insert(0, "1")
return_payment_min_entry.grid(row=7, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Payment Max", bg="#f0f0f0").grid(row=7, column=6, sticky="w", padx=5, pady=5)
return_payment_max_entry = tk.Entry(inputs_frame)
return_payment_max_entry.insert(0, "1")
return_payment_max_entry.grid(row=7, column=7, padx=5, pady=5)

tk.Label(inputs_frame, text="Return Reasons (comma-separated)", bg="#f0f0f0").grid(row=8, column=0, sticky="w", padx=5, pady=5)
return_reason_entry = tk.Entry(inputs_frame, width=50)
return_reason_entry.insert(0, "Defective,Expired,Wrong Item")
return_reason_entry.grid(row=8, column=1, columnspan=7, padx=5, pady=5)

# Button to generate SQL
generate_button = tk.Button(window, text="Generate SQL", command=handle_generate, bg="#007BFF", fg="white", font=("Arial", 12))
generate_button.grid(row=9, column=0, padx=10, pady=10, sticky="ew")

# Result text area with a copy button
result_frame = ttk.Frame(window, padding="10")
result_frame.grid(row=10, column=0, sticky="nsew", padx=10, pady=5)

result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=120, height=15, font=("Consolas", 10))
result_text.grid(row=0, column=0, padx=5, pady=5)

copy_all_button = tk.Button(result_frame, text="📋 Copy All", command=copy_all_to_clipboard, bg="#28a745", fg="white", font=("Arial", 10))
copy_all_button.grid(row=0, column=1, padx=5, pady=5, sticky="n")

copy_only_purchases_button = tk.Button(result_frame, text="📋 Copy Only purchases", command=copy_only_purchases_to_clipboard, bg="#28a745", fg="white", font=("Arial", 10))
copy_only_purchases_button.grid(row=0, column=2, padx=5, pady=5, sticky="n")

copy_only_purchases_return_button = tk.Button(result_frame, text="📋 Copy Only purchases Return", command=copy_only_purchases_returns_to_clipboard, bg="#28a745", fg="white", font=("Arial", 10))
copy_only_purchases_return_button.grid(row=0, column=3, padx=5, pady=5, sticky="n")

# Main loop
window.mainloop()
