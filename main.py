import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

created_at_format = '%a %b %d %Y %H:%M:%S GMT%z'


@bot.event
async def on_ready():
    print('Ready')


@bot.command()
async def whois(ctx: commands.Context, user_id: str):
    user_id = int(user_id)
    try:
        found = await bot.fetch_user(user_id)
    except discord.NotFound:
        await ctx.send('No user found by the given ID.')
    except discord.HTTPException:
        await ctx.send('Failed to fetch due to HTTP exception.')
    embed = discord.Embed(color=discord.Color.blurple())
    embed \
        .add_field(name='User ID', value=str(found.id), inline=False) \
        .add_field(name='Created At', value=found.created_at.strftime(created_at_format), inline=False) \
        .set_thumbnail(url=found.avatar.url) \
        .set_author(name=f'{found.name}#{found.discriminator}', icon_url=found.avatar.url) \
        .set_footer(text='Local time')
    embed.timestamp = found.created_at
    await ctx.send(embed=embed)


bot.run(os.environ.get('FETCHER_TOKEN'))
