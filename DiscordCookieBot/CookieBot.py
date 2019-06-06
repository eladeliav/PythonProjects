import discord
from discord.ext import commands

TOKEN = 'NTExMjc0MzAyNjU4NTc2NDE0.DsoiCQ.KlAmeK-aJQKAFH7UpFEqCKUjC_0'

client = commands.Bot(command_prefix='!')
Extensions = ['BasicCommands', 'Music', 'MemeCommands']
Roles_Can_Use = ['513055460044046367', '491305275874082827']  #shabtaibot, Admin

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))
    print('Client Id: {}'.format(client.user.id))
    print(discord.utils.oauth_url(client.user.id))
    print('-' * 75)
    print('Bot is ready.')


def checks_roles(roles):
    return True
    for ok_role in Roles_Can_Use:
        for check_role in roles:
            if ok_role == check_role.id:
                return True
    return False


@client.event
async def on_message(message):
    author = message.author
    if message.author.bot:
        return
    if author.id == '271681252904402947':  # is me
        await client.process_commands(message)
        return
    if 'https' not in message.content:
        message.content = message.content.lower()
    list_of_user_roles = author.roles
    if not checks_roles(list_of_user_roles):
        await client.send_message(message.channel, "Ha. Gay guy can't use bot.")
        return
    else:
        await client.process_commands(message)


def main():
    for extension in Extensions:
        try:
            client.load_extension(extension)
            print('{} extension loaded successfully.'.format(extension))
        except Exception as e:
            print("{} extension couldn't be loaded. {}".format(extension, e))
    client.run(TOKEN)


if __name__ == '__main__':
    main()
