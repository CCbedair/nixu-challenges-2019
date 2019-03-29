# The solution for "Lisby-3" challenge.

## Step
1. Using our decomiler we again dump the assembly and take a look a it. It seems there are a lot more functions in this one compared to Lisby-2 challenge. ![decompile](0.png)
2. We check the 'for', 'new', 'op' codes and implement those in our execute function. ![newcodes](1.png)
3. We implement the new functions according to the specifications and run the code again, we however fail to get the correct output, so
we go for analysing the code manually. ![output](2.png)
4. After some time, we now what each tape/function is doing.
5. So, we implement a quick Python script that emulates the program and we get our flag.
![flag](4.png)

## The tapes
1. Tape 1 - gets the first element
2. Tape 2 - gets the second element
3. Tape 3 - 'gen-rev' function
4. Tape 5 - zips the mangle and flag together in a pair list of elements
5. Tape 6 - mapping function
6. Tape 4 - closure function


## Flag
The flag that we obtained is NIXU18{lambada_the_pretty_good!}
