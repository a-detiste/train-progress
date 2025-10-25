#!/usr/bin/python3

# (c) 2025 Alexandre Detiste

import threading
import time
from typing import Any, NoReturn

import paho.mqtt.client as mqtt
import pygame

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)



class Progress:
    '''display the progression of a vehicle on a forecasted route

    the vehicle can get diverted anytime
    '''

    theoric: list[str] = []
    stops: list[str] = []
    currentStop: str | None = None
    colour: tuple[int, int, int] = GREEN

    def __init__(self) -> None:
        pygame.init()
        self.broker = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "train")
        self.broker.on_connect = self.on_connect
        self.broker.on_message = self.on_message
        self.font = pygame.font.SysFont("Arial", 32)

    def run(self) -> NoReturn:
        pygame.display.set_caption("local-iv")
        self.screen = pygame.display.set_mode((640, 480))
        background = pygame.Surface(self.screen.get_size())
        background.fill(WHITE)
        self.screen.blit(background, (0, 0))
        pygame.display.update()

        threading.Thread(target=self.pygame_events).start()
        self.broker.connect("127.0.0.1")
        self.broker.loop_forever()

    def pygame_events(self) -> NoReturn:
        '''the final embedded target has no keyboard and would run in "cage" display manager'''
        while True:
            for event in pygame.event.get():
                # on 'close window' or Ctrl-C
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.unicode == "\x03"
                ):
                    self.broker.disconnect()
                    pygame.quit()
                    exit()

    def on_connect(
        self,
        client,
        userdata: Any,
        flags,
        reason_code,
        properties
    ) -> None:
        client.subscribe("colour", True)
        client.subscribe("theoric", True)
        client.subscribe("line", True)
        client.subscribe("stop", True)

    def on_message(
        self,
        client,
        userdata: Any,
        msg
    ) -> None:
        message = msg.payload.decode("ascii", "ignore")
        print(msg.topic, message)
        if msg.topic == 'theoric':
            self.theoric = message.split(',')
        elif msg.topic == 'line':
            self.stops = message.split(',')
        elif msg.topic == 'colour':
            self.colour = pygame.Color("#" + message)
        else:
            self.currentStop = message
        self.redraw()

    def redraw(self) -> None:
        line = self.stops or self.theoric
        if self.theoric and self.theoric != line:
            print('diversion')
        if not line:
            return
        for i, point in enumerate(line):
            x = 70
            y = 70*(1+i)
            pygame.draw.circle(self.screen, self.colour, (x, y), 20)
            txtsurf = self.font.render(point, True, WHITE)
            self.screen.blit(txtsurf, (x - txtsurf.get_width() // 2, y - txtsurf.get_height() // 2))
            time.sleep(0.7)
            pygame.display.update()

progress = Progress()
progress.run()
