from discord import *
from datetime import *
from .lists import *
from os import getenv
from random import *
from discord.ext import commands
from dotenv import load_dotenv


def main():
    intents = Intents.all()
    with open("hitlist.txt", "r") as f:
        hitlist = f.read().splitlines()

    bot = commands.Bot(command_prefix='.', intents=intents)

    load_dotenv("token.env")
    TOKEN = getenv('TOKEN')
    pt = ["squirtle", "ivysaur", "charizard"]
    shorthands = {"ganon": "ganondorf", "brawler": "mii_brawler", "krool": "kingkrool", "dk": "donkey_kong", "donkey kong": "donkey_kong"}
    miis = ["mii_brawler", "mii_gunner", "mii_swordfighter"]

    @bot.tree.command(name='ufd', description="Quickly see a move's stats and hitbox")
    async def ufd(interaction, character: str, move: str):
        if character.lower() in pt:
            await interaction.response.send_message(
                f"https://ultimateframedata.com/hitboxes/pt_{character.title()}/{character.title()}{move.title()}.gif \n")
        else:

            await interaction.response.send_message(
                f"https://ultimateframedata.com/hitboxes/{character.title()}/{character.title()}{move.title()}.gif \n")

    @bot.tree.command(name='hitlist', description='Add them to the hitlist')
    async def hitlist_config(interaction, member: str):
        channel = interaction.channel
        if member not in hitlist:
            hitlist.append(str(member))
            await interaction.response.send_message(f"{member} added to the HITLIST...", ephemeral=True, delete_after=3)
            await channel.send(f"Target added to the HITLIST...")
            with open("hitlist.txt", "w") as f:
                for i in hitlist:
                    f.write(f"{i}\n")
        elif member in hitlist:
            hitlist.remove(member)
            await interaction.response.send_message(f"Target removed from the HITLIST")
            with open("hitlist.txt", "w") as f:
                for i in hitlist:
                    f.write(f"{i}\n")

    @bot.tree.command(name='vengeance', description='MY REVENGGGGEEEE')
    async def vengeance(ctx):
        channel = ctx.channel
        print(channel)
        for i in range(0, randint(5, 7)):
            await channel.send("<@1095350739301310674>", delete_after=randint(0, 5))

   # @bot.tree.command(name='update_h2h', description='Create or update a head to head')
   # async def create_h2h(interaction, user1, user2):
   #     pass

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
            elif str(message.author) == 'randomness8736' and str(message.author) in hitlist:
                await message.channel.send("I didn't ask", delete_after=5)
                await timeout_user(message.author)
            elif 'aegis' in message.content.lower() and message.author in hitlist:
                await message.delete()

                #@586987213024133162
                await message.channel.send(f"<@{message.author.id}> Did you mean Eajis?", delete_after=5)

    # async def reset_username(member: Member):
    #    if str(member) == '1mpy':
    #        chosen_username = str(illu_names[randint(0, (len(illu_names)) - 1)])
    #        print(chosen_username)
    #        await member.edit(nick=chosen_username)
    #

    @bot.event
    async def on_member_update(before, after):
        channel = bot.get_channel(956606255974199327)
        print(channel)
        if str(after) == '':
            pass

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

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')
        await bot.tree.sync()

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
