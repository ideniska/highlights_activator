import os
from .models.py import Book, Quote


def test_kindle_parser():

    # --- KINDLE NOTES FILE PARSER --- #
    notes_line_list = []
    notes_list = []
    notes_dict = {}

    # TODO implement file extension check - if it is TXT then start parser if it is not - show alert "wrong file"

    with open(
        "media/user_uploads/kindle_notes_denis_2OoBhW5.txt", "r", encoding="utf-8"
    ) as kindle_file:
        for line in kindle_file:
            if len(line) > 1:
                notes_line_list.append(line)

    # with open('/Users/denissakhno/Downloads/kindle_notes.txt', 'w') as notes_file:
    #     notes_file.write('\n'.join(notes_line_list))

    brake_index_list = []
    for index in range(0, len(notes_line_list)):
        if notes_line_list[index] == "==========\n":
            brake_index = index
            brake_index_list.append(brake_index)

    def find_2nd(
        string, substring
    ):  # I use this func to find second appearance of '|' symbol to slice date added string
        return string.find(substring, string.find(substring) + 1)

    for i in range(len(brake_index_list) - 1):
        first_br_point = brake_index_list[
            i
        ]  # I use this to find range between ===== which is a note contents
        second_br_point = brake_index_list[i + 1]
        notes_sublist = []
        for index in range(first_br_point, second_br_point):
            notes_sublist.append(notes_line_list[index])
        notes_list.append(notes_sublist)

    for sublist in notes_list:
        try:
            book_title = sublist[1].strip("\ufeff")
            if sublist[2].count("|") == 1:
                start_slice = sublist[2].find("|") + 2
                stop_slice = None
            else:
                start_slice = find_2nd(sublist[2], "|") + 2
                stop_slice = None
            date_added = sublist[2][start_slice:stop_slice]
            quote = sublist[3].strip("\xa0")
            if book_title.strip() in notes_dict:
                notes_dict[f"{book_title.strip()}"][
                    f"{date_added.strip()}"
                ] = quote.strip()
            else:
                notes_dict[f"{book_title.strip()}"] = {}
                notes_dict[f"{book_title.strip()}"][
                    f"{date_added.strip()}"
                ] = quote.strip()
        except IndexError:
            continue

    # print(notes_dict['Разбуди в себе исполина (Энтони Роббинс)'])
    # print(random.choice(list(notes_dict.items())))

    # random_book = random.choice(list(notes_dict))
    # random_quote = random.choice(list(notes_dict[random_book].items()))[1]

    ## --- ADD PARSED TXT TO DATABASE --- ##
    for book in notes_dict:
        new_book_entry = Book.create(book_title_db=book)
        for date_added, note in notes_dict[book].items():
            new_quote_entry = Quote.create(
                date_added_db=date_added, quote_db=note, from_book=book
            )
            new_quote_entry.save()
        new_book_entry.save()


test_kindle_parser()
