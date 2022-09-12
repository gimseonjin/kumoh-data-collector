import time
import schedule
from src.robot import Robot
from src.tool.json_file_manager import JsonFileManager
from src.tool.selenium_context_manager import SeleniumContextManager
from src.tool.mongodb_context_manager import MongodbContextManager


def main() -> None:

    base_urls = JsonFileManager.read_data_from_local("resoure/base_urls.json")
    saved_board_count = JsonFileManager.read_data_from_local("resoure/saved_board_count.json")
    saved_urls = JsonFileManager.read_data_from_local("resoure/saved_urls.json")

    with SeleniumContextManager() as driver: # type: ignore
        robot = Robot(driver)

        for target in zip(base_urls, saved_board_count):
            base_url = target[0]
            saved_count = target[1]
            total_board_number = robot.get_total_board_numbers(base_url)

            if saved_count == total_board_number:
                print(f"INFO : {base_url} Not Updated")
                continue

            print(f"INFO : Start Getting Offset")
            offset = 1
            print(f"BASE URL : {base_url} - {offset}")

            print(f"INFO : Start Getting Board URLS")
            board_url_list = robot.get_all_board_url(base_url, saved_urls, offset)

            if board_url_list:
                print(f"INFO : Find Unsaved Boards!!")
                board_list = robot.get_boards_from_url(board_url_list)
                
                with MongodbContextManager() as driver: # type: ignore
                    
                    driver.saved_url.insert_many(board_list)

                JsonFileManager.save_data_in_local("resoure/saved_urls.json", saved_urls)


if __name__ == "__main__":
    schedule.every(10).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
        