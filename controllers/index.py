import colorsys #nos permitira convertir valores hexa a hls para ordenarlos con los criterios que escribirmos

import web

# Esto le dice a web.py que busque los archivos HTML en la carpeta 'views'
render = web.template.render('views/')

class Index:
    def GET(self):
        # Esto renderiza el archivo index.html
        return render.index()

def calc_priori(color):
    color = color.replace("#", "").lower() #Si el usuario escribe un # o en mayusculas arreglamos eso quitandolo y poniendolo en minusculas

    total = 0


    for caracter in color:
        if caracter.isdigit():
            total += int(caracter) #el puntaje del numero es el numero

        elif caracter.isalpha():
            total += ord(caracter) - ord('a') #el puntaje se basa en el orden que ocupa del abecedario gracias a ord que nos da el valor ascii del caracter

    return total


def hexa_hsl(color): #de hex a hsl

    color = color.replace("#", "").lower()


    #Esta linea me ayuda a procentar mejor: Los colores hexadecimales se dividen en rrvvaa rojo, verde, azul
    #Como cada uno esta en base 16 le decimos a python que los interprete asi, y los convierta en rgb
    #Asi por ejemplo... ff es 255
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)


    #Como la libreria trabaja con valores de 0 y 1 usamos esta divicion para no usar numeros tan grandes, dividiendolo entre 255
    r, g, b = r / 255, g / 255, b / 255


    #Aqui se hace la convercion real '.rgb_to_hls' nos devuelve valores del tono, luminosidad y saturacion del 0 al 1. Hace la matematica complicada que no quiero hacer
    tono, luminosidad, saturacion = colorsys.rgb_to_hls(r, g, b)


    #Usando los valores del 0 al 1 los multimplicamos por los grados del circulo cromatico. Y por la saturacion que se extpresa en prosentaje
    tono_grados = tono * 360
    saturacion_pct = saturacion * 100

    return tono_grados, saturacion_pct


def color_valido(color): #Todo lo necesario para que el color sea valido como tener 6 digitos y asi
    color = color.replace("#", "").lower()

    if len(color) != 6:
        return False

    carc_valido = "0123456789abcdef"
    for caracter in color:
        if caracter not in carc_valido:
            return False

    return True


def main():
    colores_ingr = []  #Guardamos los colores que el usuario ingreso

    print("- -  COLORES HEXADECIMALES - -")
    print("Escribe 'fin' cuando termines.\n")

    


    #Como la lista esta ordenada en: entrada, puntaje, tono y saturacion, llendo del 0 al 3 x[2] es el tono y x[3] la saturacion
    #Esto generara una lista diferente, donde use el tono y saturacion como bases, siendo la saturacion la forma de desempatar.
    #El key=lambda es para que el .sort no lea todo, sino que vaya uno por uno
    colores_ingr.sort(key=lambda x: (x[2], x[3]))

    print("\n- - COLORES ORDENADOS - -")
    for color, puntaje, tono, saturacion in colores_ingr:
        print(color)


main()
