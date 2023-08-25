import uno_gfx_api
import time

def run_examples():
    print('Running test examples.')

    # checks that the Uno Graphics library can be reached
    uno_gfx_api.dependency_test()

    # instantiate the basic game window object
    uno_gfx = uno_gfx_api.unoGfx()

    # set the welcome message
    uno_gfx.set_welcome_message(welcome_message='Welcome to PyUno!')

    # draws the "Choose number of CPUs" screen and polls for a click on one of the buttons
    uno_gfx.choose_num_players()

    # get the number of cpus the player clicked
    x = uno_gfx.get_num_cpu()

    # print the user's selection to make sure it worked
    print("User selected "+str(x)+" CPUs to play against.")

    # set the starting number of cards per player and total number of cards
    uno_gfx.set_card_counts(total_cards=220, cards_per_player=20)

    # set up the main game board
    uno_gfx.main_setup()

    # set up the active card
    uno_gfx.set_active_card("blue", "Reverse")

    # draw everything
    uno_gfx.update_window()

    # wait 2s then pretend it's CPU 1 turn
    time.sleep(2)
    uno_gfx.set_message('It\'s CPU 1\'s turn.')
    uno_gfx.cpu_list[0].toggle_highlight()
    uno_gfx.update_window()

    # pretend CPU 1 had to draw a card
    time.sleep(2)
    uno_gfx.set_message('CPU 1 drew two cards.')
    uno_gfx.cpu_list[0].card_count += 2
    uno_gfx.draw_pile.draw_pile_size -= 2
    uno_gfx.update_window()
    uno_gfx.cpu_list[0].toggle_highlight()

    time.sleep(2)
    uno_gfx.set_message('Set draw pile size to 0')
    uno_gfx.set_draw_pile_size(0)
    uno_gfx.update_window()

    time.sleep(2)
    uno_gfx.set_message('Set draw pile size to 25')
    uno_gfx.set_draw_pile_size(25)
    uno_gfx.update_window()

    time.sleep(2)
    uno_gfx.set_message('It\'s your turn')
    uno_gfx.player_hand.add_player_card('green', 'number', 7)
    uno_gfx.player_hand.add_player_card('red', 'number', 0)
    uno_gfx.player_hand.add_player_card('green', 'draw2')
    uno_gfx.player_hand.add_player_card('wild', 'draw4')
    uno_gfx.player_hand.add_player_card('yellow', 'number', 3)
    uno_gfx.player_hand.add_player_card('blue', 'number', 9)
    uno_gfx.player_hand.toggle_highlight()
    uno_gfx.update_window()

    time.sleep(2)
    uno_gfx.set_message('You played wild draw 4')
    uno_gfx.player_hand.remove_card_index(3)
    uno_gfx.set_active_card('wild', 'draw4')
    uno_gfx.player_hand.toggle_highlight()
    uno_gfx.update_window()

    time.sleep(2)
    uno_gfx.set_message('Set discard pile size to 15')
    uno_gfx.active_pile.discard_pile_size = 15
    uno_gfx.update_window()

    time.sleep(2)
    uno_gfx.set_message('Set discard pile size to 0')
    uno_gfx.active_pile.discard_pile_size = 0
    uno_gfx.update_window()

    time.sleep(2)
    uno_gfx.set_message('Set discard pile size to 35')
    uno_gfx.active_pile.discard_pile_size = 35
    uno_gfx.update_window()

    time.sleep(2)
    uno_gfx.set_message('You played green 7')
    uno_gfx.player_hand.remove_card_index(0)
    uno_gfx.set_active_card('green', '7')
    uno_gfx.update_window()


    time.sleep(2)
    uno_gfx.player_hand.add_player_card("yellow","reverse")
    uno_gfx.player_hand.add_player_card("red", "9")
    uno_gfx.player_hand.add_player_card("blue", "skip")
    uno_gfx.player_hand.toggle_highlight()
    while len(uno_gfx.player_hand.cards)>0:
        uno_gfx.set_message('Select a card to play')
        selected_card_index = uno_gfx.read_player_move()
        uno_gfx.set_message('Selected card index ' + str(selected_card_index))
        uno_gfx.player_hand.remove_card_index(selected_card_index)
        uno_gfx.update_window()
        time.sleep(2)
