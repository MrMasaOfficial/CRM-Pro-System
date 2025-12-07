from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
    QDialog, QFormLayout, QTabWidget, QSpinBox, QDoubleSpinBox,
    QTextEdit, QDateTimeEdit, QComboBox, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt, QDateTime, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap
from db import Database

STYLE_SHEET = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    
    QTabWidget::pane {
        border: 1px solid #ddd;
    }
    
    QTabBar::tab {
        background-color: #e0e0e0;
        color: #333;
        padding: 8px 20px;
        margin-right: 2px;
        border: 1px solid #999;
        border-bottom: none;
        border-radius: 4px 4px 0 0;
        font-weight: bold;
    }
    
    QTabBar::tab:selected {
        background-color: #2196F3;
        color: white;
    }
    
    QTabBar::tab:hover {
        background-color: #1976D2;
    }
    
    QPushButton {
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 11px;
    }
    
    QPushButton:hover {
        background-color: #1976D2;
    }
    
    QPushButton:pressed {
        background-color: #0d47a1;
    }
    
    QPushButton#deleteBtn {
        background-color: #f44336;
    }
    
    QPushButton#deleteBtn:hover {
        background-color: #d32f2f;
    }
    
    QLineEdit {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 6px;
        background-color: white;
        font-size: 11px;
    }
    
    QLineEdit:focus {
        border: 2px solid #2196F3;
    }
    
    QTableWidget {
        border: 1px solid #ddd;
        gridline-color: #e0e0e0;
        background-color: white;
    }
    
    QTableWidget::item {
        padding: 5px;
    }
    
    QTableWidget::item:selected {
        background-color: #2196F3;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #1976D2;
        color: white;
        padding: 5px;
        border: none;
        font-weight: bold;
    }
    
    QComboBox {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 6px;
        background-color: white;
    }
    
    QComboBox:focus {
        border: 2px solid #2196F3;
    }
    
    QComboBox::drop-down {
        border: none;
    }
    
    QSpinBox, QDoubleSpinBox {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 6px;
        background-color: white;
    }
    
    QSpinBox:focus, QDoubleSpinBox:focus {
        border: 2px solid #2196F3;
    }
    
    QTextEdit {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 6px;
        background-color: white;
    }
    
    QTextEdit:focus {
        border: 2px solid #2196F3;
    }
    
    QLabel {
        color: #333;
    }
    
    QDialog {
        background-color: #f5f5f5;
    }
