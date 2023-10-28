import sqlite3



def main():
    conn = sqlite3.connect('calls.db')

    cursor = conn.cursor()

    # Crear una nueva tabla con un comando SQL
    cursor.execute('''
    CREATE TABLE calls (
        id INTEGER PRIMARY KEY,
        fecha TEXT,
        hora TEXT,
        ruta TEXT,
        transcript TEXT,
        keywords TEXT,
        peligro, BOOL,
        serv1 TEXT,
        serv2 TEXT,
        serv3 TEXT         
    )
    ''')

    # Guardar (confirmar) los cambios
    conn.commit()

    conn.close()




if __name__ == '__main__':
    main()