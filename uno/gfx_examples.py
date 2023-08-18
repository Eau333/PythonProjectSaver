import uno_gfx_api


def run_examples():
    print('Running test examples.')
    uno_gfx_api.dependency_test()
    uno_gfx = uno_gfx_api.unogfx()
    uno_gfx.choose_num_players('Welcome to PyUno!')
    uno_gfx.update_window()

