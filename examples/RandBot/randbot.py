#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import numpy as np
import interface


class RandBot(interface.Bot):
    """Bot que juega aleatoriamente."""
    NAME = "RandBot"

    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una acción (jugada)."""
        cx, cy = state["position"]
        lighthouses = dict((tuple(lh["position"]), lh)
                           for lh in state["lighthouses"])

        # Si estamos en un faro...
        if (cx, cy) in lighthouses:
            # Probabilidad 60%: conectar con faro remoto válido
            if lighthouses[(cx, cy)]["owner"] == self.player_num:
                if random.randrange(100) < 60:
                    possible_connections = []
                    for dest in lighthouses:
                        # No conectar con sigo mismo
                        # No conectar si no tenemos la clave
                        # No conectar si ya existe la conexión
                        # No conectar si no controlamos el destino
                        # Nota: no comprobamos si la conexión se cruza.
                        if (dest != (cx, cy) and
                                lighthouses[dest]["have_key"] and
                                [cx, cy] not in lighthouses[dest]["connections"] and
                                lighthouses[dest]["owner"] == self.player_num):
                            possible_connections.append(dest)

                    if possible_connections:
                        return self.connect(random.choice(possible_connections))

            # Probabilidad 60%: recargar el faro
            if random.randrange(100) < 60:
                energy = random.randrange(state["energy"] + 1)
                return self.attack(energy)

        # Mover aleatoriamente
        move = self.decision_mov(cx, cy, lighthouses)
        # moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        # Determinar movimientos válidos
        # moves = [(x, y) for x, y in moves if self.map[cy + y][cx + x]]
        # move = random.choice(moves)
        return self.move(*move)

    def decision_mov(self, x, y, lighthouses):

        distancias = []

        for i in lighthouses:
            d_x1 = abs(x - i.position[0])
            d_y1 = abs(y - i.position[1])
            dist = math.sqrt(d_x1 ^ 2 + d_y1 ^ 2)
            distancias.append(dist)

        x_res = x - lighthouses[0].position[0]
        y_res = y - lighthouses[1].position[1]
        x_move = 0
        y_move = 0

        if x_res < 0:
            x_move = -1
        elif y_res < 0:
            y_move = -1
        elif x_res > 0:
            x_move = 1
        elif y_res > 0:
            y_move = 1

        move = (x_move, y_move)
        return move


if __name__ == "__main__":
    iface = interface.Interface(RandBot)
    iface.run()
