from fuzzywuzzy import process
from botconstants import RIGHTS, BOT_DESCRIPTION

        
Queries = [
    (
        ["lawyer"],
        "Better Call Saul!"
    ),
    (
        ["oh Jimmy"],
        "Don't you fucking Oh, Jimmy me!"
    ),
    (
        ["how?"],
        "First thing's first, you're gonna put a dollar in my pocket. Both of you."
    ),
    (
        ["skylar"],
        "Skyler! It's a beautiful name! Reminds me of a... big beautiful sky!"
    ),
    (
        ["good to meet you","nice to meet you","hello"],
        "Don't drink and drive, but if you do, call me!"
    ),
    (
        ["Who can I sue"],
        "Who can you sue? Try police departments, libraries, construction companies, school officials, cleaning services, financial institutions (local and international), your neighbors, your family members, your church, synagogue or other religious institution, your employers, your employers' customers, suppliers, companies in other countries; companies that made the drugs that were turned into the drugs that you took. The possibilities are limitless!"
    ),
    (
        ["rights"],
       RIGHTS
    ),
    (
        ["paul badman"],
       BOT_DESCRIPTION
    )
]


TRIGGERS = []
RESPONSES = {}

for query in Queries:
    response = query[1]
    for trigger in query[0]:
        TRIGGERS.append(trigger)
        RESPONSES[trigger] = response


del Queries


def check_for_triggers(str):
    """
        Returns message if triggerd,
            or else returns none

    """
    result = process.extractOne(str, TRIGGERS, score_cutoff = 80)
    
    if result:
        return RESPONSES[result[0]]
    
    return None