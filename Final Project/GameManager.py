import turtle 
from Player import Player
from Position import Position
import pdb
import random
import time
import os.path
from os import path
import math

class Card(): # Creates Card images and onclick functionality for game
    def __init__(self, front_image, x, y, manager):
        '''
        Name: __init__
        Parameters: self, front_image, x, y
        Return: None
        '''
        self.back_image = "card_back.gif" 
        self.front_image = front_image
        self.front_turtle = turtle.Turtle()
        self.x = x
        self.y = y
        self.faceup = False
        self.active = True
        self.manager = manager
    
    def setup(self):
        '''
        Name: setup
        Parameters: self
        Return: None
        '''
        self.front_turtle.up()
        self.front_turtle.shape(self.back_image)
        self.front_turtle.goto(self.x, self.y)
        self.front_turtle.onclick(self.process_click)
        self.front_turtle.st()

    def deactivate(self):
        '''
        Name: deactivate
        Parameters: self
        Return: None
        '''
        self.active = False
        self.front_turtle.ht() 

    def flip_faceup(self):
        '''
        Name: flip_faceup
        Parameters: self
        Return: None
        '''
        self.front_turtle.shape(self.front_image)
        self.faceup = True

    def flip_facedown(self):
        '''
        Name: flip_facedown
        Parameters: self
        Return: None
        '''
        self.front_turtle.shape(self.back_image)
        self.faceup = False

    def process_click(self, x, y):
        '''
        Name: process_click
        Parameters: self, x, y
        Return
        '''
        self.manager.process_card_click(self)
        
       
    def __str__(self):
        ''''
        Name: __str__
        Parameters: self
        Return: self.front_image
        '''
        return self.front_image


    def __eq__(self, other):
        '''
        Name: __eq__
        Parameters: self, other
        Return: string of self = string of other
        '''
        return str(self) == str(other)
    


