from os import environ


SESSION_CONFIGS = [
    dict(
        name='all_parts',
        display_name="Full experiment",
        app_sequence=['real_effort', 'public_good_game'],
        num_demo_participants=3,
    ),
    # dict(
    #     name='public_good_game',
    #     display_name="Public good game 1 round",
    #     app_sequence=['public_good_game'],
    #     num_demo_participants=3,
    # ),
    # dict(
    #     name='real_effort',
    #     display_name="real effort",
    #     app_sequence=['real_effort'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['number_of_correct_answers']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '2341505234943'

INSTALLED_APPS = ['otree']