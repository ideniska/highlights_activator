import os

def start_kindle_parser(file, user_name):

    save_path = 'uploads/'
    name_of_file = user_name
    completeName = os.path.join(save_path, name_of_file+".txt")  

   