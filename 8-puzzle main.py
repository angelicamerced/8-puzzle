from puzzle_algo import Algo
import pygame
import pygame_gui
import time
import global_colors

SCREEN_SIZE = (800, 600)
pygame.init()
BASICFONT = pygame.font.Font('Roboto-Medium.ttf',50)
pygame.display.set_caption('8 Puzzle Game')
window_surface = pygame.display.set_mode(SCREEN_SIZE)
background = pygame.Surface(SCREEN_SIZE)
background.fill(pygame.Color(global_colors.WHITE))
manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')
pygame_gui.core.IWindowInterface.set_display_title(self=window_surface,new_title="8-Puzzle")


def display_elements():
    #Elements
    '''
    pygame_gui.elements.ui_label.UILabel(manager=manager,
                                        text="8-Puzzle Game",
                                        relative_rect=pygame.Rect((250, 5), (300, 50)),
                                        object_id="#title_box"
                                        )
    '''

display_elements()
#solve button
solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((375, 100), (90, 30)),
                                             text='Solve',
                                             manager=manager,
                                             object_id="#solve_btn")

#algorithm dropdown
dropdown_layout_rect = pygame.Rect((320, 60), (200, 35))
algorithmOptions = ["A*","BFS"]
algorithmDropDown = pygame_gui.elements.UIDropDownMenu(options_list=algorithmOptions,
                                                       starting_option=algorithmOptions[1],
                                                       relative_rect=dropdown_layout_rect,
                                                       manager=manager)

#shuffle button
button_layout_rect = pygame.Rect((340, 170), (150, 30))
shuffle_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='Shuffle',
                                             manager=manager)

def draw_blocks(blocks):
    for block in blocks:
        if block['block'] != 0:
            pygame.draw.rect(window_surface, global_colors.BLUE_GROTTO, block['rect'])
            textSurf = BASICFONT.render(str(block['block']), True, global_colors.NAVY_BLUE)
            textRect = textSurf.get_rect()
            textRect.center = block['rect'].left+50,block['rect'].top+50
            window_surface.blit(textSurf, textRect)
        else:
            pygame.draw.rect(window_surface, global_colors.ROYAL_BLUE, block['rect'])

def solveAnimation(moves):
    for mv in moves:
        zero = puzzle.matrix.searchBlock(0)
        if mv == "right":
            puzzle.matrix.moveright(zero)
        elif mv == "left":
            puzzle.matrix.moveleft(zero)
        elif mv == "up":
            puzzle.matrix.moveup(zero)
        elif mv == "down":
            puzzle.matrix.movedown(zero)
        puzzle.setBlocksMatrix()
        draw_blocks(puzzle.blocks)
        pygame.display.update()
        time.sleep(0.2)

window_surface.blit(background, (0, 0))
pygame.display.update()
clock = pygame.time.Clock()
puzzle = Algo.new(250, 220, 330, 330)
puzzle.initialize()
algorithm = "BFS"
fstate="1,2,3,4,5,6,7,8,0"
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    puzzle.randomBlocks()
                elif event.ui_element == solve_button:

                    if algorithm == "BFS":
                        moves = puzzle.bfs()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.lastSolveTime)
                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.cost)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((570, 300), (40, 50)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algorithm.split(" ")[0],
                                                                                                object_id="#bfs",
                                                                                                )
                        solveAnimation(moves)

                    elif algorithm == "A*":
                        moves = puzzle.a_star()
                        tempo = "{temp: .5f} seconds".format(temp = puzzle.lastSolveTime)
                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.cost)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((570, 300), (80, 60)),
                                                                                                manager = manager,
                                                                                                action_long_desc = report_msg,
                                                                                                window_title =algorithm.split(" ")[0],
                                                                                                )
                        solveAnimation(moves)

            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithmDropDown:
                    algorithm = event.text
        manager.process_events(event)

    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    draw_blocks(puzzle.blocks)
    pygame.display.update()
