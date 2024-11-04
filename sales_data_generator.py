import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
from datetime import datetime, timedelta
from tkinter.font import Font

# The divider function
def divider(title):
    return (
        "\n\n\n"
        + "-- -----------------------------------------------------\n"
        + f"-- {title}\n"
        + "-- -----------------------------------------------------\n"
    )

# Function to generate SQL data based on inputs
def generate_random_sales_data(num_records, sale_id_starting, customer_id_range, employee_id_range, date_range, payment_method_id_range, payment_amount_range,
                               sale_details_range, product_unit_id_range, sale_price_range, quantity_range, unit_discount_range):
    sales_sql = "INSERT INTO `trade`.`sale` (`customer_id`, `employee_id`, `date`)\nVALUES\n"
    payments_sql = "INSERT INTO `trade`.`sale_payment` (`sale_id`, `employee_id`, `payment_method_id`, `amount`, `notes`, `payment_date`)\nVALUES\n"
    sale_details_sql = "INSERT INTO `trade`.`sale_detail` (`sale_id`, `product_unit_id`, `sale_price`, `quantity`, `unit_discount`)\nVALUES\n"
    
    sales_values = []
    payment_values = []
    sale_details_values = []

    start_date = datetime.strptime(date_range[0], '%Y-%m-%d')
    end_date = datetime.strptime(date_range[1], '%Y-%m-%d')

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
        for _ in range(num_sale_details):
            product_unit_id = random.randint(product_unit_id_range[0], product_unit_id_range[1])
            sale_price = round(random.uniform(sale_price_range[0], sale_price_range[1]), 2)
            quantity = random.randint(quantity_range[0], quantity_range[1])
            unit_discount = round(random.uniform(unit_discount_range[0], unit_discount_range[1]), 2)
            sale_details_values.append(f"({sale_id}, {product_unit_id}, {sale_price}, {quantity}, {unit_discount})")

    sales_sql += ",\n".join(sales_values) + ";"
    payments_sql += ",\n".join(payment_values) + ";"
    sale_details_sql += ",\n".join(sale_details_values) + ";"

    return (
        divider(f"Insert {num_records} sales starting from sale_id {sale_id_starting}")
        + sales_sql
        + divider("Insert sale payments corresponding to the above sales")
        + payments_sql
        + divider("Insert sale details corresponding to the above sales")
        + sale_details_sql
    )

# Function to handle UI input and generate SQL
def handle_generate():
    try:
        num_records = int(num_records_entry.get())
        sale_id_starting = int(sale_id_starting_entry.get())
        customer_id_range = (int(customer_id_min_entry.get()), int(customer_id_max_entry.get()))
        employee_id_range = (int(employee_id_min_entry.get()), int(employee_id_max_entry.get()))
        # discount_range = (float(discount_min_entry.get()), float(discount_max_entry.get()))
        date_range = (date_start_entry.get(), date_end_entry.get())
        payment_method_id_range = (int(payment_method_min_entry.get()), int(payment_method_max_entry.get()))
        payment_amount_range = (float(payment_min_entry.get()), float(payment_max_entry.get()))
        sale_details_range = (int(sale_details_min_entry.get()), int(sale_details_max_entry.get()))
        product_unit_id_range = (int(product_unit_min_entry.get()), int(product_unit_max_entry.get()))
        sale_price_range = (float(sale_price_min_entry.get()), float(sale_price_max_entry.get()))
        quantity_range = (int(quantity_min_entry.get()), int(quantity_max_entry.get()))
        unit_discount_range = (float(unit_discount_min_entry.get()), float(unit_discount_max_entry.get()))

        result = generate_random_sales_data(
            num_records, sale_id_starting, customer_id_range, employee_id_range,
             date_range, payment_method_id_range, payment_amount_range,
            sale_details_range, product_unit_id_range, sale_price_range, quantity_range, unit_discount_range
        )

        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, result)
    except ValueError:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Invalid input. Please check your entries.")

# Function to copy the generated SQL to clipboard
def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(result_text.get('1.0', tk.END))
    window.update()
    messagebox.showinfo("Copied", "SQL has been copied to the clipboard.")

