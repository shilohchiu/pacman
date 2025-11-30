"""
Score contains class definitions for score 
and helper methods for querying firestore

score is imported by query_fs and classes
"""
class Score:
    #constructor
    def __init__(self, initial = "adm", high_score = 0, scores = None, curr_score = 0):
        if scores is None:
            scores = []
        self.initial = initial
        self.high_score = high_score
        self.scores = scores
        self.curr_score = curr_score

    @staticmethod
    def from_dict(source):
        return Score(
            initial=source.get("initial"),
            high_score=source.get("high_score"),
            scores=source.get("scores"),
            curr_score=source.get("curr_score"),
        )

    def to_dict(self):
        return {
            #"initial" : self.initial,
            "high_score": self.high_score,
            "scores": self.scores,
            "curr_score":self.curr_score
        }

    def get_high_score(self):
        return self.high_score

    def get_initial(self):
        return self.initial

    def get_curr_score(self):
        return self.curr_score

    def adj_curr_score(self, point):
        self.curr_score += point

    def reset_curr_score(self):
        self.curr_score = 0
