from selenium.webdriver.common.by import By
from tqdm import tqdm

from src.tool.selenium_context_manager import SeleniumContextManager
from src.tool.json_file_manager import JsonFileManager


class Robot():

    def __init__(self, driver) -> None:
        self.driver = driver


    def get_total_board_numbers(self, base_url:str):

        self.driver.get(f"{base_url}")
        self.driver.implicitly_wait(5)
        total_board_number = int(self.driver.find_element(By.XPATH, '//*[@id="jwxe_main_content"]/div[2]/div[2]/form[1]/fieldset/div/p/strong').text)

        return total_board_number

    
    def get_all_board_url(self, base_url:str, saved_urls:dict, article_max_offset:int):

        board_url_list = []

        for i in tqdm(range(0, article_max_offset+1, 100)):
            self.driver.get(f"{base_url}?mode=list&&articleLimit=100&article.offset={i}")
            self.driver.implicitly_wait(5)
            a_list = self.driver.find_elements(By.XPATH, '/html/body/div[1]/section/div/div[2]/article/div/div[2]/div[2]/div[1]/table/tbody/tr/td/a')
            for a in a_list:
                url = a.get_attribute("href")
                article_number = self.get_article_number(url)
                if not article_number in saved_urls:
                    board_url_list.append(url)
                    saved_urls[article_number] = True
        
        return board_url_list


    def get_boards_from_url(self, urls:str):

        board_list = []

        for url in tqdm(urls):

            self.driver.get(url)
            self.driver.implicitly_wait(5)

            try:
                title = self.driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/article/div/div[2]/div[2]/div[1]/div/div[1]/h4')
                date = self.driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/article/div/div[2]/div[2]/div[1]/div/div[2]/dl[3]/dd')
                writer = self.driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/article/div/div[2]/div[2]/div[1]/div/div[2]/dl[1]/dd')
                content = self.driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/article/div/div[2]/div[2]/div[1]/div/div[3]')

                board = {
                    "title" : title.text,
                    "date" : date.text,
                    "writer" : writer.text,
                    "content" : content.text,
                    "url" : url
                }

                board_list.append(board)

            except:
                print(f"LOCKED BOARD : {url}")
            
        
        return board_list


    def get_article_number(self, url:str):

        split_url = url.split("&")

        article_number = split_url[1].split("=")[1]

        return article_number