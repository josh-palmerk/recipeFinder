import sys
import mysql.connector
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QWidget, QComboBox, QListWidget, QListWidgetItem, QLineEdit
try:
    from config import db_config
except:
    print("Config file error. Please arrange DB credentials as db_config <dict> in config.py")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RecipeBase GUI")
        self.resize(800, 600)

        # Create various widgets
        self.table = QTableWidget()
        self.table.setColumnCount(0)
        self.table.setHorizontalHeaderLabels([])
        self.table.setSortingEnabled(True)

        self.columns_list = QListWidget()

        self.table_combo = QComboBox()
        # self.columns_combo = QComboBox()

        self.query_type_combo = QComboBox()
        self.query_type_combo.addItems(["SELECT", "INSERT", "UPDATE", "DELETE"])

        self.btn_execute = QPushButton("Execute")

        self.replace_line_edit = QLineEdit()
        self.int_line_edit = IntegerLineEdit()

        self.btn_execute.clicked.connect(self.execute_query)

        # Widget Attributes
        self.replace_line_edit.setPlaceholderText("Input")
        self.int_line_edit.setPlaceholderText("(table_)id")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.table_combo)
        # layout.addWidget(self.columns_combo)
        layout.addWidget(self.query_type_combo)
        layout.addWidget(self.btn_execute)
        layout.addWidget(self.columns_list)
        layout.addWidget(self.replace_line_edit)
        layout.addWidget(self.int_line_edit)
        self.replace_line_edit.hide()
        self.int_line_edit.hide()

        # Main widget
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Populate tables combo box
        self.populate_tables_combo()

        # Connect signals
        self.query_type_combo.currentIndexChanged.connect(self.handle_query_type_change)
        # if self.columns_list is not type('NoneType'): 
        #   self.table_combo.currentIndexChanged.connect(self.adjust_list_widget_height(self.columns_list))

        self.table_combo.currentIndexChanged.connect(self.populate_columns_list)

        # Set default table display
        self.populate_columns_list()
        self.select_data(self.table_combo.currentText(), [self.columns_list.item(i).text() for i in range(self.columns_list.count())])

    def adjust_list_widget_height(self, list_widget) -> None:
        # Calculate the total height based on the height of each item
        total_height = sum(list_widget.sizeHintForRow(row) for row in range(list_widget.count()))
        list_widget.setFixedHeight(total_height)

    def handle_query_type_change(self, index):
        # Show/hide QLineEdit widgets based on the selected query type
        query_type = self.query_type_combo.itemText(index)
        if query_type == "INSERT":
            self.replace_line_edit.show()
            self.int_line_edit.hide()
        elif query_type == "UPDATE":
            self.int_line_edit.show()
            self.replace_line_edit.show()
        elif query_type == "DELETE":
            self.int_line_edit.show()
            self.replace_line_edit.hide()    
        else:
            self.replace_line_edit.hide()
            self.int_line_edit.hide()

    def populate_columns_list(self):
        # Clear columns list
        self.columns_list.clear()

        # Get selected table
        selected_table = self.table_combo.currentText()

        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        #  DESCRIBE query gets column names
        cursor.execute(f"DESCRIBE {selected_table}")
        columns = cursor.fetchall()

        # Populate columns list with checklist items
        for column in columns:
            item = QListWidgetItem(column[0])
            item.setCheckState(Qt.Unchecked)  # Initially unchecked
            self.columns_list.addItem(item)

        # Close connection
        cursor.close()
        conn.close()

    def populate_tables_combo(self):
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Execute SHOW TABLES query
        cursor.execute("SHOW TABLES")

        # Fetch table names
        tables = cursor.fetchall()

        # Populate tables combo box
        self.table_combo.addItems([table[0] for table in tables])

        # Close connection
        cursor.close()
        conn.close()

    def populate_columns_combo(self):
        # Clear columns combo box
        self.columns_combo.clear()

        # Get selected table
        selected_table = self.table_combo.currentText()

        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Execute DESCRIBE query to get column names
        cursor.execute(f"DESCRIBE {selected_table}")

        # Fetch column names
        columns = cursor.fetchall()

        # Populate columns combo box
        self.columns_combo.addItems([column[0] for column in columns])

        # Close connection
        cursor.close()
        conn.close()

    def populate_columns_headers(self, column_data):
        # Clear columns combo box
        self.table.setColumnCount(0)
        self.table.setHorizontalHeaderLabels([])

        self.table.setColumnCount(len(column_data))
        self.table.setHorizontalHeaderLabels([column[0] for column in column_data])

    def execute_query(self):
        # Get selected query type
        query_type = self.query_type_combo.currentText()
        # Get selected table and column
        selected_table = self.table_combo.currentText()
        selected_columns = [self.columns_list.item(i).text() for i in range(self.columns_list.count()) if self.columns_list.item(i).checkState() == Qt.Checked]

        replace_text = self.replace_line_edit.text()
        int_line = self.int_line_edit.text()

        # Execute query based on selected type
        if query_type == "SELECT" and len(selected_columns) > 0:
            self.select_data(selected_table, selected_columns)
        elif query_type == "INSERT" and len(selected_columns) > 0 and replace_text != "":
            self.insert_data(selected_table, selected_columns, replace_text)  # replace_text)
        elif query_type == "UPDATE" and len(selected_columns) == 1 and replace_text != "" and int_line != 0:
            self.update_data(selected_table, selected_columns, replace_text, int_line)  # replace_text)
        elif query_type == "DELETE" and int_line != 0:
            self.delete_data(selected_table, int_line)

    def refresh_table(self):
        self.table.clear()
        selected_table = self.table_combo.currentText()
        selected_columns = [self.columns_list.item(i).text() for i in range(self.columns_list.count()) if self.columns_list.item(i).checkState() == Qt.Checked]
        self.select_data(selected_table, selected_columns)

    def select_data(self, table, columns):
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Define the SQL query with placeholders for table and column
        query = f"SELECT {', '.join(columns)} FROM {table}"

        # Execute SELECT query with parameters
        cursor.execute(query)

        # Fetch data
        data = cursor.fetchall()

        # Populate table
        self.table.setRowCount(0)
        self.table.setColumnCount(len(columns))  # Set the correct number of columns
        self.table.setHorizontalHeaderLabels(columns)  # Set column headers directly

        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

        # Close connection
        cursor.close()
        conn.close()

    def insert_data(self, table: str, columns: list, user_input: str):
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        joined = ', '.join(columns)
        # Example INSERT query
        query = f"INSERT INTO {table} ({joined}) VALUES ({user_input})"
        cursor.execute(query)
        conn.commit()

        # Close connection
        cursor.close()
        conn.close()

        self.refresh_table()

    def update_data(self, table, column, user_input_txt, user_input_int):
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # user_input_int = int(user_input_int.text())
        # Example UPDATE query
        query = f"UPDATE {table} SET {column[0]} = {user_input_txt} WHERE {table}_id = {user_input_int}"
        cursor.execute(query)
        conn.commit()

        # Close connection
        cursor.close()
        conn.close()

        # Refresh table
        self.refresh_table()

    def delete_data(self, table, user_input_int):
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Example DELETE query
        query = f"DELETE FROM {table} WHERE {table}_id = {user_input_int}"
        cursor.execute(query)
        conn.commit()

        # Close connection
        cursor.close()
        conn.close()

        # Refresh table
        self.refresh_table()


class IntegerLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set validator to allow only integer input
        regex = QRegExp("[0-9]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
