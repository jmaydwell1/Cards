class Player: # Creates Player and score of that player to compare to other players scores

    def __init__(self,name,score):
        '''
        Name: __init__
        Parameters: self, name, scores
        Return: none
        '''
        self.name = name
        self.score = score
        
    def __lt__(self, other):
        '''
        Name: __lt__
        Parameters: self, other
        Return: self.score < other.score
        '''
        return self.score < other.score
        
    def __eq__(self, other):
        '''
        Name: __eq__
        Parameters: self, other
        Return: self.score == other.score
        '''
        return self.score == other.score
