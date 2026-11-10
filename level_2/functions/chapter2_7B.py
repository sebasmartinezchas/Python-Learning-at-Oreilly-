# Exercise
class VotingPoll:
    def __init__(self) -> None:
        self.candidate_A=0
        self.candidate_B=0
        self.candidate_C=0

    def vote_A(self):
        self.candidate_A+=1

    def vote_B(self):
        self.candidate_B += 1

    def vote_C(self):
            self.candidate_C += 1

voting_poll = VotingPoll()
# Give 3 votes to candidate A
voting_poll.vote_A()
voting_poll.vote_A()
voting_poll.vote_A()

# Give 2 votes to candidate B
voting_poll.vote_B()
voting_poll.vote_B()

# Give 1 vote to candidate C
voting_poll.vote_C()


print(
    f"A: {voting_poll.candidate_A} B: {voting_poll.candidate_B}  C: {voting_poll.candidate_C}  "
)
