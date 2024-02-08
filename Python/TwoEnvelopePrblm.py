import random
import msvcrt
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.returns = []
        self.money = 0
    
    def CollapseReturns(self):
        for val in self.returns:
            if val == 'x':
                self.money += 1
            else:
                self.money += 2
    

class Switcher(Player):
    def __init__(self):
        Player.__init__(self, 'Switcher')

    def ChooseEnvelope(self, envelopes):
        choice = envelopes[1-random.randint(0, 1)]#this emulates randomly choosing an evenlope then switching
        self.returns.append(choice)

class Chooser(Player):
    def __init__(self):
        Player.__init__(self, 'Chooser')

    def ChooseEnvelope(self, envelopes):
        choice = envelopes[random.randint(0, 1)]
        self.returns.append(choice)

class Simulator:
    def __init__(self, numtrials):
        self.numtrials = numtrials
        self.players = [Switcher(), Chooser()]
        self.envelopes = self.RegenerateEnvelopes()
        self.starttime = time.time()
    
    def RegenerateEnvelopes(self):
        values = ['x', '2x']
        randomindex1 = random.randint(0, 1)
        randomindex2 = 1 - randomindex1
        evelope1 = values[randomindex1]
        evelope2 = values[randomindex2]
        return [evelope1, evelope2]

    def RunSimulation(self):
        for player in self.players:
            for i in range(self.numtrials):
                self.envelopes = self.RegenerateEnvelopes()
                player.ChooseEnvelope(self.envelopes)
                # Check for 'p' key press
                if msvcrt.kbhit() and msvcrt.getch() == b'p':
                    print("\n\n\n\n\n")
                    print('CURRENT STATUS:')
                    print('Current Player:', player.name)
                    currtime = time.time()
                    timeelapsed = currtime-self.starttime
                    print('Time Elapsed:', timeelapsed)
                    if player.name == 'Switcher':
                        percentagetrialsdone = i/(2*self.numtrials)
                    else:
                        percentagetrialsdone = i/(self.numtrials)
                    estimatedtimeremaining = timeelapsed/percentagetrialsdone-timeelapsed
                    print('Estimated Time Remaining:', estimatedtimeremaining//1, 'seconds')
                    print('\n\n')
                
            player.CollapseReturns()
            print(player.name, player.money)
        
        if self.players[0].money > self.players[1].money:
            print('Switcher did:', self.players[0].money/self.players[1].money*100-100, '% better')
        else:
            print('Chooser did:', self.players[1].money/self.players[0].money*100-100, '% better')
        print("Total time elapsed:", time.time()-self.starttime, "seconds")


n=1250000
simulation = Simulator(n)
simulation.RunSimulation()