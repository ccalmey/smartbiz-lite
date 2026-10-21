#SMARTBIZ MVP 
#SYSTEM DEVELOPER: CALMEY CROWN @rown.calmey 
#START DATE: 3.12.2025
#UPDATE: 15.04.2026

# app.py
# SMARTBIZ LITE ¡ª Flask App

from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, request, redirect, url_for, session, flash 

from functools import wraps

from datetime import datetime

from db import get_db_connection, DB_PATH

app = Flask(__name__)



BUSINESS_PIN_HASH = generate_password_hash('1234')

app.secret_key = 'smartbiz-lite-secret'


# ----------MAIN ROUTES ----------

# ---------- LOGIN ROUTE ----------------------------------------------------------------------------------



# ---------- LOGOUT ROUTE --------------------------------------------------------------------------

#DEBUG ROUTE (TEMP)

@app.route("/debug/path")
def debug_path():
    from db import DB_PATH
    return DB_PATH
    
# ---------- HELPER FUNCTIONS -----------------------------------------------------------------------

def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
    
def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0

# ---------- HOME ROUTE ------------------------------------------------------------------------------

@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    
    #TOTALS (Summary)
    cur.execute("SELECT COALESCE(SUM(total), 0) FROM sales")
    total_sales = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    total_expenses = cur.fetchone()[0]
    
    profit = total_sales - total_expenses
    
    #DAILY SALES (today)
    cur.execute("""
                SELECT COALESCE(SUM(amount*quantity), 0)
                FROM sales
                WHERE DATE(created_at) =
                DATE('now')
                """)
    today_sales = cur.fetchone()[0]
    
    #DAILY EXPENSES (today)
    cur.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE DATE(created_at) = 
                DATE('now')
                """)
    today_expenses = cur.fetchone()[0]
    today_profit = today_sales - today_expenses
    
    #FETCH RECENT ACTIVITY WITH TIMESTAMPS
    cur.execute("""
                SELECT item, amount, quantity, total, created_at
                FROM sales
                ORDER BY created_at DESC
                LIMIT 5
                """)
    recent_sales = cur.fetchall()
    
    cur.execute("""
                SELECT id, name, amount, created_at
                FROM expenses
                WHERE deleted = 0
                ORDER BY created_at DESC
                LIMIT 5
                """)
    recent_expenses = cur.fetchall()
    
    #TODAY'S TOP ITEMS
    
    cur.execute("""
                SELECT item,
                SUM(quantity) AS total_qty,
                SUM(total) AS total_amount
                FROM sales
                WHERE DATE (created_at) = 
                DATE('now')
                GROUP BY item
                ORDER BY total_amount DESC
                """)
    daily_top_items = cur.fetchall()
    
    #THIS WEEK'S TOP ITEMS
    
    cur.execute("""
                SELECT
                item,
                SUM(quantity) as total_qty,
                SUM(total) as total_amount
                FROM sales
                WHERE DATE(created_at) >=
                DATE('now', 'weekday 1', '-7 days')
                GROUP BY item
                ORDER BY total_amount DESC
                LIMIT 5
                """)
    weekly_top_items = cur.fetchall()
    
    # WEEKLY SALES (Mon - Today)
    cur.execute("""
                SELECT COALESCE(SUM(total), 0)
                FROM sales
                WHERE DATE(created_at) >= 
                DATE('now', 'weekday 1', '-7 days')
                """)
    week_sales = cur.fetchone()[0]
    
    # WEEKLY EXPENSES (Mon - Today)
    cur.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE DATE(created_at) >=
                DATE('now', 'weekday 1', '-7 days')
                """)
    
    week_expenses = cur.fetchone()[0]
    
    week_profit = week_sales - week_expenses
    
    #MONTHLY SALES (current Month)

    #CURRENT MONTH SALLES(for display)

    current_month = datetime.now().strftime("%B %Y")

    #MONTHLY SUMMARY (current month only)
    cur.execute("""
                SELECT COALESCE(SUM(total), 0) AS sales
                FROM sales
                WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
                """)
    month_sales = cur.fetchone()['sales']
    
    #MONTHLY EXPENSES (current Month)
    cur.execute("""
                SELECT COALESCE(SUM(amount), 0) AS expenses
                FROM expenses
                WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
                """)
    month_expenses = cur.fetchone()['expenses']
    
    month_profit = month_sales - month_expenses

    monthly = [{
        'month': current_month,
        'sales': month_sales,
        'expenses':month_expenses,
        'profit':month_profit
    }]
    
    #DAILY BREAKDOWN (This Week)
    cur.execute("""
                SELECT
                DATE (created_at)as day,
                SUM(total)as sales
                FROM sales
                WHERE DATE(created_at) >= 
                DATE('now', 'weekday 1', '-7 days')
                GROUP BY day
                """)
    daily_sales = {row['day']: row['sales'] for row in cur.fetchall()}
    
    cur.execute("""
                SELECT 
                DATE(created_at) as day,
                SUM(amount) as expenses
                FROM expenses 
                WHERE DATE (created_at) >=
                DATE('now', 'weekday 1', '-7 days')
                GROUP BY day
                """)
    daily_expenses = {row['day']: row['expenses'] for row in cur.fetchall()}
    
    weekly_breakdown = []
    
    for day in set(daily_sales) | set(daily_expenses):
        sales = daily_sales.get(day, 0)
        expenses = daily_expenses.get(day, 0)
        
        weekly_breakdown.append({
            'day': day,
            'sales': sales,
            'expenses': expenses,
            'profit': sales - expenses
        })
        
    weekly_breakdown.sort(key=lambda x: x['day'])
    
    #MONTLY BUSINESS SUMMARY (for dashboard)
    cur.execute("""
                SELECT strftime('%Y-%m', created_at) AS month,
                    SUM(total) AS sales
                FROM sales
                GROUP BY month
                ORDER BY month DESC
                """)
    sales_by_month = cur.fetchall()
    
    cur.execute("""
                SELECT strftime('%Y-%m', created_at) AS month,
                    SUM(amount) AS expenses
                FROM expenses
                GROUP BY month
                ORDER BY month DESC
                """)
    expenses_by_month = cur.fetchall()
    
    sales_map = {row['month']: row['sales']
                 for row in sales_by_month}
    
    expenses_map = {row['month']: row['expenses']
                    for row in expenses_by_month}
    
    months = sorted(set(sales_map) | set(expenses_map), reverse=True)
    
    monthly = []
    for m in months:
        s = sales_map.get(m,0)
        e = expenses_map.get(m,0)

        readable_month = datetime.strptime(m, "%Y-%m").strftime("%B %Y")

        monthly.append({
            'month' : readable_month,
            'sales' : s,
            'expenses' : e,
            'profit': s - e,
        })
        
    #MONTHLY TOP ITEMS(for dashboard)
    cur.execute("""
                    SELECT
                        strftime('%Y-%m', created_at) AS month,
                        item,
                        SUM(quantity) AS total_qty,
                        SUM(total) AS total_amount
                    FROM sales
                    WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
                    GROUP BY item
                    ORDER BY total_amount DESC
                    LIMIT 5
                    """)
    rows = cur.fetchall()

    monthly_items = []
    for row in rows:
        readable_month = datetime.strptime(row["month"], "%Y-%m").strftime("%B %Y")

        monthly_items.append({
            "month": readable_month,
            "item": row["item"],
            "total_qty": row["total_qty"],
            "total_amount": row["total_amount"]
        })
    conn.close()

    return render_template(
        "index.html",
        total_sales=total_sales,
        total_expenses=total_expenses,
        profit=profit,
        today_sales=today_sales,
        today_expenses=today_expenses,
        today_profit=today_profit,
        daily_top_items=daily_top_items,
        weekly_top_items=weekly_top_items,
        week_sales=week_sales,
        week_expenses=week_expenses,
        week_profit=week_profit,
        weekly_breakdown=weekly_breakdown,
        recent_sales=recent_sales,
        recent_expenses=recent_expenses,
        monthly=monthly,
        monthly_items=monthly_items
        
    )

