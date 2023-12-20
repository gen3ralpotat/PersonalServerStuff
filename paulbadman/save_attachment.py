import botconstants as constants
import database

"""

    Adds and stores stickers

"""

__ATTACHMENTS = database.ATTACHMENT_TABLE

def add_attachment(ctx : constants.DISCORD_PY_CONTEXT,name : str):

    # existence check
    result = __ATTACHMENTS.find_one(name=name)

    if result:
        return f"{name} is already saved"


    # missing image check
    attachments = ctx.message.attachments

    if len(attachments) < 1:
        print('You forgot to attach an attachment..... Sticker not added')

    __ATTACHMENTS.insert(dict(name=name,url=attachments[0].url))

    return f"this sticker can be used by typing `{constants.COMMAND_PREFIX}get {name}`"


async def get_attachment(ctx : constants.DISCORD_PY_CONTEXT,name: str)-> str | None:
    
    result = __ATTACHMENTS.find_one(name=name)

    if not result:
        return f"{name} does not exist"
    
    await ctx.message.delete()

    return f"{result['url']} AKA `{name}` from {ctx.author.mention}"

def list_saved(ctx : constants.DISCORD_PY_CONTEXT)->str:

    results = __ATTACHMENTS.all()

    names = []

    for row in results:
        names.append(row['name'])

    return f'List of all saved attachments:{'\n- '}{('\n- '.join(names))}'

