import pygame
import string
import time

pygame.font.init()

width = 1000
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chatbox")

font = pygame.font.Font("SpaceMono-Regular.ttf", 16)

class Chatbox:
    def __init__(self, x, y, width, height, colour):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)
        self.colour = colour
        self.data = [""]
        self.currentLine = ""
        self.carIdx = 0

        self.cursor = pygame.Rect((self.x+40 + 10*self.carIdx, self.y+self.height-60), (1, 20))

    def updateCaret(self):
        self.cursor = pygame.Rect((self.x+40 + 10*self.carIdx, self.y+self.height-60), (1, 20))
        

    def update(self, win):
        self.updateCaret()
        
        pygame.draw.rect(win, self.colour, self.rect, 0, 5)
        pygame.draw.rect(win, (56,58,64), (self.x+10, self.y+self.height-70, self.width-20,40), 0, 5)
        
        for i in range(len(self.data)-1, -1, -1):
            text = font.render(self.data[i], 1, (229, 232, 235))
            win.blit(text, (self.x+40, self.y+self.height-(i+3)*40))

        win.blit(font.render(self.currentLine, 1, (229, 232, 235)), (round(self.x+40), round(self.y+self.height-62)))

        if time.time() % 1 > 0.5:
            # topleft = (self.rect.x + 5, self.rect.y + 10)
            pygame.draw.rect(win, (229, 232, 235), self.cursor)

    def addMessage(self):
        self.data.insert(0, self.currentLine)
        self.currentLine = ""
        self.carIdx = 0
        self.updateCaret()

    def addChar(self, newChar):
        self.currentLine = self.currentLine[:self.carIdx] + newChar + self.currentLine[self.carIdx:]
        self.carIdx += 1
        self.updateCaret()

def redrawWindow(win, c):
    win.fill((43, 45, 49))
    c.update(win)

    pygame.display.update()

def main():
    run = True
    c = Chatbox(40, 40, 920, 520, (49, 51, 56))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        currentChar = ""

        keys = pygame.key.get_pressed()
        isShifted = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                currentChar = pygame.key.name(event.key)
                if event.key == pygame.K_SPACE:
                    currentChar = " "
                if event.key == pygame.K_RETURN:
                    c.addMessage()
                if event.key == pygame.K_BACKSPACE:
                    c.carIdx = max(0, c.carIdx-1)
                    c.currentLine = c.currentLine[:c.carIdx] + c.currentLine[c.carIdx+1:]
                    c.updateCaret()

                # for moving the caret
                if event.key == pygame.K_RIGHT:
                    c.carIdx = min(len(c.currentLine), c.carIdx + 1)
                if event.key == pygame.K_LEFT:
                    c.carIdx = max(0, c.carIdx - 1)

        c.updateCaret()

                
        if isShifted:
            currentChar = currentChar.upper()

        if currentChar in string.printable and not currentChar == '':
            c.addChar(currentChar)

        redrawWindow(win, c)

main()
