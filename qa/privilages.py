class Privilages():
    """
    Privilages control what user can do in system.
    """
    _create_post = 1
    _vote_up = 15
    _flag_posts = 15
    _comment_everywhere = 50
    _vote_down = 150
    _create_tags = 1500
    _edit_question_and_answer = 2000
    _protect_questions = 15000
    _trusted_user = 20000

    _privilages = {
        0: ['create_post'],
        15: ['vote_up', 'flag_posts'],
        50: ['comment_everywhere'],
        150: ['vote_down'],
        1500: ['create_tags'],
        2000: ['edit_question_and_answer'],
        15000: ['protect_questions'],
        20000: ['trusted_user']
    }

    def __init__(self, user):
        self.reputation = user.profile.reputation

    def get_user_privilages(self):
        user_privilages = []
        for i in self._privilages.keys():
            if self.reputation >= i:
                user_privilages += self._privilages[i]
        return user_privilages

    def check_privilage(self, privilage):
        if privilage == 'create_post':
            return self.reputation >= self._create_post
        elif privilage == 'vote_up':
            return self.reputation >= self._vote_up
        elif privilage == 'flag_posts':
            return self.reputation >= self._flag_posts
        elif privilage == 'comment_everywhere':
            return self.reputation >= self._comment_everywhere
        elif privilage == 'vote_down':
            return self.reputation >= self._vote_down
        elif privilage == 'create_tags':
            return self.reputation >= self._create_tags
        elif privilage == 'edit_question_and_answer':
            return self.reputation >= self._edit_question_and_answer
        elif privilage == 'protect_questions':
            return self.reputation >= self._protect_questions
        elif privilage == 'trusted_user':
            return self.reputation >= self._trusted_user
        else:
            return False
