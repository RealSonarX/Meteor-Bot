from discord import *
from datetime import *
from .lists import *
from os import getenv
from random import *
from discord.ext import commands
from dotenv import load_dotenv
#test
def main():

    intents = Intents.all()

    bot = commands.Bot(command_prefix='.', intents=intents)

    load_dotenv("token.env")
    TOKEN = getenv('TOKEN')


    # tree = app_commands.CommandTree(bot)

    @bot.tree.command(name='vengeance', description='MY REVENGGGGEEEE')
    async def vengeance(ctx):
        channel = ctx.channel
        print(channel)
        for i in range(0, randint(5, 7)):
            await channel.send("<@1095350739301310674>", delete_after=randint(0, 5))


    @bot.tree.command(name='newjoins', description='Find new joins')
    async def newjoins(interaction, elim_date: str):
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
            # print(e)
            if e >= i:
                print(member.name)
                new_joins.append(f"{member.name}")
        await interaction.response.send_message(f"Getting list of new users after {elim_date}! Check Python Terminal")
        complete_message = '\n'.join(new_joins)
        await channel.send(f"```{complete_message}```")


    async def timeout_user(member: Member):
        await member.timeout(timedelta(seconds=5), reason=f"Joe")


    @bot.event
    async def on_message(message):
        # print(message.author)
        print(f"New Message : {message.content}")
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
            elif '<@&1328843759764639895>' in message.content:
                await message.channel.send('https://tenor.com/view/cat-but-heres-the-yapping-gif-5342913541658644726')
            elif 'aegis' in message.content.lower():
                await message.channel.send("")
            # elif str(message.author) == 'randomness8736':
            #    await message.channel.send("I didn't ask", delete_after=5)
            #    await timeout_user(message.author)


    async def reset_username(member: Member):
        if str(member) == '1mpy':
            chosen_username = str(illu_names[randint(0, (len(illu_names)) - 1)])
            print(chosen_username)
            await member.edit(nick=chosen_username)


    @bot.event
    async def on_member_update(before, after):
        channel = bot.get_channel(956606255974199327)
        print(channel)
        if str(after) == '':
            pass
            # if str(after.nick) not in :
            #    await channel.send(f'Nice try {after.mention}', delete_after=1)
            #    await reset_username(after)


    #    if str(after) == '_the_aegis_':
    #        if str(after.nick) not in illu_names and before.nick != after.nick:
    #            await channel.send(f'Nice try {after.mention}', delete_after=1)
    #            await reset_username(after)


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


    bot.run(TOKEN)


if __name__ == "__main__":
    main()
