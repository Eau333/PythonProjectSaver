import pyglet
import random

def dependency_test():
    print('API successfully invoked.')


class unogfx():
    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_size(1500, 1000)
        pyglet.gl.glClearColor(255, 255, 255, 1.0)
        self.labels = []
        self.shapes = []

    def update_window(self):
        @self.window.event
        def on_draw():
            self.window.clear()
            for shape in self.shapes:
                shape.draw()
            for label in self.labels:
                label.draw()
            # pyglet.app.exit()

        self.window.switch_to()
        self.window.dispatch_event('on_draw')
        self.window.dispatch_events()
        self.window.flip()

    class clickable_circle_label():
        def __init__(self, scale: float, text: str, x: float, y: float):
            self.label = pyglet.text.Label(text,
                                       font_name='Arial',
                                       font_size=36*scale,
                                       bold=True,
                                       x=x, y=y,
                                       anchor_x='center', anchor_y='center',
                                       color=(0, 0, 0, 255))
            randcolor = [random.randint(150,255), random.randint(150,255), random.randint(150,255)]
            self.backdrop = pyglet.shapes.Circle(x=x, y=y, radius=100,
                                                 color = (randcolor[0], randcolor[1], randcolor[2]))
    def choose_num_players(self, welcome_message: str):
        welcome_label = pyglet.text.Label(welcome_message,
                                       font_name='Arial',
                                       font_size=50,
                                       bold=True,
                                       x=self.window.width / 2, y=self.window.height * 3 / 4,
                                       anchor_x='center', anchor_y='center',
                                       color=(0, 0, 0, 255))
        cpu_prompt_label = pyglet.text.Label('How many CPUs would you like to play against?',
                                       font_name='Arial',
                                       font_size=36,
                                       x=self.window.width / 2, y=self.window.height * 2.5 / 4,
                                       anchor_x='center', anchor_y='center',
                                       color=(0, 0, 0, 255),)
        self.labels.append(welcome_label)
        self.labels.append(cpu_prompt_label)
        x_inc = self.window.width/7
        for i in range (1,7):
            temp_click_label = self.clickable_circle_label(1.0, str(i), x_inc*i, self.window.height*1.5/4)
            self.labels.append(temp_click_label.label)
            self.shapes.append(temp_click_label.backdrop)