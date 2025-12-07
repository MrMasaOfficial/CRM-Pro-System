import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name: str = "crm.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                city TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_customer(self, name: str, phone: str = "", email: str = "", 
                     address: str = "", city: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, phone, email, address, city)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, phone, email, address, city))
        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()
        return customer_id
    
    def get_all_customers(self) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, phone, email, address, city FROM customers ORDER BY name')
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    def get_customer(self, customer_id: int) -> Optional[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, phone, email, address, city FROM customers WHERE id = ?', (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return customer
    
    def update_customer(self, customer_id: int, name: str, phone: str = "", 
                       email: str = "", address: str = "", city: str = ""):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers 
            SET name = ?, phone = ?, email = ?, address = ?, city = ?
            WHERE id = ?
        ''', (name, phone, email, address, city, customer_id))
        conn.commit()
        conn.close()
    
    def delete_customer(self, customer_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()
    
    def search_customers(self, search_term: str) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute('''
            SELECT id, name, phone, email, address, city FROM customers 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR city LIKE ?
            ORDER BY name
        ''', (search_pattern, search_pattern, search_pattern, search_pattern))
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    def add_sale(self, customer_id: int, product: str, quantity: int, 
                 price: float, notes: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        total = quantity * price
        cursor.execute('''
            INSERT INTO sales (customer_id, product, quantity, price, total, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, product, quantity, price, total, notes))
        conn.commit()
        sale_id = cursor.lastrowid
        conn.close()
        return sale_id
    
    def get_all_sales(self) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, s.customer_id, c.name, s.product, s.quantity, 
                   s.price, s.total, s.sale_date, s.notes
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            ORDER BY s.sale_date DESC
        ''')
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    def get_customer_sales(self, customer_id: int) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, customer_id, product, quantity, price, total, sale_date, notes
            FROM sales
            WHERE customer_id = ?
            ORDER BY sale_date DESC
        ''', (customer_id,))
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    def delete_sale(self, sale_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sales WHERE id = ?', (sale_id,))
        conn.commit()
        conn.close()
    
    def get_customer_total_sales(self, customer_id: int) -> float:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(total) FROM sales WHERE customer_id = ?', (customer_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result[0] is not None else 0.0
    
    def search_sales(self, search_term: str) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute('''
            SELECT s.id, s.customer_id, c.name, s.product, s.quantity, 
                   s.price, s.total, s.sale_date, s.notes
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            WHERE c.name LIKE ? OR s.product LIKE ?
            ORDER BY s.sale_date DESC
        ''', (search_pattern, search_pattern))
        sales = cursor.fetchall()
        conn.close()
        return sales
