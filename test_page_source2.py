from bs4 import BeautifulSoup

result = []

with open('page_source2.html', encoding='utf8') as f:
    content = f.read()

    soup = BeautifulSoup(content, 'html5lib')
    print(soup.title)

    el_holder = soup.find_all(class_='imgHolder')

    for e_holder in el_holder:
        href = e_holder.a.get('href')

        result.append(href)

print(result)