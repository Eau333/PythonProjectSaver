import parabola
import matplotlib.pyplot as plt

# if __name__ == '__main__':
print("Hi Lucas. This is what happens when you don't wrap your main script in the if __name__ =='__main__' block!")
# initialize a parabola passing through origin with vertex at 4,8
p = parabola.Parabola([0,0], [10,10], [20,0])
x = []
y = []

for i in range(0,21):
    x.append(i)
    y.append(p.eval(i))

plt.plot(x, y)
plt.show()
