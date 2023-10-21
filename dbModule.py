from calendar import c
from re import T
import mysql.connector

title_max_length = 100
subtitle_max_length = 350
text_max_lendth = 8_388_608; # because max len for mediumtext - 16MB, that 8 388 608 chars in utf-8
picture_name_max_length = 50
picture_type_max_length = 15


# function to get connection config
def get_connection_config_dictionary():
    try:
        with open('connection config.txt') as f:
            data = f.readlines()
        
        connection_config = {}
        
        for cl in data:                             # cl is connection line
            line = cl.replace('\n', '').split(':')
            connection_config[line[0]] = line[1]
        
    except:
        print('\'connection config.txt\' not found or corrupted.\nPlease, input requasted information to connect database:')
        
        connection_config = {}
        
        connection_config['host'] = input('host:\t')
        connection_config['user'] = input('user:\t')
        connection_config['password'] = input('password:\t')
        connection_config['database'] = input('database:\t')
            
        with open('connection config.txt', 'w') as f:
            for key in connection_config:
                f.write(f'{key}:{connection_config[key]}\n')
    finally:
        return connection_config


db_creation_line = f'''CREATE TABLE IF NOT EXISTS articles (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR({title_max_length}) NOT NULL,
	subtitle VARCHAR({subtitle_max_length}) NOT NULL,
	date_of_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	article MEDIUMTEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pictures (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    picture BLOB NOT NULL,
    picture_name VARCHAR({picture_name_max_length}) UNIQUE NOT NULL,
    picture_type VARCHAR({picture_type_max_length}) NOT NULL
);
'''
add_article_line = '''
INSERT INTO articles(title, subtitle, article) 
VALUES ('@title', '@subtitle', '@article');
'''
find_by_substring_in_title_line = '''
SELECT * FROM articles WHERE title LIKE '%@substring%';
'''
find_by_id_line = '''
SELECT * FROM articles WHERE id=@id;
'''
delete_article_line = '''
DELETE FROM articles WHERE id='@id';
'''
add_picture_line = '''
INSERT INTO pictures(picture, picture_name, picture_type) VALUES (%s, \'@picture_name\', \'@type\');
'''
get_picture_by_name_line = '''
SELECT * FROM pictures WHERE picture_name='@name';
'''
delete_picture_line = '''
DELETE FROM pictures WHERE picture_name='@name';
'''


connection_config = get_connection_config_dictionary()

# to get
def get_connection():
    return mysql.connector.connect(host=connection_config['host'], user=connection_config['user'], 
                                     password=connection_config['password'], database=connection_config['database'])
def get_connection_and_cursor():
    connection = get_connection()
    cursor = connection.cursor()
    connection.autocommit = True
    
    return (connection, cursor)
# to kill connection
def dispose(connection, cursor):
    connection.close()
    cursor.close()

connection = get_connection()
cursor = connection.cursor()

connection.autocommit = True

# logging. simplify debug
log = print

# if db was not created, create
cursor.execute(db_creation_line)

dispose(connection, cursor)


def is_article_valid(title: str, subtitle: str, article: str):
    is_valid = len(title) <= title_max_length and len(subtitle) <= subtitle_max_length and len(article) <= text_max_lendth
    
    return is_valid
def is_picture_valid(name: str, picture_type: str):
    acceptable_types = ['image/png', 'image/bmp', 'image/gif', 'image/jpeg']
    
    is_valid = picture_type in acceptable_types and len(name) < picture_name_max_length
    
    return is_valid


# function to add new article
def add_new_article(title: str, subtitle: str, article: str):
    if not is_article_valid(title, subtitle, article):
        raise Exception('invalid article')

    try:
        connection, cursor = get_connection_and_cursor()

        sql_action = add_article_line.replace('@title', title).replace('@subtitle', subtitle).replace('@article', article);

        cursor.execute(sql_action);

        log(f'added article with title: {title}')
    finally:
        dispose(connection, cursor)
    

# function to find by substring in title
# if found nothing, return None
def find_by_substring_in_title(substring: str):
    connection, cursor = get_connection_and_cursor()
    
    log(f'requested by substring: {substring}')    

    sql_action = find_by_substring_in_title_line.replace('@substring', substring)
    cursor.execute(sql_action)
    
    finded_articles = cursor.fetchall()
    
    dispose(connection, cursor)    

    if len(finded_articles) == 0:
        return None
    else:
        return finded_articles
    

# find by id
def find_by_id(id: str):
    id = str(id) # for safety    

    connection, cursor = get_connection_and_cursor()
    
    log(f'requested by id: {id}')    

    sql_action = find_by_id_line.replace('@id', id)
    cursor.execute(sql_action)

    finded_article = cursor.fetchall()
    
    dispose(connection, cursor)

    if len(finded_article) != 1:
        return None
    else:
        return finded_article

# delete article
def delete_article_from_db(id: str):
    id = str(id)    

    log(f'article with id={id} has been deleted')
    connection, cursor = get_connection_and_cursor()

    sql_action = delete_article_line.replace('@id', id)
    
    cursor.execute(sql_action)

    dispose(connection, cursor)


# add picture
# type can accept next values: image/png, image/bmp, image/gif, image/jpeg
def add_picture(picture: bytes, name: str, picture_type: str):
    if not is_picture_valid(name, picture_type):
        raise Exception('invalid picture')

    try:
        connection, cursor = get_connection_and_cursor()
        
        sql_action = add_picture_line.replace('@picture_name', name).replace('@type', picture_type) 

        cursor.execute(sql_action, (picture,))      # this is only transfer this way, because this is binary
        
        log(f'Added picture: {name}')
        
    finally:
        dispose(connection, cursor)

# find picture by name
def find_picture_by_name(name: str):
    log(f'picture {name} has been requested')    

    connection, cursor = get_connection_and_cursor()

    sql_action = get_picture_by_name_line.replace('@name', name)

    cursor.execute(sql_action)
    finded_picture = cursor.fetchall()
    
    dispose(connection, cursor)     
    
    if len(finded_picture) != 1:
        return None
    else:
        return finded_picture[0]        # to simplify work with it

# delete picture
def delete_picture_from_db(name: str):
    log(f'picture {name} has been deleted')
    
    connection, cursor = get_connection_and_cursor()
    
    sql_action = delete_picture_line.replace('@name', name)
    
    cursor.execute(sql_action)

    dispose(connection, cursor)

