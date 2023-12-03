import asyncio
import discord
import src.Util as util
from src.Models import *

# Your Discord API Token!
TOKEN = ''


# Channel_ID (TEXT CHANNEL)
# Replace this with your Channel ID 
CHANNEL_ID = 0

# Guild_ID (Server Channel)
# Katzenlo  723575347672514611
# PNPRPG    697210498071920720

GUILD_ID = 723575347672514611
client = discord.Client()


channel = client.get_channel(CHANNEL_ID)

# external (my) logic
file_path_spell_book = "src\\spells.json"
file_path_casters = "src\\players.json"
file_path_creatures = "src\\creatures.json"
logic = DonnyDiceEngine(client, file_path_spell_book, file_path_casters, file_path_creatures)

# don: global async access to certain text channel see channel-id.
ch_allgemein: discord.TextChannel

list_admin_user = []

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    author_full_name = str(message.author)
    author_name = str(message.author.name)
    author_id = message.author.id
    m = str(message.content)
    m_split = m.split(" ")
    m_split_len = len(m_split)
    m_0 = m_split[0]
    ret = ""
    print(f"{author_full_name}_{author_id}: {m}")    # debug.

    # only admin is allowed following
    if author_full_name in list_admin_user:
        # only allowed user message are processed else ignored.
        if message.content.startswith("admin") or message.content.startswith("cmd"):
            if m_split_len >= 2:
                m_1 = m_split[1]
                if m_1 in ["restart", "neustart"]:
                    pass
                    # funktioniert nichts
                    # await client.close()
                    # await client.run(TOKEN)
                    ret = "nice try :)"
                    await ch_allgemein.send(ret)

            if m_split_len >= 3:
                m_1 = m_split[1]
                name = ""
                for i in range(2, m_split_len):
                    name += str(m_split[i]) + " "
                if m_1 in ["change_name", "change-name"]:
                    print(f"new name is {name}")
                    try :
                        await change_bot_name(name)
                    except discord.HTTPException:
                        ret = "Discord: You are changing your username or Discord Tag too fast. Try again later."
                        await ch_allgemein.send(ret)
                    return

    # else every chat entry is checked

    ret = logic.input_validation_service(m, author_id)
    if len(ret) > 0:
        await ch_allgemein.send(ret)
        return
    return
    if len(ret) > 0:
        await ch_allgemein.send(ret)


@client.event
async def change_bot_name(new_name: str):
    await client.user.edit(username=new_name)

@client.event
async def on_ready():
    global ch_allgemein
    ch_allgemein = client.get_channel(CHANNEL_ID)
    admin = client.get_guild(GUILD_ID).owner
    list_admin_user.append(admin.name + "#" + admin.discriminator)
    list_admin_user.append("Alraunenschrei#4855")
    print(f"@ channel {ch_allgemein} of {client.get_guild(GUILD_ID)}")
    print(f'The BOT {client.user.name}, id= {client.user.id} is now online')
    print(f'Allowed users are {list_admin_user}')

client.run(TOKEN)







