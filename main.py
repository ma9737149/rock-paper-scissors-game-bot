import discord,random,sqlite3
from discord.ext import commands


client = commands.Bot(command_prefix="!", intents= discord.Intents.all())

tree = client.tree

@client.event
async def on_ready():
    synced =  await tree.sync()

    db = sqlite3.connect("data.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS user_data(user_id INTEGER PRIMARY KEY , win INTEGER , lose INTEGER , draw INTEGER)")

    db.commit()
    db.close()


    print(f"Synced {len(synced)} command(s)\nBot is ready to use...")


class play_game(discord.ui.View):
    def __init__(self,players:list,current_player):
        super().__init__(timeout=None)
        self.players = players
        self.current = current_player
        self.users_chooses = {
            
        }

    def open_acc(self,user_id):
        db = sqlite3.connect("data.db")
        cur = db.cursor()

        cur.execute("SELECT * FROM user_data WHERE user_id = ?" , (user_id,))

        data = cur.fetchone()

        if data:
            db.close()
            return 
        else:
            cur.execute("INSERT INTO user_data VALUES(?,?,?,?)", (user_id, 0 , 0 , 0))
            db.commit()
            db.close()
        
    def update_data_win(self,user_id):
        self.open_acc(user_id)
        db = sqlite3.connect("data.db")
        cur = db.cursor()

        cur.execute("UPDATE user_data SET win = win + 1 WHERE user_id = ?" , (user_id,))

        db.commit()
        db.close()

    def update_data_lose(self,user_id):
        self.open_acc(user_id)
        db = sqlite3.connect("data.db")
        cur = db.cursor()

        cur.execute("UPDATE user_data SET lose = lose + 1 WHERE user_id = ?" , (user_id,))

        db.commit()
        db.close()

    def update_data_draw(self,user_id,user_id_2):
        self.open_acc(user_id)
        self.open_acc(user_id_2)
        db = sqlite3.connect("data.db")
        cur = db.cursor()

        cur.execute("UPDATE user_data SET draw = draw + 1 WHERE user_id = ?" , (user_id,))
        cur.execute("UPDATE user_data SET draw = draw + 1 WHERE user_id = ?" , (user_id_2,))

        db.commit()
        db.close()


    async def check_winner(self,interaction,user_choice_turn_2,another_choice,index_another_choice):
                
            if user_choice_turn_2 == "rock" and another_choice == "scissors" or user_choice_turn_2 == "scissors" and another_choice == "paper" or user_choice_turn_2 == "paper" and another_choice == "rock":
                await interaction.message.edit(content=f"{interaction.user.mention} Won", view= None)
                self.update_data_win(interaction.user.id)
                self.update_data_lose(index_another_choice)

            elif another_choice == user_choice_turn_2:
                await interaction.message.edit(content="It's Draw" , view = None)
                self.update_data_draw(interaction.user.id , index_another_choice)
            
            else:
                await interaction.message.edit(content = f"<@{index_another_choice}> Won" , view = None)
                self.update_data_win(index_another_choice)
                self.update_data_lose(interaction.user.id)


    

    @discord.ui.button(label = "Rock" , style=discord.ButtonStyle.danger)
    async def _rock(self, interaction:discord.Interaction,button:discord.ui.button):
            if self.current != interaction.user.id:
                await interaction.response.send_message("it's not your turn or you are not playing absloutly" , ephemeral= True)
                return
                


            
            await interaction.response.defer()
            self.users_chooses[self.current] = "rock"

            current_player_index = self.players.index(interaction.user.id)
            current_player = 0 if current_player_index == 1 else 1
            self.current = self.players[current_player]

            if len(self.users_chooses) == 2:

                user_choice_turn_2 = self.users_chooses[interaction.user.id]
                index_another_choice = self.players[0] if self.players.index(interaction.user.id) == 1 else self.players[1]
                another_choice = self.users_chooses[index_another_choice]

                await self.check_winner(interaction,user_choice_turn_2,another_choice,index_another_choice)
                return


            await interaction.message.edit(content=f"<@{self.current}> now it's your turn")






    @discord.ui.button(label = "Paper" , style=discord.ButtonStyle.green)
    async def _paper(self, interaction:discord.Interaction,button:discord.ui.button):
            if self.current != interaction.user.id:
                await interaction.response.send_message("it's not your turn or you are not playing absloutly" , ephemeral= True)
                return
            
                


            
            await interaction.response.defer()
            self.users_chooses[self.current] = "paper"

            current_player_index = self.players.index(interaction.user.id)
            current_player = 0 if current_player_index == 1 else 1
            self.current = self.players[current_player]

            if len(self.users_chooses) == 2:

                user_choice_turn_2 = self.users_chooses[interaction.user.id]
                index_another_choice = self.players[0] if self.players.index(interaction.user.id) == 1 else self.players[1]
                another_choice = self.users_chooses[index_another_choice]

                await self.check_winner(interaction,user_choice_turn_2,another_choice,index_another_choice)
                return


            await interaction.message.edit(content=f"<@{self.current}> now it's your turn")




    @discord.ui.button(label = "Scissors" , style=discord.ButtonStyle.blurple)
    async def _scissors(self, interaction:discord.Interaction,button:discord.ui.button):

            if self.current != interaction.user.id:
                await interaction.response.send_message("it's not your turn or you are not playing absloutly" , ephemeral= True)
                return
                


            
            await interaction.response.defer()
            self.users_chooses[self.current] = "scissors"

            current_player_index = self.players.index(interaction.user.id)
            current_player = 0 if current_player_index == 1 else 1
            self.current = self.players[current_player]

            if len(self.users_chooses) == 2:

                user_choice_turn_2 = self.users_chooses[interaction.user.id]
                index_another_choice = self.players[0] if self.players.index(interaction.user.id) == 1 else self.players[1]
                another_choice = self.users_chooses[index_another_choice]

                await self.check_winner(interaction,user_choice_turn_2,another_choice,index_another_choice)

                return
                    
                




            await interaction.message.edit(content=f"<@{self.current}> now it's your turn")







