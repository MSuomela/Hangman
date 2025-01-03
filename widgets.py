import pygame
import func

class TextButton:
    def __init__(self, screen, text, size, pos,  on_click, anchor_point = "center",):
        self.screen = screen
        
        normal_font = pygame.font.Font(None, size)
        hover_font = pygame.font.Font(None, size + 10)
        
        self.on_click = on_click
        
        self.normal_surf = normal_font.render(text, False, "black")
        self.hover_surf = hover_font.render(text, False, "white")
        
        self.normal_rect = self.normal_surf.get_rect()
        self.hover_rect = self.hover_surf.get_rect()
        
        setattr(self.normal_rect, anchor_point, pos)
        self.hover_rect.center = self.normal_rect.center
        
        self.rect = self.normal_rect ##
        self.surf = self.normal_surf #
        
    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.rect = self.hover_rect
            self.surf = self.hover_surf
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.on_click()
        else:
            self.rect = self.normal_rect
            self.surf = self.normal_surf
            
    def blit(self):
        self.screen.blit(self.surf, self.rect)

class Button:
    def __init__(self, text, font, box):
        self.box_color = "white"
        self.text = text
        self.font = font
        self.box = box
        self.active = True
        self.surf = self.font.render(text, False, "black")
        self.text_rect = self.surf.get_rect(center=box.center)

    def is_pressed(self):
        self.box_color = "white" #reset color
        is_pressed = False

        mouse_pos = pygame.mouse.get_pos()
        if self.box.collidepoint(mouse_pos):
            self.box_color = "green" #hover color
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                is_pressed = True 
        return is_pressed

    def deactivate(self):
        self.active = False
        self.box_color = "white"

    def activate(self):
        self.active = True
        self.box_color = "white"


    def blit(self, screen):
        screen.fill(self.box_color, self.box)
        screen.blit(self.surf, self.text_rect)
        if self.active == False:
            pygame.draw.line(screen, "red", self.box.topleft, self.box.bottomright, 5)

class Score:
    def __init__(self, font, pos, anchor_point="center"):
        self.score = 0
        self.font = font
        self.pos = pos
        self.anchor_point = anchor_point

        self.surf = None
        self.rect = None

        self.render() #render score
        
    def add_score(self, score):
        self.score += score
        self.render()

    def render(self):
        self.surf = self.font.render(f"SCORE: {self.score}", False, "black")
        self.rect = self.surf.get_rect()
        setattr(self.rect, self.anchor_point, self.pos) #set position


    def blit(self, screen):
        screen.blit(self.surf, self.rect)



class Letter:
    def __init__(self, letter, font, box, visible=True):
        self.letter = letter
        self.font = font
        self.box = box
        self.visible = visible
        self.letter_surf = font.render(letter, False, "black")
        self.letter_rect = self.letter_surf.get_rect(center=box.center) 


class Text:
    def __init__(self, text, font, color, pos):
        self.text = text
        self.font = font
        self.color = color
        self.surf = self.font.render(text, False, color)
        self.rect = self.surf.get_rect(pos=center)

    def blit(self, screen):
        screen.blit(self.surf, self.rect)



class Line:
    def __init__(self, color, start_pos, end_pos, width=1):
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width 

    def draw(self, surf):
        pygame.draw.line(surf, self.color, self.start_pos, self.end_pos, self.width)

class Circle:
    def __init__(self, color, center, radius, width=1):
        self.color = color
        self.center = center
        self.radius = radius
        self.width = width

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, self.center, self.radius, self.width)

class MultilineText:
    def __init__(self, screen, text, font, color, pos):
        lines = text.splitlines()
        self.lines = []
        self.screen = screen
        x, y = pos
        linesize = font.get_linesize()
        for line in lines:
            surf = font.render(line, False, color)
            rect = surf.get_rect(center=(x, y))
            l = (surf, rect)
            self.lines.append(l)
            y += linesize
    def blit(self):
        for line in self.lines:
            self.screen.blit(line[0], line[1])

