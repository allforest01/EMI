from replit import db
from table2ascii import table2ascii, PresetStyle, Alignment
from time import time


def eagle_view():
    problems_count = len(db['problems']['ordered_list'])
    users_count = len(db['users']['ordered_list'])

    prev_ma = 0
    for ma in range(0, problems_count, 10):
        output = table2ascii(
            header=['ID'] + [user for user in db['users']['ordered_list']] + ['FIRST AC'],
            body=[(['[' + str(i + 1) + '] ' + db['problems']['ordered_list'][i]] + db['table'][i].value + [db['problems']['detailed_list'][db['problems']['ordered_list'][i]]['first_ac']]) for i in range(prev_ma, min(ma + 10, problems_count))],
            footer=['TOTAL AC'] + [db['users']['detailed_list'][user]['total_ac'] for user in db['users']['ordered_list']] + ['#'],
            first_col_heading=True,
            last_col_heading=True,
            style=PresetStyle.ascii_compact,
            column_widths=[15] + [11] * users_count + [10],
            alignments=[Alignment.LEFT] + [Alignment.CENTER] * users_count + [Alignment.LEFT]
        )
        prev_ma = ma + 10
        print(output)


start = time()
eagle_view()
print('Time elapsed: ' + str(time() - start))
