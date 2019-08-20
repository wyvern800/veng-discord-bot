import os
from discord.ext.commands import Bot, BucketType
import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
import time
import asyncio

# Autor: Matheus Ferreira
# Se estou hosteando no meu pc deve estar True
localhost = bool(True)
# Declarando as variáveis
messages = joined = 0
# Declarando o prefixo utilizado nos comandos
bot = commands.Bot(command_prefix='!')
# Declarando os status do bot
status = cycle(['💎 Vengeance BR 💎', 'Digite !ajuda para obter minha ajuda!', 'O melhor clã brasileiro!',
                'Digite !ajuda para obter minha ajuda', 'Junte-se a nós', 'Digite !ajuda para obter minha ajuda',
                'Join FC: Vengeance BR', 'Bot programado by Theusin', 'Digite !ajuda para obter minha ajuda'])

# Função que irá ler a token
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Chama a função e lê a token que está dentro do arquivo de texto
token = read_token()


# Atualizador de stats do bot
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

# Loop para trocar o status do bot no discord
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

# Envia uma mensagem de pronto quando o bot está on_ready()
@bot.event
async def on_ready():
    change_status.start()
    print('Bot ready.')

# Printa quando um membro se junta ao discord
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


@bot.command(pass_context=True)
@commands.cooldown(1, 5, type=BucketType.user)
async def cox(ctx, quantity: int):
    if 0 <= quantity <= 5:   # Tier 0
        await add_role_based_on_kc(ctx, quantity, 'CoX: Tier 0')
    elif 5 <= quantity <= 24:    # Tier 1
        await add_role_based_on_kc(ctx, quantity, 'CoX: Tier 1')
    elif 25 <= quantity <= 74:    # Tier 2
        await add_role_based_on_kc(ctx, quantity, 'CoX: Tier 2')
    elif 75 <= quantity <= 149:  # Tier 3
        await add_role_based_on_kc(ctx, quantity, 'CoX: Tier 3')
    elif 150 <= quantity <= 499:  # Tier 4
        await add_role_based_on_kc(ctx, quantity, 'CoX: Tier 4')
    elif quantity >= 500:  # Tier 5
        await add_role_based_on_kc(ctx, quantity, 'CoX: Tier 5')
# Errors for cox command
@cox.error
async def cox_error(ctx, error):
    await get_errors(ctx, error)


# Adiciona role ao membro baseado no KC dele
async def add_role_based_on_kc(ctx, quantity, role_name):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(f':dragon_face:  De acordo com o seu KC, que é **{quantity}** completions, seu grupo do CoX foi alterado para **{role_name}**!')
    await ctx.message.author.add_roles(discord.utils.get(ctx.guild.roles, name=role_name))
    await ctx.message.delete()

# Eight ball command
@bot.command(aliases=['8ball'])
@commands.cooldown(1, 5, type=BucketType.user)
async def _8ball(ctx, *, question):
    responses = [
        'É uma certeza',
        'Não tenho certeza',
        'Mais ou menos sim',
        'Definitivamente, sim!',
        'Não',
        'Infelizmente não',
        'Sim',
        'Minha resposta é não',
        'Os deuses de Gielinor dizem que não',
        'Eu duvido',
        'Parece bom!']
    await ctx.send(f'Pergunta: {question}?\nResposta: {random.choice(responses)}')
# Errors for 8ball command
@_8ball.error
async def _8ball_error(ctx, error):
    await get_errors(ctx, error)

# Command to clear messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, amount=5):
    await ctx.send(f'Pronto, eu limpei as {amount} mensagens!')
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=amount)
# Errors for Limpar command
@limpar.error
async def limpar_error(ctx, error):
    await get_errors(ctx, error)


# Command to kick a person
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'O usuário {member.mention} foi kickado!')
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=1)
# Errors for Kick command
@kick.error
async def kick_error(ctx, error):
    await get_errors(ctx, error)


# Command to ban a person
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    await ctx.send(f'O usuário {member.mention} foi banido!')
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=1)
# Errors for BAN command
@ban.error
async def ban_error(ctx, error):
    await get_errors(ctx, error)


@bot.command()
@commands.cooldown(1, 5, type=BucketType.user)
async def ajuda(ctx):
    embed = discord.Embed(title="Vengeance BR Bot", description="Lista de comandos")
    embed.add_field(name="!rsn <nick>", value="Troca seu nick do discord para o nome desejado (deve ser um nick do runescape)")
    embed.add_field(name="!8ball <pergunta>", value="Faça uma pergunta ao bot e tenha uma resposta")
    await ctx.send(content=None, embed=embed)

# Command used to set RuneScape's nickname
@bot.command(pass_context=True)
@commands.cooldown(1, 5, type=BucketType.user)
async def rsn(ctx, *, nick):
    await ctx.channel.purge(limit=1)
    await ctx.author.edit(nick=nick)
    await ctx.send(f':white_check_mark:  Acabei de alterar o RSN do usuário **{ctx.author}** para **{nick}**, obrigado por setar seu Nick do RuneScape :green_heart:!')
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=1)
# Errors for RSN command
@rsn.error
async def rsn_error(ctx, error):
    await get_errors(ctx, error)

# other features
bot.loop.create_task(atualizar_stats())


# Manipulate errors and send message
async def manipulate_error(ctx, error_message: ""):
    await ctx.channel.purge(limit=1)
    await ctx.send(error_message)
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=1)


# Gets the errors
async def get_errors(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await manipulate_error(ctx, "Este comando está em cooldown!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await manipulate_error(ctx, "Você precisa ao menos digitar um nick de RuneScape para que o comando funcione!")
    elif isinstance(error, commands.MissingPermissions):
        await manipulate_error(ctx, "Você não tem permissões para usar este comando!")
    elif isinstance(error, commands.BotMissingPermissions):
        await manipulate_error(ctx, "Oh não, o BOT está sem permissões, printe isso e mande ao Theusin!")

#try:
if localhost:
    bot.run(token)
else:
    bot.run(str(os.environ.get('BOT_TOKEN')))
#except discord.errors.LoginFailure as e:
    #print("Login unsuccessful.")
