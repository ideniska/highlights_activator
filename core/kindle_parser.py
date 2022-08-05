import random

user_email = "user3@gmail.com"

# --- KINDLE NOTES FILE PARSER --- #
notes_line_list = []
notes_list = []
notes_dict = {}

# TODO change file name to user uploaded file
with open('/Users/denissakhno/Documents/GitHub/Denis-codes-stuff/100daysofcode/web dev/Highlights Activator website and app/app_folder/uploads/4', 'r', encoding='utf-8') as kindle_file:
    for line in kindle_file:
        if len(line) > 1:
            notes_line_list.append(line)

# with open('/Users/denissakhno/Downloads/kindle_notes.txt', 'w') as notes_file:
#     notes_file.write('\n'.join(notes_line_list))

brake_index_list = []
for index in range(0, len(notes_line_list)):
    if notes_line_list[index] == '==========\n':
        brake_index = index
        brake_index_list.append(brake_index)

def find_2nd(string, substring): # I use this func to find second appearance of '|' symbol to slice date added string
   return string.find(substring, string.find(substring) + 1)

for i in range(len(brake_index_list)-1):
    first_br_point = brake_index_list[i] # I use this to find range between ===== which is a note contents
    second_br_point = brake_index_list[i+1]
    notes_sublist = []
    for index in range(first_br_point, second_br_point):
        notes_sublist.append(notes_line_list[index])
    notes_list.append(notes_sublist)


for sublist in notes_list:
    try:
        book_title = sublist[1].strip('\ufeff')
        if sublist[2].count('|') == 1:
            start_slice = sublist[2].find('|') + 2
            stop_slice = None
        else:
            start_slice = find_2nd(sublist[2], '|') + 2
            stop_slice = None
        date_added = sublist[2][start_slice: stop_slice]
        quote = sublist[3].strip('\xa0')
        if book_title.strip() in notes_dict:
            notes_dict[f'{book_title.strip()}'][f'{date_added.strip()}'] = quote.strip()
        else:
            notes_dict[f'{book_title.strip()}'] = {}
            notes_dict[f'{book_title.strip()}'][f'{date_added.strip()}'] = quote.strip()
    except IndexError:
        continue

# print(notes_dict['Разбуди в себе исполина (Энтони Роббинс)'])
# print(random.choice(list(notes_dict.items())))

random_book = random.choice(list(notes_dict))
random_quote = random.choice(list(notes_dict[random_book].items()))[1]
#print(list(notes_dict))
#print(notes_dict)
#print(random_book)
#print(random_quote)

# search_for_fav_book = True
# while search_for_fav_book:
#     random_book = random.choice(list(notes_dict))
#     if notes_dict[random_book]['favorite_book'] == 'yes':
#         search_for_fav_book = False

