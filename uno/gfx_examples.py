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
    uno_gfx.set_card_counts(total_cards=190, cards_per_player=20)

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
    uno_gfx.update_window()


