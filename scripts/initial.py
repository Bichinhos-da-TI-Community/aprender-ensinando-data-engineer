# Bibliotecas do discord necessarias
from discord import Intents
from discord.ext import commands
from discord.ext import tasks

# Controle da chave do Bot
from dotenv import load_dotenv
import os

load_dotenv('scripts/bot.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

print(BOT_TOKEN)

# Bot intents
intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# URL para adicionar o BOT
# https://discord.com/api/oauth2/authorize?client_id=1194738896345514024&permissions=66560&scope=bot

# Multiplos "on_ready" evento não funciona!

# Diferente formas de acessar canais especificos
allowed_channel_ids = [1195050883629715520]
allowed_channels = ["general"]

# Teste simples para ver se o bot funciona!
#@bot.event
#async def on_ready():
#    print(f'We have logged in as {bot.user}')

# STREAM/ Pegando mensagem se a mensagem estiver na lista de canal permitido!
@bot.event
async def on_message(message):
    if message.channel.name in allowed_channels:
        print(f'Message ID: {message.id}')
        print(f'Timestamp: {message.created_at}')
        print(f'Author: {message.author}')
        print(f'Channel: {message.channel.name}')
        print(f'Content: {message.content}')
        print(f'Created At: {message.created_at}')
        print(f'Edited At: {message.edited_at}')
        for attachment in message.attachments:
            print(f'Attachment: {attachment.url}')
        for mention in message.mentions:
            print(f'Mention: {mention}')
        for channel_mention in message.channel_mentions:
            print(f'Channel Mention: {channel_mention}')
        for role_mention in message.role_mentions:
            print(f'Role Mention: {role_mention}')
        if '@here' in message.content:
            print('Message includes @here mention')
        if '@everyone' in message.content:
            print('Message includes @everyone mention')
        print('------------------------')  # Separator for readability

# STREAM/ Verifica se houve mudança nos roles dos membros do canal, precisa testar se funciona!
@bot.event
async def on_member_update(before, after):
    before_roles = set(role.name for role in before.roles)
    after_roles = set(role.name for role in after.roles)

    new_roles = after_roles - before_roles
    lost_roles = before_roles - after_roles

    if new_roles:
        print(f'{after.name} has gained roles: {", ".join(new_roles)}')
    if lost_roles:
        print(f'{after.name} has lost roles: {", ".join(lost_roles)}')


# BATCH/ Pega todas mensagens a cada 60 segundos dos canais escolhidos
@tasks.loop(seconds=60)
async def fetch_new_messages():
    channel = bot.get_channel(1195050883629715520)
    messages = []
    async for message in channel.history(limit=None):
        messages.append(message)
    for message in messages:
        print(f'Message ID: {message.id}')
        print(f'Timestamp: {message.created_at}')
        print(f'Author: {message.author}')
        print(f'Channel: {message.channel.name}')
        print(f'Content: {message.content}')
        print('------------------------')

        
# BATCH/ Pega as informações dos usuários, precisa melhorar
"""
@bot.event
async def on_ready():
    for guild in bot.guilds:
        async for member in guild.fetch_members(limit=None):
            print(f'Name: {member.name}')
            print(f'Display Name: {member.display_name}')
            print(f'Avatar: {member.avatar.url}')
            print(f'Roles: {[role.name for role in member.roles]}')
            print(f'Joined At: {member.joined_at}')
            print(f'Permissions: {member.guild_permissions}')
            print('------------------------')  # Separator for readability
"""
            
# Código para poder rodar o código de pegar as mensagens em batch
      
@bot.event
async def on_ready():
    fetch_new_messages.start()


bot.run(BOT_TOKEN)