class join_game_view(discord.ui.View):
    def __init__(self,author:discord.Member,message:discord.Message,vs_user:discord.Member):
        super().__init__(timeout=60)
        self.author = author
        self.m = message
        self.vs_user = vs_user
        self.users = []

    @discord.ui.button(label = "join" , style=discord.ButtonStyle.green)
    async def _join(self, interaction : discord.Interaction, button:discord.ui.Button):
        if interaction.user.id != self.vs_user.id:
            await interaction.response.send_message(f"this request not for you it's just for {self.vs_user.mention}" , ephemeral=True)
        
        elif interaction.user.id == self.author.id:
            await interaction.response.send_message("you allready joined" , ephemeral=True)

        else:

            self.users.append(self.author.id)
            self.users.append(self.vs_user.id)

            current_player = random.choice(self.users)

            await interaction.message.edit(content="request accepted" , view = None) 
            await interaction.response.send_message(f"Choose from these btns <@{current_player}>",view = play_game(self.users,current_player))



    @discord.ui.button(label= "cancel" , style = discord.ButtonStyle.danger)
    async def _cancel(self, interaction : discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.vs_user:
            await interaction.message.edit(content="request reject" , view = None) 
        else:
            await interaction.response.send_message(f"this request not for you it's just for {self.vs_user.mention}" , ephemeral=True)
    





def open_acc_and_get_data(user_id):
        db = sqlite3.connect("data.db")
        cur = db.cursor()

        cur.execute("SELECT win , lose , draw  FROM user_data WHERE user_id = ?" , (user_id,))

        data = cur.fetchone()

        if data:
            win , lose , draw = data[0] , data[1] , data[2]
            db.close()
            return win , lose , draw
        else:
            cur.execute("INSERT INTO user_data VALUES(?,?,?,?)", (user_id, 0 , 0 , 0))
            db.commit()
            db.close()
            return 0 , 0 , 0





@tree.command(name="rps-game" , description= "simple rps-game bot")
async def _rps_game(interaction:discord.Interaction,member:discord.Member):
    if member.bot:
        await interaction.response.send_message("you can't play rps-game vs bots",ephemeral=True) 
    elif member.id == interaction.user.id:
        await interaction.response.send_message("you can't choose yourself" ,ephemeral=True)
    else:
        await interaction.response.send_message(f"{member.mention}, {interaction.user.name} asks you to join",ephemeral=False,view=join_game_view(interaction.user,interaction.message,member))


@tree.command(name = "show_rps_game_info" , description = "show user info about win , lose , draw , games which played ")
async def _show_rps_game_info(interaction : discord.Interaction , member : discord.Member = None):

    member = member if member != None else interaction.user

    if member.bot:
        await interaction.response.send_message("bot cannot play games" , ephemeral=True)
        return

    win , lose , draw = open_acc_and_get_data(member.id)
    matches_played = win + lose + draw

    embed = discord.Embed(title = f"{member.name} rps game info" , description = f"" , color= discord.Colour.dark_blue())

    embed.add_field(name = "Win:" , value = win , inline = False)
    embed.add_field(name = "Lose:" , value = lose , inline = False)
    embed.add_field(name = "Draw:" , value = draw , inline = False)
    embed.add_field(name = "Matches Played:" , value = matches_played , inline = False)
    embed.set_author(name = f"{member.name}" , icon_url = member.display_avatar)
    embed.set_footer(text=f"requested by : {interaction.user.display_name}" , icon_url = interaction.user.display_avatar)

    await interaction.response.send_message(embed=embed , ephemeral=False)





client.run("TOKEN")