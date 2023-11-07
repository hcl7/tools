import pymssql
import argparse
import os

Black = '\x1b[30m'
Red = '\x1b[31m'
Green = '\x1b[32m'
Yellow = '\x1b[33m'
Blue = '\x1b[34m'
Magenta = '\x1b[35m'
Cyan = '\x1b[36m'
White = '\x1b[37m'
Default = '\x1b[39m'
LightGray = '\x1b[90m'
LightRed = '\x1b[91m'
LightGreen = '\x1b[92m'
LightYellow = '\x1b[93m'
LightBlue = '\x1b[94m'
LightMagenta = '\x1b[95m'
LightCyan = '\x1b[96m'
LightWhite = '\x1b[97m'

def clear():
	return os.system('clear')

def logo():
	clear()
	print (LightBlue + "	 ___  _____   _____ _ __  " + Default)
	print (LightBlue + "	/ __|/ _ \ \ / / _ \ |_ \ " + Default)
	print (LightBlue + "	\__ \  __/\ V /  __/ | | |" + Default)
	print (LightBlue + "	|___/\___| \_/ \___|_| |_|" + Default)
	print (LightBlue + "							  " + Default)

logo()

class DynamicSQLManager:
    def __init__(self, server, database, username, password,port):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.connection = None
        self.schema = {
            'tables': {},
            'foreign_keys': {}
        }

    def connect(self):
        try:
            self.connection = pymssql.connect(server=f'{self.server}',user=f'{self.username}',password=f'{self.password}', database=f'{self.database}')
            print(f"{Green}[+] Connected to database: {self.database}{Default}")
            return True
        except pymssql.Error as e:
            print(f"{LightRed}[*] Connection Error: {e}{Default}")
            return False

    def discover_schema(self):
        if self.connection is None:
            if not self.connect():
                return

        try:
            cursor = self.connection.cursor()

            # Retrieve table names and columns
            cursor.execute("SELECT table_name, column_name FROM INFORMATION_SCHEMA.COLUMNS")
            for row in cursor.fetchall():
                table_name, column_name = row[0], row[1]
                if table_name not in self.schema['tables']:
                    self.schema['tables'][table_name] = []
                self.schema['tables'][table_name].append(column_name)

            # Retrieve foreign key information
            cursor.execute("SELECT fk.name AS constraint_name, OBJECT_NAME(fk.parent_object_id) AS table_name, cp.name AS column_name, OBJECT_NAME(fk.referenced_object_id) AS referenced_table_name, cr.name AS referenced_column_name FROM sys.foreign_keys fk INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id INNER JOIN sys.columns cp ON cp.object_id = fkc.parent_object_id AND cp.column_id = fkc.parent_column_id INNER JOIN sys.columns cr ON cr.object_id = fkc.referenced_object_id AND cr.column_id = fkc.referenced_column_id")
            for row in cursor.fetchall():
                constraint_name, table_name, column_name, referenced_table_name, referenced_column_name = row
                self.schema['foreign_keys'][constraint_name] = {
                    'table_name': table_name,
                    'column_name': column_name,
                    'referenced_table_name': referenced_table_name,
                    'referenced_column_name': referenced_column_name
                }

            cursor.close()
        except pymssql.Error as e:
            print(f"{LightRed}[*] Schema Discovery Error: {e}{Default}")

    def build_dynamic_query(self, tables, conditions):
        if self.connection is None:
            if not self.connect():
                return
        if not tables:
            raise ValueError(f"{LightRed}[*] No tables specified in the query!...{Default}")

        select_columns = self.get_all_columns(tables)
        select_clause = ", ".join(select_columns)

        query = f"SELECT {select_clause} FROM {tables[0]}"

        for i in range(1, len(tables)):
            if tables[i] not in self.schema['tables']:
                raise ValueError(f"{LightRed}[*] Table '{tables[i]}' does not exist in the schema!...{Default}")
            
            foreign_keys = [fk for fk in self.schema['foreign_keys'].values() if fk['table_name'] == tables[i - 1] and fk['referenced_table_name'] == tables[i]]
            if len(foreign_keys) != 1:
                raise ValueError(f"{LightRed}[*] Invalid or missing foreign key relationship between '{tables[i - 1]}' and '{tables[i]}'{Default}")
            fk = foreign_keys[0]
            
            query += f" JOIN {tables[i]} ON {tables[i - 1]}.{fk['column_name']} = {tables[i]}.{fk['referenced_column_name']}"

        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
            query += where_clause

        return query

    def get_all_columns(self, tables):
        columns = []
        for table in tables:
            if table not in self.schema['tables']:
                raise ValueError(f"{LightRed}[*] Table '{table}' does not exist in the schema.{Default}")
            
            table_columns = self.schema['tables'][table]
            columns.extend([f"{table}.{column}" for column in table_columns])

        return columns

    def generate_condition(self, tables, columns):
        conditions = []
        for table in tables:
            if table not in self.schema['tables']:
                print(f"{LightRed}[*] Table '{table}' not found in the schema!...{Default}")
            else:
                for column in columns:
                    if column not in self.schema['tables'][table]:
                        print(f"{LightRed}[*] Column '{column}' not found in table '{table}'!...{Default}")
                    else:
                        condition = f"{table}.{column} = %s"
                        conditions.append(condition)

        return conditions


    def execute_query(self, query, params=None):
        if self.connection is None:
            if not self.connect():
                return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymssql.Error as e:
            print(f"{LightRed}[*] Query Execution Error: {e}{Default}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()

# Example usage of the DynamicSQLManager
if __name__ == "__main__":
    dynamic_sql_manager = DynamicSQLManager(
        server="ip",
        database="db",
        username="",
        password="",
        port=1433
    )

    description = f"{Cyan}Dynamic SQL Query Generator{Default}"
    table_help = f"{Yellow}Specify tables for the query{Default}"
    column_help = f"{Yellow}Specify columns for conditions{Default}"
    value_help = f"{Yellow}Specify values for conditions{Default}"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--table", action="append", help=table_help)
    parser.add_argument("-c", "--column", action="append", help=column_help)
    parser.add_argument("-v", "--value", action="append", help=value_help)

    args = parser.parse_args()

    tables = args.table or []
    columns = args.column or []
    values = args.value or []

    if not tables or not columns or not values:
        parser.error(f"{LightRed}[*] Please specify tables, columns, and values for the query!..." + Default)

    dynamic_sql_manager.discover_schema()
    conditions = dynamic_sql_manager.generate_condition(tables, columns)
    dynamic_query = dynamic_sql_manager.build_dynamic_query(tables, conditions)
    print(f"{LightYellow}[+] Dynamic Query: {Default}", dynamic_query)
    result = dynamic_sql_manager.execute_query(dynamic_query, params=tuple(values))

    if result:
        for row in result:
            print(row)

    dynamic_sql_manager.close_connection()
