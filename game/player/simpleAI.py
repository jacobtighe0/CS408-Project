from random import randint
import player.player
import player.simpleAI

class SimpleAI(player.Player):

    def __init__(self, name = "simpleAI", money = 500.0):
        self.name = name
        self.money = money
        self.handValue = 0.0
        self.hand = []
        self.deposit = 0.0
        self.bet = 0.0
        self.game = None # Records current game being played
        self.prevAction = None # Records previous action to prevent infinite loops

    def setGame(self, game):
        self.game = game

    def raising(self, raising = None):
        """
        Function for getting random input
        :returns: TODO

        """
        print(self.money, self.debt)
        #return randint(1, self.money - self.debt) if self.money > self.debt else 0.0 
        return randint(1, 1 + int((self.money - self.debt)/3)) if self.money > self.debt else 0.0 

    def checkBet(self):
        """
        Checks only if difference between deposit and bet is zero
        
        :returns: True/False based on if you can check or not
        """
        if self.debt:
            return False
        else:
            print("{} check".format(self.name))
            return (self.bet,0)
        
    def options(self):
        options = { 0: self.quit,
                    1: self.checkBet ,
                    2: self.callBet , 
                    3: self.raiseBet , 
                    4: self.foldBet , 
                    5: self.allin,
                    }
            
        while True:
            chance = 0 # AI's chance of winning (initially 0)
            if self.game is not None:

                wins = 0 # Increases by 1 if AI wins a simulated game
                loops = 10000 # Number of simulations

                i = 0
                while i<loops:
                    wins += self.simulateGame()
                    i+=1
                chance = (wins/loops)*100 # AI's chance of winning

                print("AI chance of winning:") # --- FOR TESTING ONLY ---
                print(chance)

            if self.bet == -1:
                if chance < 20:
                    action = 4
                else:
                    action = 5
            else:
                if chance < 50:
                    if (self.checkBet() == False):
                        action = 2
                    else:
                        action = 1
                elif chance < 90:
                    if self.prevAction == 3: # Stops AI from raising infinitely
                        if (self.checkBet() == False):
                            action = 2
                        else:
                            action = 1
                    else:
                        action = 3
                else:
                    action = 5
                
            choosed = options[action]()
            self.prevAction = action
            if choosed:
                return choosed
            else:
                continue
    
    def simulateGame(self):
        import copy
        simGame = copy.deepcopy(self.game)

        simGame.dealer.cardControl.shuffle()
        while len(simGame.dealer.cardControl.tableCards) < 5:
            simGame.dealer.cardControl.drawTable()

        #print(simGame.dealer.cardControl.tableCards)

        winners = simGame.dealer.chooseWinner(simGame.players)
        x = [winner.name for winner in winners]
        if x[0] == self.name:
            return 1
        else:
            return 0
    