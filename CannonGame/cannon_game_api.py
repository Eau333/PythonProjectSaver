import pyglet
import ctypes
import tkinter
from tkinter import simpledialog
import math
import time
import random
ctypes.windll.user32.SetProcessDPIAware()


# some code stolen from uno_gfx_api.py
class CannonGameGfx:
    def __init__(self):
        # initializing the game window
        self.window = pyglet.window.Window()
        self.window.set_size(1500, 1000)
        pyglet.gl.glClearColor(0.5, 0.8, 1, 1.0)
        self.wind = 0
        self.grass = pyglet.shapes.BorderedRectangle(x=0, y=0,
                                                              width=1500, height=300,
                                                              color=(50, 150, 50, 255),
                                                              border_color=(0, 150, 0, 255))
        self.playerone = pyglet.shapes.Circle(x=275, y=275,
                                                     radius=75,
                                                     color=(0, 0, 0, 255),
                                                     )
        self.playertwo = pyglet.shapes.Circle(x=1225, y=275,
                                                     radius=75,
                                                     color=(0, 0, 0, 255),
                                                     )
        self.windlabel = pyglet.text.Label("",
                                       font_name='Arial',
                                       font_size=36,
                                       bold=True,
                                       x=750, y=200,
                                       anchor_x='center', anchor_y='center',
                                       color=(0, 0, 0, 255))
        self.ball = None
        self.gunpowder = []
        self.root = tkinter.Tk()
        self.root.eval(f'tk::PlaceWindow {self.root._w} center')
        self.root.withdraw()
        self.firstturn = True
        self.updateWind()
        self.update_window()
        while True:
            self.playerTurn()
            self.firstturn = not self.firstturn
            # FIX LOOP LATER

    def update_window(self):
        @self.window.event
        def on_draw():
            self.window.clear()
            self.grass.draw()
            self.playerone.draw()
            self.playertwo.draw()
            self.windlabel.draw()
            if self.ball is not None:
                self.ball.shape.draw()
        self.window.switch_to()
        self.window.dispatch_event('on_draw')
        self.window.dispatch_events()
        self.window.flip()

    def playerTurn(self):
        prompt = "Enter the angle in degrees:"
        invalidSyntax = True
        while invalidSyntax:
            selected_angle = simpledialog.askstring(title="It's your turn.",
                                                         prompt=prompt,
                                                         parent=self.root)
            try:
                selected_angle = float(selected_angle)
                invalidSyntax = False
            except:
                pass
        prompt = "Enter the amount of gun powder:"
        invalidSyntax = True
        while invalidSyntax:
            selected_force = simpledialog.askstring(title="It's your turn.",
                                                         prompt=prompt,
                                                         parent=self.root)
            try:
                selected_force = float(selected_force)
                invalidSyntax = False
            except:
                pass
        self.ball = cannonball(selected_angle, selected_force, self.firstturn)
        self.fire()

    def fire(self):
        tick = 1/30
        gravity = 300
        while True:
            self.update_window()
            if self.detectHit():
                self.ball.shape.x = 2000
                self.update_window()
                return True
            if self.ball.shape.y <= -75:
                return False
            self.ball.shape.x += self.ball.xspeed * tick
            self.ball.shape.y += self.ball.yspeed * tick
            self.ball.yspeed -= gravity * tick
            self.ball.xspeed += (self.wind - self.ball.xspeed) * tick
            time.sleep(tick)

    def updateWind(self):
        self.wind = random.randint(-1000, 1000)
        self.windlabel.text = "wind:"+str(self.wind)

    def detectHit(self):
        targetx = 0
        targety = 0
        targetradius = 0
        if self.firstturn:
            targetx = self.playertwo.x
            targety = self.playertwo.y
            targetradius = self.playertwo.radius
        else:
            targetx = self.playerone.x
            targety = self.playerone.y
            targetradius = self.playerone.radius
        xdiff = targetx - self.ball.shape.x
        ydiff = targety - self.ball.shape.y
        if math.sqrt((xdiff * xdiff) + (ydiff * ydiff)) < (self.ball.shape.radius + targetradius):
            return True
        return False

class cannonball:
    def __init__(self,angle,force,turn):
        self.shape = pyglet.shapes.Circle(x=350, y=350, radius=30,
                                     color=(0, 0, 0))
        if not turn:
            self.shape.x = 1150
        self.cspeed = 3
        self.rspeed = force * self.cspeed
        self.xspeed = self.rspeed * math.cos(angle/180*math.pi)
        self.yspeed = self.rspeed * math.sin(angle/180*math.pi)
