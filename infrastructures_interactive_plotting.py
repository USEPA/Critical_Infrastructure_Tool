# -*- coding: utf-8 -*-
"""
infrastructures_interactive_plotting.py
Created on Sun Aug 27 14:39:25 2019

"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

def plotting(t,n,lower_bounds,upper_bounds,timeSpan, imageFileName, contam):

    colors = np.array(['darkorange','blue','green','gold','magenta','cornflowerblue','indigo','black', 'brown', 'brown', 'gray', 'purple', 'maroon', 'navy', 'pink'])
    labels = np.array(['water','energy','transport','communications','government', 'food', 'emergency', 'waste management','healthcare','finance', 'chemical', 'commercial', 'dams', 'defense', 'nuclear'])
    fig, ax = plt.subplots(figsize=(17,8))
    for i in range(0, 9):
        ax.plot(t[:len(n)], n[:,i], color = colors[i], label = labels[i])
        #ax.plot(t, contam[:,i], color = colors[i], label = str("Uncontaminated " +  labels[i]), linestyle="--")
        if t[len(n)-1] < timeSpan:
            ax.plot([t[len(n)-1], timeSpan], [n[len(n)-1][i], n[len(n)-1][i]], color = colors[i])
        if lower_bounds is not None and upper_bounds is not None:
            ax.fill_between(t[:len(n)], lower_bounds[:,i], upper_bounds[:,i], facecolor=colors[i], label=(labels[i] + " (95% conf)"), alpha=0.5)
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Efficiency (%)')
    ax.set_xlim([0,timeSpan])
    ax.set_ylim([0,110])
    if lower_bounds is not None and upper_bounds is not None:
        ax.legend(loc='upper left',bbox_to_anchor=(1.05, 1),ncol=2,borderaxespad=0)
    else:
        ax.legend(loc='upper left',bbox_to_anchor=(1.05, 1),ncol=1,borderaxespad=0)
    fig.subplots_adjust(right=0.65)
    #fig.suptitle('Infrastructure Efficiency Time Profiles\n(Right-click to hide all\nMiddle-click to show all)',
                     #va='top', size='large')
    fig.suptitle('Infrastructure Efficiency Time Profiles',
                     va='top', size='large')
    figname = imageFileName + ".png"
    fignameDecon = imageFileName + "Decon" + ".png"
    if not os.path.exists("Images"):
        os.makedirs("Images")
    fig.savefig("Images/" + figname)
    leg = interactive_legend()
    return fig, ax, leg


def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()
    leg = InteractiveLegend(ax.get_legend())
    return leg

class InteractiveLegend(object):
    def __init__(self, legend):
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:

            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            #HARD CODED sequence to determine if confidence intervals are displayed or not and hiding both line and intervals concurrently
            if len(list(self.lookup_artist.values())) == 32:
                if isinstance(artist,matplotlib.lines.Line2D):
                    artist2index=list(self.lookup_artist.values()).index(artist)-16
                else:
                    artist2index=list(self.lookup_artist.values()).index(artist)+16
                artist2 = self.lookup_artist[list(self.lookup_artist.keys())[artist2index]]
                artist2.set_visible(not artist2.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()
