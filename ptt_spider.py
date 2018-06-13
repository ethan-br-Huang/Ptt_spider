import regex
import requests
import json
import base64
from PIL import Image
from io import BytesIO


def get_theme_url(prefix, start_page):
    condition_1 = regex.compile('<div class="title">\s+<a href="([^"]+)">', regex.I)
    while start_page > 0:
        urls = []
        url = '{}index{}.html'.format(prefix, start_page)
        headers = {'cookie': '__cfduid=d9fb114b4ad0673a1499e77f38a4aa47a1516688782; over18=1'}
        rdata = requests.get(url, headers=headers)
        url_list = condition_1.findall(rdata.text)
        for u in url_list:
            urls += ["https://www.ptt.cc{}".format(u)]
        start_page -= 1
        yield urls


def get_theme_info(urls):
    themes_info = []
    main_condition = regex.compile('<div id="main-container">([\d\D]*?)<span class="f2">', regex.I)
    image_condition = regex.compile('data-id=["\']([^"\']+)["\']', regex.I)

    for url in urls:
        try:
            headers = {'cookie': '__cfduid=d9fb114b4ad0673a1499e77f38a4aa47a1516688782; over18=1'}
            rdata = requests.get(url, headers=headers)
            main_content = main_condition.search(rdata.text).group(0)
            images = image_condition.findall(main_content)
            themes_info += images
        except Exception as e:
            continue

    return themes_info


def get_ptt_image_id(code, start_page):
    all_info = {}
    urls = get_theme_url("https://www.ptt.cc/bbs/{}/".format(code), start_page)
    for u in urls:
        tmp = get_theme_info(u)
        for t in tmp:
            all_info[t] = 0
        if len(all_info) >= 1000:
            break
    return list(all_info.keys())


def download_image(img_ids):
    for id in img_ids:
        url = f"https://i.imgur.com/{id}.jpg"
        content = requests.get(url).content
        yield content


def resize_image(content):
    im = Image.open(BytesIO(content)).convert('RGB')
    nim = im.resize((300, 300), Image.BILINEAR)
    buffered = BytesIO()
    nim.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


if __name__ == '__main__':
    img_ids = get_ptt_image_id('Beauty', 2509)  # Discussion code & start page

    for id, content in enumerate(download_image(img_ids)):
        bs64 = resize_image(content)
        with open("images/{}".format(img_ids[id]), mode="wb") as fp:
            fp.write(bs64)
