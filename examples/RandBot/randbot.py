#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import math
import random
import sys
import statistics as stats
import numpy as np
import interface


def decision_energy(state, lighthouse):
    energia = 0
    energias = []
    for lh in (state["lighthouses"]):
        energias.append(lh["energy"])

    energias = sorted(energias)
    mediana = stats.median(energias)

    if lighthouse["energy"] == 0:
        energia = 160 + mediana
    else:
        energia_faro = lighthouse["energy"]
        energia = 160 + energia_faro + mediana

    return energia


def decision_mov(cx, cy, state, player_num):
    distancias = []
    for i in (state["lighthouses"]):
        x_l, y_l = i["position"]
        if x_l != cx or y_l != cy:
            if i["owner"] != player_num:
                d_x1 = abs(cx - x_l)
                d_y1 = abs(cy - y_l)
                if d_x1 > d_y1:
                    dist = d_x1
                    distancias.append(dist)
                else:
                    dist = d_y1
                    distancias.append(dist)

            else:
                distancias.append(1000)
        else:
            distancias.append(1000)

    min1 = np.amin(distancias)
    i1 = distancias.index(min1)

    l = (state["lighthouses"])[i1]
    x_l, y_l = l["position"]

    if cy > y_l and cx > x_l:
        move = (-1, -1)
    elif cy > y_l and cx < x_l:
        move = (1, -1)
    elif cy < y_l and cx > x_l:
        move = (-1, 1)
    elif cy < y_l and cx < x_l:
        move = (1, 1)
    elif cy == y_l and cx > x_l:
        move = (-1, 0)
    elif cy == y_l and cx < x_l:
        move = (1, 0)
    elif cy > y_l and cx == x_l:
        move = (0, -1)
    elif cy < y_l and cx == x_l:
        move = (0, 1)

    return move


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
                            return self.connect(possible_connections[0])

            if lighthouses[(cx, cy)]["owner"] != self.player_num:
                # Probabilidad 60%: recargar el faro
                energy = decision_energy(state, lighthouses[(cx, cy)])
                # energy = random.randrange(state["energy"] + 1)
                return self.attack(energy)

        move = decision_mov(cx, cy, state, self.player_num)
        return self.move(*move)


if __name__ == "__main__":
    iface = interface.Interface(RandBot)
    iface.run()
