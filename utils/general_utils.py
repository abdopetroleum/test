import copy

def with_keys(dict, keys):
    temp = copy.deepcopy(dict)

    for key in temp:
        if key not in keys:
            del dict[key]
    
    return dict

def without_keys(dict, keys):
    temp = copy.deepcopy(dict)

    for key in temp:
        if key in keys:
            del dict[key]
    
    return dict