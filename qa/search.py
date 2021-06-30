import re
from django.contrib.postgres.search import (
    SearchQuery, SearchVector, SearchRank)
from django.db.models import Count
from .models import Question


class QuestionSearch():
    def __init__(self, query):
        self.search_class = SearchDispatcher(query).get_search_class()

    def get_result(self):
        return self.search_class.get_result()


class SearchDispatcher():
    '''
    Determine which type of search user wants.
    '''

    def __init__(self, query):
        self.query = query

    def get_search_class(self):
        if re.search(r'^user:\d+', self.query):
            return ByAuthorSearch(self.query)
        elif re.search(r'^answers:\d+', self.query):
            return ByNumberOfAnswersSearch(self.query)
        elif re.search(r'^isaccepted:(yes|no)', self.query):
            return ByAcceptance(self.query)
        elif re.search(r'^score:\d+', self.query):
            return ByScore(self.query)
        return PlainSearch(self.query)


class BaseSearch():
    def __init__(self, query):
        self.query = query
        self.search_vector = SearchVector('title', 'body_html')

    def set_search_query(self, q):
        res = re.search(r'"(.*)"', q)
        if res:
            self.search_query = SearchQuery(res.group(1), search_type='phrase')
        else:
            self.search_query = SearchQuery(q)

    def get_result(self):
        self.set_search_query(self.query)
        result = Question.objects.annotate(
            search=self.search_vector,
            search_rank=SearchRank(self.search_vector, self.search_query)
        ).filter(search=self.search_query).order_by('-search_rank')
        return result


class PlainSearch(BaseSearch):
    def __init__(self, query):
        super().__init__(query)


class ByAuthorSearch(BaseSearch):
    def __init__(self, query):
        super().__init__(query)
        self.pattern = r'^user:(?P<user_id>\d+) (?P<q>.*)'
        match = re.search(self.pattern, query)
        self.user_id = int(match.group('user_id'))
        self.query = match.group('q')

    def get_result(self):
        result = super().get_result()
        return result.filter(user__id=self.user_id)


class ByNumberOfAnswersSearch(BaseSearch):
    def __init__(self, query):
        super().__init__(query)
        self.pattern = r'^answers:(?P<num_ans>\d+) (?P<q>.*)'
        match = re.search(self.pattern, query)
        self.query = match.group('q')
        self.number_of_answers = int(match.group('num_ans'))

    def get_result(self):
        result = super().get_result()
        # return result.filter(answer_set__count=self.number_of_answers)
        return result.annotate(answer_count=Count('answer')) \
            .filter(answer_count=self.number_of_answers)


class ByScore(BaseSearch):
    def __init__(self, query):
        super().__init__(query)
        self.pattern = r'^score:(?P<score>\d+) (?P<q>.*)'
        match = re.search(self.pattern, query)
        self.query = match.group('q')
        self.score = int(match.group('score'))

    def get_result(self):
        result = super().get_result()
        return result.filter(vote__gte=self.score)


class ByAcceptance(BaseSearch):
    def __init__(self, query):
        super().__init__(query)
        self.pattern = r'^isaccepted:(?P<accepted>yes|no) (?P<q>.*)'
        match = re.search(self.pattern, query)
        if match:
            self.query = match.group('q')
            if match.group('accepted') == 'yes':
                self.is_accepted = True
            else:
                self.is_accepted = False

    def get_result(self):
        result = super().get_result()
        return result.filter(answer__accepted=self.is_accepted)
