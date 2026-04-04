from django.http import HttpResponse
import random

def quote(request):
    quotes = [
   "The realization that life is absurd cannot be an end, but only a beginning.",
   "We have art in order not to die of life.",
   "The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.",

    ]

    return HttpResponse(random.choice(quotes))
