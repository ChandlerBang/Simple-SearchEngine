from lxml import html
import os
import requests
from bs4 import BeautifulSoup

seed_url = u"http://shakespeare.mit.edu/"
file_folder = 'The Complete Works of William Shakespeare/'

<<<<<<< HEAD
# this part of code is beyond the range of this course
=======
# this part of code is beyond the range of our class
>>>>>>> 3f83adafd4226c76c362e47a5e7617686c847ae7
# and the process of crawling the webpage is really boring and time-consuming
# so I do not have much to comment
# if you are interest in this, welcome to contact me after the project closed.
def main():
    x = html.parse(seed_url)
    categories = x.xpath('//tr/td/h2/text()')
    for i in range(1, 5):
        if (i < 4):
            book_names= x.xpath('//table[@align="center"]/tr[2]/td[{0}]/a'.format(i))
            for book in book_names:
                href1 = book.xpath('attribute::href')[0]  # Now get the link for this book Act&Scene
                Go_to_ScenePage(seed_url + href1, categories[i-1], book.text)  # categories[i-1] means the correspoding Comedy/Tragedy/...
        else:
            book_names= x.xpath('//table[@align="center"]/tr[2]/td/em/a')
            for book in book_names:
                href1 = book.xpath('attribute::href')[0]  # 现在得到了这本书对应的Act&Scene链接
                GetPoetry(seed_url + href1, categories[3].replace('\n', ''), book.text.replace('\n', ''))

# go to new link page
def Go_to_ScenePage(href1, category, book):
    href2 = html.parse(href1)
    # Find Act&Scene corresponding name and links
    scenes_numbers = href2.xpath('/html/body/p[starts-with(text(),"\nAct")]/text()')
    scenes_names = href2.xpath('/html/body/p[starts-with(text(),"\nAct")]/a')
    scenes_numbers = [x for x in scenes_numbers if len(x)>1]  # Remove line breaks ['\n'][' ']
    for number, name in zip(scenes_numbers, scenes_names):
        number = number.replace(":", " ")[1:]     # remove ['\nAct1 Scene:'] \n
        content_href = href1[:-10] + name.xpath("attribute::href")[0]  #  new links
        name = name.text.replace(":", " ")
        Go_to_ContentPage(content_href, category.replace('\n', ''), book.replace('\n', ''), number+name)

# go to new link page
def GetPoetry(href, category, book):
    href1 = html.parse(href)
    path = file_folder + category + r'/' + book + r'/'
    if not os.path.exists(path):
        os.makedirs(path)

    if book == 'The Sonnets':
        names = href1.xpath('//a[contains(@href,"sonnet")]')
        for name in names:
            content_href = 'http://shakespeare.mit.edu/Poetry/'+ name.xpath("attribute::href")[0]
            name = name.text.replace('?','').replace(':', '')
            filename = path + name + '.txt'
            content_href = html.parse(content_href)
            main_text = content_href.xpath('/html/body/blockquote/text()')
            f = open(filename, 'w')
            f.write(content_href.xpath('/html/body/h1/text()')[0] +'\n')
            for text in main_text:
                f.write(text + '\n')
            f.close()

    else:
        filename = path + book + '.txt'
        r = requests.get(href, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html.parser")
        f = open(filename, 'w')
        f.write(soup.get_text())
        f.close()

def Go_to_ContentPage(content_href, category, book, name):
    # go to new link
    content_href = html.parse(content_href)

    path = file_folder + category + r'/' + book + r'/'
    if not os.path.exists(path):
        os.makedirs(path)
    filename = path + name + '.txt'
    if os.path.exists(filename):   # If the file already exists, it is no longer written
        return

    # Write txt file
    title = content_href.xpath('/html/body/h3/text()')[0]  # 文章标题
    abstracts = content_href.xpath('/html/body/blockquote/i/text()')  # Article Summary, May be more than one line

    # Write txt file
    f = open( filename, 'w')
    f.write(title + '\n')
    for abstract in abstracts:
        f.write(abstract +'\n')
    subtitles = content_href.xpath('/html/body/a/b/text()')  # Article subtitle
    print(name)
    for i in range(len(subtitles)):
        part_text = content_href.xpath('/html/body/blockquote[{0}]/a/text()'.format(i + 2))  # The text starts with blockquote[2]
        f.write(subtitles[i] + '\n')
        for text in part_text:
            f.write(text + '\n')
    f.close()


if __name__ == '__main__':
    main()





