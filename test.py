while True:
    a = int(input())
    b = a ** 4
    b = b % 16711680
    b = hex(b).split('x')[-1]
    b = '#' + '0' * (6 - len(b)) + b
    print(b)



#dec_color = int(self.color[1:7], 16)
#dec_color *= 16
#dec_color = dec_color % 16711680
#dec_color = hex(dec_color).split('x')[-1]
#child_color = '#' + '0' * (6 - len(dec_color)) + dec_color