"""

class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer_data=None):
        super().__init__(parent)
        self.customer_data = customer_data
        self.init_ui()
        if customer_data:
            self.load_customer_data()
    
    def init_ui(self):
        self.setWindowTitle("إضافة عميل جديد" if not self.customer_data else "تعديل بيانات العميل")
        self.setGeometry(100, 100, 450, 350)
        self.setStyleSheet(STYLE_SHEET)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("معلومات العميل" if self.customer_data else "بيانات العميل الجديد")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("أدخل اسم العميل")
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("رقم الهاتف")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("البريد الإلكتروني")
        
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("العنوان")
        
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("المدينة")
        
        label_font = QFont()
        label_font.setBold(True)
        
        name_lbl = QLabel("الاسم:")
        name_lbl.setFont(label_font)
        form_layout.addRow(name_lbl, self.name_input)
        
        phone_lbl = QLabel("الهاتف:")
        phone_lbl.setFont(label_font)
        form_layout.addRow(phone_lbl, self.phone_input)
        
        email_lbl = QLabel("البريد الإلكتروني:")
        email_lbl.setFont(label_font)
        form_layout.addRow(email_lbl, self.email_input)
        
        address_lbl = QLabel("العنوان:")
        address_lbl.setFont(label_font)
        form_layout.addRow(address_lbl, self.address_input)
        
        city_lbl = QLabel("المدينة:")
        city_lbl.setFont(label_font)
        form_layout.addRow(city_lbl, self.city_input)
        
        layout.addLayout(form_layout)
        layout.addSpacing(20)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        save_btn = QPushButton("✓ حفظ")
        save_btn.setMinimumWidth(100)
        cancel_btn = QPushButton("✕ إلغاء")
        cancel_btn.setMinimumWidth(100)
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_customer_data(self):
        self.name_input.setText(self.customer_data[1])
        self.phone_input.setText(self.customer_data[2] or "")
        self.email_input.setText(self.customer_data[3] or "")
        self.address_input.setText(self.customer_data[4] or "")
        self.city_input.setText(self.customer_data[5] or "")
    
    def get_data(self):
        return {
            'name': self.name_input.text(),
            'phone': self.phone_input.text(),
            'email': self.email_input.text(),
            'address': self.address_input.text(),
            'city': self.city_input.text()
        }

class SaleDialog(QDialog):
    def __init__(self, parent=None, db=None, customer_id=None):
        super().__init__(parent)
        self.db = db
        self.customer_id = customer_id
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("تسجيل مبيعة جديدة")
        self.setGeometry(100, 100, 550, 450)
        self.setStyleSheet(STYLE_SHEET)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("تسجيل مبيعة")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.customer_combo = QComboBox()
        self.update_customers_list()
        
        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("اسم المنتج")
        
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setMinimum(1)
        self.quantity_spinbox.setValue(1)
        self.quantity_spinbox.setMaximum(10000)
        
        self.price_spinbox = QDoubleSpinBox()
        self.price_spinbox.setMinimum(0.0)
        self.price_spinbox.setDecimals(2)
        self.price_spinbox.setMaximum(999999.99)
        
        self.total_label = QLabel("0.00")
        total_font = QFont()
        total_font.setBold(True)
        total_font.setPointSize(11)
        self.total_label.setFont(total_font)
        self.total_label.setStyleSheet("color: #2196F3;")
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("أضف ملاحظات اختيارية...")
        self.notes_input.setMaximumHeight(100)
        
        label_font = QFont()
        label_font.setBold(True)
        
        customer_lbl = QLabel("العميل:")
        customer_lbl.setFont(label_font)
        form_layout.addRow(customer_lbl, self.customer_combo)
        
        product_lbl = QLabel("المنتج:")
        product_lbl.setFont(label_font)
        form_layout.addRow(product_lbl, self.product_input)
        
        qty_lbl = QLabel("الكمية:")
        qty_lbl.setFont(label_font)
        form_layout.addRow(qty_lbl, self.quantity_spinbox)
        
        price_lbl = QLabel("السعر (للوحدة):")
        price_lbl.setFont(label_font)
        form_layout.addRow(price_lbl, self.price_spinbox)
        
        total_lbl = QLabel("الإجمالي:")
        total_lbl.setFont(label_font)
        form_layout.addRow(total_lbl, self.total_label)
        
        notes_lbl = QLabel("الملاحظات:")
        notes_lbl.setFont(label_font)
        form_layout.addRow(notes_lbl, self.notes_input)
        
        layout.addLayout(form_layout)
        layout.addSpacing(20)
        
        self.quantity_spinbox.valueChanged.connect(self.update_total)
        self.price_spinbox.valueChanged.connect(self.update_total)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        save_btn = QPushButton("✓ حفظ المبيعة")
        save_btn.setMinimumWidth(120)
        cancel_btn = QPushButton("✕ إلغاء")
        cancel_btn.setMinimumWidth(100)
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        if self.customer_id:
            for i in range(self.customer_combo.count()):
                if int(self.customer_combo.itemData(i)) == self.customer_id:
                    self.customer_combo.setCurrentIndex(i)
                    break
    
    def update_customers_list(self):
        self.customer_combo.clear()
        customers = self.db.get_all_customers()
        for customer in customers:
            self.customer_combo.addItem(customer[1], customer[0])
    
    def update_total(self):
        total = self.quantity_spinbox.value() * self.price_spinbox.value()
        self.total_label.setText(f"{total:.2f}")
    
    def get_data(self):
        return {
            'customer_id': int(self.customer_combo.currentData()),
            'product': self.product_input.text(),
            'quantity': self.quantity_spinbox.value(),
            'price': self.price_spinbox.value(),
            'notes': self.notes_input.toPlainText()
        }

class CRMApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("CRM Pro System")
        self.setApplicationVersion("1.0.0")
        self.setStyle('Fusion')
        self.setStyleSheet(STYLE_SHEET)
        
        self.db = Database()
        self.main_window = MainWindow(self.db)
        self.main_window.show()

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setStyleSheet(STYLE_SHEET)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("نظام إدارة العملاء - CRM Pro")
        self.setGeometry(100, 100, 1400, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        
        self.customers_tab = QWidget()
        self.sales_tab = QWidget()
        
        self.init_customers_tab()
        self.init_sales_tab()
        
        self.tabs.addTab(self.customers_tab, "العملاء")
        self.tabs.addTab(self.sales_tab, "المبيعات")
        
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
    
    def init_customers_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        header = QLabel("إدارة العملاء")
        header_font = QFont()
        header_font.setPointSize(13)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        search_label = QLabel("🔍 بحث:")
        search_label_font = QFont()
        search_label_font.setBold(True)
        search_label.setFont(search_label_font)
        
        self.customer_search = QLineEdit()
        self.customer_search.setPlaceholderText("ابحث باسم أو هاتف أو بريد أو مدينة...")
        self.customer_search.setMinimumHeight(35)
        self.customer_search.textChanged.connect(self.search_customers)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.customer_search)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        add_btn = QPushButton("➕ إضافة عميل")
        add_btn.setMinimumHeight(35)
        add_btn.setMinimumWidth(120)
        
        edit_btn = QPushButton("✏️ تعديل")
        edit_btn.setMinimumHeight(35)
        edit_btn.setMinimumWidth(100)
        
        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.setObjectName("deleteBtn")
        delete_btn.setMinimumHeight(35)
        delete_btn.setMinimumWidth(100)
        
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.setMinimumWidth(100)
        
        add_btn.clicked.connect(self.add_customer)
        edit_btn.clicked.connect(self.edit_customer)
        delete_btn.clicked.connect(self.delete_customer)
        refresh_btn.clicked.connect(self.load_customers)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(6)
        self.customers_table.setHorizontalHeaderLabels(
            ["معرف", "الاسم", "الهاتف", "البريد الإلكتروني", "العنوان", "المدينة"]
        )
        self.customers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.customers_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.customers_table.setSelectionMode(QTableWidget.SingleSelection)
        self.customers_table.setRowHeight(25, 25)
        self.customers_table.setAlternatingRowColors(True)
        
        layout.addLayout(search_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.customers_table)
        
        self.customers_tab.setLayout(layout)
        self.load_customers()
    
    def load_customers(self):
        customers = self.db.get_all_customers()
        self.customers_table.setRowCount(0)
        
        for row, customer in enumerate(customers):
            self.customers_table.insertRow(row)
            for col, data in enumerate(customer):
                self.customers_table.setItem(row, col, QTableWidgetItem(str(data)))
    
    def search_customers(self):
        search_term = self.customer_search.text()
        if not search_term:
            self.load_customers()
            return
        
        customers = self.db.search_customers(search_term)
        self.customers_table.setRowCount(0)
        
        for row, customer in enumerate(customers):
            self.customers_table.insertRow(row)
            for col, data in enumerate(customer):
                self.customers_table.setItem(row, col, QTableWidgetItem(str(data)))
    
    def add_customer(self):
        dialog = CustomerDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            if not data['name']:
                QMessageBox.warning(self, "تحذير", "يجب إدخال اسم العميل")
                return
            
            self.db.add_customer(
                data['name'],
                data['phone'],
                data['email'],
                data['address'],
                data['city']
            )
            self.load_customers()
            QMessageBox.information(self, "نجاح", "تم إضافة العميل بنجاح")
    
    def edit_customer(self):
        current_row = self.customers_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "تحذير", "اختر عميل لتعديله")
            return
        
        customer_id = int(self.customers_table.item(current_row, 0).text())
        customer_data = self.db.get_customer(customer_id)
        
        dialog = CustomerDialog(self, customer_data)
        if dialog.exec_():
            data = dialog.get_data()
            if not data['name']:
                QMessageBox.warning(self, "تحذير", "يجب إدخال اسم العميل")
                return
            
            self.db.update_customer(
                customer_id,
                data['name'],
                data['phone'],
                data['email'],
                data['address'],
                data['city']
            )
            self.load_customers()
            QMessageBox.information(self, "نجاح", "تم تحديث بيانات العميل بنجاح")
    
    def delete_customer(self):
        current_row = self.customers_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "تحذير", "اختر عميل لحذفه")
            return
        
        customer_id = int(self.customers_table.item(current_row, 0).text())
        customer_name = self.customers_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل تريد حذف العميل '{customer_name}'؟\nسيتم حذف جميع مبيعاته أيضاً",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_customer(customer_id)
            self.load_customers()
            QMessageBox.information(self, "نجاح", "تم حذف العميل بنجاح")
    
    def init_sales_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        header = QLabel("تتبع المبيعات")
        header_font = QFont()
        header_font.setPointSize(13)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        search_label = QLabel("🔍 بحث:")
        search_label_font = QFont()
        search_label_font.setBold(True)
        search_label.setFont(search_label_font)
        
        self.sales_search = QLineEdit()
        self.sales_search.setPlaceholderText("ابحث باسم العميل أو المنتج...")
        self.sales_search.setMinimumHeight(35)
        self.sales_search.textChanged.connect(self.search_sales)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.sales_search)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        add_btn = QPushButton("➕ إضافة مبيعة")
        add_btn.setMinimumHeight(35)
        add_btn.setMinimumWidth(130)
        
        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.setObjectName("deleteBtn")
        delete_btn.setMinimumHeight(35)
        delete_btn.setMinimumWidth(100)
        
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.setMinimumWidth(100)
        
        add_btn.clicked.connect(self.add_sale)
        delete_btn.clicked.connect(self.delete_sale)
        refresh_btn.clicked.connect(self.load_sales)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(9)
        self.sales_table.setHorizontalHeaderLabels(
            ["معرف", "م.ع", "اسم العميل", "المنتج", "الكمية", "السعر", "الإجمالي", "التاريخ", "الملاحظات"]
        )
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.setSelectionMode(QTableWidget.SingleSelection)
        self.sales_table.setRowHeight(25, 25)
        self.sales_table.setAlternatingRowColors(True)
        
        layout.addLayout(search_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.sales_table)
        
        self.sales_tab.setLayout(layout)
        self.load_sales()
    
    def load_sales(self):
        sales = self.db.get_all_sales()
        self.sales_table.setRowCount(0)
        
        for row, sale in enumerate(sales):
            self.sales_table.insertRow(row)
            for col, data in enumerate(sale):
                self.sales_table.setItem(row, col, QTableWidgetItem(str(data)))
    
    def search_sales(self):
        search_term = self.sales_search.text()
        if not search_term:
            self.load_sales()
            return
        
        sales = self.db.search_sales(search_term)
        self.sales_table.setRowCount(0)
        
        for row, sale in enumerate(sales):
            self.sales_table.insertRow(row)
            for col, data in enumerate(sale):
                self.sales_table.setItem(row, col, QTableWidgetItem(str(data)))
    
    def add_sale(self):
        customers = self.db.get_all_customers()
        if not customers:
            QMessageBox.warning(self, "تحذير", "يجب إضافة عميل أولاً")
            return
        
        dialog = SaleDialog(self, self.db)
        if dialog.exec_():
            data = dialog.get_data()
            if not data['product']:
                QMessageBox.warning(self, "تحذير", "يجب إدخال اسم المنتج")
                return
            
            self.db.add_sale(
                data['customer_id'],
                data['product'],
                data['quantity'],
                data['price'],
                data['notes']
            )
            self.load_sales()
            QMessageBox.information(self, "نجاح", "تم إضافة المبيعة بنجاح")
    
    def delete_sale(self):
        current_row = self.sales_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "تحذير", "اختر مبيعة لحذفها")
            return
        
        sale_id = int(self.sales_table.item(current_row, 0).text())
        
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            "هل تريد حذف هذه المبيعة؟",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_sale(sale_id)
            self.load_sales()
            QMessageBox.information(self, "نجاح", "تم حذف المبيعة بنجاح")
