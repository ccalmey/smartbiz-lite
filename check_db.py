



#SMARTBIZ MVP 
#SYSTEM DEVELOPER: CALMEY CROWN @rown.calmey 
#START DATE: 18.12.2025
#UPDATE: 18.12.2025

# app.py
# SMARTBIZ LITE ¡ª Flask App


import sqlite3

conn = sqlite3.connect("smartbiz.db")
cur = conn.cursor()

cur.execute("SELECT * FROM sales")
print(cur.fetchall())

cur.execute("SELECT * FROM expenses")
print(cur.fetchall())

conn.close()