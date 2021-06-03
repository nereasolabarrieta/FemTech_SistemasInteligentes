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
        move = self.decision_mov(cx, cy, state)
        # moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        # Determinar movimientos válidos
        # moves = [(x, y) for x, y in moves if self.map[cy + y][cx + x]]
        # move = random.choice(moves)
        return self.move(*move)

    def decision_mov(self, state):

        lh = state["lighthouses"]
        x_l, y_l = lh[20]["position"]

        x, y = state["position"]
        x_res = 10
        y_res = 10

        if x_res < 0:
            x_move = -1
        else:
            x_move = 1
        if y_res < 0:
            y_move = -1
        else:
            y_move = 1

        move = (x_move, y_move)
        return move


if __name__ == "__main__":
    iface = interface.Interface(RandBot)
    iface.run()
