import pygame
import func
import stateMachine as sm

pygame.init()
screen = pygame.display.set_mode((800, 400))
running = True

state_machine = sm.StateMachine(screen, None)
states = states = {
        "Play": sm.Play(state_machine),
        "Main menu" : sm.MainMenu(state_machine),
        "Credits" : sm.Credits(state_machine)
        }
state_machine.states = states
state_machine.state = states["Main menu"]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #press x to quit
            running = False 
        state_machine.handle_events(event)
        
    state_machine.process()
    state_machine.draw()
    pygame.display.update()
    
pygame.quit()
sys.exit()