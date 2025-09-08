import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from urllib.parse import urljoin, urlparse
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    """
    通用网页爬虫类
    """
    
    def __init__(self, url, delay=1,):
        """
        初始化爬虫
        
        Args:
            headers (dict): HTTP请求头
            delay (float): 请求间隔时间（秒）
        """
        self.session = requests.Session()
        self.delay = delay
        self.url = url
        # 设置默认请求头
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
        }
        res = requests.get(self.url,headers=default_headers)
        res = requests.get(self.url,headers=default_headers)
        self.cookiestr = ''
        for key, value in res.cookies.get_dict().items():
            self.cookiestr += key + '=' + value + ';'
        
        default_headers['cookie'] = self.cookiestr
        default_headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.session.headers.update(default_headers)
    
    
    def get_page(self):
        """
        获取网页内容
        
        Args:
            url (str): 网页URL
            
        Returns:
            requests.Response: 响应对象
        """
        try:
            logger.info(f"正在获取页面: {self.url}")
            response = self.session.get(self.url)
            response.raise_for_status()  # 检查请求是否成功
            time.sleep(self.delay)  # 延迟避免过于频繁的请求
            return response
        except requests.RequestException as e:
            logger.error(f"获取页面失败 {self.url}: {e}")
            return None
    
    def form_html(self,form_data,url=None):
        if url:
            response = self.session.post(url,data=form_data)
        else:
            response = self.session.post(self.url,data=form_data)
        return response.text

    
    def parse_html(self, html_content):
        """
        解析HTML内容
        
        Args:
            html_content (str): HTML内容
            
        Returns:
            BeautifulSoup: 解析后的BeautifulSoup对象
        """
        return BeautifulSoup(html_content, 'html.parser')
    
    def extract_text(self, soup, selector=None):
        """
        提取文本内容
        
        Args:
            soup (BeautifulSoup): BeautifulSoup对象
            selector (str): CSS选择器
            
        Returns:
            list: 提取的文本内容列表
        """
        if selector:
            elements = soup.select(selector)
            return [elem.get_text(strip=True) for elem in elements]
        else:
            return [soup.get_text(strip=True)]
    
    def extract_links(self, soup, base_url=None):
        """
        提取所有链接
        
        Args:
            soup (BeautifulSoup): BeautifulSoup对象
            base_url (str): 基础URL，用于补全相对链接
            
        Returns:
            list: 链接列表
        """
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if base_url:
                href = urljoin(base_url, href)
            links.append({
                'text': link.get_text(strip=True),
                'url': href
            })
        return links
    
    def extract_images(self, soup, base_url=None):
        """
        提取所有图片链接
        
        Args:
            soup (BeautifulSoup): BeautifulSoup对象
            base_url (str): 基础URL，用于补全相对链接
            
        Returns:
            list: 图片链接列表
        """
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            if base_url:
                src = urljoin(base_url, src)
            images.append({
                'alt': img.get('alt', ''),
                'src': src
            })
        return images
    
    def scrape_page(self, url, extract_links=True, extract_images=True, text_selector=None):
        """
        爬取单个页面信息
        
        Args:
            url (str): 页面URL
            extract_links (bool): 是否提取链接
            extract_images (bool): 是否提取图片
            text_selector (str): 文本提取的CSS选择器
            
        Returns:
            dict: 页面信息
        """
        response = self.get_page(url)
        if not response:
            return None
            
        soup = self.parse_html(response.text)
        
        result = {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'text': self.extract_text(soup, text_selector)
        }
        
        if extract_links:
            result['links'] = self.extract_links(soup, url)
            
        if extract_images:
            result['images'] = self.extract_images(soup, url)
            
        return result
    
    def save_to_json(self, data, filename):
        """
        保存数据到JSON文件
        
        Args:
            data (dict/list): 要保存的数据
            filename (str): 文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"数据已保存到 {filename}")
    
    def save_to_csv(self, data, filename, fieldnames=None):
        """
        保存数据到CSV文件
        
        Args:
            data (list): 要保存的数据列表
            filename (str): 文件名
            fieldnames (list): 字段名列表
        """
        if not data:
            logger.warning("没有数据可保存")
            return
            
        if isinstance(data, dict):
            data = [data]
            
        if not fieldnames:
            fieldnames = data[0].keys()
            
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"数据已保存到 {filename}")

# 使用示例
if __name__ == "__main__":
    # 创建爬虫实例
    scraper = WebScraper()
    
    # 示例：爬取一个页面
    # url = "https://example.com"
    # result = scraper.scrape_page(url)
    # 
    # if result:
    #     print(f"标题: {result['title']}")
    #     print(f"文本内容: {result['text'][:100]}...")
    #     scraper.save_to_json(result, "page_data.json")