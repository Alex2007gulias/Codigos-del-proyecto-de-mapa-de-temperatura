# Import necessary libraries
import pygame
import time
import csv

# Define color constants
C1 = (160, 210, 100)  # Verde hierba suave (17°C)
C2 = (180, 220, 80)   # Verde limón claro
C3 = (210, 230, 50)   # Verde-amarillo
C4 = (240, 240, 50)   # Amarillo pastel
C5 = (255, 210, 50)   # Amarillo intenso
C6 = (255, 170, 40)   # Ámbar
C7 = (255, 120, 30)   # Naranja
C8 = (255, 80, 30)    # Rojo-naranja
C9 = (255, 40, 40)    # Rojo vivo
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# List of colors to be used for temperature representation
colors = [C1, C2, C3, C4, C5, C6, C7, C8, C9]

# Initialize Pygame
pygame.init()

# Función para leer datos de un único CSV con múltiples columnas (una por aula)
def read_csv_data(filename):
    with open(filename, newline='') as f:
        data = csv.reader(f, delimiter=',')
        # Saltar la fila de encabezados
        headers = next(data)
        # Leer todas las columnas (cada columna es un aula)
        aulas_data = []
        for col in zip(*data):  # Transponer las filas a columnas
             aulas_data.append([float(value.replace(',', '.')) for value in col if value.strip()])
        return aulas_data

# Leer datos del archivo CSV consolidado
csv_file = "c:/Users/Administrador/Downloads/Projecte_temperatura/Proves_python/Temp-Data.2.csv"
temperature_data = read_csv_data(csv_file)

# Define coordinates for temperature points on the map and which data column they use
# Ahora el segundo número en cada tupla se refiere al índice de columna en el CSV
Cordenadas = [
    ((85, 90), 0),  
    ((235, 90), 3),
    ((330, 90), 4),
    ((460, 90), 6),
    ((550, 90), 7),
    ((640, 90), 8),
    ((800, 90), 2),
    ((170, 220), 1),
    ((400, 90), 5)
]

# Resto del código permanece igual...
def compresio(listas):
    comprimida = []
    interval_size = (25 - 17) / 9
    
    for lista in listas:
        comprimida_lista = []
        for temperatura in lista:
            if temperatura < 17:
                comprimida_lista.append(0)
            elif temperatura >= 25:
                comprimida_lista.append(8)
            else:
                index = int((temperatura - 17) / interval_size)
                index = max(0, min(8, index))
                comprimida_lista.append(index)
        comprimida.append(comprimida_lista)
    return comprimida

# Function to draw temperature points on the screen
def dibujar_punto(screen, coordenadas, comprimida, colors, index):
    for (x, y), data_index in coordenadas:
        if data_index < len(comprimida) and index < len(comprimida[data_index]):
            color_index = comprimida[data_index][index]
            if color_index < len(colors):  # Additional safety check
                pygame.draw.circle(screen, colors[color_index], (x, y), 20)

# Set up the Pygame window
screen = pygame.display.set_mode([992, 701])
pygame.display.set_caption('Temperatura Aula')

# Initialize clock for controlling frame rate
clock = pygame.time.Clock()
background_position = [0, 0]
font = pygame.font.Font(None, 36)

# Load background image
try:
    background_image = pygame.image.load("C:/Users/Administrador/Downloads/Projecte_temperatura/Proves_python/Planol 1a planta_page-0001.jpg").convert()
except pygame.error:
    print("Error: Could not load background image")
    pygame.quit()
    exit()

# Compress temperature data
comprimida = compresio(temperature_data)
index = 0
last_update = time.time()
update_interval = 0.5  # Change color every 0.5 second

# Main game loop
done = False
while not done:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Draw background
    screen.blit(background_image, background_position)

    '''
    # Display mouse coordinates (optional)
    x, y = pygame.mouse.get_pos()
    text_surface = font.render(f"({x}, {y})", True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    '''
    
    # Update color index based on time interval
    current_time = time.time()
    if current_time - last_update >= update_interval:
        # Find the maximum length among all data lists
        max_length = max(len(lista) for lista in comprimida) if comprimida else 0
        if max_length > 0:
            index = (index + 1) % max_length
        last_update = current_time
    
    # Draw temperature points
    dibujar_punto(screen, Cordenadas, comprimida, colors, index)

     # Dibujar leyenda
    leyenda_x = 800  # Posición X de la leyenda
    leyenda_y = 450  # Posición Y de la leyenda
    leyenda_ancho = 170
    leyenda_alto = 250
    
    # Fondo de la leyenda
    pygame.draw.rect(screen, WHITE, (leyenda_x, leyenda_y, leyenda_ancho, leyenda_alto))
    pygame.draw.rect(screen, BLACK, (leyenda_x, leyenda_y, leyenda_ancho, leyenda_alto), 2)
    
    # Título de la leyenda
    titulo = font.render("Leyenda", True, BLACK)
    screen.blit(titulo, (leyenda_x + 40, leyenda_y + 5))
    
    # Rangos de temperatura y colores
    rangos = [
        ("<17°C", C1),
        ("17-17.9°C", C2),
        ("18-18.9°C", C3),
        ("19-19.9°C", C4),
        ("20-20.9°C", C5),
        ("21-21.9°C", C6),
        ("22-22.9°C", C7),
        ("23-23.9°C", C8),
        (">=24°C", C9)
    ]
    
    # Dibujar elementos de la leyenda
    for i, (texto, color) in enumerate(rangos):
        # Círculo de color
        pygame.draw.circle(screen, color, (leyenda_x + 20, leyenda_y + 40 + i*25), 8)
        # Texto
        texto_surface = font.render(texto, True, BLACK)
        screen.blit(texto_surface, (leyenda_x + 40, leyenda_y + 30 + i*25))
    
    # Mostrar el índice actual de medición
    texto_medicion = font.render(f"Dia: {(index+101)//100}", True, BLACK)
    screen.blit(texto_medicion, (leyenda_x + 60 , leyenda_y + leyenda_alto - 280))
    
    
    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()