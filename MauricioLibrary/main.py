import parabola

# if __name__ == '__main__':
print("Hi Lucas. This is what happens when you don't wrap your main script in the if __name__ =='__main__' block!")
# initialize a parabola passing through origin with vertex at 4,8
p = parabola.Parabola([0,0], [4,8], [8,0])
print(p.eval(0))
print(p.eval(2))
print(p.eval(4))
print(p.eval(6))
print(p.eval(8))