
W = 0
H = 0

actualUser = None

# Pages
actualPage = 8 # 0: Login 1: Register 2: Menu 3: Selection 4: Game 5: Leaderboard 6: Config 7: GameOver 8: Intro
running = True

# Sonds
actualSong = 2
activeSond = True
music = True
volumen = 0.7

#Game
mode = 0 # 0: Ninguno 1: Tiempo 2: Pieza
limit = 60
speed = 1
viewScore = 0
piecesHasNum = True

dimX = 12
dimY = 21

activePieces = []

#data
states = [("Estado no seleccionado", None),"Amazonas", "Anzoátegui", "Apure", "Aragua", "Barinas", "Bolívar", "Carabobo", "Cojedes", "Delta Amacuro", "Dependencias Federales", "Distrito Federal", "Falcón", "Guárico", "Lara", "Mérida", "Miranda", "Monagas", "Nueva Esparta", "Portuguesa", "Santander", "Sucre", "Táchira", "Trujillo", "Vargas", "Yaracuy", "Zulia"]

#fonts
fontLekton = "./public/fonts/Lekton-Regular.ttf"
fontLektonBold = "./public/fonts/Lekton-Bold.ttf"
fontAldrich = "./public/fonts/Aldrich-Regular.ttf"

#Archives
fileUsers = "./data/JUGADORES.bin"