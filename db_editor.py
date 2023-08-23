from replit import db, database


def print_db(data, tab, end='\n'):
    if (type(data) != database.database.ObservedDict):
        if (type(data) == database.database.ObservedList):
            print(str(data.value).replace("'", '"'), end=end)
        elif (type(data) == str):
            print('"' + str(data) + '"', end=end)
        else:
            print(str(data), end=end)
        return
    print('{')
    data_len = len(data.keys())
    for index, key in enumerate(data.keys()):
        print('\t' * tab + '"' + str(key) + '": ', end='')
        print_db(data[key], tab + 1,
                 ('\n' if index == data_len - 1 else ',\n'))
    print('\t' * tab + '}', end=end)


def print_replit_db():
    print('{')
    db_len = len(db.keys())
    for index, key in enumerate(db.keys()):
        print('\t"' + str(key) + '": ', end='')
        print_db(db[key], 1, ('\n' if index == db_len - 1 else ',\n'))
    print('}')


# for problem in db['problems']['detailed_list']:
#     db['problems']['detailed_list'][problem]['total_ac'] = len(db['problems']['detailed_list'][problem]['solved_by'])

# for user in db['users']['detailed_list']:
#     db['users']['detailed_list'][user]['total_ac'] = len(
#         db['users']['detailed_list'][user]['solved_of'])

# for problem in db['problems']['detailed_list']:
#     db['problems']['detailed_list'][problem]['first_ac'] = (
#             db['problems']['detailed_list'][problem]['solved_by'][0]
#             if db['problems']['detailed_list'][problem]['total_ac'] else '#')

# db['table'] = [['#'] * 5 for i in range(23)]

# for i in range(23):
#     problem = db['problems']['ordered_list'][i]
#     for j in range(5):
#         user = db['users']['ordered_list'][j]
#         db['table'][i][j] = ('AC' if problem in db['users']['detailed_list'][user]['solved_of'] else '#')

# for i in db['table']:
#     del i[-1]

# for problem in db['users']['detailed_list']['oáH']['solutions']:
#     db['users']['detailed_list']['oáH']['solved_of'].append(problem)

# db['users']['detailed_list']['oáH']['total_ac'] += 8

# for i in range(10):
#     del db['users']['detailed_list']['Tienes']['solved_of'][-1]

# db['users']['detailed_list']['Tienes']['total_ac'] -= 10

# del db['problems']['detailed_list']['QBMAX']['solved_by'][-1]
# db['problems']['detailed_list']['QBMAX']['total_ac'] -= 1

# for i in range(10):
#     del db['problems']['detailed_list']['QBSTR']['solved_by'][-1]

# for i in range(7):
#     del db['problems']['detailed_list']['QBSTR']['solved_by'][-2]

# db['problems']['detailed_list']['QBSTR']['total_ac'] -= 17

for problem in db['problems']['detailed_list']:
    if len(db['problems']['detailed_list'][problem]['solved_by']) != 0:
        db['problems']['detailed_list'][problem]['first_ac'] = db['problems']['detailed_list'][problem]['solved_by'][0]
    else:
        db['problems']['detailed_list'][problem]['first_ac'] = '#'
        

print_replit_db()

# db['users']['detailed_list']['Kiese']['solutions']['NKBAS'] = '#'
# db['users']['detailed_list']['Kiese']['solutions']['VMMTFIVE'] = '#'
# db['users']['detailed_list']['Kiese']['solutions']['BLOPER'] = '#'
