class Scores:
    Count = 1

    def __init__(self, attackerpoints, defenderpoints):
        self.attackerpoints = attackerpoints
        self.defenderpoints = defenderpoints

    def addPointsForAttacker(self):
        self.attackerpoints += 10
        self.defenderpoints -= 10

    def addPointsForDefender(self):
        self.defenderpoints += 10
        self.attackerpoints -= 10

    def addPointsForDefender_RTT(self):
        self.defenderpoints += 20
        self.attackerpoints -= 20

    def getPointsForAttacker(self):
        return self.attackerpoints

    def getPointsForDefender(self):
        return self.defenderpoints

    def checkScores(self):
        print('attacker score is : ', self.attackerpoints)
        print('defender score is : ', self.defenderpoints)
