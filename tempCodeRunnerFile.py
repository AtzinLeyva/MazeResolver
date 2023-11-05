def mover_jugador(x, y):
    global jugador
    if 0 <= x < len(m) and 0 <= y < len(m[0]):
        valor_casilla = int(m[x][y])
        costos = definir_costos_movimiento()