# ---------- SALES ROUTE -----------------------------------------------------------------------------------
@app.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "POST":
        item = request.form.get("item", "").strip()
        amount_raw = request.form.get("amount", "")
        quantity_raw = request.form.get("quantity", "")
        
        if not item or not amount_raw or not quantity_raw:
            flash("All fields are required", "error")
            return render_template("sales.html")
    
        amount = to_float(amount_raw)
        quantity = to_int(quantity_raw)
        
        if amount <= 0 or quantity <= 0:
            flash("Amount and quantity must be greater than Zero", "error")
            return render_template("sales.html")
        
        total = amount * quantity
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO sales (item, amount, quantity, total, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (item, amount, quantity, total, created_at))

        conn.commit()
        conn.close()
        
        flash("Sale added successfully!", "success") 
        
        return redirect(url_for("home"))

    return render_template("sales.html")

# ---------- EDIT SALES ROUTE -----------------------------------------------------------------------------------
@app.route("/sales/edit/<int:sale_id>", methods=["GET", "POST"])
def edit_sale(sale_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        item = request.form['item'] 
        amount = float(request.form['amount'])
        quantity = int(request.form['quantity'])
        total = amount * quantity
        
        cur.execute("""
                    UPDATE sales
                    SET item=?, amount=?, quantity=?, total=?
                    WHERE id=?
                    """, (item, amount, quantity, total, sale_id))
        
        conn.commit()
        conn.close()
        
        flash("Sales updated successfully!", "success")
        
        return redirect(url_for ('sales_history'))
    
    cur.execute("SELECT * FROM sales WHERE id=?", (sale_id,))
    
    sale = cur.fetchone()
    conn.close()
    
    return render_template('edit_sale.html', sale=sale)
   
 
# ---------- DELETE SALES ROUTE -----------------------------------------------------------------------------------
@app.route("/sales/delete/<int:sale_id>", methods=["GET", "POST"])
def delete_sale(sale_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    #FETCH SALE BEFORE DELETING
    cur.execute("SELECT * FROM  sales WHERE id=?", (sale_id,))
    sale = cur.fetchone()
    
    if sale:
        session['undo_sale'] = dict(sale)
        
        cur.execute("DELETE FROM sales WHERE id=?", (sale_id,))
        conn.commit()
        flash("Sale Deleted. Undo?", "undo_sale")
    
    conn.close()
    
    return redirect (url_for ('sales_history'))

# ---------- TEST ROUTE -------------------------------------------------

#@app.route("/pin-delete-test")
#def pin_delete_test():
    #return "CONFIRM DELETE ROUTE IS LIVE"

# ---------- CONFIRM DELETE SALES ROUTE -------------------------------------------------


# ---------- UNDO SALES ROUTE -------------------------------------------------------------
@app.route("/undo-sale", methods=["POST"])
def undo_sale():
    sale = session.pop('undo_sale', None)
    
    if sale:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
                    INSERT INTO sales (item, amount, quantity, total, created_at)
                    VALUES (?,?,?,?,?)
                    """,(
                        sale['item'],
                        sale['amount'],
                        sale['quantity'],
                        sale['total'],
                        sale['created_at']
                    ))
        conn.commit()
        conn.close()
        
        flash("Sale restored successfully", 'success')
        
    return redirect(url_for("sales_history"))

# ---------- SALES HISTORY ROUTE ------------------------------------------------------------------------------------

@app.route('/history/sales')
def sales_history():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
                SELECT id, item, amount, quantity, total, created_at
                FROM sales
                ORDER BY created_at DESC
                LIMIT 20
                """)
    sales = cur.fetchall()
    
    conn.close()
    
    return render_template('sales_history.html', sales=sales)

# ---------- EXPENSES ROUTE --------------------------------------------------------------------------------

@app.route("/expenses", methods=["GET", "POST"])
def expenses():
    if request.method == "POST":
        name = request.form["name"]
        amount = to_float(request.form.get("amount"))

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO expenses (name, amount, created_at)
            VALUES (?, ?, ?)
        """, (name, amount, created_at))

        conn.commit()
        conn.close()
        
        flash("Expense added successfully!", "success")

        return redirect(url_for("home"))

    return render_template("expenses.html")

# ---------- EDIT EXPENSES ROUTE ------------------------------------------------------------------------

@app.route('/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name'] 
        amount = float(request.form['amount'])
        total = amount
        
        cur.execute("""
                    UPDATE expenses
                    SET name=?, amount=?
                    WHERE id=?
                    """, (name, amount, expense_id,))
        
        conn.commit()
        conn.close()
        
        flash("Expense updated successfully!", "success")
        
        return redirect(url_for ('expenses_history'))
    
    cur.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    
    expenses = cur.fetchone()
    conn.close()
    
    return render_template('edit_expense.html', expenses=expenses)

# ---------- DELETE EXPENSES ROUTE ------------------------------------------------------------------------
@app.route("/expenses/delete/<int:expense_id>", methods=['GET', 'POST'])
def delete_expense(expense_id):
    conn = get_db_connection()
    cur = conn.cursor()
        
    #Fetch before delete
    cur.execute("SELECT * FROM expenses WHERE id =?", (expense_id,))
    expenses = cur.fetchone()
    
    if expenses:
        session["undo_expense"] = dict(expenses)
        
        cur.execute("""
                    UPDATE expenses
                    SET deleted = 1
                    WHERE id = ?
                    """, (expense_id,))
        conn.commit()
        flash("Expense deleted. Undo?", 'undo_expense')
        
    conn.close()
    return redirect(url_for("expenses_history"))

# ---------- UNDO EXPENSES ROUTE ------------------------------------------------------------------------
@app.route("/undo-expense", methods=["POST"])
def undo_expense():
    expenses = session.pop('undo_expense', None)
    
    if expenses:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
                    INSERT INTO expenses ( name, amount, created_at, deleted)
                    VALUES (?,?,?,0)
                    """,(
                        expenses['name'],
                        expenses['amount'],
                        expenses['created_at']
                    ))
        conn.commit()
        conn.close()
        
        flash("Expense restored successfully", 'success')
        
    return redirect(url_for("expenses_history"))

