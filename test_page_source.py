from bs4 import BeautifulSoup

result = []

with open('page_source.html', encoding='utf8') as f:
    content = f.read()

    soup = BeautifulSoup(content, 'html5lib')
    print(soup.title)

    el_card = soup.find_all(class_='card')

    for el_card_item in el_card:
        el_card_a = el_card_item.find(class_='card-body')

        href= el_card_a.a.get('href')
        text = el_card_a.a.text
        item = {
            'href': href,
            'text': text
        }

        result.append(item)

print(result)