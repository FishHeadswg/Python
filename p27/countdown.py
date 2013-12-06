def countdown(n):
    print(n)
    if n == 0:  # this is the base case
        return  # return, instead of making more recursive calls
    countdown(n - 1)  # the recursive call
    
countdown(10)