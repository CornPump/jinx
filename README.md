# jinx
Scrapping Reddit , analyzing comments with LLM and other tools

Welcome to jinx project, here we have various tools to help us analyze
Reddit subs.
Please check requirements file and fix your Reddits credentials in the credentials
Package in order to use jinx project.

Requirements:
python 3.11.4, pip install requirements.txt


Example of plot created with jinx:
![tmp](https://github.com/CornPump/jinx/assets/143328149/130320ee-2a85-49ba-9a0d-9f63f3929ea7)



* submine is the module that scraps reddit sub, use it in order to scrap threads.
    Example of code that mines the last 10 daily thread from BitcoinMarkets sub:

    ins = submine.Submine(sub_name="BitcoinMarkets",post_name="daily",limit=10)
    ins.scrap_whole_sub(is_whole=False)

