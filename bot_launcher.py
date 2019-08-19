import discord
from discord.ext import commands, tasks
import time
import asyncio

messages = joined = 0


async def atualizar_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Hora: {int(time.time())}, Mensagens: {messages}, Membros que se juntaram: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)

Client = discord.Client()
client = commands.Bot(command_prefix = '!')


# Sends a ready message on_ready() to the console
@client.event
async def on_ready():
    print('Bot ready.')


@client.event
async def on_message(message):
    global messages
    messages += 1

    id = client.get_guild(611817575600488449)
    valid_users = ["ferreirA#1058"]

    if str(message.channel) == "poste-seu-rsn-aqui":
        if message.content.find("!hello") != -1:
            await message.channel.send("Hi")
        elif message.content == "!usuarios":
            await message.channel.send(f"""Quantidade de Membros {id.member_count}""")

    if str(message.channel) == "poste-seu-rsn-aqui":
        if message.content == "!help":
            embed = discord.Embed(title="Help on BOT", description="Some useful commands")
            embed.add_field(name="!hello", value="Greets the user")
            embed.add_field(name="!users", value="Prints number of users")
            await message.channel.send(content=None, embed=embed)

# Prints when a member joins a server which has this bot running
@client.event
async def on_member_join(member):
    global joined
    joined += 1

    for channel in member.guild.channels:
        if str(channel) == "novos-membros":  # We check to make sure we are sending the message in the general channel
            await channel.send(f'{member.mention}, acabou de entrar no servidor, seja bem vindo!')

# Prints when a member lefts a server which has this bot running
@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == "despedidas":  # We check to make sure we are sending the message in the general channel
            await channel.send(f'{member.mention}, acabou de sair do servidor, hasta la vista!')


@client.event # This event runs whenever a user updates: status, game playing, avatar, nickname or role
async def on_member_update(before, after):
    n = after.nick
    if n: # Check if they updated their username
        if n.lower().count("theusin") > 0: # If username contains tim
            last = before.nick
            if last: # If they had a usernae before change it back to that
                await after.edit(nick=last)
            else: # Otherwise set it to "NO STOP THAT"
                await after.edit(nick="Não!")

client.loop.create_task(atualizar_stats())
client.run('NjEyNDMxNzk4OTk1MjU1MzM3.XVnxrA._mDq7Qa0lb5dlhHbyJEMm-iOIUY')
