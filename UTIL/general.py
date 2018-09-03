import os


# Each website é um projeto separado(pasta)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project' + directory)
        os.makedirs(directory)


def create_folders(directory):
    # diretorio sports
    directory_english_sports = directory + '/sports/english_texts'
    directory_pictures_sports = directory + '/sports/pictures'
    if not os.path.exists(directory_english_sports):
        print('Creating project' + directory_english_sports)
        os.makedirs(directory_english_sports)

    if not os.path.exists(directory_pictures_sports):
        print('Creating project' + directory_pictures_sports)
        os.makedirs(directory_pictures_sports)
    # diretorio brazil
    directory_english_brazil = directory + '/brazil/english_texts'
    directory_pictures_brazil = directory + '/brazil/pictures'
    if not os.path.exists(directory_english_brazil):
        print('Creating project' + directory_english_brazil)
        os.makedirs(directory_english_brazil)

    if not os.path.exists(directory_pictures_brazil):
        print('Creating project' + directory_pictures_brazil)
        os.makedirs(directory_pictures_brazil)
    # diretorio world
    directory_english_world = directory + '/world/english_texts'
    directory_pictures_world = directory + '/world/pictures'
    if not os.path.exists(directory_english_world):
        print('Creating project' + directory_english_world)
        os.makedirs(directory_english_world)

    if not os.path.exists(directory_pictures_world):
        print('Creating project' + directory_pictures_world)
        os.makedirs(directory_pictures_world)
    # diretorio business
    directory_english_business = directory + '/business/english_texts'
    directory_pictures_business = directory + '/business/pictures'
    if not os.path.exists(directory_english_business):
        print('Creating project' + directory_english_business)
        os.makedirs(directory_english_business)

    if not os.path.exists(directory_pictures_business):
        print('Creating project' + directory_pictures_business)
        os.makedirs(directory_pictures_business)
    # diretorio sao paulo
    directory_english_saopaulo = directory + '/saopaulo/english_texts'
    directory_pictures_saopaulo = directory + '/saopaulo/pictures'
    if not os.path.exists(directory_english_saopaulo):
        print('Creating project' + directory_english_saopaulo)
        os.makedirs(directory_english_saopaulo)

    if not os.path.exists(directory_pictures_saopaulo):
        print('Creating project' + directory_pictures_saopaulo)
        os.makedirs(directory_pictures_saopaulo)
    # diretorio sciente_health
    directory_english_health = directory + '/science_health/english_texts'
    directory_pictures_health = directory + '/science_health/pictures'
    if not os.path.exists(directory_english_health):
        print('Creating project' + directory_english_health)
        os.makedirs(directory_english_health)

    if not os.path.exists(directory_pictures_health):
        print('Creating project' + directory_pictures_health)
        os.makedirs(directory_pictures_health)
    # diretorio culture
    directory_english_culture = directory + '/culture/english_texts'
    directory_pictures_culture= directory + '/culture/pictures'
    if not os.path.exists(directory_english_culture):
        print('Creating project' + directory_english_culture)
        os.makedirs(directory_english_culture)

    if not os.path.exists(directory_pictures_culture):
        print('Creating project' + directory_pictures_culture)
        os.makedirs(directory_pictures_culture)
    # diretorio travel
    directory_english_travel = directory + '/travel/english_texts'
    directory_pictures_travel = directory + '/travel/pictures'
    if not os.path.exists(directory_english_travel):
        print('Creating project' + directory_english_travel)
        os.makedirs(directory_english_travel)

    if not os.path.exists(directory_pictures_travel):
        print('Creating project' + directory_pictures_travel)
        os.makedirs(directory_pictures_travel)
    # diretorio ombudsman
    directory_english_ombudsman = directory + '/ombudsman/english_texts'
    directory_pictures_ombudsman= directory + '/ombudsman/pictures'
    if not os.path.exists(directory_english_ombudsman):
        print('Creating project' + directory_english_ombudsman)
        os.makedirs(directory_english_ombudsman)

    if not os.path.exists(directory_pictures_ombudsman):
        print('Creating project' + directory_pictures_ombudsman)
        os.makedirs(directory_pictures_ombudsman)
    # diretorio 2016_olympic_Games
    directory_english_2016_olympicgames = directory + '/2016_olympicgames/english_texts'
    directory_pictures_2016_olympicgames = directory + '/2016_olympicgames/pictures'
    if not os.path.exists(directory_english_2016_olympicgames):
        print('Creating project' + directory_english_2016_olympicgames)
        os.makedirs(directory_english_2016_olympicgames)

    if not os.path.exists(directory_pictures_2016_olympicgames):
        print('Creating project' + directory_pictures_2016_olympicgames)
        os.makedirs(directory_pictures_2016_olympicgames)


# create queue and crawled files(if not created)

def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        if data is not None:
            data.encode('cp1252', errors='replace')
            file.write(data + '\n')


# Delete the contents of a file

def delete_file_contents(path):
    with open(path, 'w'):
        pass


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)