from pywander.crawler.utils import download

filename = './test.webp'
image_url = 'https://img.photos18.com/images/image/1963/19634365.webp?1656828830'
download(image_url, filename=filename)