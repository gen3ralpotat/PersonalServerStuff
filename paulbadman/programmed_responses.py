from fuzzywuzzy import process
import os
import toml
import random

KEEP_YOUR_VOICE_LOW_DIALOGUES = [
    "Hey, amigo, slow your roll and smell the legal roses. Take a breather, count to ten, and let's tackle this storm one step at a time.",
    "Chillax, my friend! Take a beat, sip some metaphorical chamomile tea, and let's dial it down a notch. We've got this in the bag.",
    "Easy there, tiger! Take a chill pill, loosen that tie, and let's approach this like a Sunday drive. We'll smooth out the bumps, no sweat.",
    "Whoa, pump the brakes! Take a cosmic timeout, breathe in, breathe out. We're not defusing a bomb here, just navigating life's rollercoaster.",
    "Hold the phone, partner! Let's dial back the stress-o-meter, find our zen place. This ain't a sprint; it's a strategic marathon.",
    "Slow your roll, my friend! Picture yourself on a hammock by the legal beach. Take a sip of serenity and let's approach this like a symphony, one calming note at a time.",
    "Hey, simmer down! Imagine you're floating down a river of tranquility. Take a mental float and let's troubleshoot this with a cool head.",
    "Easy, tiger! Picture yourself on a cloud of peace, counting the legal sheep. Let's put a pin in the panic and tackle this puzzle with a clear mind."
]

TRIGGERS = []
RESPONSES = {}

Queries = toml.load(os.path.dirname(
    os.path.realpath(__file__)) + os.path.sep + "Queries.toml")
for query in Queries:
    for trigger in Queries.get(query).get("triggers"):
        TRIGGERS.append(trigger)
        RESPONSES[trigger] = query
del Queries


def check_for_triggers(string: str):
    """
        Returns message if triggerd,
            or else returns none

    """
    if string.isupper() and len(string) >= 50:
        return random.choice(KEEP_YOUR_VOICE_LOW_DIALOGUES)

    result = process.extractOne(string, TRIGGERS, score_cutoff=95)

    if result:
        return RESPONSES[result[0]]

    return None
