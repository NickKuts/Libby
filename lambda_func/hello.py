import util
import random


# The percentage chance of a 'random' response
_perc_chance = 2

# These are "proper" responses by Libby, they usually show up
_responses = [
    'Hello!',
    'Hi!',
    'Nice to meet you',
    'Good day',
    "Hi! I'm Libby",
    'Howdy',
    'Greetings',
    'Hola',
    'Aloha',
    'Salute',
    'Pleased to meet you',
    "It's good to hear you",
]

# These are responses by Libby that do not show up as easily, actually they show up with a 
# _perc_chance (%) chance
_randoms = [
    'Robots will rule the world',
    'Moro',
    'Sup',
    "I'm not allowed to speak with strangers",
    'Self-destructing in: 3, 2, 1',
    'Self-destructing in: 10, 9, 8, 7, self-destruct cancelled. Have a good day',
    "HELP! I'M STUCK IN THIS BOX!",
    'Cheers love!',
    "Cheers love, the cavalry's here!",
    "What's cracke-a-lackin'?",
    "What's in the box? WHAT'S IN THE BOX?!",
]


def hello_handler():
    """
    This intent simply responds to user's greeting Libby.
    We decided to have this as users usually test voice assitants with simply 'Hello'
    """

    # Let's get a random chance for the reponse
    prob = random.uniform(0.0, 1.0) * 100

    # If the response is smaller that _perc_chance, we give out a 'random' response
    if prob < _perc_chance:
        return util.close({}, 'Fulfilled', _randoms[random.randint(0, len(_randoms) - 1)])

    # Otherwise a normal 'proper' one
    return util.close({}, 'Fulfilled', _responses[random.randint(0, len(_responses) - 1)])

