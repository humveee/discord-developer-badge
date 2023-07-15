
from discord import Intents,Interaction
from discord.ext import commands
from discord import app_commands
from discord import VerificationLevel,ContentFilter
from requests import get,post,patch
from os import system
from win32api import GetAsyncKeyState
from time import sleep

class Cog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    @app_commands.command(name="badge")
    async def test(self, interaction:Interaction):
        if interaction.guild.rules_channel is not None:
            await interaction.guild.rules_channel.delete()
        if interaction.guild.public_updates_channel is not None:
            await interaction.guild.public_updates_channel.delete()
        rules = await interaction.guild.create_text_channel("rules")
        updates = await interaction.guild.create_text_channel("updates")
        await interaction.guild.edit(verification_level=VerificationLevel.high, explicit_content_filter=ContentFilter.all_members)
        await interaction.guild.edit(community=True, rules_channel=rules,public_updates_channel=updates)
        await interaction.response.send_message("Server setup for developer badge done :white_check_mark: (You will be able to claim it in 1 day : https://discord.com/developers/active-developer)")


class Client(commands.Bot):
    def __init__(self, command_prefix, intents=Intents.all(), **options) -> commands.Bot:
        super().__init__(command_prefix, intents=intents, **options)
    async def on_ready(self):
        await self.add_cog(Cog(self))
        await self.tree.sync()
        print("Logged as %s, use /badge to receive badge, click 'q' to exit" % (self.user))
        await self.wait_for_key()
    async def wait_for_key(self):
        while True:
            sleep(0.1)
            if not GetAsyncKeyState(0x51):
                continue
            await self.close()
            print("Exit")
            exit(0)
            break
class Cli():
    def __init__(self) -> None:
        self.main()
    def create_app(self):
        if not self._token:
            return
        app_request = post("https://discord.com/api/v10/applications", headers={
            "Authorization":self._token
        }, json={
            "name":"Developer Badge2",
            "team_id":None
        })
        if not str(app_request.status_code)[0] == "2":
            print("Error while creating app")
            sleep(4)
            return self.main()
        print("[+] Created app")
        reset_request = post("https://discord.com/api/v9/applications/%s/bot/reset" % (app_request.json()['id']), headers={
            "Authorization":self._token
        })

        if not str(reset_request.status_code)[0] == "2":
            print("Error while creating app")
            sleep(4)
            return self.main()
        print("[+] Got bot token")
        self._bot_token = reset_request.json()['token']
        set_intents = patch("https://discord.com/api/v9/applications/%s" % (app_request.json()['id']), headers={
            "Authorization":self._token
        }, json={
            "bot_public":app_request.json()['bot_public'],
            "bot_require_code_grant":app_request.json()['bot_require_code_grant'],
            "flags":565248
        })
        if not str(set_intents.status_code)[0] == "2":
            print("Error while setting app intents")
            sleep(4)
            return self.main()
        print("[+] Intents set")


    def check_token(self):
        if not self._token:
            return
        r = get("https://discord.com/api/v10/users/@me", headers={
            "Authorization":self._token
        })
        if str(r.status_code)[0] != "2":
            return False
        return True

    def main(self):
        system("cls")
        print("""
    

DDDDD                         lll                                 BBBBB                dd                
DD  DD    eee  vv   vv   eee  lll  oooo  pp pp     eee  rr rr     BB   B    aa aa      dd  gggggg   eee  
DD   DD ee   e  vv vv  ee   e lll oo  oo ppp  pp ee   e rrr  r    BBBBBB   aa aaa  dddddd gg   gg ee   e 
DD   DD eeeee    vvv   eeeee  lll oo  oo pppppp  eeeee  rr        BB   BB aa  aaa dd   dd ggggggg eeeee  
DDDDDD   eeeee    v     eeeee lll  oooo  pp       eeeee rr        BBBBBB   aaa aa  dddddd      gg  eeeee 
                                         pp                                                ggggg         

""")
        print("Created by: %s" % ("https://github.com/humvee"))
        print("Repo link : %s" % ("nigger"))
        self._token = input("Your token >> ")
        if not self.check_token():
            print("Invalid token")
            sleep(4)
            return self.main()
        self.create_app()
        bot = Client("!")
        bot.run(self._bot_token, log_handler=None)

Cli()