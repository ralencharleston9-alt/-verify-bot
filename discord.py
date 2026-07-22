import discord
from discord.ext import commands
from discord.ui import Button, View
import os

TOKEN = os.getenv("TOKEN")

VERIFIED_ROLE_NAME = "Verified"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Verify",
        style=discord.ButtonStyle.green,
        emoji="✅",
        custom_id="verify_button"
    )
    async def verify(self, interaction: discord.Interaction, button: Button):

        role = discord.utils.get(
            interaction.guild.roles,
            name=VERIFIED_ROLE_NAME
        )

        if role is None:
            role = await interaction.guild.create_role(
                name=VERIFIED_ROLE_NAME
            )

        if role in interaction.user.roles:
            await interaction.response.send_message(
                "You are already verified!",
                ephemeral=True
            )
            return

        await interaction.user.add_roles(role)

        await interaction.response.send_message(
            "✅ You are now verified!",
            ephemeral=True
        )


@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.has_permissions(administrator=True)
async def verify(ctx):

    embed = discord.Embed(
        title="Verification",
        description="Click the button below to verify and gain access to the server.",
        color=0x00ff00
    )

    await ctx.send(
        embed=embed,
        view=VerifyView()
    )


bot.run(TOKEN)