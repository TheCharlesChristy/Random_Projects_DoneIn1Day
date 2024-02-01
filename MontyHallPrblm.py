import random

class Door:
    def __init__(self):
        self.prize = None
    
    def Open(self):
        return self.prize
    
    def setPrize(self, prize):
        self.prize = prize

class Host:
    def __init__(self, doors):
        self.doors = doors

    def RevealDoor(self, Player_selection):
        if Player_selection == 0:
            if self.doors[1].prize == 'Goat':
                return 1
            else:
                return 2
        elif Player_selection == 1:
            if self.doors[0].prize == 'Goat':
                return 0
            else:
                return 2
        else:
            if self.doors[0].prize == 'Goat':
                return 0
            else:
                return 1

class Player:
    def __init__(self, strategy):
        self.wins = 0
        self.strategy = strategy
        self.currentSelection = -1
    
    def ChooseDoor(self, DoorRevealed):
        if self.currentSelection < 0:
            self.currentSelection = random.randint(0,2)
        else:
            if self.strategy=="Switch":
                if self.currentSelection==0:
                    if DoorRevealed==1:
                        self.currentSelection=2
                    else:
                        self.currentSelection=1
                elif self.currentSelection==1:
                    if DoorRevealed==0:
                        self.currentSelection=2
                    else:
                        self.currentSelection=0
                elif self.currentSelection==2:
                    if DoorRevealed==0:
                        self.currentSelection=1
                    else:
                        self.currentSelection=0
            else:
                pass
        return self.currentSelection
    
    def RecievePrize(self, prize):
        if prize=='Car':
            self.wins+=1
        self.currentSelection=-1
    
    def Reset(self):
        self.wins = 0
        self.strategy = 'Stay'
        self.currentSelection = -1

class Game:
    def __init__(self, player):
        self.door1 = Door()
        self.door2 = Door()
        self.door3 = Door()
        self.doors = [self.door1,self.door2,self.door3]
        cardoor = random.randint(0,2)
        for i in range(len(self.doors)):
            door = self.doors[i]
            if i == cardoor:
                door.setPrize("Car")
            else:
                door.setPrize("Goat")
        self.Host = Host(self.doors)
        self.Player = player

    def Play(self):
        Player_selection = self.Player.ChooseDoor(-1)
        DoorRevealed = self.Host.RevealDoor(Player_selection)
        Final_Player_Choice = self.Player.ChooseDoor(DoorRevealed)
        Final_Prize = self.doors[Final_Player_Choice].prize
        self.Player.RecievePrize(Final_Prize)
        print(self.Player.strategy, "Won", Final_Prize)
        return self.Player

class Simulation:
    def __init__(self):
        self.Player = Player('Switch')
        self.switchwins = 0
        self.staywins = 0

    def runGame(self):
        currgame = Game(self.Player)
        self.Player = currgame.Play()
    
    def runSim(self, trials):
        for i in range(trials//2):
            self.runGame()
        self.switchwins = self.Player.wins
        self.Player.Reset()
        for i in range(trials//2):
            self.runGame()
        self.staywins = self.Player.wins
        print("Switch Player Won", self.switchwins, "Games")
        print("Stay Player Won", self.staywins, "Games")
        print("For Every Game The Stay Player Won, The Switch Player Won", self.switchwins/self.staywins, "Games")

        

sim = Simulation()
gameseach = 100000
n = gameseach*2
sim.runSim(n)

