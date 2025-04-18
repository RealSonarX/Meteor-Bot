from os import getenv
from random import *
from unicodedata import *
from tinydb import *
from discord import *
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import *
from asyncio import *

load_dotenv("token.env")
if (getenv('DEV_ENV')) == 'True':
    DEV_ENV = True
else:
    DEV_ENV = False
if DEV_ENV:
    from lists import *
    from aioconsole import *
else:
    from .lists import *

#
def main():
    intents = Intents.all()
    watchlist = []

    async def check_spammer(member, increment, channel):
        for i in watchlist:
            if i['username'] == str(member):
                if i['spam_count'] >= 20:
                    await timeout_user(member, 20)
                    await channel.send(f"{nope_list[randint(0, (len(nope_list) - 1))]}",
                                               reference=message)
                i.update({'spam_count': (i['spam_count'] + increment)})
                await sleep(60)
                i.update({'spam_count': (i['spam_count'] - increment)})

    def db():
        db = TinyDB('db.json')
        return db

    def profile_view(member):
        Profile = Query()
        profile_data = db().search(Profile.id == member.id)
        print(f"Requesting profile data")
        print(profile_data)
        user_avatar = member.avatar.url

        try:
            colour = profile_data[0]['colour']
        except:
            colour = 0x00b0f4
        embed = Embed(colour=colour)
        main = profile_data[0]['main']

        maincodename = char_code_names[main.lower()]
        alt = profile_data[0]['alt']
        try:
            desc = profile_data[0]['desc']
        except:
            desc = 'Awaiting description!'
        try:
            secondary = profile_data[0]['secondary']
        except:
            secondary = ''
        embed.add_field(name=f"{member}",
                        value=desc,
                        inline=False)
        embed.add_field(name="Main", value=f"{main.title()} ", inline=False)
        if secondary != '':
            embed.add_field(name="Secondary", value=f"{(profile_data[0]['secondary']).title()} ", inline=False)
        embed.set_image(
            url=f"https://raw.githubusercontent.com/joaorb64/StreamHelperAssets/refs/heads/main/games/ssbu/mural_art/{maincodename.lower()}_0{alt}.png")
        embed.set_thumbnail(url=user_avatar)
        return embed

    bot = commands.Bot(command_prefix='.', intents=intents)

    TOKEN = getenv('TOKEN')

    pt = ["squirtle", "ivysaur", "charizard"]
    shorthands = {"ganon": "ganondorf", "brawler": "mii_brawler", "krool": "kingkrool", "dk": "donkey_kong",
                  "donkey kong": "donkey_kong"}
    miis = ["mii_brawler", "mii_gunner", "mii_swordfighter"]

    @tasks.loop(seconds=3)
    async def send_messagee():
        global channel, index_of_msg

        if DEV_ENV:
            if channel != bot.get_channel(956606255974199327):
                channel = channel
            else:
                channel = bot.get_channel(956606255974199327)
            try:

                msg = await ainput(": ")
                actual_msg = msg
                if msg[0] == '#':
                    construction_msg = []
                    for i in msg[1: (len(msg))]:
                        construction_msg.append(i)
                    channel_find = True
                    channel_name = ''
                    index_counter = 0
                    for i in construction_msg:
                        if i == ' ':
                            channel_find = False
                        else:
                            channel_name += i
                            index_counter += 1

                        if not channel_find:
                            break
                    actual_msg = ''
                    construction_counter = 0
                    for i in construction_msg:
                        if construction_counter >= index_counter:
                            actual_msg += i
                        construction_counter += 1
                    for i in bot.get_all_channels():
                        if i.name == channel_name:
                            channel = bot.get_channel(i.id)
                    await channel.send(f"{actual_msg}")
                elif msg[0] == '/':
                    msg = msg[1:]
                    content = msg[1:]
                    if msg[0] == 't':

                        for i in bot.get_all_members():

                            if str(i.name) == content:
                                await timeout_user(i, 10)
                else:
                    await channel.send(f"{actual_msg}")


            except Exception:
                pass

    @bot.tree.command(name='viewprofile', description='View profiles of server members')
    async def smasher_profile_view(interaction, member: Member):
        embed = profile_view(member)
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
    async def smasher_profile_update(interaction, main: str, alt: app_commands.Choice[int], secondary: str = '',
                                     desc: str = "Awaiting description!"):
        Profile = Query()
        member = str(interaction.user)

        main = main.lower()
        alt = int(alt.value)
        passed = True
        try:
            main_codename = char_code_names[main.lower()]
            if secondary != '':
                sec_codename = char_code_names[secondary.lower()]
        except:
            main_codename = 0
            sec_codename = 0
            await interaction.response.send_message("You didn't enter a valid character!")
            passed = False
        if any(i in normalize('NFKD', ''.join(str(desc.lower()))) for i in american_words):
            passed = False
            await interaction.response.send_message("You thought.")
        if DEV_ENV:
            passed = False
        if passed:

            if db().search(Profile.id == interaction.user.id) != []:
                db().update({'member': member, 'alt': alt, 'main': main, 'id': interaction.user.id, 'desc': desc,
                             'secondary': secondary},
                            Profile.id == interaction.user.id)
            else:
                db().insert({'member': member, 'alt': alt, 'main': main, 'id': interaction.user.id, 'desc': desc,
                             'secondary': secondary})
            embed = profile_view(interaction.user)
            await interaction.response.send_message("Updated your profile!", embed=embed)

    @bot.tree.command(name='announce', description='Ping everyone individually')
    async def ping_everyone(interaction):
        if str(interaction.user) not in ascended_users:
            await interaction.response.send_message(nope_list[randint(0, (len(nope_list) - 1))])
        else:
            msg = ''
            for i in bot.get_all_members():
                msg += f"<@{i.id}> "
            await interaction.response.send_message(msg, delete_after=2)

    @bot.tree.command(name='rules', description='Shows the server rules')
    async def view_rules(interaction):
        channel = interaction.channel.name
        counter = 0
        for i in rules:
            await channel.send(f"Rule {counter} : {i}")
            counter += 1

    @bot.tree.command(name='speak')
    async def speak(interaction, msg: str):
        channel = interaction.channel
        await interaction.response.send_message("Done", ephemeral=True, delete_after=1)
        await channel.send(msg)

    @bot.tree.command(name='vengeance', description='MY REVENGGGGEEEE')
    async def vengeance(interaction, channel: TextChannel, member: Member):
        if str(member.name) not in ascended_users:
            print(f"{str(member.name)} ran command /vengeance")
            await interaction.response.send_message(f"We do a little trolling", ephemeral=True, delete_after=3)
            for i in range(0, randint(10, 15)):
                await channel.send(f"<@{member.id}>", delete_after=1)

        else:
            await interaction.response.send_message(nope_list[randint(0, (len(nope_list) - 1))])

    async def timeout_user(member: Member, duration: int):
        await member.timeout(timedelta(minutes=duration), reason=f"Spam")
        print(f"Timouted {member.name}")

    @bot.event
    async def on_message(message):
        quotes = bot.get_channel(931598462879944764)
        if (message.type) == MessageType.reply:

            original_msg = message.reference.resolved
            original_msg = original_msg.content
            print(f'#{message.channel}  {str(message.author)}: {str(message.content)} (replied to "{original_msg}")')

        else:
            print(f"#{message.channel}  {str(message.author)}: {str(message.content)}")

        message.content = normalize("NFKD", message.content)
        if str(message.author) != 'Meteor#1277' and not DEV_ENV:
            if message.channel == quotes and message.attachments == []:
                await message.delete()
                await message.channel.send("No talking in this channel please!", delete_after=3)
            if 'meta knight' in message.content.lower():
                await message.channel.send(meta_knight)
                await check_spammer(message.author, 10, message.channel)
            elif any(i in ''.join(str(message.content.lower())) for i in american_words):
                await message.delete()
                await message.channel.send(f"<@{message.author.id}> Outta here with that Amer*can nonsense bruv ()",
                                           delete_after=2)
            elif any(i in ''.join(str(message.content.lower())) for i in banned_words):
                await message.delete()

            elif 'roy' in message.content.lower():
                if randint(0, 5) == 1:
                    await message.channel.send(roy[randint(0, len(roy)-1)])
                await check_spammer(message.author, 10, message.channel)
            elif 'aegis' in message.content.lower() or 'pythra' in message.content.lower():
                if randint(0, 10) == 1:
                    await message.channel.send(pythra_copypasta)
            elif '@everyone' in message.content.lower() and str(message.author) not in ascended_users:
                await message.channel.send(f"{nope_list[randint(0, (len(nope_list) - 1))]}", reference=message)
                await timeout_user(message.author, 1440)
            elif ('meat' in message.content.lower() or 'meet' in message.content.lower()) and (
                    str(message.author) == 'khaoslatet'):
                await message.channel.send(f"{nope_list[randint(0, (len(nope_list) - 1))]}", reference=message)
                await message.delete()
            elif 'neat' in message.content.lower():
                await message.channel.send("Neat is a mod by Vazkii")
            elif 'neil' in message.content.lower():
                await message.reply('https://raw.githubusercontent.com/RealSonarX/Meteor-Bot/refs/heads/main/src/meteor_bot/neil.jpeg')

    @bot.event
    async def on_member_update(before, after):
        channel = bot.get_channel(956606255974199327)


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
        guild = bot.get_guild(906804682452779058)
        print(f'We have logged in as {bot.user}')

        if DEV_ENV:
            for i in bot.get_all_members():
                print(f"{str(i.name)} ({i.status}) : {i.id}")
                #try:
                #    timeout_user(i)

            print("Done!")

        for i in bot.get_all_members():
            watchlist.append({'username': i.name, 'spam_count': 0})
        send_messagee.start()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()

# Quickping List
# Yappers = <@&1328843759764639895>
# Admin = <@&1345846227593596988>


# Pixel = <@487247155741065229>
# Serry = <@586987213024133162>
