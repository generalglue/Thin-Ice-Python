'''
Name: Victor Li
Date: 5/7/2020
Description: Pygame remake of Club Penguin's Thin-ice
'''

# Import classes used for the game
import pygame as pg
from sprites import *
from settings import *


class Game():
    '''This class defines the main game'''

    def __init__(self):
        '''This initalizer takes the game scene as a paraemter, initalizes
        the image and rect attributes and other variables used for the player'''
        
        # Starts up the game and the audio
        pg.init()
        pg.mixer.init()
        pg.display.set_caption("Thin-Ice!")
        
        # Allows to hold down input keys
        pg.key.set_repeat(150, 150)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        
        # Clock used to set the frame rate
        self.clock = pg.time.Clock()
        
        # Holds the map data
        self.mapData = []
        
        
    def loadData(self):
        '''This method loads data from files outside of Python'''
        self.playerSpriteSheet = Spritesheet(PLAYERSPRITE, PLAYERXML)
        self.waterSpriteSheet = Spritesheet(WATERSPRITE, WATERXML)
        
        # Loads the Background music
        pg.mixer.music.load('sound/music.mp3')
        pg.mixer.music.set_volume(0.1)
        
        # Sound effect when a player moves
        self.moveSound = pg.mixer.Sound("sound/move.mp3")
        self.moveSound.set_volume(0.05)

    def loadMap(self):
        '''Load the current level by reading a .txt '''
        currentMap = open("test.txt", "r")
        for line in currentMap:
            self.mapData.append(line)
            
        for row, tiles in enumerate(self.mapData):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                if tile == '0':
                    Unused(self, col, row)
                if tile == 'F':
                    Free(self, col, row) 
                if tile == 'P':
                    Free(self, col, row)
                    self.player = Player(self, col, row)
                    


    def new(self):
        '''This method initializes all the variables and sets up the game '''
        
        self.loadData()
        
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.movable = pg.sprite.Group()
        
        # Load the map
        self.loadMap()        
        
        pg.mixer.music.play(-1)
        

    def run(self):
        '''This method is the game loop which runs most of the game '''
        self.looping = True
        while self.looping:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        '''This method updates all classes/objects as part of the game loop '''
        self.allSprites.update()

    def drawGrid(self):
        '''This method draws the grid for more precise x,y coordinates '''
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def draw(self):
        '''This method draws all the sprites onto the screen '''
        self.screen.fill(BGCOLOR)
        #self.drawGrid()
        self.allSprites.draw(self.screen)
        pg.display.flip()
              

    def events(self):
        '''This method handles the event handling'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)

g = Game()
while True:
    g.new()
    g.run()
