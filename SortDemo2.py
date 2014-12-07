# -*- coding: utf-8 -*-
import wx
import random


Animation_Panel_WIDTH = 0

LEFT_START_POSITION = 50
LOW_HEIGHT = 100
ELEMENT_NUMBER = 15
width = 900 / (ELEMENT_NUMBER * 2)
gap = 900 / (ELEMENT_NUMBER * 4)
BarData = []
Height = []

DEFAULT_DELAY = 500
MIN_DELAY = 20
MAX_DELAY = 1000
cache_pos = []
SORT_ALGORITHM_NAME_LISTS = [u"插入排序", u"冒泡排序", u"快速排序"]


def swap(j):
    BarData[j][1], BarData[j + 1][1] = BarData[j + 1][1], BarData[j][1]
    BarData[j][3], BarData[j + 1][3] = BarData[j + 1][3], BarData[j][3]


def insertion_sort():
    for i in xrange(len(BarData) - 1):
        for j in xrange(len(BarData) - 1 - i):
            if BarData[j][3] > BarData[j + 1][3]:
                cache_pos.append(j)
                swap(j)
                return True
    return False


def bubble_sort():
    for i in xrange(len(BarData), 1, -1):
        for j in xrange(i - 1):
            if BarData[j][3] > BarData[j + 1][3]:
                cache_pos.append(j)
                swap(j)
                return True
    return False


def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot_element = random.choice(a)[3]
    small = [i for i in a if i[3] < pivot_element]
    medium = [i for i in a if i[3] == pivot_element]
    large = [i for i in a if i[3] > pivot_element]
    # print small
    return quick_sort(small) + medium + quick_sort(large)


SORT_ALGORITHM_FUNCTION = [insertion_sort, bubble_sort, quick_sort]


class AnimationPanel(wx.Panel):
    def __init__(self, parent, ID=-1, pos=(0, 0), size=(Animation_Panel_WIDTH, 400)):
        wx.Panel.__init__(self, parent, ID, pos, size)
        self.SetBackgroundColour(wx.Colour(207, 230, 255))
        self.font = wx.Font(14, wx.DEFAULT, wx.ITALIC, wx.NORMAL)

        self.GenerateBarData(LEFT_START_POSITION)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        self.sort_algorithm = None

    def GenerateBarData(self, left_pos):
        for i in range(ELEMENT_NUMBER):
            left_pos += (width + gap)
            height = random.randrange(5, 300)
            BarData.append([left_pos, LOW_HEIGHT, width, height])
        self.RevertBarData()

    def RevertBarData(self):
        maxH = self.maxHeight()
        for h in range(ELEMENT_NUMBER):
            moveH = maxH - BarData[h][3]
            yPos = BarData[h][1]
            yPos += moveH
            BarData[h][1] = yPos

    def maxHeight(self):
        global Height
        Height = []
        for h in range(ELEMENT_NUMBER):
            Height.append(BarData[h][3])
        return max(Height)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        color = wx.Colour(0, 146, 199)
        dc.SetBrush(wx.Brush(color))
        dc.SetFont(self.font)
        dc.SetTextForeground(color)
        for i in range(ELEMENT_NUMBER):
            dc.DrawRectangle(*BarData[i])
            h = str(BarData[i][3])
            x = BarData[i][0]
            y = BarData[i][1] + BarData[i][3]
            dc.DrawText(h, x, y)

    def OnTimer(self, event):
        # print self.sort_algorithm
        if self.sort_algorithm == quick_sort:
            global BarData
            BarData = self.sort_algorithm(BarData)
            self.Refresh()
            self.timer.Stop()
            wx.MessageBox(u"排序完成！")
        elif self.sort_algorithm():
            self.Refresh()
            self.timer.Start(self.speed_slider.GetValue())
        else:
            self.timer.Stop()
            wx.MessageBox(u"排序完成！")


