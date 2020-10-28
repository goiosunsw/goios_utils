import numpy as np
import matplotlib.pyplot as pl
from matplotlib.patches import Ellipse

from itertools import product


def bodeplot(f, h, xscale='lin', yscale='db', ax=None, **kwargs):
    """
    Plot a complex-valued function h(f) in module/ phase
    pair of axes
    
    Arguments:
    * f: frequency values for h
    * h: complex-valued function of f
    * xscale ('lin', 'log' or 'oct')
    * yscale ('lin', 'log', 'db' or  'dbpow')
    """
    if ax is None:
        fig, ax = pl.subplots(2, sharex=True)

    else:
        fig = ax[0].figure

    if xscale == 'lin' or xscale == 'log':
        x = f
        ax[1].set_xlabel('Frequency (Hz)')
    elif xscale == 'oct':
        x = np.log2(f)
        ax[1].set_xlabel('Octaves')
    if yscale == 'lin' or yscale == 'log':
        yabs = np.abs(h)
        yarg = np.angle(h)
        ax[0].set_ylabel('Magnitude (lin)')
    elif yscale == 'db':
        yabs = 20*np.log10(np.abs(h))
        yarg = np.angle(h)
        ax[0].set_ylabel('Magnitude (dB)')
    elif yscale == 'dbpow':
        yabs = 10*np.log10(np.abs(h))
        yarg = np.angle(h)
        ax[0].set_ylabel('Magnitude (dB)')
    ax[1].set_ylabel('Phase (rad)')

    ax[0].plot(x, yabs, **kwargs)
    ax[1].plot(f, yarg, **kwargs)

    if xscale == 'log':
        ax[0].set_xscale('log')
        ax[1].set_xscale('log')
    if yscale == 'log':
        ax[0].set_yscale('log')

    yrange = np.diff(ax[1].get_ylim())
    npi = yrange/np.pi
    pifrac = 2*np.pi/yrange

    mult = 1
    div = 2

    def format_func(value, tick_number):
        # find number of multiples of pi/2
        N = int(np.round(div * value / np.pi))
        if N == 0:
            return "0"
        elif N == div:
            return r"$\pi$"
        elif N == -div:
            return r"$-\pi$"
        elif N == 1:
            return r"$\pi/{}$".format(div)
        elif N == -1:
            return r"$-\pi/{}$".format(div)

        elif N % div > 0:
            return r"${0}\pi/{1}$".format(N, div)
        else:
            return r"${0}\pi$".format(N // div)

    ax[1].yaxis.set_minor_locator(pl.MultipleLocator(mult*np.pi/div/8))
    ax[1].yaxis.set_major_locator(pl.MultipleLocator(mult*np.pi/div))
    ax[1].yaxis.set_major_formatter(pl.FuncFormatter(format_func))

    return fig, ax


def getCovEllipse(x,y):
    """
    get the coordinates of an ellipse that represents the covariance of data given as x,y
    
    returns x_mean, y_mean, width, height, angle
    """
    chisquare_val = 2.4477;
    evalue,evec = np.linalg.linalg.eig(np.cov(x,y))
    midx = np.argmax(evalue)
    
    angle = np.arctan(evec[1,midx]/evec[0,midx])
    xm = np.mean(x)
    ym = np.mean(y)
    w = chisquare_val*np.sqrt(np.max(evalue))
    h = chisquare_val*np.sqrt(np.min(evalue))
    
    return xm, ym, w, h, angle


def ellipseplot(x,y,groups=None,groups2=None,ax=None,color=None,ls='-',lw=2,alpha=1,plotpoints=False,pointalpha=.5,
                styles={'ls':['-','--',':','-.'],'lw':[2,1]},label=None):
    if ax is None:
        #_,ax = pl.subplots(1)
        ax=pl.gca()
        
    if groups is None:
        if len(x)>1:
            xe,ye,we,he,ela = getCovEllipse(x,y)
            if color is None:
                # fake plotting individual points per phoneme, just to get a color
                # individual points are already plotted below, with different markers per population
                ln=pl.plot(x,y,'.',markersize=0)
                # get color of points
                color = ln[0].get_color()

            el = Ellipse(xy=(xe,ye), width=we, height=he, angle=ela/2/np.pi*360, facecolor='none', edgecolor=color, lw=lw,ls=ls,label=label)
            ax.add_patch(el)
            if plotpoints:
                ax.plot(x,y,'.',color=color,alpha=pointalpha)
            return el
        elif len(x)==1:
            lns=ax.plot(x,y,'o',color=color)
            el = Ellipse(xy=(0,0), width=1, height=1, angle=0, facecolor='none', edgecolor=color, lw=lw,ls=ls,label=label)
            return el
        else:

            el = Ellipse(xy=(0,0), width=1, height=1, angle=0, facecolor='none', edgecolor=color, lw=lw,ls=ls,label=label)
        return el

    gru = np.unique(groups)
    lns = []
    labs = []
    
    if groups2 is not None:

        for gr in gru:
            # fake plotting individual points per phoneme, just to get a color
            # individual points are already plotted below, with different markers per population
            ln=pl.plot(x,y,'.',markersize=0)
            # get color of points
            color = ln[0].get_color()
            for g2,(ls,lw) in zip(np.unique(groups2),product(styles['ls'],styles['lw'])):
                xg = x[(groups == gr)&(groups2 == g2)]
                yg = y[(groups == gr)&(groups2 == g2)]
                el = ellipseplot(xg,yg,ax=ax,ls=ls,lw=lw,color=color,alpha=alpha,plotpoints=plotpoints,pointalpha=pointalpha)
                lns.append(el)
                labs.append(str(gr)+' '+str(g2))
    else:
        for gr in gru:
            xg = x[groups == gr]
            yg = y[groups == gr]
            el = ellipseplot(xg,yg,ax=ax,ls=ls,lw=lw,color=color,alpha=alpha,plotpoints=plotpoints,pointalpha=pointalpha)
            lns.append(el)
            labs.append(gr)
    
    pl.legend(lns,labs) 
    return ax
    