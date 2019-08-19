import os
from discord.ext.commands import Bot
import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
import time
import asyncio
import requests
import asyncio

messages = joined = 0

# Se estou hosteando no meu pc deve estar True
localhost = bool(False)

async def atualizar_stats():
    await bot.wait_until_ready()
    global messages, joined

    while not bot.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Hora: {int(time.time())}, Mensagens: {messages}, Membros que se juntaram: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)

bot = Bot(command_prefix="!")
status = cycle(['💎 Vengeance BR 💎', 'Digite !ajuda para obter minha ajuda!', 'O melhor clã brasileiro!', 'Digite !ajuda para obter minha ajuda','Junte-se a nós', 'Digite !ajuda para obter minha ajuda','Join FC: Vengeance BR', 'Bot programado by Theusin', 'Digite !ajuda para obter minha ajuda'])

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

# Sends a ready message on_ready() to the console
@bot.event
async def on_ready():
    change_status.start()
    print('Bot ready.')

@bot.event
async def on_message(message):
    global messages
    messages += 1

    id = bot.get_guild(611817575600488449)
    valid_users = ["ferreirA#1058", "Wenty#9784"]

    if message.content.find("!clear") != -1:
        if str(message.author) in valid_users:
            await message.channel.send(f'Pronto, eu limpei todas as mensagens!')
            await message.channel.purge()
        else:
            await message.channel.send(f'Você não tem permissão para usar este comando!')
            await message.channel.purge(limit=2)
    # Comando usado para trocar on nickname instantaneo
    if str(message.channel) == "poste-seu-rsn-aqui":
            await message.author.edit(nick=message.content)
            await message.channel.purge(limit=1)

    # Comandos que só irão funcionar no chat-room interagir-com-os-bots
    if str(message.channel) == "interagir-com-os-bots":
        if message.content.find("!ola") != -1:
            await message.channel.send("Oi")
        elif message.content == "!usuarios":
            await message.channel.send(f"""Quantidade de Membros: {id.member_count}""")
        elif message.content == "!ajuda":
            embed = discord.Embed(title="Ajuda com o BOT?", description="Alguns comandos úteis")
            embed.add_field(name="!usuarios", value="Mostra a quantidade de usuários no discord")
            embed.add_field(name="!ola", value="Dê um oi para o bot")
            await message.channel.send(content=None, embed=embed)

# Prints when a member joins a server which has this bot running
@bot.event
async def on_member_join(member):
    global joined
    joined += 1
    responses = ['acabou de mamar piteno', 'está na phome de dinheiro e veio pedir esmola pro clan',
                 'viu a oportunidade de brilhar e entrou', 'está acenando para todos ao entrar no server',
                 'look at this dude, look at the top of his hair']
    for channel in member.guild.channels:
        if str(channel) == "novos-membros":  # We check to make sure we are sending the message in the general channel
            await channel.send(f'{member.mention}, {random.choice(responses)}, seja bem vindo!')

# Prints when a member lefts a server which has this bot running
@bot.event
async def on_member_remove(member):
    global joined
    joined -= 1

    for channel in member.guild.channels:
        if str(channel) == "despedidas":  # We check to make sure we are sending the message in the general channel
            await channel.send(f'{member.mention}, acabou de sair do servidor, hasta la vista!')


# @bot.event # This event runs whenever a user updates: status, game playing, avatar, nickname or role
# async def on_member_update(before, after):
#    n = after.nick
#    if n: # Check if they updated their username
#        if n.lower().count("theusin") or n.lower().count("wenty") > 0: # If username contains tim
#            last = before.nick
#            if last: # If they had a usernae before change it back to that
#                await after.edit(nick=last)
#            else: # Otherwise set it to "NO STOP THAT"
#                await after.edit(nick="Não!")

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.loop.create_task(atualizar_stats())
#try:
if localhost:
    bot.run(token)
else:
    bot.run(str(os.environ.get('BOT_TOKEN')))
#except discord.errors.LoginFailure as e:
    #print("Login unsuccessful.")
