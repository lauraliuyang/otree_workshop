import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'public_good_game'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 3
    #ENDOWMENT = cu(100)
    #ENDOWMENT = 100
    MULTIPLIER = 1.8


class Subsession(BaseSubsession):
    random_payoff_round = models.IntegerField()


class Group(BaseGroup):
    #total_contribution = models.CurrencyField()
    #individual_share = models.CurrencyField()
    total_contribution = models.FloatField()
    individual_share = models.FloatField()



class Player(BasePlayer):
    contribution = models.IntegerField()
    #you can define the max and min for the contribution, also add labels to the contribution.
    # min = 0, max = C.ENDOWMENT, label = "How much will you contribute"
    earnings = models.FloatField()
    endowment = models.IntegerField()

# Define function
def set_payoffs(group: Group):
    players = group.get_players()
    contribution = [p.contribution for p in players]
    group.total_contribution = sum(contribution)
    group.individual_share = round(
            group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP, 2
    )
    for p in players:
        # p.payoff = round(p.endowment - p.contribution + group.individual_share, 2)
        p.earnings = round(p.endowment - p.contribution + group.individual_share, 2)

#Subsessions have a method group_randomly() that shuffles players
# randomly, so they can end up in any group, and any position within the group.
# creating_session is a function that oTree can identify, it will run at the begining of each round
# if the grouping is depends on say, ;last round performance, you will need to define other functions for group
def creating_session(subsession: Subsession):
    subsession.group_randomly()
    subsession.random_payoff_round = random.randint(1, C.NUM_ROUNDS)

# PAGES
class RoundIntro(Page):
    def before_next_page(player: Player, timeout_happened):
        player.endowment = player.participant.number_of_correct_answers*10

class Contribution(Page):
    form_model = "player"
    form_fields = ["contribution"]



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass

class FinalResults(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        earning_list =[]
        random_round_earnings = 0
        # [(0, p_in_1), (1, p_in_2)]
       # for temp_player in all_players:
        #    earning_list.append(temp_player.earnings)
        for round_number, temp_player in enumerate(all_players):
            earning_list.append((round_number + 1, temp_player.earnings))
            random_round_earnings = temp_player.in_round(temp_player.subsession.random_payoff_round).earnings
        #earning_list = [(round_number + 1, temp_player.earnings) for round_number, temp_player in enumerate(all_players)]
        return {
            'earning_list': earning_list,
            'random_round_earnings': random_round_earnings
        }

page_sequence = [RoundIntro, Contribution, ResultsWaitPage, Results,FinalResults]
