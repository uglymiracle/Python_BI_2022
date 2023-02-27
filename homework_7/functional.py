def func_chain(*args):

    #sequential execution of all functions
    def func(x):
        for f in args:
            x = f(x)
        return x
    
    return func


def sequential_map(*args):

    chain = func_chain(*args[:-1])
    return list(map(chain, args[-1]))


def consensus_filter(*args):
    
    lst = args[-1]
    
    #filtering
    for f in args[:-1]:
        lst_bool = list(map(f, lst))
        
        for i in range(len(lst_bool)-1, -1, -1):
            if not lst_bool[i]:
                del lst[i]

    return lst

def conditional_reduce(*args):
    
    lst = args[-1]
    f_bool = args[0] #function for filter
    f = args[1] 

    #filtering
    lst_bool = list(map(f_bool, lst)) 
    for i in range(len(lst_bool)-1, -1, -1):
        if not lst_bool[i]:
            del lst[i]
            
    #output
    final_lst = lst[0]
    for x in lst[1:]:
        final_lst = f(final_lst, x)
    return final_lst


def multiple_partial(*args, **kwargs):
    
    return [lambda x, f=f: f(x, **kwargs) for f in args]
