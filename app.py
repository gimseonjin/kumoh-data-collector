import time
import schedule
from src.robot import Robot
from src.tool.json_file_manager import JsonFileManager
from src.tool.selenium_context_manager import SeleniumContextManager
from src.tool.mongodb_context_manager import MongodbContextManager


TARGETS = JsonFileManager.read_data_from_local("resoure/targets.json")
SAVED_URLS = JsonFileManager.read_data_from_local("resoure/saved_urls.json")
DEFAULT_OFFSET = 1


def main() -> None:

    with SeleniumContextManager() as driver: # type: ignore
        robot = Robot(driver)

        for i, target in enumerate(TARGETS):
            base_url = target[0]
            saved_count = target[1]
            total_board_number = robot.get_total_board_numbers(base_url)

            if saved_count == total_board_number:
                print(f"INFO : {base_url} Not Updated")
                continue
            
            TARGETS[i][1] = total_board_number
            JsonFileManager.save_data_in_local("resoure/targets.json", TARGETS)
            print(f"INFO : Start Getting Board URLS")
            board_url_list = robot.get_all_board_url(base_url, SAVED_URLS, DEFAULT_OFFSET)

            if board_url_list:

                print(f"INFO : Find Unsaved Boards!!")
                board_list = robot.get_boards_from_url(board_url_list)
                
                with MongodbContextManager() as driver: # type: ignore
                    
                    driver.saved_url.insert_many(board_list)

                JsonFileManager.save_data_in_local("resoure/saved_urls.json", SAVED_URLS)


if __name__ == "__main__":

    print(f"INFO : System Start!!")
    schedule.every(5).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
