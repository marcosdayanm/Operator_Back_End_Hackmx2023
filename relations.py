from cs50 import SQL
db = SQL("sqlite:///calls.db")
import re


def patrons(text):
    # Se seleccionan todas las palabras clave
    palabras = db.execute("SELECT * FROM keywords")
    words = []

    # Se inserta en la lista words cada palabra clave
    for i in palabras:
        words.append(i['words'])


    # se divide cada palabra en un elemento de una lista

    text = re.split(r'\s+|[,.;!?]+', text.lower())
    keyspass = []

   #print("Esto es el text: ", text)

    keys = set()


    keysunfiltered = db.execute("SELECT * FROM keywords")

    for k in keysunfiltered:
        keyspass.append(k['words'])

    # Se inserta cada palabra clave que haya en el string en keys
    for i in keyspass:
        keys.add(i)





    # Extraer las relaciones en una lista de diccionarios
    relations = db.execute("SELECT * FROM relations")
    rels = []
    for i in relations:
        rels.append({'key1': i['key1'], 'key2': i['key2'], 'popup': i['popup']})
        #print(i)




    # Insertar en sql si hay un popup por las keywords
    popup = 'None'
    cambio = False
    for i in rels:
        if (i['key1'] in text) and (i['key2'] in text):
            popup = i['popup']
            #print("Este es popup: ", i['popup'])
            cambio = True
            break
    

    palabras3 = {"sangre", "heridos", "muerta", "muerto", "cadaver", "herido", "ataque", "incendio", "secuestraron"}

    # Seleccionar el nivel de prioridad en base a las keywords
    if not cambio:
        weight = 1
    elif any(palabra in keys for palabra in palabras3):
        weight = 3
    else:
        weight = 2


    # Ésto se hace en el main file
    #db.execute("INSERT INTO calls (peligro, priority) VALUES (?,?)", popup, weight)
    
    return keyspass, popup, weight


if __name__ == "__main__":
    patrons("Hola, buenas tardes. Sí, quiero reportar un secuestro aquí en la calle Xochicalco 12, en la delegación Arbarte. Sí. Sí, sí, sí. Sí, yo me encontraba afuera de la calle, al lado de mi casa. Justamente en Xochicalco 12 iba saliendo de mi casa. Sí, eran las dos de la tarde. La calle estaba sola y una camioneta blanca, que no logré apreciar las placas, no logré apreciar si tenía placas, se llevó a dos personas, cuatro sujetos armados. Estoy seguro que le hicieron daño y al momento está en fuga. No, no sé. Sí, espero n. Sí, hubo bastante violencia en el acto. Sí, estoy bastante preocupado, pero me quedo aquí para esperar a la patrulla. Pero quiero saber en cuánto tiempo llegan, porque es una emergencia. Ya está huyendo la camioneta. Sí, es la primera vez que presencio un secuestro. Okey. Okey, okey. Sí, puedo esperar aquí. Sí. Sí, ya varios vecinos están enterados de la situación De hecho, aquí vienen dos y tendré que colgarles por lo mismo. Pero espero a la patrulla. Muchas gracias.")