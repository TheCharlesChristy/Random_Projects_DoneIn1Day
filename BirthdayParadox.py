import random
import msvcrt
import time
class Person:
    def __init__(self):
        self.birthday = random.randint(0,365)

class Room:
    def __init__(self, numofpeople):
        self.numofpeople = numofpeople
        self.people = []
        for i in range(numofpeople):
            self.people.append(Person())
        
    def CheckForSameBirthdays(self):
        birthdays = []
        for person in self.people:
            birthdays.append(person.birthday)
        for p1 in range(len(birthdays)):
            b1 = birthdays[p1]
            comparisons = birthdays[p1+1:]
            for day in comparisons:
                if b1==day:
                    return True
        return False
        
class Simulation:
    def __init__(self, maxnumofpeople, trialspersim):
        self.trialspersim = trialspersim
        self.maxnumofpeople = maxnumofpeople
        self.people_matches = [0]*maxnumofpeople
        self.people_matchpercentage = [0]*maxnumofpeople
        self.currsimstarttime = 0
        self.people_avgtimetocomplete = [0]*maxnumofpeople
    
    def runSim(self):
        self.currsimstarttime = time.time()
        for i in range(1,self.maxnumofpeople+1):
            for x in range(self.trialspersim):
                room = Room(i)
                if room.CheckForSameBirthdays():
                    self.people_matches[i-1] += 1
                    if msvcrt.kbhit():
                        msvcrt.getch()
                        print(f"Current room: {room.numofpeople} people, Trial number: {x+1}")
            self.people_avgtimetocomplete[i-1] = (time.time()-self.currsimstarttime)/self.trialspersim
        for i in range(len(self.people_matches)):
            self.people_matchpercentage[i] = str((self.people_matches[i]/self.trialspersim)*100)+'%'
        


numoftrials = 100
maxnumofpeople = 1000
sim = Simulation(maxnumofpeople, numoftrials)
sim.runSim()

with open('BirthdayParadoxResults.txt', 'w') as f:
    for i in range(len(sim.people_matchpercentage)):
        f.write(str(i+1)+' people: '+sim.people_matchpercentage[i]+'  Avg time to complete a trial: '+str(sim.people_avgtimetocomplete[i])+'\n')