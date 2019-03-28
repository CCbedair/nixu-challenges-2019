# The solution for challenge "Bad memories part 5"

There are several methods to complete this task. I decided to provide one of them. The steps that I took to complete the task:
1. Let's start by analysing the image
2. Let's discover the strings-> nothing
3. Let's discover the strings with little endian-> nothing
4. Let's try clipboard -> got a hit "You are on right track, try harder"
5. Let's have a look at memory dump -> found a string with basic ROT32 cipher
![The picture of memory dump](Unknown-2)
6. Let's decrypt it. The flag is found
![The picture of final result](Unknown)
# The flag
NIXU{this_w4s_th3_easy_one}
