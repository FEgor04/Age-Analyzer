At first, you should create settings.py.
Here is the settings.py sample.
```python
token = 'your_vk_token'
version = 5.101
target = "0"
analyze = True
input_file = 'research.csv'
output_file = 'research_analyzed.csv'
analyze_file = 'research_analyzed.csv'
```

#### How to analyze someone's age:
Set **target** variable equal to target's id or short link

If target's profile age is -1, then the year of birth is not defined on target's page.
<hr>

#### How to analyze .csv file:
Set analyze variable in **settings.py** = *True*. Then, create input file.  
It should be formed like: 
```csv
ID,Real Age,VK Age,Mean,Harmonic Mean,Mode,Median
``` 

You should also set path to files in input_file, output_file, analyze_file variables in settings.py.
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
As you can see, on my local PC it gives more data than on my VPS. It`s really bad because I've trained my neuronet on local PC data.
<br>

So, if you can help with fixing this issue - please contact me. <br>
My VK: `vk.com/fegor2004` <br>
My Telegram: `@FEgor04`