# ---------- EXPENSES HISTORY ROUTE ------------------------------------------------------------------------

@app.route('/history/expenses')
def expenses_history():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
                SELECT id, name, amount, created_at
                FROM expenses
                WHERE deleted = 0 OR deleted is NULL
                ORDER BY created_at DESC
                LIMIT 20
                """)
    expenses = cur.fetchall()
    conn.close()
    
    return render_template('expenses_history.html', expenses=expenses)

# ---------- DAILY TOTALS ROUTE ------------------------------------------------------------------------


@app.route('/daily')
def daily_totals():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
                SELECT DATE(created_at) AS day, 
                SUM(amount * quantity) AS sales
                FROM sales
                GROUP BY day
                ORDER BY day DESC
                """)
    sales_by_day = cur.fetchall()
    cur.execute("""
                SELECT DATE(created_at) AS day, 
                SUM(amount) AS expenses
                FROM expenses
                GROUP BY day
                ORDER BY day DESC
                """)
    expenses_by_day = cur.fetchall()
    
    
    cur.execute("""
                SELECT item,
                SUM(quantity) AS total_qty,
                SUM(total) AS total_amount
                FROM sales
                WHERE DATE(created_at) = DATE('now')
                GROUP BY item
                ORDER BY total_amount DESC
                """)
    today_item_totals = cur.fetchall()
    
    conn.close()
    
    sales_map = {row['day']: row['sales'] for row in sales_by_day} 
    expenses_map = {row['day']: row['expenses'] for row in expenses_by_day}
    
    days = sorted(set(sales_map) | set(expenses_map), reverse=True)
    
    daily = []
    for day in days:
        s = sales_map.get(day,0)
        e = expenses_map.get(day,0)
        daily.append({
            'day':day,
            'sales': s,
            'expenses': e,
            'profit': s - e,
        })
        
    return render_template('daily.html', daily=daily)

