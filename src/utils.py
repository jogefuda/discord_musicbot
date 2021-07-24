
def truncate(s: str, width: int=48):
    n = 0
    i = 0
    for c in s:
        i += 1
        if ('\u4e00' <= c <= '\u9fa5'):
            n += 2
        else:
            n += 1
        if n >= width:
            break
    
    return s if len(s) < width else '{0}...'.format(s[:i])

def process_bar(percent: int, width: int=1):
    percent = max(0, min(percent, 100))
    c = max(0, (width // 100 * percent))
    s = []
    for _ in range(c):
        s.append('▪')
    s.append('➤')
    for _ in range(width-c-1):
        s.append('▫')
    return ''.join(s)
