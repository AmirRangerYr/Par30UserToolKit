import discord
from discord import Option

PROFILE_IMAGE = "https://par30negar.ir/wp-content/uploads/jet-engine-forms/1/2025/09/profileLogo.png"
token = "Here" #Place Your Token here 

bot = discord.Bot(intents=discord.Intents.all())

def make_embed(ctx, title, desc):
    e = discord.Embed(title=title, description=desc, color=0x2f3136)
    if ctx.guild and ctx.guild.icon:
        e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
    e.set_footer(text=f"Powered by par30negar.ir 💙",icon_url=PROFILE_IMAGE)
    return e

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Powerd By Par30negar.ir 💙"))
    print(f"Logged in as {bot.user}\nPowerd By 💙'Par30negar.ir'💙")

# Error handler for all commands
@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, discord.errors.LoginFailure):
        print("Token is invalid, please check your token.")
    elif isinstance(error, discord.Forbidden):
        await ctx.respond("Bot does not have permission to execute this command.", ephemeral=True)
    else:
        await ctx.respond(f"An error occurred: {error}", ephemeral=True)


#commend info: Shows user avatar with download link
@bot.slash_command(name="avatar", description="Show user avatar with download link")
async def avatar(ctx: discord.ApplicationContext, member: Option(discord.Member, "Select a user", required=False)):
    member = member or ctx.author
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    e = make_embed(ctx, f"Avatar — {member}", f"[Click to Download]({avatar_url})")
    e.set_image(url=avatar_url)
    await ctx.respond(embed=e)


#commend info: Shows user information
@bot.slash_command(name="userinfo", description="Show user information")
async def userinfo(ctx: discord.ApplicationContext, member: Option(discord.Member, "Select a user", required=False)):
    member = member or ctx.author
    e = make_embed(ctx, f"User Info — {member}", None, inline=False)
    e.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url, inline=False)
    e.add_field(name="🆔 ID", value=member.id, inline=False)
    e.add_field(name="🏷️ Tag", value=f"{member}", inline=False)
    e.add_field(name="📅 Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
    e.add_field(name="📥 Joined Server", value=member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "Unknown", inline=False)
    roles = ", ".join([r.mention for r in member.roles[1:]]) or "No Roles"
    e.add_field(name="🎭 Roles", value=roles, inline=False)
    await ctx.respond(embed=e)

#commend info: Shows detailed server information
@bot.slash_command(name="serverinfo", description="Show detailed server information")
async def serverinfo(ctx: discord.ApplicationContext):
    g = ctx.guild
    e = make_embed(ctx, f"Server Info — {g.name}", None)
    if g.icon:
        e.set_thumbnail(url=g.icon.url)
    e.add_field(name="🆔 ID", value=g.id, inline=False)
    e.add_field(name="👑 Owner", value=g.owner, inline=False)
    e.add_field(name="👥 Members", value=g.member_count, inline=False)
    e.add_field(name="📂 Channels", value=len(g.channels), inline=False)
    e.add_field(name="🎭 Roles", value=len(g.roles), inline=False)
    e.add_field(name="📅 Created At", value=g.created_at.strftime("%Y-%m-%d"), inline=False)
    await ctx.respond(embed=e)

#commend info: Shows role information
@bot.slash_command(name="roleinfo", description="Show information about a role")
async def roleinfo(ctx: discord.ApplicationContext, role: Option(discord.Role, "Select a role")):
    e = make_embed(ctx, f"Role Info — {role.name}", None)
    e.add_field(name="🆔 ID", value=role.id, inline=False)
    e.add_field(name="🎨 Color", value=str(role.color), inline=False)
    e.add_field(name="👥 Members", value=len(role.members), inline=False)
    e.add_field(name="📅 Created At", value=role.created_at.strftime("%Y-%m-%d"), inline=False)
    await ctx.respond(embed=e)


if __name__ == "__main__":
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print("Token is invalid, please check your token.")
    except discord.errors.DiscordServerError:
        print("Network is invalid, please check your network.")
