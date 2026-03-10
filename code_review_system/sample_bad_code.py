def badFunction(x,y,z):
    result = 0
    for i in range(100):
        for j in range(100):
            for k in range(100):
                result += x + y + z + i + j + k
    return result

class badclass:
    def __init__(self):
        self.value = 1

    def anotherBadFunction(self, a, b, c, d, e, f, g, h, i, j):
        if a == 1:
            if b == 2:
                if c == 3:
                    if d == 4:
                        if e == 5:
                            if f == 6:
                                if g == 7:
                                    if h == 8:
                                        if i == 9:
                                            if j == 10:
                                                return True
        return False

# No comments, poor naming, long functions, nested structures
