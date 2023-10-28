from cs50 import SQL


db = SQL("sqlite:///calls.db")


# words = ['arma', 'disparo', 'bala', 'pistola', 'accidente', 'herido', 'heridos', 'volteado', 'choque', 'fuego', 'incendio', 'secuestraron', 'muerto', 'muerta', 'cadaver', 'sangre']

# for word in words:
#     db.execute("INSERT INTO keywords (words) VALUES (?)", word)

# Se seleccionan todas las palabras clave
palabras = db.execute("SELECT * FROM keywords")
words = []

# Se inserta en la lista words cada palabra clave
for i in palabras:
    words.append(i['words'])


text = "Sangre pistola disparo incendio".split()

keys = []

# Se inserta cada palabra clave que haya en el string en keys
for i in text:
    if (i in words) and (i not in keys):
        keys.append(i)

# Se corrobora con if statements si hay secuencias de keywords
if "disparo" in keys and "sangre" in keys:
    db.execute("INSERT INTO calls (peligro) VALUES (?)", "Despachar Ambulancia")

elif "disparo" in keys and "pistola" in keys:
    db.execute("INSERT INTO calls (peligro) VALUES (?)", "Despachar Policía")

elif "fuego" in keys and "incendio" in keys:
    db.execute("INSERT INTO calls (peligro) VALUES (?)", "Despachar Bomberos")

else:
    db.execute("INSERT INTO calls (peligro) VALUES (?)", "None")


