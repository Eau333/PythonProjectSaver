import matplotlib.pyplot as plt

if __name__ == '__main__':

    def savings(t):
        return t * 100 - 300

    x = []
    y = []

    for i in range(0,12):
        x.append(i)
        y.append(savings(i))

    plt.plot(x,y)
    plt.grid()
    plt.show()