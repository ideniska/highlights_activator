from .models import Book, Quote


def start_kindle_parser(file_path, user_id):

    # --- KINDLE NOTES FILE PARSER --- #
    notes_line_list = []
    notes_list = []
    notes_dict = {}

    with open(file_path, "r", encoding="utf-8") as kindle_file:
        for line in kindle_file:
            if len(line) > 1:
                notes_line_list.append(line)

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

    print("notes_list", notes_list)
    print("--------------------------------")
    print("--------------------------------")
    print(
        "notes_sublist ",
        notes_sublist,
    )
    print("--------------------------------")
    print("--------------------------------")

    for sublist in notes_list:
        try:
            book_title = sublist[1].split("(")[0].strip("\ufeff")
            # print("book_title ", sublist[1])
            author = sublist[1].split("(")[1].strip()[:-1]
            if "," in author:
                author = author.replace(",", "")
            # print("author ", author)
            if sublist[2].count("|") == 1:
                start_slice = sublist[2].find("|") + 2
                stop_slice = None
            else:
                start_slice = find_2nd(sublist[2], "|") + 2
                stop_slice = None
            date_added = sublist[2][start_slice:stop_slice]
            quote = sublist[3].strip("\xa0")
            # if book_title.strip() in notes_dict:
            #     notes_dict[f"{book_title.strip()}"][
            #         f"{date_added.strip()}"
            #     ] = quote.strip()
            # else:
            #     notes_dict[f"{book_title.strip()}"] = {}
            #     notes_dict[f"{book_title.strip()}"][
            #         f"{date_added.strip()}"
            #     ] = quote.strip()
            if author in notes_dict:
                if book_title.strip() in notes_dict[author]:
                    notes_dict[author][book_title.strip()][
                        date_added.strip()
                    ] = quote.strip()
                else:
                    pass
            else:
                notes_dict[author] = {}
                print(f"{notes_dict=}")
                notes_dict[author][book_title.strip()] = {}
                # print(f"{notes_dict[author][book_title.strip()]=}")
                print(f"{notes_dict=}")
                notes_dict[author][book_title.strip()][
                    date_added.strip()
                ] = quote.strip()
                print(f"{notes_dict=}")
        except IndexError:
            continue

    # print(notes_dict)
    # print("notes_dict ", {k: notes_dict[k] for k in list(notes_dict)[:2]})

    # --- ADD PARSED TXT TO DATABASE --- ##
    # for author in notes_dict:
    #     for book in author:
    #         new_book_entry = Book(title=book, author=author, owner=user_id)
    #         new_book_entry.save()
    #         # TODO GOOGLE bulk create
    #         # TODO GOOGLE db transaction
    #         for date_added, note in notes_dict[book].items():
    #             print("date_added ", date_added)
    #             print("note ", note)
    #             new_quote_entry = Quote(
    #                 date_added=date_added,
    #                 text=note,
    #                 book=new_book_entry,
    #                 owner=user_id,
    #             )
    #             new_quote_entry.save()

    new_book_entry_list = []
    new_quote_entry_list = []

    for author in notes_dict:
        # print(f"{author=}")
        for book in notes_dict[author]:
            # print(f"{book=}")
            book_obj = Book(title=book, author=author, owner=user_id)
            new_book_entry_list.append(book_obj)
            for date_added, note in notes_dict[author][book].items():
                # print("notes_dict[author][book] ", notes_dict[author][book])
                # print("date_added, note ", date_added, note)
                new_quote_entry_list.append(
                    Quote(
                        date_added=date_added,
                        text=note,
                        book=book_obj,
                        owner=user_id,
                    )
                )

    Book.objects.bulk_create(new_book_entry_list)
    Quote.objects.bulk_create(new_quote_entry_list)
