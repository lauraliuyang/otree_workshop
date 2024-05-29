import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'real_effort'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    PRICE_PER_CORRECT_ANSWER = cu(2)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_entered = models.IntegerField()
    sum_of_numbers = models.IntegerField()
    random_number_1 = models.IntegerField()
    random_number_2 = models.IntegerField()
    number_of_correct_answers = models.IntegerField(initial = 0)


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.random_number_1 = random.randint(1, 100)
        p.random_number_2 = random.randint(1, 100)


# This method is automatically called once when the session is created. It is typically used to
# perform setup tasks such as initializing data, setting up randomizations,
# and configuring participants' initial states.

# PAGES
class AddNumbers(Page):
    form_model = 'player'
    form_fields = ['number_entered']

    @staticmethod
    def vars_for_template(player: Player):
        player.sum_of_numbers = player.random_number_1 + player.random_number_2
        return {
            'random_number_1': player.random_number_1,
            'random_number_2': player.random_number_2,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.number_entered == player.sum_of_numbers:
            player.payoff = C.PRICE_PER_CORRECT_ANSWER
            player.number_of_correct_answers = 1

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass



class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        total_payoff = 0
        number_of_correct_answers = 0
        for temp_player in all_players:
            total_payoff = total_payoff + temp_player.payoff
            number_of_correct_answers = number_of_correct_answers + temp_player.number_of_correct_answers
        if player.round_number == C.NUM_ROUNDS:
            player.participant.number_of_correct_answers = number_of_correct_answers
        return {
            'total_payoff': total_payoff,
            'number_of_correct_answers': number_of_correct_answers,
        }

page_sequence = [AddNumbers, ResultsWaitPage, Results, FinalResults]
