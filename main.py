import discord
from discord.ext import commands
from meapi import Me

intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

me = Me(interactive_mode=True)

@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user.name}')
    general_channel = discord.utils.get(bot.guilds[0].channels, name='general')
    if general_channel:
        await general_channel.send('Hi everyone!')
        await general_channel.send('To lookup a phone number, type: `!lookup <phone_number>`')

@bot.command()
async def lookup(ctx, phone_number: str):
    res = me.phone_search(phone_number)
    if res:
        embed = discord.Embed(title=f"Details for {phone_number}", color=discord.Color.blue())
        embed.add_field(name="Name", value=res.name, inline=False)

        if res.user:
            user = res.user
            embed.add_field(name="User Details",
                            value=f'{user.name=}, {user.email=}, {user.slogan=}, {user.profile_picture=}', inline=False)

            profile = res.get_profile()
            embed.add_field(name="Profile Details",
                            value=f'{profile.date_of_birth=}, {profile.location_name=}, {profile.gender=}, {profile.device_type=}',
                            inline=False)

            # 📱 Get social media accounts:
            social_details = ""
            for social in profile.social:
                if social:
                    social_details += f"Social media ({social.name}): {social.profile_url}\n"
                    for post in social.posts:
                        social_details += f"Post from {post.posted_at}:\n{post.text_first}\n{post.text_second}\n\n"
            if social_details:
                embed.add_field(name="Social Media", value=social_details, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f'No details found for {phone_number}.')

bot.run('')