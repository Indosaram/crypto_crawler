import time

from tqdm import tqdm
from selenium_base import SeleniumBase
import pandas as pd

class FearGreedIndexScraper(SeleniumBase):
    def __init__(self):
        super().__init__()

        self.base_url = 'https://datavalue.dunamu.com/feargreedindex'

    def run(self):
        self.driver.get(self.base_url)
        time.sleep(3)

        last_page_xpath = '/html/body/div[2]/div/div[1]/div/div/div[4]/div/div[3]/span/a[6]'
        last_page_num = int(self.driver.find_element_by_xpath(last_page_xpath).text)

        next_button_xpath = '//*[@id="table-series_next"]'

        result = pd.DataFrame()

        for _ in tqdm(range(1, last_page_num)):
            result = pd.concat([result, self._run()], ignore_index=True)
            self.click(next_button_xpath)

        result.to_csv("result.csv")

    def _run(self):
        table_body_xpath = '//*[@id="table-series"]'

        table_body_element = self.driver.find_element_by_xpath(table_body_xpath)
        table_body_html = table_body_element.get_attribute('outerHTML')

        return pd.read_html(table_body_html)[0]
        

if __name__ == '__main__':
    scraper = FearGreedIndexScraper()

    scraper.run()