class Alphabet:
    def __init__(self, font, box, pos, anchor_point="center"):
        self.pos = pos
        self.font = font
        self.box = box
        self.buttons = []
        alphabet = ["A","B","C","D","E","F","G","H",
        "I","J","K","L","M","N","O","P","Q","R","S",
        "T","U","V","W","X","Y","Z"]

        width_inc = box.w + 10
        height_inc = box.h + 10

        x = 13 * width_inc - 10
        y = 2  * height_inc - 10
        self.rect = pygame.Rect((0, 0),(x, y)) #create a rectangle that can fit the entire Alphabet
        setattr(self.rect, anchor_point, pos) #set position

        row = 0
        i = 0
        for letter in alphabet:
            if i == 13:
                row = row + 1
                i = 0
            button = Button(text=letter, font=font, box=pygame.Rect((self.rect.x + width_inc * i, self.rect.y + height_inc * row),(self.box.w, self.box.h)))
            self.buttons.append(button)
            i = i + 1

    def reset_buttons(self):
        print("reset buttons")
        for button in self.buttons:
            button.active = True



    def blit(self, screen):
        #screen.fill("red", self.rect)
        for button in self.buttons:
            button.blit(screen)
      


class HiddenWord:
    def __init__(self, box, font, pos, anchor_point="center"):
        self.pos = pos
        self.anchor_point = anchor_point
        self.font = font
        self.box = box
        self.word = None
        self.hidden_letters = []
        self.width_inc = self.box.w + 10
        self.rect = None
        self.counter = 0 #count how many letters are visible
        self.new_word()
            
    def new_word(self):
        self.hidden_letters = [] #clear hidden_letters
        self.counter = 0 #clear counter
        self.word = func.get_word() #get new hidden word

        w = len(self.word) * self.width_inc - 10
        h = self.box.h

        self.rect = pygame.Rect((0,0),(w, h)) #create a rectangle that can fit the entire word
        setattr(self.rect, self.anchor_point, self.pos) #set rect position

        for  i, letter in enumerate(self.word): #create hidden letters
            self.hidden_letters.append(Letter(box=pygame.Rect((self.rect.x + self.width_inc * i, self.rect.y),(self.box.w, self.box.h)), font=self.font, letter=letter, visible=False))
        
    def blit(self, screen):
        for letter in self.hidden_letters:
            screen.fill("white", letter.box) #fill the box, blit letter if visible
            if letter.visible == True:
                screen.blit(letter.letter_surf, letter.letter_rect)
                
    def guess_letter(self, guess): #update score
        value = 0
        for letter in self.hidden_letters:
            if letter.visible == True:
                value += 1
            elif letter.letter == guess:
                letter.visible = True
                value += 1
        if value == len(self.word): #word was fully revealed
            score_word()

class Hangman:
    def __init__(self, rect, pos, surf, anchor_point="center"):
        self.rect = rect
        self.pos = pos
        self.anchor_point = anchor_point
        self.surf = surf
        self.counter = 0
        setattr(self.rect, self.anchor_point, self.pos) #set position
        self.line_data = [Line("black", self.rect.bottomleft, self.rect.topleft, 5),
        Line("black", (self.rect.x, self.rect.y + 150), (self.rect.x + 200, self.rect.y + 150), 5),
        Line("black", (self.rect.x + 200, self.rect.y + 150), (self.rect.x + 200, self.rect.y + 200), 5),
        Line("black", (self.rect.x, self.rect.y), (self.rect.x + 125, self.rect.y), 5),
        Line("black", (self.rect.x, self.rect.y + 50), (self.rect.x + 50, self.rect.y), 6),
        Line("black", (self.rect.x + 125, self.rect.y), (self.rect.x + 125, self.rect.y + 35), 5),
        Circle("black", (self.rect.x + 125, self.rect.y + 50), 15, 5),
        Line("black", (self.rect.x + 125, self.rect.y + 65), (self.rect.x + 125, self.rect.y + 100), 5),
        Line("black", (self.rect.x + 125, self.rect.y + 100), (self.rect.x + 110, self.rect.y + 125), 6),
        Line("black", (self.rect.x + 125, self.rect.y + 100), (self.rect.x + 140, self.rect.y + 125), 6),
        Line("black", (self.rect.x + 125, self.rect.y + 75), (self.rect.x + 105, self.rect.y + 90), 6),
        Line("black", (self.rect.x + 125, self.rect.y + 75), (self.rect.x + 145, self.rect.y + 90), 6),
        ]
        self.draw_lines = []

    def add_line(self):
        self.draw_lines.append(self.line_data[self.counter])
        self.counter += 1

    def reset_lines(self):
        self.counter = 0
        self.draw_lines = []

    def blit(self, screen):
        for line in self.draw_lines:
            line.draw(screen)



