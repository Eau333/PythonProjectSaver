import uno_gfx_api


def run_examples():
    print('Running test examples.')

    # checks that the Uno Graphics library can be reached
    uno_gfx_api.dependency_test()

    # instantiate the basic game window object
    uno_gfx = uno_gfx_api.unogfx()

    # takes in a welcome message
    # draws the "Choose number of CPUs" screen and polls for a click on one of the buttons
    # the result is stored in x, which is a string
    x=uno_gfx.choose_num_players('Welcome to PyUno!')

    print("User selected "+x+" CPUs to play against.")

    uno_gfx.update_window()

