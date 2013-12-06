def deep_reverse(p):
    if is_list(p):
        result = []
        for i in range(len(p) -1, -1, -1):
            result.append(deep_reverse(p[i]))
        return result
    else:
        return p