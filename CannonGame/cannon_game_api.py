import pyglet
import ctypes
import tkinter
from tkinter import simpledialog
import math
import time
ctypes.windll.user32.SetProcessDPIAware()


# some code stolen from uno_gfx_api.py
class CannonGameGfx:
    def __init__(self):
        # initializing the game window
        self.window = pyglet.window.Window()
        self.window.set_size(1500, 1000)
        pyglet.gl.glClearColor(0.5, 0.8, 1, 1.0)
        self.grass = pyglet.shapes.BorderedRectangle(x=0, y=0,
                                                              width=1500, height=300,
                                                              color=(50, 150, 50, 255),
                                                              border_color=(0, 150, 0, 255))
        self.playerone = pyglet.shapes.BorderedRectangle(x=200, y=200,
                                                     width=150, height=150,
                                                     color=(0, 0, 0, 255),
                                                     border_color=(0, 0, 0, 255))
        self.playertwo = pyglet.shapes.BorderedRectangle(x=1150, y=200,
                                                         width=150, height=150,
                                                         color=(0, 0, 0, 255),
                                                         border_color=(0, 0, 0, 255))
        self.ball = None
        self.gunpowder = []
        self.root = tkinter.Tk()
        self.root.eval(f'tk::PlaceWindow {self.root._w} center')
        self.root.withdraw()

    def update_window(self):
        @self.window.event
        def on_draw():
            self.window.clear()
            self.grass.draw()
            self.playerone.draw()
            self.playertwo.draw()
            if self.ball is not None:
                self.ball.shape.draw()
        self.window.switch_to()
        self.window.dispatch_event('on_draw')
        self.window.dispatch_events()
        self.window.flip()

    def playerTurn(self):
        prompt = "Enter the angle in degrees:"
        selected_angle = simpledialog.askstring(title="It's your turn.",
                                                     prompt=prompt,
                                                     parent=self.root)
        prompt = "Enter the amount of gun powder:"
        selected_force = simpledialog.askstring(title="It's your turn.",
                                                     prompt=prompt,
                                                     parent=self.root)
        self.ball = cannonball(float(selected_angle),float(selected_force))
        self.fire()

    def fire(self):
        tick = 1/30
        gravity = 300
        for i in range(0, 1000):
            self.update_window()
            self.ball.shape.x += self.ball.xspeed * tick
            self.ball.shape.y += self.ball.yspeed * tick
            self.ball.yspeed -= gravity * tick
            time.sleep(tick)

class cannonball:
    def __init__(self,angle,force):
        self.shape = pyglet.shapes.Circle(x=350, y=350, radius=30,
                                     color=(0, 0, 0))
        self.cspeed = 3
        self.rspeed = force * self.cspeed
        self.xspeed = self.rspeed * math.cos(angle/180*math.pi)
        self.yspeed = self.rspeed * math.sin(angle/180*math.pi)



