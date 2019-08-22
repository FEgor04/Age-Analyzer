At first, you should create settings.py.
Here is the settings.py sample.
```python
token = 'your_vk_token'
version = 5.101
target = "0"
analyze = true
input_file = 'research.csv'
output_file = 'research_analyzed.csv'
analyze_file = 'research_analyzed.csv'
```

####How to analyze someone`s age:
Set **target** variable equal to target's id or short link

If target's profile age is -1, then the year of birth is not defined on target's page.
<hr>

####How to analyze .csv file:
Set analyze variable in **settings.py** = *True*. Then, create input file.  
It should be formed like: 
```csv
ID,Real Age,VK Age,Mean,Harmonic Mean,Mode,Median
``` 

You should also set path to files in input_file, output_file, analyze_file variables in settings.py.

