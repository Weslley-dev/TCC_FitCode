import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Listar todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Tabelas no SQLite:")
for table in tables:
    print(f"  - {table[0]}")

# Verificar dados em cada tabela
print("\nDados em cada tabela:")
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  {table_name}: {count} registros")

conn.close()
