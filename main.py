import discord, os, random
from discord.ext import tasks, commands
from replit import db
from table2ascii import table2ascii, PresetStyle, Alignment
from itertools import cycle
from flask import Flask
from threading import Thread
from time import time

import test

bot_commands = [
    'ping', 'add_problem', 'get_problem', 'add_user', 'solved', 'solution',
    'solved_of', 'solved_by', 'eagle_view', 'leaderboard', 'help_me',
    'test_eagle_view', 'rand'
]
last_command = ''
last_time_solved = time()

command_prefix = 'EMI?'
intents = discord.Intents.all()
client = commands.Bot(command_prefix=command_prefix, intents=intents)

# keeping the bot alive
app = Flask('')


@app.route('/')
def main():
    return "EMI#2467 is ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


# adding a background task
status = cycle(['with Subaru', 'with Puck', 'with Rem', 'with Ram'])


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_ready():
    keep_alive()
    change_status.start()
    print(f"{format(client.user)} is running")
    if not 'problems' in db:
        db['problems'] = {'ordered_list': list(), 'detailed_list': dict()}
    if not 'users' in db:
        db['users'] = {'ordered_list': list(), 'detailed_list': dict()}


@client.event
async def on_message(message):
    if message.author.bot:
        return

    global last_command, last_time_solved

    if message.content.startswith(command_prefix):
        command = message.content.split(' ')[0][4:]
        if command in bot_commands:
            if command == 'solved':
                if last_command == 'solved' and time() - last_time_solved < 30:
                    await message.channel.send(
                        'Quá nhanh và quá nguy hiểm :pikachu:')
                last_time_solved = time()
            last_command = command
            await client.process_commands(message)
        else:
            await message.channel.send('Lệnh này không tồn tại!')
        return

    if message.content.find('ngủ') != -1:
        await message.channel.send(f'Chúc {message.author} ngủ ngon!')
    elif message.content.find('bot') != -1 or message.content.find(
            'Bot') != -1 or message.content.find(
                'BOT') != -1 or message.content.find(
                    'emi') != -1 or message.content.find(
                        'Emi') != -1 or message.content.find('EMI') != -1:
        await message.channel.send(
            random.choice([
                'Bạn nhắc gì tui :(', 'Tui đã làm gì sai :(',
                'Tui đau đầu quá :(', 'Huhu tha cho tui'
            ]))
    if random.randrange(50) == 0:
        await message.channel.send('Vâng :)')


@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {client.latency * 1000}ms')


@client.command()
async def add_problem(ctx, *args):
    if len(args) != 2:
        await ctx.send('Dữ liệu không chính xác!')
        return
    (problem_id, problem_url) = args
    if problem_id in db['problems']['ordered_list']:
        await ctx.send(f'Đã tồn tại {problem_id} trong danh sách problems!')
        return
    db['problems']['ordered_list'].append(problem_id)
    db['problems']['detailed_list'][problem_id] = {
        'url': problem_url,
        'solved_by': list(),
        'total_ac': int(),
        'first_ac': '#'
    }
    db['table'].append(['#'] * len(db['users']['ordered_list']))
    await ctx.send('Đã thêm thành công!')


@client.command()
async def get_problem(ctx, *args):
    if len(args) != 1:
        await ctx.send('Dữ liệu không chính xác!')
        return
    problem_id = args[0]
    await ctx.send(db['problems']['detailed_list'][problem_id]['url'])


@client.command()
async def add_user(ctx, *args):
    if len(args) != 2:
        await ctx.send('Dữ liệu không chính xác!')
        return
    (user_id, user_name) = args
    if user_id in db['users']['ordered_list']:
        await ctx.send(f'Đã tồn tại {user_id} trong danh sách users!')
        return
    db['users']['ordered_list'].append(user_id)
    db['users']['detailed_list'][user_id] = {
        'name': user_name,
        'solved_of': list(),
        'solutions': dict(),
        'total_ac': int()
    }
    for i in db['table']:
        i.append('#')
    await ctx.send('Đã thêm thành công!')


