import discord
from discord.ext import commands
from discord import RawReactionActionEvent, Embed
import re
import PANEL


class ROLEMANAGING(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload: RawReactionActionEvent):

        try:
          guild = await self.bot.fetch_guild(payload.guild_id)
          channel = await guild.fetch_channel(payload.channel_id)
          message = await channel.fetch_message(payload.message_id)
        except:
          return
        
        bot = await guild.fetch_member(message.author.id)
        status = str(bot.status)
        if(status != "offline"):return

        member = await guild.fetch_member(payload.user_id)
        emoji = payload.emoji
        print(emoji)
        print(str(emoji))
        if not (guild and channel and message and member and emoji and bot): return
        print("process1 has passed")

  
        if PANEL.isPanel(message):
          print("process2 has passed")
          try:
            await message.remove_reaction(emoji,member)
          except:
            return
          
          print("process3 has passed")
          
          paneldescription = message.embeds[0].description
          print(paneldescription)
          if not paneldescription: return
          description = "This is an easter egg"
          print("process4 has passed")

          pattern = f"{str(emoji)}:<@&(\\d+)>"
          roleid = re.search(pattern,paneldescription) 
          if not roleid: return
          print("process5 has passed")
          print(roleid.group(1))
          role = guild.get_role(int(roleid.group(1)))
          mention = f"<@{member.id}>"
          if not role: description="役職が存在しないか、見当たりません"
          else:
            print("process6 has passed")

            if(role in member.roles):
              action = lambda: member.remove_roles(role)
              description = f"{mention}の役職を解除しました"

            else:
              action = lambda: member.add_roles(role)
              description = f"{mention}の役職を付与しました"

            try:
              print("process7-1 has passed")
              await action()
            except Exception as e:
              print(e)
              print("process7-2 has passed")
              description = "役職の設定に失敗しました\n"
              print("section1")
              me = guild.me
              print("section2") #<=====ここまでいく
              if not me.roles[0].manage_role:
                description += "botに「役職の管理」の権限がないかも？"
                print("pre-sections1") #<====ここにはいかない
              if bot.top_role.position <= role.position:
                description += "BOTの一番上の役職よりも高い役職をつけようとしてるかも？"
                print("pre-sections2") #<====ここにもいかない
              if role.is_default():
                description += "everyone役職だからかも？"
                print("pre-sections3") #<====ここにもいかない
              if role.is_bot_managed():
                description += "特定のbotにしか付与出来な役職だからかも？"
                print("pre-sections4") #<====ここにもいかない
              if role.is_premium_subscriber():
                description += "サーバーブースター用の役職だからかも？"
                print("pre-sections5") #<====ここにもいかない
              else:
                description += "原因が全然わからん！"
                print("pre-sections6") #<====ここにもいかない
              print("section 3") #<====ここにもいかない

            try:
              print("process8 has passed")
              embed = Embed(description=description)
              msg = await channel.send(content=mention,embed=embed)
              await msg.delete(delay=5)
            except Exception as e:
              print("exception occured")
              print(e)
              return

          return



