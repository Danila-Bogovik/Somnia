import Utils
from Utils import replace_russian_with_english

# change it, if you if you changed the domain
link_prefix = 'https://webpractik-articles.ru/'

def create_link(title: str, day: int, mounth: int):
    link = title.lower()
    
    link = [replace_russian_with_english(c) for c in link]
    
    link = ''.join(link)
    
    if day <= 0 or day > 31 or mounth <= 0 or mounth > 12:
        raise Exception('Wrong data at creation link!')
    else:
        return f'{link_prefix}{link}-{mounth}-{day}';

    