@client.command()
async def solved(ctx, *args):
    if len(args) != 3:
        await ctx.send('Dữ liệu không chính xác!')
        return
    (user_id, problem_id, pastebin) = args
    if not user_id in db['users']['ordered_list']:
        await ctx.send(f'Không tồn tại {user_id} trong danh sách users!')
        return
    user_index = db['users']['ordered_list'].index(user_id)
    if not problem_id in db['problems']['ordered_list']:
        await ctx.send(f'Không tồn tại {problem_id} trong danh sách problems!')
        return
    if problem_id in db['users']['detailed_list'][user_id]['solved_of']:
        await ctx.send('Thích phá không?')
        return
    problem_index = db['problems']['ordered_list'].index(problem_id)
    db['problems']['detailed_list'][problem_id]['solved_by'].append(user_id)
    db['problems']['detailed_list'][problem_id]['total_ac'] += 1
    if db['problems']['detailed_list'][problem_id]['first_ac'] == '#':
        db['problems']['detailed_list'][problem_id]['first_ac'] = user_id
    db['users']['detailed_list'][user_id]['solved_of'].append(problem_id)
    db['users']['detailed_list'][user_id]['solutions'][problem_id] = pastebin
    db['users']['detailed_list'][user_id]['total_ac'] += 1
    db['table'][problem_index][user_index] = 'AC'
    await ctx.send('Đã thêm thành công!')


@client.command()
async def solution(ctx, *args):
    if len(args) != 2:
        await ctx.send('Dữ liệu không chính xác!')
        return
    (problem_id, user_id) = args
    if not user_id in db['users']['ordered_list']:
        await ctx.send(f'Không tồn tại {user_id} trong danh sách users!')
        return
    if not problem_id in db['problems']['ordered_list']:
        await ctx.send(f'Không tồn tại {problem_id} trong danh sách problems!')
        return
    if not problem_id in db['users']['detailed_list'][user_id]['solved_of']:
        await ctx.send('Người ta chưa giải bài này :(')
        return
    await ctx.send(
        db['users']['detailed_list'][user_id]['solutions'][problem_id])


@client.command()
async def solved_of(ctx, *args):
    if len(args) != 1:
        await ctx.send('Dữ liệu không chính xác!')
        return
    problem_id = args[0]
    if not problem_id in db['problems']['ordered_list']:
        await ctx.send(f'Không tồn tại {problem_id} trong danh sách problems!')
        return
    await ctx.send(
        db['problems']['detailed_list'][problem_id]['solved_by'].value)


@client.command()
async def solved_by(ctx, *args):
    if len(args) != 1:
        await ctx.send('Dữ liệu không chính xác!')
        return
    user_id = args[0]
    if not user_id in db['users']['ordered_list']:
        await ctx.send(f'Không tồn tại {user_id} trong danh sách users!')
        return
    await ctx.send(db['users']['detailed_list'][user_id]['solved_of'].value)


@client.command()
async def eagle_view(ctx, start=-1, end=-1):
    if (start != -1):
        await param_view(ctx, start, end)
        return

    start_time = time()

    problems_count = len(db['problems']['ordered_list'])
    users_count = len(db['users']['ordered_list'])

    for ma in range(0, problems_count, 5):
        output = table2ascii(
            header=['ID'] + [user for user in db['users']['ordered_list']] +
            ['FIRST AC'],
            body=[(
                ['[' + str(i + 1) + '] ' + db['problems']['ordered_list'][i]] +
                db['table'][i].value + [
                    db['problems']['detailed_list'][
                        db['problems']['ordered_list'][i]]['first_ac']
                ]) for i in range(ma, min(ma + 5, problems_count))],
            footer=['TOTAL AC'] + [
                db['users']['detailed_list'][user]['total_ac']
                for user in db['users']['ordered_list']
            ] + ['#'],
            first_col_heading=True,
            last_col_heading=True,
            style=PresetStyle.ascii_compact,
            column_widths=[15] +
            [len(user) + 2 for user in db['users']['ordered_list']] + [10],
            alignments=[Alignment.LEFT] + [Alignment.CENTER] * users_count +
            [Alignment.LEFT])
        await ctx.send('```' + output + '```')

    await ctx.send('```Time elapsed: ' + str(time() - start_time) + '```')


