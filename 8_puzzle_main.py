from puzzle_algo import Algo
import pygame
import pygame_gui
import time
import global_colors

SCREEN_SIZE = (850, 600)
pygame.init()
BASICFONT = pygame.font.Font('Roboto-Medium.ttf',50)
pygame.display.set_caption('8 Puzzle Game')
window_surface = pygame.display.set_mode(SCREEN_SIZE)
background = pygame.Surface(SCREEN_SIZE)
background.fill(pygame.Color(global_colors.BABY_BLUE))
manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')
pygame_gui.core.IWindowInterface.set_display_title(self=window_surface,new_title="8-Puzzle")

#shuffle button
button_layout_rect = pygame.Rect((340, 40), (150, 30))
shuffle_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='Shuffle',
                                             manager=manager)

#algorithm dropdown
dropdown_layout_rect = pygame.Rect((290, 100), (270, 40))
algorithmOptions = ["A* Algorithm","Breadth-First Search Algorithm"]
algorithmDropDown = pygame_gui.elements.UIDropDownMenu(options_list=algorithmOptions,
                                                       starting_option=algorithmOptions[1],
                                                       relative_rect=dropdown_layout_rect,
                                                       manager=manager)

#solve button
solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 160), (200, 40)),
                                             text='Solve',
                                             manager=manager,
                                             object_id="#solve_btn")

def draw_blocks(blocks):
    for block in blocks:
        if block['block'] != 0:
            pygame.draw.rect(window_surface, global_colors.BLUE_GREEN, block['rect'])
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
algorithm = "Breadth-First Search Algorithm"
fstate="1,2,3,4,5,6,7,8,0"
is_running = True
show_confirmaton = False
tempo = ''
info = ''

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    random_blocks = puzzle.randomBlocks()
                elif event.ui_element == solve_button:
                    if algorithm == "Breadth-First Search Algorithm":
                        try:
                            comp_time, moves = puzzle.bfs(random_blocks)
                            print('Solution found!')
                        except NameError:
                            comp_time, moves = 0, []
                        tempo = "{temp: .3f} seconds".format(temp = comp_time)
                        info = '<b>Visited nodes:</b>'+str(puzzle.cost)+'\n<b>Time:</b>'+tempo+ '\n<b>No. of Steps:</b> '+str(len(moves))
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((570, 300), (100, 40)),
                                                                                                manager = manager,
                                                                                                action_long_desc = info,
                                                                                                window_title =algorithm.split(" ")[0],
                                                                                                )
                        solveAnimation(moves)

                    elif algorithm == "A* Algorithm":
                        moves = puzzle.a_star()
                        tempo = "{temp: .3f} seconds".format(temp = puzzle.lastSolveTime)
                        info = '<b>Visited nodes:</b> '+str(puzzle.cost)+'\n<b>Time:</b>'+tempo+ '\n<b>No. of Steps:</b> '+str(len(moves))
                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((570, 300), (80, 60)),
                                                                                                manager = manager,
                                                                                                action_long_desc = info,
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
