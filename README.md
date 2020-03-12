# Age Analyzer
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0bd5abc01d3a4b13a99a2d343aafdacd)](https://app.codacy.com/manual/fegor2004/Age-Analyzer?utm_source=github.com&utm_medium=referral&utm_content=FEgor04/Age-Analyzer&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.com/FEgor04/Age-Analyzer.svg?branch=master)](https://travis-ci.com/FEgor04/Age-Analyzer)
[![codecov](https://codecov.io/gh/FEgor04/Age-Analyzer/branch/master/graph/badge.svg)](https://codecov.io/gh/FEgor04/Age-Analyzer)

## Install

At first, make sure you have this libraries:
  1. requests 
  2. numpy
  3. pandas
  4. sklearn
  5. matplotlib
  6. pyTelegramBotAPI
  
And, if they are not, install them with this command:
```shell script
pip3 install requests numpy pandas sklearn matplotlib pyTelegramBotAPI
```
Finally, you need to set **vk_api** and **tg_api** environment variables.
## How to analyze someone's age 

Set ``ANALYZE`` variable on **True** <br>
Then launch `__main__.py` file with this:
```shell script
python __main__.py
```
Script will ask you to input target's ID, and then it will print his age.
## How to collect data
To collect data, you need to create **.csv** file and fill it like that:

| ID        | Real Age | VK Age | Mean | Harmonic Mean | Mode | Median | std |
|-----------|----------|--------|------|---------------|------|--------|-----|
| fegor2004 | 15       | 24     |      |               |      |        |     |
|           |          |        |      |               |      |        |     |
|           |          |        |      |               |      |        |     |
And so on.. <br>
Then set `FILL_CSV` variable to **TRUE** and launch script

## How to train model
To train model, make sure your .csv table is filled. <br>
Then, set `TRAIN_MODEL` variable to **TRUE** and launch script.
## How to launch bot
To launch bot, you should have your `neuronet.sav` file with trained model.
Then, just set `BOT` variable to **TRUE** and launch script 