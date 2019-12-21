At first, you should create settings.py.
Here is the settings.py sample.
```python
token = 'your_vk_token'
version = 5.101     # Set latest version
neural_network_file = 'neuronet_file'
                    # You need this if you want to analyze someone's age
target = 'target_vk_id'
analyze = True
log_needed = False
                    # If you want to launch telegram bot you will also need this:
tg_api = 'your_telegram_token'
                    # If you need logging:
log_needed = True
```
#### How to analyze someone's age:
Set ``target`` variable equal to target's id or short link <br>
Then set `analyze = True` <br>
Then launch `__main__.py` file with this:
```
$ python __main__.py
```
<hr>

#### NEED HELP
I really need some help.
On my VPS located in Netherlands `age_analyzer.get_friends_ages("fegor2004")` gives this:
```
Ages: [21, 21, 24, 24, 51, 51, 24, 16, 16, 16, 21, 22, 25, 16, 34, 19, 19, 28, 20, 24, 25, 16] 
```
But on my local PC in Russia it gives this:
```
Ages: [21, 21, 24, 24, 51, 51, 24, 16, 16, 16, 15, 15, 15, 21, 15, 15, 22, 25, 15, 14, 16, 34, 19, 19, 28, 15, 20, 15, 24, 25, 15, 15, 15, 16] 
```
As you can see, on my local PC it gives more data than on my VPS. It`s really bad because I've trained my neural network on local PC data.
<br>

So, if you can help with fixing this issue - please contact me. <br>
My VK: [vk.com/fegor2004](https://vk.com/fegor2004) <br>
My Telegram: [@FEgor04](https://t.me/fegor04)

