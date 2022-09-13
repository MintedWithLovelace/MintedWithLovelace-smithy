import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="&", intents=intents)
load_dotenv()
invites = {}


@client.event
async def on_ready():
    for guild in client.guilds:
        invites[guild.id] = await guild.invites()


def find_invite_by_code(invite_list, code):
    for inv in invite_list:
        if inv.code == code:
            return inv


@client.event
async def on_member_join(member):
    invites_before_join = invites[member.guild.id]
    invites_after_join = await member.guild.invites()
    for invite in invites_before_join:
        if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
            user_entry = "\n" + f"Member {member.name} Joined" + "\n" + f"Invite Code: {invite.code}" + "\n" + f"Inviter: {invite.inviter}"
            print(user_entry)
            with open('/path/to/InviteUseLog.log', 'a') as bot_log:
                bot_log.write(user_entry)
                bot_log.close()
            invites[member.guild.id] = invites_after_join
            return


@client.event
async def on_member_remove(member):
    invites[member.guild.id] = await member.guild.invites()


token = os.getenv("TOKEN")
client.run(token)