# Create the UI window
window = tk.Tk()
window.title("Random Sales Data Generator")
window.configure(bg="#f0f0f0")
window.geometry("900x700")

# Create input fields frame
inputs_frame = ttk.Frame(window, padding="10")
inputs_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Row 1: num_records, sale_id_starting
tk.Label(inputs_frame, text="Number of Records", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=5, pady=5)
num_records_entry = tk.Entry(inputs_frame)
num_records_entry.insert(0, "1000")
num_records_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale ID Starting", bg="#f0f0f0").grid(row=0, column=2, sticky="w", padx=5, pady=5)
sale_id_starting_entry = tk.Entry(inputs_frame)
sale_id_starting_entry.insert(0, "13")
sale_id_starting_entry.grid(row=0, column=3, padx=5, pady=5)

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

# Additional input for unit discount range
tk.Label(inputs_frame, text="Unit Discount Min", bg="#f0f0f0").grid(row=6, column=0, sticky="w", padx=5, pady=5)
unit_discount_min_entry = tk.Entry(inputs_frame)
unit_discount_min_entry.insert(0, "0.00")
unit_discount_min_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Unit Discount Max", bg="#f0f0f0").grid(row=6, column=2, sticky="w", padx=5, pady=5)
unit_discount_max_entry = tk.Entry(inputs_frame)
unit_discount_max_entry.insert(0, "0.00")
unit_discount_max_entry.grid(row=6, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Date Start", bg="#f0f0f0").grid(row=2, column=4, sticky="w", padx=5, pady=5)
date_start_entry = tk.Entry(inputs_frame)
date_start_entry.insert(0, "2020-01-01")
date_start_entry.grid(row=2, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Date End", bg="#f0f0f0").grid(row=2, column=6, sticky="w", padx=5, pady=5)
date_end_entry = tk.Entry(inputs_frame)
date_end_entry.insert(0, "2024-10-10")
date_end_entry.grid(row=2, column=7, padx=5, pady=5)

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
payment_min_entry.insert(0, "0.00")
payment_min_entry.grid(row=3, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Payment Amount Max", bg="#f0f0f0").grid(row=3, column=6, sticky="w", padx=5, pady=5)
payment_max_entry = tk.Entry(inputs_frame)
payment_max_entry.insert(0, "0.00")
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
sale_price_min_entry.insert(0, "10.00")
sale_price_min_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(inputs_frame, text="Sale Price Max", bg="#f0f0f0").grid(row=5, column=2, sticky="w", padx=5, pady=5)
sale_price_max_entry = tk.Entry(inputs_frame)
sale_price_max_entry.insert(0, "150.00")
sale_price_max_entry.grid(row=5, column=3, padx=5, pady=5)

tk.Label(inputs_frame, text="Quantity Min", bg="#f0f0f0").grid(row=5, column=4, sticky="w", padx=5, pady=5)
quantity_min_entry = tk.Entry(inputs_frame)
quantity_min_entry.insert(0, "0")
quantity_min_entry.grid(row=5, column=5, padx=5, pady=5)

tk.Label(inputs_frame, text="Quantity Max", bg="#f0f0f0").grid(row=5, column=6, sticky="w", padx=5, pady=5)
quantity_max_entry = tk.Entry(inputs_frame)
quantity_max_entry.insert(0, "0")
quantity_max_entry.grid(row=5, column=7, padx=5, pady=5)

# Button to generate SQL
generate_button = tk.Button(window, text="Generate SQL", command=handle_generate, bg="#007BFF", fg="white", font=("Arial", 12))
generate_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

# Result text area with a copy button
result_frame = ttk.Frame(window, padding="10")
result_frame.grid(row=7, column=0, sticky="nsew", padx=10, pady=5)

result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=120, height=15, font=("Consolas", 10))
result_text.grid(row=0, column=0, padx=5, pady=5)

copy_button = tk.Button(result_frame, text="📋 Copy", command=copy_to_clipboard, bg="#28a745", fg="white", font=("Arial", 10))
copy_button.grid(row=0, column=1, padx=5, pady=5, sticky="n")

# Adjust column and row weights for resizing
window.grid_rowconfigure(7, weight=1)
window.grid_columnconfigure(0, weight=1)

# Start the main loop
window.mainloop()

