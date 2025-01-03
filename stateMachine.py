import pygame
import widgets
import func

class StateMachine:
    def __init__(self, screen, states):
            self.states = states
            self.screen = screen
            self.state = None 
            
    def handle_events(self, event):
        self.state.handle_event(event)
        
    def process(self):
        self.state.process()
        
    def draw(self):
        self.state.draw()
        
    def transition_state(self, state):
        self.state = self.states[state]

class State:
    def __init__(self, state_machine):
        self.state_machine = state_machine  # Store reference to the state machine
        
    def handle_event(self, event):
        pass

    def update(self):
        pass
        
    def process(self):
        pass

    def draw(self, screen):
        pass
    

class MainMenu(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.screen = self.state_machine.screen
        def play():
            self.state_machine.transition_state("Play")
        def credit():
            self.state_machine.transition_state("Credits")
        def quit_game():
            pygame.quit()
            exit()
        def test():
            print("test")
            
        tb1 = widgets.TextButton(self.screen,"Play", 50, (400,200), play)
        tb2 = widgets.TextButton(self.screen,"Quit", 50, (400, 350), quit_game, "midbottom")
        tb3 = widgets.TextButton(self.screen,"High Score", 50, (400, tb1.rect.centery + 50), test)
        tb4 = widgets.TextButton(self.screen,"Credits", 50, (400, 20), credit, "midtop")
        
        self.buttons = {tb2, tb3, tb1, tb4}
        
    def process(self):
        for button in self.buttons:
            button.process()
            
                
    def draw(self):
        pygame.Surface.fill(self.screen,"pink") #bg
        for btn in self.buttons:
            btn.blit()
            
class Credits(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        font = pygame.font.Font(None, 30)
        self.screen = self.state_machine.screen
        self.line = widgets.MultilineText(self.screen, "Game made\nBy\nMilo Komulainen", font, "white", (400, 50))
        #self, text, font, pos, color, alignment="left"
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #change state to main_menu
                self.state_machine.transition_state("Main menu")
            
    def draw(self):
        pygame.Surface.fill(self.screen, "pink")
        self.line.blit()
        
            
class Play(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)

        self.screen = self.state_machine.screen

        basic_font = pygame.font.Font(None, 32)
        box = pygame.Rect(0,0, 30, 30)
        rect = pygame.Rect(0,0, 200,200)

        self.hidden_word = widgets.HiddenWord(box=box, font=basic_font, pos=(400, 25), anchor_point="midtop")
        self.alphabet = widgets.Alphabet(box=box, font=basic_font, pos=(400, 375), anchor_point="midbottom")
        self.score = widgets.Score(font=basic_font, pos=(700, 25), anchor_point="midtop")
        self.hangman = widgets.Hangman(rect=rect, surf=self.screen, pos=(400, self.hidden_word.rect.bottom + 25), anchor_point="midtop")
       

    def handle_event(self, event):           
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
                
            elif event.key == pygame.K_ESCAPE: #change state to main_menu
                self.state_machine.transition_state("Main menu")

            elif event.key == pygame.K_RETURN:
                if len(self.user_input) == 1: #guess letter
                    print(self.user_input)
                    self.hidden_word.guess_letter(self.user_input)
     
                elif len(self.user_input) == len(self.hidden_word.word): #guess word
                    guess = self.hidden_word.guess_word(self.user_input)

                else:
                    print("input must be a sigle letter or the entire word")
                    
                
            else: #add letter to the input box
                if len(self.user_input) < len(self.hidden_word.word):
                    self.user_input += event.unicode

    def process(self): #handle buttons
        for button in self.alphabet.buttons:
            if button.active == True:
                if button.is_pressed():
                    button.deactivate() # 
                    self.guess_letter(button)


    def guess_letter(self, button):
        indices = func.find_all(self.hidden_word.word.lower(), button.text.lower()) #find out if the letter you pressed occures in the word
        if indices: #right answer
            for i in indices:
                self.hidden_word.hidden_letters[i].visible = True
                self.score.add_score(50)
                self.hidden_word.counter += 1
                if self.hidden_word.counter == len(self.hidden_word.word): #entire word was revealed
                    self.new_word()
                    self.hangman.reset_lines()
        else: #wrong answer
            self.hangman.add_line()
   
    def new_word(self):
        self.hidden_word.new_word()
        self.alphabet.reset_buttons()


    def draw(self):
        pygame.Surface.fill(self.screen, "yellow") #bg
        self.hidden_word.blit(self.screen)
        self.alphabet.blit(self.screen)
        self.score.blit(self.screen)
        self.hangman.blit(self.screen)

class Game_over(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.screen = state_machine.screen
        game_over = pygame.font.Font(None, 60)
        self.line = widgets.Text("GAME OVER",game_over, "white", (400, 200))

    def draw(self):
        pygame.Surface.fill(self.screen, "black")


