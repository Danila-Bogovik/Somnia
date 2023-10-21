import qrcode
import io
import base64

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_data = io.BytesIO()
    img.save(img_data, format='PNG')
    img_data.seek(0)
    
    encoded_img_data = base64.b64encode(img_data.read()).decode('utf-8')
    html_code = f'<img src="data:image/png;base64,{encoded_img_data}" alt="QR Code">'
    return html_code

def replace_russian_with_english(text):
    english_text = ''
    russian_to_english = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
        'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya', " ": "-"
    }
    for char in text:
        if char.lower() in russian_to_english:
            if char.isupper():
                english_text += russian_to_english[char.lower()]
            else:
                english_text += russian_to_english[char]
        else:
            english_text += char
    return english_text

#пример QR
# url = "https://example.com"
# html = generate_qr_code(url)
# print(html)

#пример транслита
# russian_text = "Женя гей"
# english_text = replace_russian_with_english(russian_text)
# print(english_text)  # Выводит "zhenya-gey"