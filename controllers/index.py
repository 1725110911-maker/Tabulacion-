import web
import colorsys #nos permitira convertir valores hexa a hls para ordenarlos con los criterios que escribirmos

render = web.template.render('views', base='layout')

# Esta lista mantendrá los datos vivos en la memoria del servidor
colores_ingresados = []

# --- LÓGICA DE COLORES ---
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


    if len(color) == 3:
        color = "".join([c*2 for c in color])

    r, g, b = int(color[0:2], 16) / 255.0, int(color[2:4], 16) / 255.0, int(color[4:6], 16) / 255.0

    #Aqui se hace la convercion real '.rgb_to_hls' nos devuelve valores del tono, luminosidad y saturacion del 0 al 1. Hace la matematica complicada que no quiero hacer
    tono, luminosidad, saturacion = colorsys.rgb_to_hls(r, g, b)


    #Usando los valores del 0 al 1 los multimplicamos por los grados del circulo cromatico. Y por la saturacion que se extpresa en prosentaje
    tono_grados = tono * 360
    saturacion_pct = saturacion * 100

    return tono_grados, saturacion_pct


def color_valido(color): #Todo lo necesario para que el color sea valido como tener 6 digitos y asi
    color = color.replace("#", "").lower()

    if len(color) not in (3, 6): 
        return False

    carc_valido = "0123456789abcdef"
    for caracter in color:
        if caracter not in carc_valido:
            return False

    return True

# --- CONTROLADOR WEB ---
class Index:
    def GET(self):
        # Solo leemos la variable global
        global colores_ingresados
        return render.index(colores_ingresados, "")

    def POST(self):
        # Le decimos a Python que vamos a modificar la variable global
        global colores_ingresados
        
        formulario = web.input(color="")
        entrada = formulario.color.strip()

        # Botón para limpiar
        if entrada.lower() == "limpiar":
            colores_ingresados = []
            return render.index(colores_ingresados, "Lista de colores limpiada exitosamente.")

        # Validación
        if not color_valido(entrada):
            return render.index(colores_ingresados, "Error: Color NO válido.")

        color_limpio = "#" + entrada.replace("#", "").upper()
        if len(color_limpio) == 4: 
            color_limpio = "#" + "".join([c*2 for c in color_limpio[1:]])

        # Evitar duplicados
        if not any(c['hex'] == color_limpio for c in colores_ingresados):
            puntaje = calc_priori(entrada)
            tono, saturacion = hexa_hsl(entrada)
            
            nuevo_color = {
                'hex': color_limpio,
                'puntaje': puntaje,
                'tono': tono,
                'saturacion': saturacion
            }
            colores_ingresados.append(nuevo_color)

            # Ordenamos la lista global
            colores_ingresados.sort(key=lambda x: (x['tono'], x['saturacion'], x['puntaje']))
            
            mensaje = f"Color {color_limpio} agregado."
        else:
            mensaje = "Error: Ese color ya está en la lista."

        return render.index(colores_ingresados, mensaje)