class GameManager():
    def __init__(self):
        '''
        Name: __init__
        Parameter: self
        Return: none-> constructor
        '''
        self.status_turtle = turtle.Turtle()
        self.guesses = 0
        self.matches = 0
        self.players = []
        self.name = None
        self.flip_card = None
        self.window = turtle.Screen()
        self.window.setup(800,800)
        self.window.bgcolor("white")  
        

    def process_card_click(self, card):
        '''
        Name: process_click
        Parameters: self, card 
        Return
        '''

        if not card.active:
            # Card is not active so don't do anything as this card is hidden
            return
        
        if card.faceup:
            # Card is already faceup. There is nothing to do
            return

        if self.flip_card is card:
            # This card is already the first one flipped. Don't need to do anything more if its clicked again
            return

        # Let's flip this card faceup since it hasn't already been done
        card.flip_faceup()

        if self.flip_card is None:
            # This is the first card flipped. Assign it to self.flip_card slot and wait for another card to be clicked
            self.flip_card = card
            return
        
        # Let's leave them faceup for a bit before flipping them facedwon or hiding them forever
        time.sleep(1)

        # At this point, a different card is already flipped and stored in the self.flip_card slot
        if card == self.flip_card:
            # We have a match if the current Card has the same image as the Card in the self.flip_card slot
            self.matches = self.matches + 1
            # Now deactivate current card and other self.flip_card since it's a match
            card.deactivate()
            self.flip_card.deactivate()
        else:
            # The self.flip_card doesn't match the current Card so just flip both cards facedown
            card.flip_facedown()
            self.flip_card.flip_facedown()
            
        self.guesses = self.guesses + 1
        # Clear the self.flip_card slot as the match is now hidden and no cards are facing up
        self.flip_card = None
        self.update_status()
        if self.matches == self.num_cards/2:
            print("You won the game")
            self.players.append(Player(self.name, self.guesses))
            self.write_scores()
                


    def draw_box(self, x, y, width, length):
        '''
        Name: draw_box
        Parameters: self, x, y, width, length
        Return: None
        '''
        box = turtle.Turtle()
        box.pensize(5)
        box.pu()
        box.setposition(x, y)
        box.pd()
        box.rt(90)
        box.fd(length)
        box.lt(90)
        box.fd(width)
        box.lt(90)
        box.fd(length)
        box.lt(90)
        box.fd(width)
        
    def read_scores(self):
        '''
        Name: read_scores
        Parameters: self
        Return Scores
        '''
        if not path.exists("scores.txt"):
            return    
        
        file1 = open("scores.txt", "r")
        while True:
            #read next line
            name = file1.readline().strip()
            #check if line is not null
            if not name:
                break
            score = int(file1.readline().strip())
            #you can access the line
            player = Player(name, score)
            self.players.append(player)
            
        
        self.players.sort()
        file1.close

    def write_scores(self):
        '''
        Name: write_scores
        Parameters: self
        Return: None
        '''
        f = open("scores.txt", 'w+')
        f.seek(0)

        self.players.sort()
        for player in self.players:
            f.write(player.name)
            f.write('\n')
            f.write(str(player.score))
            f.write('\n')

        
        f.truncate()
        f.close()

    def print_players(self):
        '''
        Name: print_players
        Parameters: self
        Return: None
        '''
        for player in self.players:
            print(player.name + "\n")
            print(str(player.score) + "\n")

    def quit_game(self, x, y):
        '''
        Name: quit_game
        Parameters: self, x, y
        Return: None
        '''
        turtle.bye()

    def update_status(self):
        '''
        Name: update_status
        Parameters: None
        Return: None
        '''
        
        self.status_turtle.reset()
        self.status_turtle.penup()
        self.status_turtle.goto(-200, -300) 
        self.status_turtle.write("Guesses: ", font=("Arial", 18, "normal") )
        self.status_turtle.setx(self.status_turtle.xcor() + 100)
        self.status_turtle.write(self.guesses,font=("Arial", 18, "normal") )
        self.status_turtle.setx(self.status_turtle.xcor() + 100)
        self.status_turtle.write("Matches: ", font=("Arial", 18, "normal"))
        self.status_turtle.setx(self.status_turtle.xcor() + 100)
        self.status_turtle.write(self.matches,font=("Arial", 18, "normal") )
        self.status_turtle.ht()


    def play(self):
        
        #draws gameboard
        self.draw_box(-380, 380, 500, 600)
        self.draw_box(140, 380, 240, 600)
        self.draw_box(-380, -240, 500, 100)
 
        self.update_status()
        
        # creates positions for cards on gameboard
        positions = []
        positions.append(Position(-300, 300))
        positions.append(Position(-200, 300))
        positions.append(Position(-100, 300))
        positions.append(Position(0, 300))
        positions.append(Position(0, 150))
        positions.append(Position(-300, 150))
        positions.append(Position(-200, 150))
        positions.append(Position(-100, 150))
        positions.append(Position(0, 0))
        positions.append(Position(-300, 0))
        positions.append(Position(-200, 0))
        positions.append(Position(-100, 0))
        
        

        self.window.register_shape("card_back.gif")
        self.window.register_shape("quitbutton.gif") 
        gifs = ["2_of_clubs.gif","3_of_hearts.gif","2_of_diamonds.gif","ace_of_diamonds.gif", "jack_of_spades.gif", "king_of_diamonds.gif","queen_of_hearts.gif"]    
        for i in range(len(gifs)):
            self.window.register_shape(gifs[i])

        self.name = self.window.textinput("Name", "Input your name")
        cards = []
        self.num_cards = self.window.numinput("Matching Game", "Input the number of cards you would like", 8, 8, 12)    
        if self.num_cards == 9:
           self.num_cards = 10
        if self.num_cards == 11:
            self.num_cards = 12
            
            
        for i in range(int(self.num_cards/2)):
        #remove positions from positions list so they cant be selected on next iteration
            random_pos1 = random.randint(0,len(positions) - 1)
            position1 = positions[random_pos1]
            positions.remove(position1)
            
            random_pos2 = random.randint(0,len(positions) - 1)
            position2 = positions[random_pos2]
            positions.remove(position2)
            
            cards.append(Card(gifs[i], position1.x, position1.y, self))
            cards.append(Card(gifs[i], position2.x, position2.y, self))

        for i in range(len(cards)):
            cards[i].setup()

        self.read_scores()
        
        # implements names in leader board 
        turtle.penup()
        turtle.setposition(200, 300)
        turtle.pendown()
        turtle.write("LEADERS")
        turtle.penup()
        for i in range(min(6, len(self.players))):
            turtle.setposition(200, 300 - 30 * (i + 1))
            turtle.pendown()
            turtle.write(f"Score: {self.players[i].score} Player: {self.players[i].name}")
            turtle.penup()
        
        # sets up quit button on gameboard
        quit_button = turtle.Turtle()
        quit_button.penup()
        quit_button.goto(300, -300)
        quit_button.shape("quitbutton.gif")
        quit_button.onclick(self.quit_game)

        
    
 
