import aiohttp
from bs4 import BeautifulSoup


async def get_news(rubric: str):
    url = f'https://lenta.ru/rubrics/{rubric}' if rubric else 'https://lenta.ru'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            news_tags = soup.find_all('a', class_='card-mini _longgrid')
            
            for news_tag in news_tags:
                news_url = 'https://lenta.ru' + news_tag['href']
                print(news_url)
            
                async with session.get(news_url) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    title = soup.find('span', class_='topic-body__title').text
                    
                    news_text = ''
                    data_tags = soup.find_all('p', class_='topic-body__content-text')
                    for tag in data_tags:
                        news_text += tag.text + '\n\n'
                    if len(news_text) + len(title) > 1000:
                        continue
                    
                    try:
                        img_page_url = 'https://lenta.ru' + soup.find('a', class_='topic-body__title-image-zoom')['href']
                    except:
                        continue
                    async with session.get(img_page_url) as response:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        img_url = soup.find('img', class_='comments-page__title-image')['src']
                        return title, news_text, img_url
