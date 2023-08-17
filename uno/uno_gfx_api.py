import pyglet
def dependency_test():
    print('API successfully invoked.')

def game_setup():
    window = pyglet.window.Window()
    window.set_size(1500,1000)
    label = pyglet.text.Label('Hello, world',
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width // 2, y=window.height // 2,
                              anchor_x='center', anchor_y='center')
    @window.event
    def on_draw():
        window.clear()
        label.draw()
        pyglet.app.exit()

    window.switch_to()
    window.dispatch_event('on_draw')
    window.dispatch_events()
    window.flip()

#    pyglet.app.run()


