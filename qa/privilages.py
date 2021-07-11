class Privilages:
    """
    Privilages control what user can do in system.
    """

    _privilages = {
        "create_post": 1,
        "vote_up": 15,
        "flag_posts": 15,
        "comment_everywhere": 50,
        "vote_down": 150,
        "create_tags": 1500,
        "edit_question_and_answer": 2000,
        "protect_questions": 15000,
        "trusted_user": 20000,
    }

    def __init__(self, user):
        self.reputation = user.profile.reputation

    def get_user_privilages(self):
        user_privilages = []
        for k, v in self._privilages.items():
            if self.reputation >= v:
                user_privilages.append(k)
        return user_privilages

    def check_privilage(self, privilage):
        if privilage in self._privilages:
            return self.reputation >= self._privilages[privilage]
