import mysql.connector

title_max_length = 100
subtitle_max_length = 350
text_max_lendth = 8_388_608; # because max len for mediumtext - 16MB, that 8 388 608 chars in utf-8


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
);'''
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

connection_config = get_connection_config_dictionary()

connection = mysql.connector.connect(host=connection_config['host'], user=connection_config['user'], 
                                     password=connection_config['password'], database=connection_config['database'])
cursor = connection.cursor()

connection.autocommit = True

# logging. simplify debug
log = print

# if db was not created, create
cursor.execute(db_creation_line)


def is_article_valid(title: str, subtitle: str, article: str):
    is_valid = len(title) <= title_max_length and len(subtitle) <= subtitle_max_length and len(article) <= text_max_lendth
    
    return is_valid


# function to add new article
def add_new_article(title: str, subtitle: str, article: str):
    if not is_article_valid(title, subtitle, article):
        raise Exception('invalid article')

    sql_action = add_article_line.replace('@title', title).replace('@subtitle', subtitle).replace('@article', article);

    cursor.execute(sql_action);

    log(f'added article with title: {title}')
    

# function to find by substring in title
# if found nothing, return None
def find_by_substring_in_title(substring: str):
    log(f'requested by substring: {substring}')    

    sql_action = find_by_substring_in_title_line.replace('@substring', substring)
    cursor.execute(sql_action)
    
    finded_articles = cursor.fetchall()
    
    if len(finded_articles) == 0:
        return None
    else:
        return finded_articles
    

# find by id
def find_by_id(id: str):
    id = str(id) # for safety    

    log(f'requested by id: {id}')    

    sql_action = find_by_id_line.replace('@id', id)
    cursor.execute(sql_action)

    finded_article = cursor.fetchall()

    if len(finded_article) != 1:
        return None
    else:
        return finded_article

# to kill connection
def dispose():
    connection.close()
    cursor.close()