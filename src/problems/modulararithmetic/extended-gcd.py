def extended_gcd(x, y):    
    print('x:', x, 'y:', y)
    if y == 0:
        %%% start a %%%
        return (x, 1, 0)
        %%% end a %%%
    else:
        %%% start b %%%
        d, a, b = extended_gcd(y, x % y)
        print('d:', d, 'a:', a, 'b:', b)
        return (d, b, a - (x // y)*b)
        %%% end b %%%
