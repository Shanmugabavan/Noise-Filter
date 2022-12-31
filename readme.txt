Required packages = opencv, numpy (better to activate conda environment)

Usage:- 
1. It will create noise filtered images in the path directory which has images that need to be filtered

2. python noise_filter.py
This command will create filtered images in the path directory filter size=3

3. python noise_filter.py --filter_size=5
We can change the filter size by command line argument

4. python noise_filter.py --filter_size=5 --path="C:\noise filtering submission"
We can pass the path of the folder as argument. default path is current directory