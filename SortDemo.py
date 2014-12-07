# -*- coding: utf-8 -*-
import random
import Tkinter


def cmp_less(a, b):
    return a < b


def cmp_greater(a, b):
    return b < a


def insertion_sort(a, comp):
    if len(a) == 1:
        return a
    b = insertion_sort(a[1:], comp)
    for i in xrange(len(b)):
        if comp(a[0], b[i]):
            b.insert(i, a[0])
            return b
    return b + [a[0]]


def bubble_sort(a, comp):
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if comp(a[j], a[i]):
                a[i], a[j] = a[j], a[i]
    return a


def quick_sort(a, comp):
    if len(a) <= 1:
        return a
    pivot_element = random.choice(a)
    small = [i for i in a if comp(i, pivot_element)]
    medium = [i for i in a if i == pivot_element]
    large = [i for i in a if comp(pivot_element, i)]
    return quick_sort(small, comp) + medium + quick_sort(large, comp)


data = []
is_playing = False


def generate_data(ev=None):
    data_size = 10
    data_range = 99
    global data
    data = [random.randint(0, data_range) for i in range(data_size)]
    global text
    text.delete(Tkinter.INSERT, Tkinter.END)
    text.insert(Tkinter.INSERT, data)


def play_data(ev=None):
    global is_playing
    global play_button
    if is_playing:
        play_button.config(text='播放')
    else:
        play_button.config(text='暂停')
        global text
        raw_data = text.get('1.0', Tkinter.END)
        if raw_data == '\n':
            print "请输入数据"
        else:
            data_list = map(int, raw_data[1:-2].split(','))
            for i in data_list:
                print i
                # print data_list
    is_playing = not is_playing


botton_padx = 24
botton_pady = 12

root = Tkinter.Tk()

button_frame = Tkinter.Frame(root)
button_frame.grid(row=0, column=0)
Tkinter.Button(button_frame, text='生成数据', command=generate_data, pady=botton_pady).grid()
Tkinter.Button(button_frame, text='插入排序', command=root.quit, pady=botton_pady).grid()
Tkinter.Button(button_frame, text='冒泡排序', command=root.quit, pady=botton_pady).grid()
Tkinter.Button(button_frame, text='快速排序', command=root.quit, pady=botton_pady).grid()

text = Tkinter.Text(root)
text.grid(row=0, column=1)
#text_contents = Tkinter.StringVar()

play_frame = Tkinter.Frame(root)
play_frame.grid(row=1, column=1)
Tkinter.Button(play_frame, text='回退', command=root.quit, padx=botton_padx).grid(row=0, column=0)
play_button = Tkinter.Button(play_frame, text='播放', command=play_data, padx=botton_padx)
play_button.grid(row=0, column=1)
Tkinter.Button(play_frame, text='单步', command=root.quit, padx=botton_padx).grid(row=0, column=3)


def main():
    #thread.start_new_thread(Tkinter.mainloop, ())
    Tkinter.mainloop()


if __name__ == '__main__':
    main()