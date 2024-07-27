import requests
import matplotlib.pyplot as plt
import json
from PIL import Image
from urllib.request import urlopen

# Función para escribir el archivo json con la información del pokémon
def escribir_archivo(nombre, peso, tamano, movimientos, habilidades, tipos, url_imagen):
    """
    Se escribe un archivo json con el nombre del pokemon y su información
    Recibe como parámetros el nombre, peso, tamaño, movimientos, habilidades y tipos
    """
    with open('pokedex/' + nombre + '.json','a') as f_archivo: # a - append (agrega texto ak final del archivo)
        f_archivo.write('{\n\"Nombre\": ' + '\"' + nombre + '\",')
        f_archivo.write('\n\"Peso\": ' + str(peso) + ',')
        f_archivo.write('\n\"Tamano\": ' + str(tamano) + ',')
        f_archivo.write('\n\"URL_imagen\": ' + '\"' + url_imagen + '\",')
        f_archivo.write('\n\"Movimientos\": ' + str(movimientos) + ',')
        f_archivo.write('\n\"Habilidades\": ' + str(habilidades) + ',')
        f_archivo.write('\n\"Tipos\": ' + str(tipos) + "\n}")

# Pedir nombre del pokpemon al usuario
no_existe = True
while no_existe:
    pokemon = input("Escribe un pokémon: ")
    # Se genera la url de la petición
    url = "https://pokeapi.co/api/v2/pokemon/" + pokemon
    # Se lanza la petición del pokémon
    respuesta = requests.get(url)
    # Si no se encuentra el pokémon se vuelve a pedir el nombre
    if respuesta.status_code != 200:
        print("Pokémon no encontrado")
    else:
        no_existe = False

# Transformar la respuesta a formato json
datos = respuesta.json()

# Obtener la url de la imagen
try:
    url_imagen = datos['sprites']['front_default']
    imagen = Image.open(urlopen(url_imagen))
except:
    print("El pokémon no tiene imagen")
    exit()

# Se genera una ventana con la imagen del pokémon
plt.title(datos['name'])
imgplot = plt.imshow(imagen)
plt.show()

# Se obtienen los datos del pokémon desde el objeto de la petición
nombre = datos['name']
peso = datos['weight']
tamano = datos['height']
movimientos = datos['moves']
habilidades = datos['abilities']
tipos = datos['types']

# Obtener movimientos y guardarlos en una lista
movimientos_json = []
for i in range(int(len(movimientos))):
    movimientos_json.append(movimientos[i]["move"]["name"])

# Obtener habilidades y guardarlos en una lista
habilidades_json = []
for i in range(int(len(habilidades))):
    habilidades_json.append(habilidades[i]["ability"]["name"])

# Obtener tipos y guardarlos en una lista
tipos_json = []
for i in range(int(len(tipos))):
    tipos_json.append(tipos[i]["type"]["name"])

# Se llama la función para crear y escribir la información del pokémon en el archivo json
# Se ocupa la función dumps de la librería json para que las listas tengan el formato correcto de comillas dobles ("") en el archivo json
escribir_archivo(nombre, peso, tamano, json.dumps(movimientos_json), json.dumps(habilidades_json), json.dumps(tipos_json), url_imagen)

