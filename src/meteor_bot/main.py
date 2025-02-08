from datetime import *
from os import getenv
from random import *
from unicodedata import *
from tinydb import *
from discord import *
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv("token.env")
DEV_ENV = (getenv('DEV_ENV'))
if DEV_ENV == 'True':
    from lists import *
    from aioconsole import *
else:
    from .lists import *


def main():
    intents = Intents.all()

    def get_hitlist():
        try:
            f = open("hitlist.txt", "x")
            hitlist = f.read().splitlines()
            f.close()
            return hitlist
        except:
            with open("hitlist.txt", "r") as f:
                hitlist = f.read().splitlines()
            return hitlist

    def db():
        db = TinyDB('db.json')
        return db

    bot = commands.Bot(command_prefix='.', intents=intents)

    TOKEN = getenv('TOKEN')

    pt = ["squirtle", "ivysaur", "charizard"]
    shorthands = {"ganon": "ganondorf", "brawler": "mii_brawler", "krool": "kingkrool", "dk": "donkey_kong",
                  "donkey kong": "donkey_kong"}
    miis = ["mii_brawler", "mii_gunner", "mii_swordfighter"]

    @tasks.loop(seconds=3)
    async def send_messagee():
        if DEV_ENV == 'True':

            try:
                channel = bot.get_channel(956606255974199327)
                msg = await ainput("Input your message: ")
                await channel.send(f"{msg}")
            except Exception:
                pass

    @bot.tree.command(name='ufd', description="Quickly see a move's stats and hitbox")
    async def ufd(interaction, character: str, move: str):
        if character.lower() in pt:
            await interaction.response.send_message(
                f"https://ultimateframedata.com/hitboxes/pt_{character.title()}/{character.title()}{move.title()}.gif \n")
        else:
            #
            await interaction.response.send_message(
                f"https://ultimateframedata.com/hitboxes/{character.title()}/{character.title()}{move.title()}.gif \n")

    #
    @bot.tree.command(name='hitlist', description='Add them to the hitlist')
    async def hitlist_config(interaction, member: str):
        try:
            #
            channel = interaction.channel
            if member not in get_hitlist():
                hitlist = get_hitlist()
                hitlist.append(str(member))
                temp_hitlist = hitlist
                await interaction.response.send_message(f"{member} added to the HITLIST...", ephemeral=True,
                                                        delete_after=3)
                await channel.send(f"Target added to the HITLIST...")
                with open("hitlist.txt", "w") as f:
                    for i in temp_hitlist:
                        f.write(f"{i}\n")
            elif member in get_hitlist():
                get_hitlist().remove(member)
                await interaction.response.send_message(f"Target removed from the HITLIST")
                with open("hitlist.txt", "w") as f:
                    for i in get_hitlist():
                        f.write(f"{i}\n")
            elif member == 'view':
                await interaction.response.send_message(f"{get_hitlist()}", ephemeral=True, delete_after=3)
        except Exception as e:
            await interaction.response.send_message(f"{e}")

    @bot.tree.command(name='vengeance', description='MY REVENGGGGEEEE')
    async def vengeance(interaction, channel: TextChannel, member: Member):
        print(channel)
        await interaction.response.send_message(f"We do a little trolling", ephemeral=True,
                                                delete_after=3)
        for i in range(0, randint(5, 7)):
            await channel.send(f"<@{member.id}>", delete_after=randint(0, 3))

    #
    # @bot.tree.command(name='update_h2h', description='Create or update a head to head')
    # async def create_h2h(interaction, user1, user2):
    #    pass
    #
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
            if e >= i:
                print(member.name)
                new_joins.append(f"{member.name}")
        await interaction.response.send_message(f"Getting list of new users after {elim_date}! Check Python Terminal")
        complete_message = '\n'.join(new_joins)
        await channel.send(f"```{complete_message}```")

    @bot.tree.command(name='viewprofile', description='View profiles of server members')
    async def smasher_profile_view(interaction, member: Member):
        Profile = Query()
        profile_data = db().search(Profile.id == member.id)
        user_avatar = member.avatar.url
        embed = Embed(colour=0x00b0f4)
        main = profile_data[0]['main']
        alt = profile_data[0]['alt']
        embed.add_field(name=f"{member}",
                        value="eee",
                        inline=False)
        embed.add_field(name="Main", value=f"{main}", inline=False)
        main = char_code_names[main.lower()]
        embed.set_image(
            url=f"https://raw.githubusercontent.com/joaorb64/StreamHelperAssets/refs/heads/main/games/ssbu/mural_art/{main.lower()}_0{alt}.png")
        embed.set_thumbnail(url=user_avatar)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='updateprofile', description='Update profile')
    @app_commands.choices(alt=[
        app_commands.Choice(name="1", value=0),
        app_commands.Choice(name="2", value=1),
        app_commands.Choice(name="3", value=2),
        app_commands.Choice(name="4", value=3),
        app_commands.Choice(name="5", value=4),
        app_commands.Choice(name="6", value=5),
        app_commands.Choice(name="7", value=6),
        app_commands.Choice(name="8", value=7)])
    async def smasher_profile_view(interaction, main: str, alt: app_commands.Choice[int]):
        Profile = Query()
        member = str(interaction.user)

        main = main.title()
        alt = int(alt.value)
        passed = True
        try:
            main = char_code_names[main.lower()]

        except:
            await interaction.response.send_message("You didn't enter a valid character!")
            passed = False
        if DEV_ENV == 'True':
            passed = False
        if passed:

            if db().search(Profile.id == interaction.user.id) != []:
                db().update({'member': member, 'alt': alt, 'main': main, 'id': interaction.user.id},
                            Profile.id == interaction.user.id)
            else:
                db().insert({'member': member, 'alt': alt, 'main': main, 'id': interaction.user.id})
            profile_data = db().search(Profile.id == interaction.user.id)
            user_avatar = interaction.user.avatar.url
            embed = Embed(colour=0x00b0f4)
            main = profile_data[0]['main']
            alt = profile_data[0]['alt']
            embed.add_field(name=f"{member}",
                            value="eee",
                            inline=False)
            embed.add_field(name="Main", value=main, inline=False)
            main = char_code_names[main.lower()]
            embed.set_image(
                url=f"https://raw.githubusercontent.com/joaorb64/StreamHelperAssets/refs/heads/main/games/ssbu/mural_art/{main.lower()}_0{alt}.png")
            embed.set_thumbnail(url=user_avatar)
            await interaction.response.send_message("Updated your profile!", embed=embed)

    async def timeout_user(member: Member):
        await member.timeout(timedelta(seconds=7), reason=f"Joe")

    #
    @bot.event
    async def on_message(message):
        quotes = bot.get_channel(931598462879944764)

        print(f"#{message.channel}  {str(message.author)}: {str(message.content)}")
        message.content = normalize("NFKD", message.content)
        if str(message.author) != 'Meteor#1277':
            if message.channel == quotes and message.attachments == []:
                await message.delete()
                await message.channel.send("No talking in this channel please!", delete_after=3)
            if 'meta knight' in message.content.lower() and DEV_ENV != "True":
                await message.channel.send(meta_knight)
            #
            elif any(i in ''.join(str(message.content.lower())) for i in american_words):
                await message.delete()
                await message.channel.send(f"<@{message.author.id}> Outta here with that Amer*can nonsense bruv",
                                           delete_after=2)

                # await timeout_user(message.author)
            elif any(i in ''.join(str(message.content.lower())) for i in banned_words):
                await message.delete()
                pass
            elif 'roy' in message.content.lower():
                if randint(0, 10) == 1:
                    await message.channel.send(roy)
            elif '<@&1328843759764639895>' in message.content:
                await message.channel.send('https://tenor.com/view/cat-but-heres-the-yapping-gif-5342913541658644726')
            elif str(message.author) == 'randomness8736' and str(message.author) in get_hitlist():
                await message.channel.send("I didn't ask", delete_after=5)
                await timeout_user(message.author)
            elif 'aegis' in message.content.lower() and str(message.author) in get_hitlist():
                await message.delete()
                await message.channel.send(f"<@{message.author.id}> Did you mean Pithra?", delete_after=5)

    #
    # async def reset_username(member: Member):
    #   if str(member) == '1mpy':
    #       chosen_username = str(illu_names[randint(0, (len(illu_names)) - 1)])
    #       print(chosen_username)
    #       await member.edit(nick=chosen_username)

    #
    @bot.event
    async def on_member_update(before, after):
        channel = bot.get_channel(956606255974199327)
        # print(channel)
        if str(after) == '':
            pass

    #
    @bot.event
    async def on_message_edit(before, after):
        author = before.author
        channel = before.channel
        if before.content != after.content and randint(0, 15) == 3:
            await channel.send(f"I saw that {author.mention}", delete_after=0.1)

    @bot.event
    async def on_reaction_add(reaction, user):
        print(f"{user} just reacted with {reaction} to message : {reaction.message.content}")

    @bot.event
    async def on_member_remove(member):
        channel = bot.get_channel(956606255974199327)
        await channel.send(f"{member} finally buggered off")

    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f'We have logged in as {bot.user}')

        if DEV_ENV == 'True':
            for i in bot.get_all_members():
                print(f"{str(i.name)} ({i.status}) id is {i.id}")
            print("Done!")
        send_messagee.start()



    # async
    get_hitlist()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