@app.route("/monthly")
def monthly_totals():
    conn = get_db_connection()
    cur = conn.cursor()

    # MONTHLY SALES
    cur.execute("""
        SELECT strftime('%Y-%m', created_at) AS month,
               SUM(total) AS sales
        FROM sales
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month DESC
    """)
    sales_by_month = cur.fetchall()

    # MONTHLY EXPENSES
    cur.execute("""
        SELECT strftime('%Y-%m', created_at) AS month,
               SUM(amount) AS expenses
        FROM expenses
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month DESC
    """)
    expenses_by_month = cur.fetchall()

    # MONTHLY TOP ITEMS
    cur.execute("""
        SELECT strftime('%Y-%m', created_at) AS month,
               item,
               SUM(quantity) AS total_qty,
               SUM(total) AS total_amount
        FROM sales
        GROUP BY month, item
        ORDER BY month DESC, total_amount DESC
    """)
    monthly_items = cur.fetchall()

    conn.close()

    sales_map = {row['month']: row['sales'] for row in sales_by_month}
    expenses_map = {row['month']: row['expenses'] for row in expenses_by_month}

    months = sorted(set(sales_map) | set(expenses_map), reverse=True)

    monthly = []
    for m in months:
        s = sales_map.get(m, 0)
        e = expenses_map.get(m, 0)
        monthly.append({
            'month': m,
            'sales': s,
            'expenses': e,
            'profit': s - e
        })

    return render_template("monthly.html", monthly=monthly, monthly_items=monthly_items)

# ---------- START APP ----------
if __name__ == "__main__":
    print("[!] Hello CALMEY: Using Database at:", DB_PATH)
    #print('\n--- REGISTERED ROUTES---')
    #for rule in app.url_map.iter_rules():
    #    print(rule)
    #    print('--------------\n')
    #print(app.url_map)
    
    app.run(debug=True)
#SALES BY PROCUCT
#AMOUNT FORMAT