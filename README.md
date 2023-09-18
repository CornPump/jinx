# jinx
Scrapping Reddit , analyzing comments with LLM and other tools

Welcome to jinx project, here we have various tools to help us analyze
Reddit subs.
Please check requirements file and fix your Reddits credentials in the credentials
Package in order to use jinx project.

Requirements:
python 3.8, pip install requirements.txt


Example of plot created with jinx:
![tmp](https://github.com/CornPump/jinx/assets/143328149/ca62a584-049e-41c3-8185-829dfd87838c)



* submine is the module that scraps reddit sub, use it in order to scrap threads.
    Example of code that mines the last 10 daily thread from BitcoinMarkets sub:

    ins = submine.Submine(sub_name="BitcoinMarkets",post_name="daily",limit=10)
    ins.scrap_whole_sub(is_whole=False)

