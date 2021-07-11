from enum import Enum


class Reputation(Enum):
    """
    Reputation list for using privilages
    """

    QUESTION_VOTE_UP = 10
    ANSWER_VOTE_UP = 10
    ANSWER_MARKED_ACCEPTED = 15
    ANSWER_MARKED_ACCEPTED_ACCEPTOR = 2
    QUESTION_VOTE_DOWN = -2
    ANSWER_VOTE_DOWN = -2
    USER_VOTE_DOWN = -1
