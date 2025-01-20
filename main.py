from discord import *
from datetime import *
from lists import *
from random import *
from discord.ext import commands


intents = Intents.all()

bot = commands.Bot(command_prefix='.', intents=intents)


# tree = app_commands.CommandTree(bot)

@bot.tree.command(name='vengeance', description='MY REVENGGGGEEEE')
async def vengeance(ctx):
    channel = ctx.channel
    print(channel)
    for i in range(0, randint(5, 7)):
        #sleep(randint(0, 1))
        await channel.send("<@1095350739301310674>", delete_after=randint(0, 5))


@bot.tree.command(name='newjoins', description='Find new joins')
async def newjoins(interaction, elim_date : str):
    guild = bot.get_guild(906804682452779058)
    channel = interaction.channel.name
    for e in guild.channels:
        if str(e.name) == str(channel):
            print("Channel")
            channel = e
    new_joins = []
    i = (datetime.strptime(elim_date, "%d/%m/%Y").date())
    print(i)
    for member in guild.members:
        e = (member.joined_at.date())
        #print(e)
        if e >= i:
            print(member.name)
            new_joins.append(f"{member.name}")
    await interaction.response.send_message(f"Getting list of new users after {elim_date}! Check Python Terminal")
    complete_message = '\n'.join(new_joins)
    await channel.send(f"```{complete_message}```")
    #for i in messages:
    #    message_list.append(i.system_content)
    #print(message_list)

async def timeout_user(member: Member):
    await member.timeout(timedelta(seconds=5), reason=f"Joe")


# async def reset_username(member: Member):
#    if str(member) == '1mpy':
#        await member.edit(nick="Impy")
#    elif str(member) == "_the_aegis_":
#
#        chosen_username = str(illu_names[randint(0, (len(illu_names)) - 1)])
#        print(chosen_username)
#        await member.edit(nick=chosen_username)


@bot.event
async def on_message(message):
    # print(message.author)
    if str(message.author) != 'Meteor#1277':

        if 'meta knight' in message.content.lower():
            await message.channel.send(meta_knight)
        elif 'roy' in message.content.lower():
            if randint(0, 10) == 1:
                await message.channel.send(roy)
        elif ':jojer:' in message.content:
            if randint(0, 5) == 1:
                await message.channel.send(
                    "Whal's literally built like the guy who gets his ass kicked by the mc at the beginning of a "
                    "karate movie")


@bot.event
async def on_member_update(before, after):
    channel = bot.get_channel(956606255974199327)
    # print(channel)

    # if str(after) == '1mpy':
    #    if str(after.nick) != 'Impy':
    #        #await channel.send(f'Nice try {after.mention}', delete_after=1)
    #        await reset_username(after)


#    if str(after) == '_the_aegis_':
#        if str(after.nick) not in illu_names and before.nick != after.nick:
#            await channel.send(f'Nice try {after.mention}', delete_after=1)
#            await reset_username(after)

# await channel.send(before)

@bot.event
async def on_message_edit(before, after):
    author = before.author
    channel = before.channel
    if before.content != after.content and randint(0, 15) == 3:

        await channel.send(f"I saw that {author.mention}", delete_after=0.1)


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(956606255974199327)
    await channel.send(f"{member} finally buggered off")
    # print(channel)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.tree.sync()

    # await tree.sync(guild=(Object(id=906804682452779058)))


# @tree.command(name = "rq", description = "a")
# async def time(interaction):
#    await interaction.response.send_message(f"Test")


# await interaction.response.send_message("command")


token = ''

bot.run(token)
