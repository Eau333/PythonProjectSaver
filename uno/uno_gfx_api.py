import pyglet
import random

def dependency_test():
    print('API successfully invoked.')


class unoGfx():
    def __init__(self):
        # fields
        self.welcome_message = None
        self.labels = []
        self.clickable_circles = []
        self.num_cpu = 0
        self.cpu_list = []
        self.total_cards = 0
        self.cards_per_player = 0
        self.discard_pile_size = 0
        self.draw_pile_size = 0
        self.main_message = None
        self.activeCard = None

        # initializing the game window
        self.window = pyglet.window.Window()
        self.window.set_size(1500, 1000)
        pyglet.gl.glClearColor(255, 255, 255, 1.0)

    def set_welcome_message(self, welcome_message):
        self.welcome_message = welcome_message

    def set_card_counts(self, total_cards: int, cards_per_player: int):
        self.total_cards = total_cards
        self.cards_per_player = cards_per_player
        self.draw_pile_size = total_cards - cards_per_player * (self.num_cpu + 1)

    def get_num_cpu(self):
        return self.num_cpu

    def update_window(self):
        @self.window.event
        def on_draw():
            self.window.clear()
            for label in self.labels:
                label.draw()
            for circle in self.clickable_circles:
                circle.draw()
            for cpu in self.cpu_list:
                cpu.draw()
            if self.activeCard is not None:
                self.activeCard.draw()
        self.window.switch_to()
        self.window.dispatch_event('on_draw')
        self.window.dispatch_events()
        self.window.flip()

    class clickable_circle():
        def __init__(self, scale: float, text: str, x: float, y: float):
            self.label = pyglet.text.Label(text,
                                       font_name='Arial',
                                       font_size=36*scale,
                                       bold=True,
                                       x=x, y=y,
                                       anchor_x='center', anchor_y='center',
                                       color=(0, 0, 0, 255))
            randcolor = [random.randint(175,255), random.randint(175,255), random.randint(175,255)]
            self.backdrop = pyglet.shapes.Circle(x=x, y=y, radius=100*scale,
                                                 color = (randcolor[0], randcolor[1], randcolor[2]))

        def draw(self):
            self.backdrop.draw()
            self.label.draw()

        def click_interior(self, x: int, y: int):
            xdiff = (x-self.backdrop.x)
            ydiff = (y - self.backdrop.y)
            dist_squared = xdiff*xdiff+ydiff*ydiff
            if dist_squared <= (self.backdrop.radius * self.backdrop.radius):
                return True
            return False

    def choose_num_players(self):
        welcome_label = pyglet.text.Label(self.welcome_message,
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
        for i in range(1,7):
            temp_click_circle = self.clickable_circle(1.0, str(i), x_inc*i, self.window.height*1.5/4)
            self.clickable_circles.append(temp_click_circle)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == pyglet.window.mouse.LEFT:
                for circle in self.clickable_circles:
                    if circle.click_interior(x, y):
                        self.num_cpu = int(circle.label.text)
                        pyglet.app.exit()
                        return

        self.update_window()
        pyglet.app.run()
        return

    class facedownCard():
        def __init__(self, base_x: int, base_y: int, card_index: int):
            stack_offset = 15
            self.base_x = base_x + card_index * stack_offset
            self.base_y = base_y - 20
            card_height = 150
            card_width = 100
            border_thickness = 5
            self.base_rectangle = pyglet.shapes.BorderedRectangle(x=self.base_x, y=self.base_y-card_height,
                                                                  width=card_width, height=card_height,
                                                                  color=(255,255,255,255),
                                                                  border_color=(0,0,0,255))
            self.black_rectangle = pyglet.shapes.Rectangle(x=self.base_x+border_thickness,
                                                           y=self.base_y-card_height+border_thickness,
                                                           width=card_width-border_thickness*2,
                                                           height=card_height-border_thickness*2,
                                                           color=(0,0,0,255))
            self.red_circle = pyglet.shapes.Circle(x=self.base_x+card_width/2, y=self.base_y-card_height/2,
                                                   radius = card_width/2-border_thickness, color=(255,0,0,255))
            self.yellow_label = pyglet.text.Label('UNO', font_name='Arial', font_size=15*card_height/100,
                                                  bold=True, x=self.base_x+card_width/2,
                                                  y=self.base_y-card_height/2,
                                                  anchor_x='center', anchor_y='center',
                                                  color=(255,255,0,255), rotation=-20)

        def draw(self):
            self.base_rectangle.draw()
            self.black_rectangle.draw()
            self.red_circle.draw()
            self.yellow_label.draw()

    class faceupCard():
        def __init__(self, scale: float, base_x: int, base_y: int, colour: str, action: str, number: int):
            card_height = 150*scale
            card_width = 100*scale
            border_thickness = 5 * scale
            self.colour = (100,100,100,255)
            if number >= 0:
                self.text = str(number)
            else:
                self.text = action
            self.base_rectangle = pyglet.shapes.BorderedRectangle(x=base_x, y=base_y-card_height,
                                                                  width=card_width, height=card_height,
                                                                  color=(255,255,255,255),
                                                                  border_color=(0,0,0,255))
            if "blue" in colour.lower():
                self.colour = (0,0,255,255)
            elif "yellow" in colour.lower():
                self.colour = (255, 255, 0, 255)
            elif "red" in colour.lower():
                self.colour = (255, 0, 0, 255)
            elif "green" in colour.lower():
                self.colour = (0, 255, 0, 255)
            elif "wild" in colour.lower():
                self.colour = (0, 0, 0, 255)

            self.color_rectangle = pyglet.shapes.Rectangle(x=base_x+border_thickness,
                                                           y=base_y-card_height+border_thickness,
                                                           width=card_width-border_thickness*2,
                                                           height=card_height-border_thickness*2,
                                                           color=self.colour)
            self.white_circle = pyglet.shapes.Circle(x=base_x+card_width/2, y=base_y-card_height/2,
                                                   radius = card_width/2-border_thickness, color=(255,255,255,255))
            self.black_label = pyglet.text.Label(self.text, font_name='Arial',
                                                 font_size=15*card_height / 100 * 5 / len(self.text),
                                                 bold=True, x=base_x+card_width/2,
                                                 y=base_y-card_height/2,
                                                 anchor_x='center', anchor_y='center',
                                                 color=(0,0,0,255), rotation=-20)

        def draw(self):
            self.base_rectangle.draw()
            self.color_rectangle.draw()
            self.white_circle.draw()
            self.black_label.draw()
            # do something

    def set_active_card(self, colour: str, action: str, number=-1):
        self.activeCard = self.faceupCard(scale=1.5, base_x=self.window.width*0.55, base_y=self.window.height*0.8,
                                          colour=colour, action=action, number=number)

    class cpuGfx():
        def __init__(self, cpu_index: int, card_count: int, base_x: int, base_y: int):
            self.is_highlighted = False
            self.card_count = card_count
            self.cards = []
            self.base_x = base_x
            self.base_y = base_y
            self.cpu_index = cpu_index
            self.label = pyglet.text.Label('',
                                          font_name='Arial',
                                          font_size=25,
                                          bold=True,
                                          x=base_x, y=base_y,
                                          color=(0, 0, 0, 255))
            self.highlight_rectangle = pyglet.shapes.Rectangle(x=self.base_x-10, y=self.base_y-180,
                                                               width=420, height=220, color=(255,255,0,150))

        def draw(self):
            if self.is_highlighted:
                self.highlight_rectangle.draw()
            self.label.text = 'CPU '+str(self.cpu_index)+': '+str(self.card_count)+' cards'
            self.label.draw()
            while len(self.cards) < self.card_count:
                self.cards.append(unoGfx.facedownCard(self.base_x, self.base_y, len(self.cards)))
            while len(self.cards) > self.card_count:
                del self.cards[-1]
            for card in self.cards:
                card.draw()

        def toggle_highlight(self):
            self.is_highlighted = ~self.is_highlighted

    def main_setup(self):
        self.clickable_circles.clear()
        self.labels.clear()
        self.main_message = pyglet.text.Label('It is your turn.',
                                          font_name='Arial',
                                          font_size=30,
                                          bold=True,
                                          x=self.window.width / 2, y=self.window.height * 1 / 4,
                                          anchor_x='center', anchor_y='center',
                                          color=(0, 0, 0, 255))
        self.labels.append(self.main_message)
        y_spacing = 0.23
        for i in range(0, self.num_cpu):
            base_x = 25
            cpu_index = 0
            if i >= 3:
                base_x += self.window.width * 0.71
                base_y = self.window.height-50 - self.window.height * y_spacing * (i % 3)
            else:
                base_y = self.window.height - 50 - self.window.height * y_spacing * ((2 - i) % 3)
            temp_cpu = self.cpuGfx(cpu_index = i+1, card_count=self.cards_per_player, base_x=base_x, base_y=base_y)
            self.cpu_list.append(temp_cpu)

    def set_message(self, message: str):
        self.main_message.text = message