class SidePanel(wx.Panel):
    def __init__(self, parent, aPanel, ID=-1, pos=(Animation_Panel_WIDTH, 0), size=(250, 500)):
        wx.Panel.__init__(self, parent, ID, pos, size)
        self.SetBackgroundColour(wx.Colour(207, 230, 255))
        self._aPanel = aPanel

        self.Data_Panel = wx.Panel(self, -1, pos=(Animation_Panel_WIDTH, 0), size=(500, 50))
        self.posCtrl = wx.TextCtrl(self, -1, " ".join(str(h) for h in Height), pos=(55, 10), size=(500, 25))
        self.posCtrl.SetInsertionPoint(0)
        data_sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        data_sizer.AddMany([wx.StaticText(self, -1, u"数据：", pos=(15, 10)), self.posCtrl])
        self.Data_Panel.SetSizer(data_sizer)

        self.Button_Panel = wx.Panel(self, -1, pos=(Animation_Panel_WIDTH, 0), size=(250, 150))
        button_sizer = wx.GridSizer(rows=2, cols=2)
        border = 3
        button_labels = ((u"开始", self.OnStart),
                         (u"上一步", self.OnStepBack),
                         (u"暂停", self.OnPause),
                         (u"下一步", self.OnStepForward))
        for eachLabel, eachHandle in button_labels:
            button = wx.Button(self.Button_Panel, -1, eachLabel)
            button.Bind(wx.EVT_BUTTON, eachHandle)
            button_sizer.Add(button, 0, wx.EXPAND | wx.ALL, border)
        self.Button_Panel.SetSizer(button_sizer)

        self.ChoiceList_Panel = wx.Panel(self, -1, pos=(Animation_Panel_WIDTH, 150), size=(250, 50))

        self.sort_algorithm_choice = wx.Choice(self.ChoiceList_Panel, -1, choices=SORT_ALGORITHM_NAME_LISTS)
        choice_sizer = wx.BoxSizer(wx.VERTICAL)
        choice_sizer.Add(wx.StaticText(self.ChoiceList_Panel, -1, u"选择一个排序算法："), 1, wx.EXPAND | wx.ALL)
        choice_sizer.Add(self.sort_algorithm_choice, 1, wx.EXPAND | wx.ALL)
        self.ChoiceList_Panel.SetSizer(choice_sizer)

        self.Speed_Panel = wx.Panel(self, -1, pos=(Animation_Panel_WIDTH, 400), size=(250, 100))
        self.speed_slider = wx.Slider(self.Speed_Panel, -1, DEFAULT_DELAY, MIN_DELAY, MAX_DELAY, wx.DefaultPosition,
                                      (250, -1),
                                      style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.speed_slider.SetTickFreq(50, 1)
        speed_sizer = wx.BoxSizer(wx.VERTICAL)
        speed_sizer.Add(wx.StaticText(self.Speed_Panel, -1, u"单帧时间调节"), 0, wx.EXPAND | wx.ALL)
        speed_sizer.Add(self.speed_slider, 0, wx.EXPAND | wx.ALL)
        self.Speed_Panel.SetSizer(speed_sizer)
        aPanel.speed_slider = self.speed_slider

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.Add(self.Data_Panel, 0, wx.EXPAND)
        box_sizer.Add(self.Button_Panel, 0, wx.EXPAND)
        box_sizer.Add(self.ChoiceList_Panel, 0, wx.EXPAND)
        box_sizer.Add(self.Speed_Panel, 0, wx.EXPAND)
        self.SetSizer(box_sizer)

    def set_algorithm(self):
        if self._aPanel.sort_algorithm is not None:
            return
        sort_algorithm_name = self.sort_algorithm_choice.GetStringSelection()
        if len(sort_algorithm_name) == 0:
            wx.MessageBox(u"请选择一个排序算法！")
        else:
            cnt = 0
            for name in SORT_ALGORITHM_NAME_LISTS:
                if sort_algorithm_name == name:
                    # print cnt, SORT_ALGORITHM_FUNCTION[cnt]
                    self._aPanel.sort_algorithm = SORT_ALGORITHM_FUNCTION[cnt]
                    global cache_pos
                    cache_pos = []
                else:
                    cnt += 1

    def OnStart(self, event):
        self.set_algorithm()
        if self._aPanel.sort_algorithm is not None:
            self._aPanel.timer.Start(DEFAULT_DELAY)

    def OnPause(self, event):
        self._aPanel.timer.Stop()

    def OnStepBack(self, event):
        self.set_algorithm()
        self._aPanel.timer.Stop()
        if len(cache_pos) > 0:
            swap(cache_pos.pop())
            self._aPanel.Refresh()

    def OnStepForward(self, event):
        self.set_algorithm()
        self._aPanel.timer.Stop()
        if self._aPanel.sort_algorithm():
            self._aPanel.Refresh()
        else:
            self._aPanel.timer.Stop()
            wx.MessageBox(u"排序完成！")


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u"排序演示", size=(1250, 500))

        self.animation_panel = AnimationPanel(self)
        self.side_panel = SidePanel(self, self.animation_panel)

        box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(self.animation_panel, 2, wx.EXPAND)
        box_sizer.Add(self.side_panel, 1, wx.EXPAND)
        self.SetSizer(box_sizer)
        # box_sizer.Fit(self)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()