@client.command()
async def test_eagle_view(ctx):
    await test.eagle_view(ctx)


@client.command()
async def param_view(ctx, start, end=-1):

    start_time = time()

    problems_count = len(db['problems']['ordered_list'])
    users_count = len(db['users']['ordered_list'])

    start -= 1

    if end == -1:
        end = min(start + 5, problems_count)

    if start > end or start < 0 or end > problems_count:
        await ctx.send('Ăn gì mà nhập ngáo vậy :/')
        return

    if end - start > 15:
        await ctx.send('Dữ liệu lớn quá gửi không nổi :(')
        return

    output = table2ascii(
        header=['ID'] + [user for user in db['users']['ordered_list']] +
        ['FIRST AC'],
        body=[(['[' + str(i + 1) + '] ' + db['problems']['ordered_list'][i]] +
               db['table'][i].value + [
                   db['problems']['detailed_list'][
                       db['problems']['ordered_list'][i]]['first_ac']
               ]) for i in range(start, end)],
        footer=['TOTAL AC'] + [
            db['users']['detailed_list'][user]['total_ac']
            for user in db['users']['ordered_list']
        ] + ['#'],
        first_col_heading=True,
        last_col_heading=True,
        style=PresetStyle.ascii_compact,
        column_widths=[15] +
        [len(user) + 2 for user in db['users']['ordered_list']] + [10],
        alignments=[Alignment.LEFT] + [Alignment.CENTER] * users_count +
        [Alignment.LEFT])
    await ctx.send('```' + output + '```')
    await ctx.send('```Time elapsed: ' + str(time() - start_time) + '```')


@client.command()
async def leaderboard(ctx):
    users_count = len(db['users']['ordered_list'])

    table = [[''] * 5 for i in range(users_count)]

    for i in range(users_count):
        user = db['users']['ordered_list'][i]
        table[i] = [
            db['users']['detailed_list'][user]['total_ac'], user,
            db['users']['detailed_list'][user]['name'], 0,
            str(db['users']['detailed_list'][user]['solved_of'][-1])
            if len(db['users']['detailed_list'][user]['solved_of']) else '#'
        ]

    table.sort(reverse=True)

    for i in range(users_count):
        table[i][3] = table[i][0]
        table[i][0] = i + 1

    output = table2ascii(header=['#', 'ID', 'NAME', 'TOTAL AC', 'LAST AC'],
                         body=table,
                         first_col_heading=True,
                         style=PresetStyle.ascii_compact,
                         alignments=[Alignment.LEFT] + [Alignment.CENTER] * 4)

    await ctx.send('```' + output + '```')

@client.command()
async def rand(ctx, start=-1, end=-1):
    start -= 1
    problems_count = len(db['problems']['ordered_list'])
    if start > end or start < 0 or end > problems_count:
        await ctx.send('Ăn gì mà nhập ngáo vậy :/')
        return
    await ctx.send(random.choice(db['problems']['ordered_list'][start - 1 : end]))

@client.command()
async def help_me(ctx):
    output = table2ascii(
        body=[['ping', 'pong!'], ['leaderboard', 'là leaderboard'],
              ['eagle_view', 'là tầm nhìn của đại bàng'],
              ['add_problem $problem_id $problem_url', 'thêm problem'],
              ['get_problem $problem_id', 'lấy url của problem'],
              ['add_user $user_id $user_name', 'thêm user'],
              ['solved $user_id $problem_id $pastebin', 'thêm bài AC'],
              ['solution $problem_id $user_id', 'lấy solution'],
              ['solved_of $problem_id', 'danh sách người đã giải của một bài'],
              ['solved_by $user_id', 'danh sách bài đã giải của một người']],
        style=PresetStyle.ascii_borderless,
        alignments=[Alignment.LEFT] * 2)
    await ctx.send('```' + output + '```')


client.run(os.environ['TOKEN'])
