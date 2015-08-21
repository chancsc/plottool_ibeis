from __future__ import absolute_import, division, print_function
# Standard
import warnings
from six.moves import zip, range
from plottool import draw_func2 as df2
# Matplotlib
import scipy.stats
import matplotlib.pyplot as plt
import vtool.histogram as htool
import utool
import utool as ut  # NOQA
import numpy as np

ut.noinject(__name__, '[plots]')


def plot_multiple_scores(known_nd_data, known_target_points, nd_labels,
                         target_label, title=None, fnum=None, pnum=None,
                         use_legend=True, ymin=None, ymax=None,
                         color_list=None, marker_list=None, **kwargs):
    r"""

    CommandLine:
        python -m plottool.plots --test-plot_multiple_scores --show

        python -m plottool.plots --exec-plot_rank_cumhist \
            --adjust=.15 --dpi=512 --figsize=11,4 --clipwhite \
            --dpath ~/latex/crall-candidacy-2015/ --save "figures/tmp.jpg"  --diskshow \

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> known_nd_data = np.array([[  1,   2,   4,   7,   1,   2,   4,   7,   1,   2,   4,   7,   1,
        ...                              2,   4,   7,   1,   2,   4,   7],
        ...                           [ 50,  50,  50,  50, 100, 100, 100, 100, 200, 200, 200, 200, 300,
        ...                            300, 300, 300, 500, 500, 500, 500]], dtype=np.int64).T
        >>> known_target_points = np.array([35, 32, 32, 30, 33, 32, 33, 30, 32, 31, 31, 32, 36, 33, 33, 32, 33,
        ...                                 33, 32, 31], dtype=np.int64)
        >>> lbl_list = ['custom', 'custom:sv_on=False']
        >>> nd_labels = [u'K', u'dsize']
        >>> target_label = 'score'
        >>> fnum = None
        >>> pnum = None
        >>> use_legend = True
        >>> title = 'test'
        >>> result = plot_multiple_scores(known_nd_data, known_target_points, nd_labels, target_label, title=title)
        >>> print(result)
        >>> ut.show_if_requested()
    """
    #import matplotlib as mpl
    assert(len(known_nd_data.T) == 2), 'cannot do more than 2 right now'

    # Put the data into a dense field grid
    nd_basis = [np.unique(arr) for arr in known_nd_data.T]
    inverse_basis = [dict(zip(arr, np.arange(len(arr)))) for arr in nd_basis]
    data_field = np.full(list(map(len, nd_basis)), np.nan)
    # Fill in field values
    for coord, val in zip(known_nd_data, known_target_points):
        index = [invbase[pt] for invbase, pt in zip(inverse_basis, coord)]
        data_field.__setitem__(tuple(index), val)

    # Setup the plots
    #num_lines = len(nd_basis[1])

    #if color_list is None:
    #    color_list = df2.distinct_colors(num_lines)

    #if marker_list is None:
    #    #marker_list = ['o'] * num_cdfs
    #    marker_list = df2.distinct_markers(num_lines)

    #plotkw = dict(markersize=10)

    label_list = ['%s=%r' % (nd_labels[1], val,) for val in nd_basis[1]]
    xdata = nd_basis[0]
    ydata_list = data_field.T
    fig = multi_plot(
        xdata, ydata_list, label_list=label_list, markersize=10,
        marker_list=marker_list, color_list=color_list, title=title,
        xlabel=nd_labels[0], ylabel=target_label, fnum=fnum, pnum=pnum,
        **kwargs)

    # Plot a line for each zdim value
    #for ix in range(num_lines):
    #    ydata = data_field.T[ix]
    #    color = color_list[ix]
    #    marker = marker_list[ix]
    #    ymask = np.isfinite(ydata)
    #    label = label_list[ix]
    #    ax.plot(xdata[ymask], ydata[ymask], color=color, marker=marker, label=label, **plotkw)

    #label_fontprop = mpl.font_manager.FontProperties(weight='light', size=8)
    #title_fontprop = mpl.font_manager.FontProperties(weight='light', size=10)
    #ax.set_xlabel(nd_labels[0], fontproperties=label_fontprop)
    #ax.set_ylabel(target_label, fontproperties=label_fontprop)

    #if ymax is None:
    #    ymax = np.nanmax(ydata)
    #if ymin is None:
    #    ymin = np.nanmin(ydata)

    #ypad_max = 1
    #ypad_min = 1
    #ax.set_ylim(ymin - ypad_min, ymax + ypad_max)

    #ax.set_yticks(nd_basis[1])
    #ax.set_xticks(nd_basis[0])
    #max_pos = np.nanmax(ydata)
    #num_ticks = 10
    #step_size = int(max_pos / num_ticks)
    #ax.set_yticks(np.arange(1, max_pos, step_size))

    #if title is not None:
    #    ax.set_title(title, fontproperties=title_fontprop)

    #if use_legend:
    #    legend_fontprop = mpl.font_manager.FontProperties(weight='light', size=8)
    #    #df2.legend(loc='upper right', fontproperties=legend_fontprop)
    #    df2.legend(loc='best', fontproperties=legend_fontprop)
    #    #ut.embed()
    #df2.dark_background()
    return fig


def plot_rank_cumhist(cdf_list, lbl_list, color_list=None, marker_list=None, edges=None,
                      fnum=None, pnum=None, title=None, xlabel='',
                      ylabel='cumfreq', use_legend=True, num_xticks=None, **kwargs):
    r"""

    CommandLine:
        python -m plottool.plots --test-plot_rank_cumhist --show

        python -m plottool.plots --exec-plot_rank_cumhist \
            --adjust=.15 --dpi=512 --figsize=11,4 --clipwhite \
            --dpath ~/latex/crall-candidacy-2015/ --save "figures/tmp.jpg"  --diskshow \

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> cdf_list = np.array(
        >>>     [[ 88,  92,  93,  96,  96,  96,  96,  98,  99,  99, 100, 100, 100],
        >>>      [ 79,  82,  82,  85,  86,  87,  87,  87,  88,  89,  90,  90,  90]])
        >>> edges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        >>> lbl_list = ['custom', 'custom:sv_on=False']
        >>> fnum = None
        >>> pnum = None
        >>> plot_rank_cumhist(cdf_list, lbl_list, edges=edges, fnum=fnum, pnum=pnum)
        >>> ut.show_if_requested()
    """

    num_cdfs = len(cdf_list)
    num_data = len(cdf_list[0])
    if color_list is None:
        color_list = df2.distinct_colors(num_cdfs)

    if edges is None:
        x_data = np.arange(num_data)
    else:
        x_data = np.array(edges[1:])
    #max_y = 0
    #min_y = None
    if True or marker_list is None:
        #marker_list = ['o'] * num_cdfs
        marker_list = df2.distinct_markers(num_cdfs)
    if len(x_data) > 256:
        marker_list = [None] * num_cdfs
    if len(x_data) <= 10:
        markersize = 12
    else:
        markersize = 7

    fig = multi_plot(
        x_data, cdf_list,
        # ---
        label_list=lbl_list, color_list=color_list, marker_list=marker_list,
        markersize=markersize, linewidth=2, markeredgewidth=2, linestyle='-',
        # ---
        num_xticks=num_xticks, xlabel=xlabel, ylabel=ylabel, title=title,
        # ---
        use_legend=use_legend,
        # ---
        **kwargs
    )

    #ax = df2.gca()
    #for ix in range(num_cdfs):
    #    y_data = cdf_list[ix]
    #    color = color_list[ix]
    #    label = lbl_list[ix]
    #    marker = marker_list[ix]
    #    max_y = max(np.max(y_data), max_y)
    #    min_y = np.min(y_data) if min_y is None else min(np.min(y_data), min_y)
    #    #ax.plot(x_data, y_data, color=color, label=label, marker=marker, linestyle='-', markersize=4, linewidth=2, markeredgewidth=0)
    #    #ax.plot(x_data, y_data, color=color, label=label, marker=marker, linestyle='-', markersize=10, linewidth=2, markeredgewidth=0, alpha=1.0)
    #    ax.plot(x_data, y_data, color=color, label=label, marker=marker, linestyle='-', markeredgewidth=2, markersize=markersize, linewidth=2)

    #ax.set_ylim(0, max_y * 1.05)
    #xbuf = (x_data.max() - x_data.min()) * .01

    #ax.set_ylim(min_y / 1.05, max_y * 1.05)
    #ax.set_xlim(x_data.min(), x_data.max()  * 1.01)
    #ax.set_xlim(max(0, x_data.min() - xbuf), x_data.max() + xbuf)

    #if figtitle is not None:
    #    df2.set_figtitle(figtitle)
    #    #df2.set_title('')
    #    #'Cumulative Histogram of GT-Ranks')

    #df2.set_xlabel(xlabel)
    #df2.set_ylabel(ylabel)

    #step_size = int(np.log(x_data.max() + 1))
    #step_size = int(np.sqrt(x_data.max() + 1))
    if num_xticks is not None:
        max_pos = (x_data.max() + 1)
        step_size = int(max_pos / num_xticks)
        df2.set_xticks(np.arange(1, max_pos, step_size))
    #df2.dark_background()

    #if use_legend:
    #    df2.legend(loc='lower right')
    #df2.dark_background()
    return fig


def multi_plot(xdata, ydata_list, **kwargs):
    r"""
    plots multiple lines

    Args:
        xdata (ndarray):
        ydata_list (list of ndarrays):

    Kwargs:
        fnum, pnum, title, xlabel, ylabel, num_xticks, use_legend, legend_loc,
        labelsize, xmin, xmax, ymin, ymax, ticksize, titlesize, legendsize
        can append _list to any of these
        plot_kw_keys = ['label', 'color', 'marker', 'markersize', 'markeredgewidth', 'linewidth', 'linestyle']

    CommandLine:
        python -m plottool.plots --exec-multi_plot

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> xdata = [1, 2, 3, 4, 5]
        >>> ydata_list = [[1, 2, 3, 4, 5], [3, 3, 3, 3, 3], [5, 4, np.nan, 2, 1], [4, 3, np.nan, 1, 0]]
        >>> kwargs = {'label_list': ['spam', 'eggs', 'jam', 'pram'],  'linestyle': '-'}
        >>> fig = multi_plot(xdata, ydata_list, **kwargs)
        >>> result = ('fig = %s' % (str(fig),))
        >>> print(result)
        >>> ut.show_if_requested()
    """
    import matplotlib as mpl
    import plottool as pt

    num_lines = len(ydata_list)

    fnum = pt.ensure_fnum(kwargs.get('fnum', None))
    pnum = kwargs.get('pnum', None)

    def parsekw_list(key, kwargs):
        """ copies relevant plot commands into plot_list_kw """
        if key in kwargs:
            val_list = [kwargs[key]] * num_lines
        elif key + '_list' in kwargs:
            val_list = kwargs[key + '_list']
        else:
            val_list = None
            #val_list = [None] * num_lines
        return val_list

    # Parse out arguments to ax.plot
    plot_kw_keys = ['label', 'color', 'marker', 'markersize', 'markeredgewidth', 'linewidth', 'linestyle']
    plot_ks_vals = [parsekw_list(key, kwargs) for key in plot_kw_keys]
    plot_list_kw = dict([(key, vals) for key, vals in zip(plot_kw_keys, plot_ks_vals) if vals is not None])

    if 'color' not in plot_list_kw:
        plot_list_kw['color'] = pt.distinct_colors(num_lines)
    if 'marker' not in plot_list_kw:
        plot_list_kw['marker']  = pt.distinct_markers(num_lines)

    valid_keys = list(plot_list_kw.keys())
    valid_vals = plot_list_kw.values()
    plot_kw_list = [dict(zip(valid_keys, vals)) for vals in zip(*valid_vals)]

    # Parse out axes formating options
    title           = kwargs.get('title', None)
    xlabel          = kwargs.get('xlabel', '')
    ylabel          = kwargs.get('ylabel', '')
    use_legend      = kwargs.get('use_legend', True)
    legend_loc      = kwargs.get('legend_loc', 'best')

    # Setup figure
    fig = pt.figure(fnum=fnum, pnum=pnum)

    # Draw plot lines
    ax = pt.gca()
    xdata = np.array(xdata)
    ydata_list = np.array(ydata_list)
    for ydata, plot_kw in zip(ydata_list, plot_kw_list):
        ymask = np.isfinite(ydata)
        ydata_ = ydata.compress(ymask)
        xdata_ = xdata.compress(ymask)
        ax.plot(xdata_, ydata_, **plot_kw)

    #max_y = max(np.max(y_data), max_y)
    #min_y = np.min(y_data) if min_y is None else min(np.min(y_data), min_y)

    # Setup axes labeling

    labelkw = {
        'fontproperties': mpl.font_manager.FontProperties(weight='light', size=kwargs.get('labelsize', 8))
    }
    ax.set_xlabel(xlabel, **labelkw)
    ax.set_ylabel(ylabel, **labelkw)

    ticksize = kwargs.get('ticksize', None)
    if ticksize is not None:
        for label in ax.get_xticklabels():
            label.set_fontsize(ticksize)
        for label in ax.get_yticklabels():
            label.set_fontsize(ticksize)

    # Setup axes limits
    xmin = kwargs.get('xmin', ax.get_xlim()[0])
    xmax = kwargs.get('xmax', ax.get_xlim()[1])
    ymin = kwargs.get('ymin', ax.get_ylim()[0])
    ymax = kwargs.get('ymax', ax.get_ylim()[1])

    # Setup axes ticks
    num_xticks = kwargs.get('num_xticks', None)
    if num_xticks is not None:
        xticks = np.linspace(xmin, xmax, num_xticks)
        ax.set_xticks(xticks)
        #max_pos = (xdata.max() + 1)
        #step_size = int(max_pos // num_xticks)
        #ax.set_xticks(np.arange(1, max_pos, step_size))
    num_yticks = kwargs.get('num_yticks', None)
    if num_yticks is not None:
        yticks = np.linspace(ymin, ymax, num_yticks)
        #ystep = (ymax - ymin) // (num_yticks - 1)
        #yticks = np.arange(ymin, ymax + ystep, ystep)
        ax.set_yticks(yticks)

    xpad = kwargs.get('xpad', None)
    ypad = kwargs.get('ypad', None)
    xpad_factor = kwargs.get('xpad_factor', None)
    ypad_factor = kwargs.get('ypad_factor', None)
    if xpad is None and xpad_factor is not None:
        xpad = (xmax - xmin) * xpad_factor
    if ypad is None and ypad_factor is not None:
        ypad = (ymax - ymin) * ypad_factor
    xpad = 0 if xpad is None else xpad
    ypad = 0 if ypad is None else ypad
    xmin, xmax = (xmin - xpad), (xmax + xpad)
    ymin, ymax = (ymin - ypad), (ymax + ypad)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # Setup title
    if title is not None:
        titlekw = {
            'fontproperties': mpl.font_manager.FontProperties(weight='light', size=kwargs.get('titlesize', 8))
        }
        ax.set_title(title, **titlekw)

    if use_legend:
        df2.legend(loc=legend_loc, size=kwargs.get('legendsize', 8))

    pt.dark_background()
    return fig


def draw_hist_subbin_maxima(hist, centers=None, bin_colors=None, maxima_thresh=.8):
    r"""
    Args:
        hist (ndarray):
        centers (None):

    CommandLine:
        python -m plottool.plots --test-draw_hist_subbin_maxima --show


    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> import plottool as pt
        >>> # build test data
        >>> hist = np.array([    6.73, 8.69, 0.00, 0.00, 34.62, 29.16, 0.00, 0.00, 6.73, 8.69])
        >>> centers = np.array([-0.39, 0.39, 1.18, 1.96,  2.75,  3.53, 4.32, 5.11, 5.89, 6.68])
        >>> TAU = np.pi * 2
        >>> bin_colors = pt.df2.plt.get_cmap('hsv')(centers / TAU)
        >>> # execute function
        >>> result = draw_hist_subbin_maxima(hist, centers, bin_colors)
        >>> # verify results
        >>> print(result)
        >>> pt.show_if_requested()
    """
    # Find maxima
    maxima_x, maxima_y, argmaxima = htool.hist_argmaxima(hist, centers, maxima_thresh)
    # Expand parabola points around submaxima
    x123, y123 = htool.maxima_neighbors(argmaxima, hist, centers)
    # Find submaxima
    submaxima_x, submaxima_y = htool.interpolate_submaxima(argmaxima, hist, centers)
    xpoints = []
    ypoints = []
    for xtup, ytup in zip(x123.T, y123.T):
        (x1, x2, x3) = xtup  # DUPLICATE CODE!!
        (y1, y2, y3) = ytup  # DUPLICATE CODE!!
        coeff = np.polyfit((x1, x2, x3), (y1, y2, y3), 2)
        x_pts = np.linspace(x1, x3, 50)
        y_pts = np.polyval(coeff, x_pts)
        xpoints.append(x_pts)
        ypoints.append(y_pts)

    maxima_thresh_val = maxima_y.max() * maxima_thresh
    plt.plot(centers, [maxima_thresh_val] * len(centers), 'r--')
    OLD = False
    if OLD:
        plt.plot(centers, hist, 'o-', colors=df2.distinct_colors(len(centers)))            # Draw hist
        plt.plot(centers, hist, 'o-', colors=df2.distinct_colors(len(centers)))            # Draw hist
        plt.plot(centers, hist, 'bo-')            # Draw hist
    else:
        #bin_colors = None
        if bin_colors is None:
            bin_colors = 'r'
            plt.plot(centers, hist, 'w-')
        else:
            # Draw Lines
            #import matplotlib as mpl
            # Create a colormap using exact specified colors
            #bin_cmap = mpl.colors.ListedColormap(bin_colors)
            # HACK USE bin_color somehow
            bin_cmap = plt.get_cmap('hsv')  # HACK
            #mpl.colors.ListedColormap(bin_colors)
            colorline(centers, hist, cmap=bin_cmap)
        # Draw Submax Parabola
        for x_pts, y_pts in zip(xpoints, ypoints):
            plt.plot(x_pts, y_pts, 'y--')
        # Draw maxbin
        plt.scatter(maxima_x,    maxima_y,    marker='o', color='w',  s=50)
        # Draw submaxbin
        plt.scatter(submaxima_x, submaxima_y, marker='*', color='r', s=100)
        # Draw Bins
        plt.scatter(centers, hist, c=bin_colors, marker='o', s=25)
        df2.dark_background()


def zoom_effect01(ax1, ax2, xmin, xmax, **kwargs):
    """
    ax1 : the main axes
    ax1 : the zoomed axes
    (xmin,xmax) : the limits of the colored area in both plot axes.

    connect ax1 & ax2. The x-range of (xmin, xmax) in both axes will
    be marked.  The keywords parameters will be used ti create
    patches.

    References:
        http://matplotlib.org/users/annotations_guide.html
    """
    from matplotlib.transforms import (
        Bbox, TransformedBbox, blended_transform_factory)

    from mpl_toolkits.axes_grid1.inset_locator import (
        BboxPatch, BboxConnector, BboxConnectorPatch)

    def connect_bbox(bbox1, bbox2,
                     loc1a, loc2a, loc1b, loc2b,
                     prop_lines, prop_patches=None):
        if prop_patches is None:
            prop_patches = prop_lines.copy()
            prop_patches["alpha"] = prop_patches.get("alpha", 1) * .01  # * 0.05
        prop_patches["alpha"] = .1

        c1 = BboxConnector(bbox1, bbox2, loc1=loc1a, loc2=loc2a, **prop_lines)
        c1.set_clip_on(False)
        c2 = BboxConnector(bbox1, bbox2, loc1=loc1b, loc2=loc2b, **prop_lines)
        c2.set_clip_on(False)

        bbox_patch1 = BboxPatch(bbox1, **prop_patches)
        bbox_patch2 = BboxPatch(bbox2, **prop_patches)

        p = BboxConnectorPatch(bbox1, bbox2,
                               #loc1a=3, loc2a=2, loc1b=4, loc2b=1,
                               loc1a=loc1a, loc2a=loc2a, loc1b=loc1b, loc2b=loc2b,
                               **prop_patches)
        p.set_clip_on(False)

        return c1, c2, bbox_patch1, bbox_patch2, p

    trans1 = blended_transform_factory(ax1.transData, ax1.transAxes)
    trans2 = blended_transform_factory(ax2.transData, ax2.transAxes)

    bbox = Bbox.from_extents(xmin, 0, xmax, 1)

    mybbox1 = TransformedBbox(bbox, trans1)
    mybbox2 = TransformedBbox(bbox, trans2)

    prop_patches = kwargs.copy()
    prop_patches['ec'] = 'none'
    prop_patches['alpha'] = 0.2

    (c1, c2, bbox_patch1, bbox_patch2, p) = \
        connect_bbox(mybbox1, mybbox2,
                     loc1a=3, loc2a=2, loc1b=4, loc2b=1,
                     prop_lines=kwargs, prop_patches=prop_patches)

    ax1.add_patch(bbox_patch1)
    ax2.add_patch(bbox_patch2)
    ax2.add_patch(c1)
    ax2.add_patch(c2)
    ax2.add_patch(p)

    return c1, c2, bbox_patch1, bbox_patch2, p

# Interface to LineCollection:


def colorline(x, y, z=None, cmap=plt.get_cmap('hsv'), norm=plt.Normalize(0.0, 1.0), linewidth=1, alpha=1.0):
    """
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width

    References:
        http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb

    CommandLine:
        python -m plottool.plots --test-colorline --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> import plottool as pt
        >>> # build test data
        >>> x = np.array([1, 3, 3, 2, 5]) / 5.0
        >>> y = np.array([1, 2, 1, 3, 5]) / 5.0
        >>> z = None
        >>> cmap = df2.plt.get_cmap('hsv')
        >>> norm = plt.Normalize(0.0, 1.0)
        >>> linewidth = 1
        >>> alpha = 1.0
        >>> # execute function
        >>> pt.figure()
        >>> result = colorline(x, y, z, cmap)
        >>> # verify results
        >>> print(result)
        >>> pt.dark_background()
        >>> pt.show_if_requested()
    """
    from matplotlib.collections import LineCollection

    def make_segments(x, y):
        """
        Create list of line segments from x and y coordinates, in the
        Returns:
            ndarray - segments in correct format for LineCollection:
                an array with shape: (numlines, points per line, 2)
                the last dimension is for x and y respectively
        """
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        return segments

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = LineCollection(segments, array=z, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc


def plot_stems(x_data, y_data, fnum=None, pnum=(1, 1, 1)):
    """

    CommandLine:
        python -m plottool.plots --test-plot_stems
        python -m plottool.plots --test-plot_stems --show

    Example:
        >>> from plottool import *  # NOQA
        >>> import plottool as pt
        >>> x_data = [1, 1, 2, 3, 3, 3, 4, 4, 5]
        >>> y_data = [1, 2, 1, 2, 1, 4, 4, 5, 1]
        >>> pt.plots.plot_stems(x_data, y_data)
        >>> pt.show_if_requested()
    """
    if fnum is None:
        fnum = df2.next_fnum()
    df2.figure(fnum=fnum, pnum=pnum, doclf=False, docla=False)
    df2.draw_stems(x_data, y_data)
    df2.set_xlabel('query index')
    df2.set_ylabel('query ranks')
    df2.dark_background()
    df2.set_figtitle('plot_stems')
    df2.legend(loc='upper left')
    df2.iup()


def plot_probabilities(prob_list,
                       prob_lbls=None,
                       prob_colors=None,
                       xdata=None,
                       prob_thresh=None,
                       figtitle='plot_probabilities',
                       fnum=None,
                       pnum=(1, 1, 1)):
    """
    Input: a list of scores (either chip or descriptor)

    Concatenates and sorts the scores
    Sorts and plots with different types of scores labeled
    """
    assert len(prob_list) > 0
    if xdata is None:
        xdata = np.arange(len(prob_list[0]))
    assert all([len(xdata) == len(density) for density in prob_list])

    if prob_lbls is None:
        prob_lbls = [lblx for lblx in range(len(prob_list))]
    if prob_colors is None:
        prob_colors = df2.distinct_colors(len(prob_list))[::-1]

    assert len(prob_list) == len(prob_lbls)
    assert len(prob_list) == len(prob_colors)
    #labelx_list = [[lblx] * len(scores_) for lblx, scores_ in enumerate(prob_list)]
    #agg_scores  = np.hstack()
    #agg_labelx  = np.hstack(labelx_list)
    #agg_sortx = agg_scores.argsort()

    if fnum is None:
        fnum = df2.next_fnum()

    df2.figure(fnum=fnum, pnum=pnum, doclf=False, docla=False)

    for tup in zip(prob_list, prob_lbls, prob_colors):
        density, label, color = tup
        ydata = density
        df2.plot(xdata, ydata, color=color, label=label, alpha=.7)
        #ut.embed()
        #help(df2.plot)

    if prob_thresh is not None:
        df2.plot(xdata, [prob_thresh] * len(xdata), 'g-', label='prob thresh')

    ax = df2.gca()
    ax.set_xlim(xdata.min(), xdata.max())
    df2.set_xlabel('score value')
    df2.set_ylabel('probability')
    df2.dark_background()
    df2.set_title(figtitle)
    df2.legend(loc='upper left')
    #df2.iup()


# Short alias
plot_probs = plot_probabilities
# Incorrect (but legacy) alias
plot_densities = plot_probabilities


def plot_sorted_scores(scores_list,
                       scores_lbls=None,
                       score_markers=None,
                       score_colors=None,
                       markersizes=None,
                       fnum=None,
                       pnum=(1, 1, 1),
                       logscale=True,
                       figtitle=None,
                       score_label='score',
                       threshold_value=None,
                       use_stems=None):
    """
    Concatenates and sorts the scores
    Sorts and plots with different types of scores labeled

    Args:
        scores_list (list): a list of scores
        scores_lbls (None):
        score_markers (None):
        score_colors (None):
        markersizes (None):
        fnum (int):  figure number
        pnum (tuple):  plot number
        logscale (bool):
        figtitle (str):

    CommandLine:
        python -m plottool.plots --test-plot_sorted_scores --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> randstate = np.random.RandomState(seed=0)
        >>> # Get a training sample
        >>> tp_support = randstate.normal(loc=6.5, size=(256,))
        >>> tn_support = randstate.normal(loc=3.5, size=(256,))
        >>> scores_list = [tp_support, tn_support]
        >>> scores_lbls = None
        >>> score_markers = None
        >>> score_colors = None
        >>> markersizes = None
        >>> fnum = None
        >>> pnum = (1, 1, 1)
        >>> logscale = True
        >>> figtitle = 'plot_sorted_scores'
        >>> result = plot_sorted_scores(scores_list, scores_lbls, score_markers, score_colors, markersizes, fnum, pnum, logscale, figtitle)
        >>> ut.show_if_requested()
        >>> print(result)
    """
    if figtitle is None:
        figtitle = 'sorted ' + score_label
    if scores_lbls is None:
        scores_lbls = [lblx for lblx in range(len(scores_list))]
    if score_markers is None:
        score_markers = ['o' for lblx in range(len(scores_list))]
    if score_colors is None:
        score_colors = df2.distinct_colors(len(scores_list))[::-1]
    if markersizes is None:
        markersizes = [12 / (1.0 + lblx) for lblx in range(len(scores_list))]
    labelx_list = [[lblx] * len(scores_) for lblx, scores_ in enumerate(scores_list)]
    agg_scores  = np.hstack(scores_list)
    agg_labelx  = np.hstack(labelx_list)

    agg_sortx = agg_scores.argsort()

    sorted_scores = agg_scores[agg_sortx]
    sorted_labelx = agg_labelx[agg_sortx]

    if fnum is None:
        fnum = df2.next_fnum()

    df2.figure(fnum=fnum, pnum=pnum, doclf=False, docla=False)

    # plot stems to get a better sense of the distribution for binary data
    if use_stems is None:
        use_stems = len(scores_list) == 2
    if use_stems:
        ymax = sorted_scores.max()
        absolute_bottom = sorted_scores.min()
        for lblx in range(len(scores_list)):
            bottom = (absolute_bottom - (ymax * .1)) if lblx % 2 == 1 else ymax
            color = score_colors[lblx]
            xdata = np.where(sorted_labelx == lblx)[0]
            ydata = sorted_scores[xdata]
            # TODO: stems for binary labels
            df2.draw_stems(xdata, ydata, setlims=False, color=color, markersize=0, bottom=bottom)
            pass

    # Plot each datapoint on a line
    for lblx in range(len(scores_list)):
        label = scores_lbls[lblx]
        color = score_colors[lblx]
        marker = score_markers[lblx]
        markersize = markersizes[lblx]
        xdata = np.where(sorted_labelx == lblx)[0]
        ydata = sorted_scores[xdata]
        #printDBG('[sorted_scores] lblx=%r label=%r, marker=%r' % (lblx, label, marker))
        df2.plot(xdata, ydata, marker, color=color, label=label, alpha=.7,
                 markersize=markersize)

    if threshold_value is not None:
        indicies = np.arange(len(sorted_labelx))
        #print('indicies.shape = %r' % (indicies.shape,))
        df2.plot(indicies, [threshold_value] * len(indicies), 'g-', label='thresh')

    if logscale:
        set_logyscale_from_data(sorted_scores)

    ax = df2.gca()
    # dont let xlimit go far over the number of labels
    ax.set_xlim(0, len(sorted_labelx) + 1)

    df2.set_xlabel('sorted ' +  score_label + ' indices')
    df2.set_ylabel(score_label)
    df2.dark_background()
    df2.set_title(figtitle)
    df2.legend(loc='upper left')
    #df2.iup()


def plot_score_histograms(scores_list,
                          scores_lbls=None,
                          score_markers=None,
                          score_colors=None,
                          markersizes=None,
                          fnum=None,
                          pnum=(1, 1, 1),
                          figtitle=None,
                          score_label='score',
                          threshold_value=None):
    """
    CommandLine:
        python -m plottool.plots --test-plot_score_histograms --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> randstate = np.random.RandomState(seed=0)
        >>> # Get a training sample
        >>> tp_support = randstate.normal(loc=6.5, size=(256,))
        >>> tn_support = randstate.normal(loc=3.5, size=(256,))
        >>> scores_list = [tp_support, tn_support]
        >>> scores_lbls = None
        >>> score_markers = None
        >>> score_colors = None
        >>> markersizes = None
        >>> fnum = None
        >>> pnum = (1, 1, 1)
        >>> logscale = True
        >>> figtitle = 'plot_scores_histogram'
        >>> result = plot_score_histograms(scores_list, scores_lbls, score_markers, score_colors, markersizes, fnum, pnum, logscale, figtitle)
        >>> ut.show_if_requested()
        >>> print(result)
    """
    if figtitle is None:
        figtitle = 'histogram of ' + score_label
    if scores_lbls is None:
        scores_lbls = [lblx for lblx in range(len(scores_list))]
    if score_markers is None:
        score_markers = ['o' for lblx in range(len(scores_list))]
    if score_colors is None:
        score_colors = df2.distinct_colors(len(scores_list))[::-1]
    if markersizes is None:
        markersizes = [12 / (1.0 + lblx) for lblx in range(len(scores_list))]
    #labelx_list = [[lblx] * len(scores_) for lblx, scores_ in enumerate(scores_list)]
    agg_scores  = np.hstack(scores_list)

    dmin = agg_scores.min()
    dmax = agg_scores.max()

    # References: http://stats.stackexchange.com/questions/798/calculating-optimal-number-of-bins-in-a-histogram-for-n-where-n-ranges-from-30
    #bandwidth = diff(range(x)) / (2 * IQR(x) / length(x) ^ (1 / 3)))

    if fnum is None:
        fnum = df2.next_fnum()

    df2.figure(fnum=fnum, pnum=pnum, doclf=False, docla=False)

    bins = None

    # Plot each datapoint on a line
    for lblx in range(len(scores_list)):
        label = scores_lbls[lblx]
        color = score_colors[lblx]
        #marker = score_markers[lblx]
        data = scores_list[lblx]

        dmin = int(np.floor(data.min()))
        dmax = int(np.ceil(data.max()))
        if bins is None:
            bins = dmax - dmin
        ax  = df2.gca()
        ax.hist(data, bins=100,
                #range=(dmin, dmax),
                label=str(label),
                color=color, alpha=.5)

    #if threshold_value is not None:
    #    indicies = np.arange(len(sorted_labelx))
    #    #print('indicies.shape = %r' % (indicies.shape,))
    #    df2.plot(indicies, [threshold_value] * len(indicies), 'g-', label='thresh')

    #ax = df2.gca()
    ## dont let xlimit go far over the number of labels
    #ax.set_xlim(0, len(sorted_labelx) + 1)

    #df2.set_xlabel('sorted ' +  score_label + ' indices')
    df2.set_xlabel(score_label)
    df2.set_ylabel('frequency')
    df2.dark_background()
    df2.set_title(figtitle)
    df2.legend(loc='upper left')
    print('[df2] show_histogram()')
    df2.dark_background()
    #return fig


def set_logyscale_from_data(y_data):
    if len(y_data) == 1:
        print('Warning: not enough information to infer yscale')
        return
    logscale_kwargs = get_good_logyscale_kwargs(y_data)
    ax = df2.gca()
    ax.set_yscale('symlog', **logscale_kwargs)


def get_good_logyscale_kwargs(y_data, adaptive_knee_scaling=False):
    # Attempts to detect knee points by looking for
    # log derivatives way past the normal standard deviations
    # The input data is assumed to be sorted and y_data
    basey = 10
    nStdDevs_thresh = 10
    # Take the log of the data
    logy = np.log(y_data)
    logy[np.isnan(logy)] = 0
    logy[np.isinf(logy)] = 0
    # Find the derivative of data
    dy = np.diff(logy)
    dy_sortx = dy.argsort()
    # Get mean and standard deviation
    dy_stats = utool.get_stats(dy)
    dy_sorted = dy[dy_sortx]
    # Find the number of standard deveations past the mean each datapoint is
    try:
        nStdDevs = np.abs(dy_sorted - dy_stats['mean']) / dy_stats['std']
    except Exception as ex:
        utool.printex(ex, key_list=['dy_stats',
                                    (len, 'y_data'),
                                    'y_data',
                                    ])
        raise
    # Mark any above a threshold as knee points
    knee_indexes = np.where(nStdDevs > nStdDevs_thresh)[0]
    knee_mag = nStdDevs[knee_indexes]
    knee_points = dy_sortx[knee_indexes]
    #printDBG('[df2] knee_points = %r' % (knee_points,))
    # Check to see that we have found a knee
    if len(knee_points) > 0 and adaptive_knee_scaling:
        # Use linear scaling up the the knee points and
        # scale it by the magnitude of the knee
        kneex = knee_points.argmin()
        linthreshx = knee_points[kneex] + 1
        linthreshy = y_data[linthreshx] * basey
        linscaley = min(2, max(1, (knee_mag[kneex] / (basey * 2))))
    else:
        linthreshx = 1E2
        linthreshy = 1E2
        linscaley = 1
    logscale_kwargs = {
        'basey': basey,
        'nonposx': 'clip',
        'nonposy': 'clip',
        'linthreshy': linthreshy,
        'linthreshx': linthreshx,
        'linscalex': 1,
        'linscaley': linscaley,
    }
    #print(logscale_kwargs)
    return logscale_kwargs


def plot_pdf(data, draw_support=True, scale_to=None, label=None, color=0,
             nYTicks=3):
    fig = df2.gcf()
    ax = df2.gca()
    data = np.array(data)
    if len(data) == 0:
        warnstr = '[df2] ! Warning: len(data) = 0. Cannot visualize pdf'
        warnings.warn(warnstr)
        df2.draw_text(warnstr)
        return
    if len(data) == 1:
        warnstr = '[df2] ! Warning: len(data) = 1. Cannot visualize pdf'
        warnings.warn(warnstr)
        df2.draw_text(warnstr)
        return
    bw_factor = .05
    if isinstance(color, (int, float)):
        colorx = color
        line_color = plt.get_cmap('gist_rainbow')(colorx)
    else:
        line_color = color

    # Estimate a pdf
    data_pdf = estimate_pdf(data, bw_factor)
    # Get probability of seen data
    prob_x = data_pdf(data)
    # Get probability of unseen data data
    x_data = np.linspace(0, data.max(), 500)
    y_data = data_pdf(x_data)
    # Scale if requested
    if scale_to is not None:
        scale_factor = scale_to / y_data.max()
        y_data *= scale_factor
        prob_x *= scale_factor
    #Plot the actual datas on near the bottom perterbed in Y
    if draw_support:
        pdfrange = prob_x.max() - prob_x.min()
        perb   = (np.random.randn(len(data))) * pdfrange / 30.
        preb_y_data = np.abs([pdfrange / 50. for _ in data] + perb)
        ax.plot(data, preb_y_data, 'o', color=line_color, figure=fig, alpha=.1)
    # Plot the pdf (unseen data)
    ax.plot(x_data, y_data, color=line_color, label=label)
    if nYTicks is not None:
        yticks = np.linspace(min(y_data), max(y_data), nYTicks)
        ax.set_yticks(yticks)


def estimate_pdf(data, bw_factor):
    try:
        data_pdf = scipy.stats.gaussian_kde(data, bw_factor)
        data_pdf.covariance_factor = bw_factor
    except Exception as ex:
        print('[df2] ! Exception while estimating kernel density')
        print('[df2] data=%r' % (data,))
        print('[df2] ex=%r' % (ex,))
        raise
    return data_pdf


def interval_stats_plot(param2_stat_dict, fnum=None, pnum=(1, 1, 1), x_label='',
                        y_label='', title=''):
    r"""

    interval plot for displaying mean, range, and std

    Args:
        fnum (int):  figure number
        pnum (tuple):  plot number

    CommandLine:
        python -m plottool.plots --test-interval_stats_plot
        python -m plottool.plots --test-interval_stats_plot --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> import plottool as pt
        >>> # build test data
        >>> param2_stat_dict = {
        ...     0.5: dict([('max', 0.0584), ('min', 0.0543), ('mean', 0.0560), ('std', 0.00143),]),
        ...     0.6: dict([('max', 0.0593), ('min', 0.0538), ('mean', 0.0558), ('std', 0.00178),]),
        ...     0.7: dict([('max', 0.0597), ('min', 0.0532), ('mean', 0.0556), ('std', 0.00216),]),
        ...     0.8: dict([('max', 0.0601), ('min', 0.0525), ('mean', 0.0552), ('std', 0.00257),]),
        ...     0.9: dict([('max', 0.0604), ('min', 0.0517), ('mean', 0.0547), ('std', 0.00300),]),
        ...     1.0: dict([('max', 0.0607), ('min', 0.0507), ('mean', 0.0541), ('std', 0.00345),])
        ... }
        >>> fnum = None
        >>> pnum = (1, 1, 1)
        >>> title = 'p vs score'
        >>> x_label = 'p'
        >>> y_label = 'score diff'
        >>> # execute function
        >>> result = interval_stats_plot(param2_stat_dict, fnum, pnum, x_label, y_label, title)
        >>> df2.show_if_requested()
        >>> # verify results
        >>> print(result)
    """
    if fnum is None:
        fnum = df2.next_fnum()
    import six
    x_data = np.array(list(six.iterkeys(param2_stat_dict)))
    sortx = x_data.argsort()
    x_data_sort = x_data[sortx]
    from matplotlib import pyplot as plt
    # Prepare y data for boxplot
    y_data_keys = ['std', 'mean', 'max', 'min']
    y_data_dict = list(six.itervalues(param2_stat_dict))
    def get_dictlist_key(dict_list, key):
        return [dict_[key] for dict_ in dict_list]
    y_data_components = [get_dictlist_key(y_data_dict, key) for key in y_data_keys]
    # The stacking is pretty much not needed anymore, but whatever
    y_data_sort = np.vstack(y_data_components)[:, sortx]
    y_data_std_sort  = y_data_sort[0]
    y_data_mean_sort = y_data_sort[1]
    y_data_max_sort  = y_data_sort[2]
    y_data_min_sort  = y_data_sort[3]
    y_data_stdlow_sort  = y_data_mean_sort - y_data_std_sort
    y_data_stdhigh_sort = y_data_mean_sort + y_data_std_sort
    FIX_STD_SYMETRY = True
    if FIX_STD_SYMETRY:
        # Standard deviation is symetric where min and max are not.
        # To avoid weird looking plots clip the stddev fillbetweens
        # at the min and max
        #ut.embed()
        outlier_min_std = y_data_stdlow_sort  < y_data_min_sort
        outlier_max_std = y_data_stdhigh_sort > y_data_max_sort
        y_data_stdlow_sort[outlier_min_std]  =  y_data_min_sort[outlier_min_std]
        y_data_stdhigh_sort[outlier_max_std] =  y_data_max_sort[outlier_max_std]
    # Make firgure
    fig = df2.figure(fnum=fnum, pnum=pnum, doclf=False, docla=False)
    ax = plt.gca()
    # Plot max and mins
    ax.fill_between(x_data_sort, y_data_min_sort, y_data_max_sort, alpha=.2, color='g', label='range')
    df2.append_phantom_legend_label('range', 'g', alpha=.2)
    # Plot standard deviations
    ax.fill_between(x_data_sort, y_data_stdlow_sort, y_data_stdhigh_sort, alpha=.4, color='b', label='std')
    df2.append_phantom_legend_label('std', 'b', alpha=.4)
    # Plot means
    ax.plot(x_data_sort, y_data_mean_sort, 'o-', color='b', label='mean')
    df2.append_phantom_legend_label('mean', 'b', 'line')
    df2.show_phantom_legend_labels()
    df2.set_xlabel(x_label)
    df2.set_ylabel(y_label)
    df2.set_title(title)
    return fig
    #df2.dark_background()
    #plt.show()


def interval_line_plot(xdata, ydata_mean, y_data_std, color=[1, 0, 0], label=None, marker='o', linestyle='-'):
    r"""
    Args:
        xdata (?):
        ydata_mean (?):
        y_data_std (?):

    CommandLine:
        python -m plottool.plots --test-interval_line_plot --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> xdata = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> ydata_mean = [2, 3, 4, 3, 3, 2, 2, 2]
        >>> y_data_std = [1, 2, 1, 1, 3, 2, 2, 1]
        >>> result = interval_line_plot(xdata, ydata_mean, y_data_std)
        >>> print(result)
        >>> ut.show_if_requested()
    """
    xdata = np.array(xdata)
    ydata_mean = np.array(ydata_mean)
    y_data_std = np.array(y_data_std)
    y_data_max = ydata_mean + y_data_std
    y_data_min = ydata_mean - y_data_std
    ax = df2.gca()
    ax.fill_between(xdata, y_data_min, y_data_max, alpha=.2, color=color)
    ax.plot(xdata, ydata_mean, marker=marker, color=color, label=label, linestyle=linestyle)
    return


def plot_search_surface(known_nd_data, known_target_points, nd_labels, target_label, fnum=None, pnum=None, title=None):
    r"""
    Args:
        known_nd_data (?): should be integral for now
        known_target_points (?):
        nd_labels (?):
        target_label (?):
        fnum (int):  figure number(default = None)

    Returns:
        ?: ax

    CommandLine:
        python -m plottool.plots --exec-plot_search_surface --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.plots import *  # NOQA
        >>> known_nd_data = np.array([x.flatten() for x in np.meshgrid(*[np.linspace(-20, 20, 10).astype(np.int32), np.linspace(-20, 20, 10).astype(np.int32)])]).T
        >>> # complicated polynomial target
        >>> known_target_points = -.001 * known_nd_data.T[0] ** 4 + .25 * known_nd_data.T[1] ** 2 - .0005 * known_nd_data.T[1] ** 4 + .001 * known_nd_data.T[1] ** 3
        >>> nd_labels = ['big-dim', 'small-dim']
        >>> target_label = ['score']
        >>> fnum = 1
        >>> ax = plot_search_surface(known_nd_data, known_target_points, nd_labels, target_label, fnum)
        >>> ut.show_if_requested()
    """
    import plottool as pt
    from mpl_toolkits.mplot3d import Axes3D  # NOQA
    fnum = pt.ensure_fnum(fnum)
    print('fnum = %r' % (fnum,))
    #pt.figure(fnum=fnum, pnum=pnum, doclf=pnum is None, projection='3d')
    pt.figure(fnum=fnum, pnum=pnum, doclf=pnum is None)

    # Convert our non-uniform grid into a uniform grid using gcd
    def compute_interpolation_grid(known_nd_data, pad_steps=0):
        """ use gcd to get the number of steps to take in each dimension """
        import fractions
        ug_steps = [reduce(fractions.gcd, np.unique(x_).tolist()) for x_ in known_nd_data.T]
        ug_min   = known_nd_data.min(axis=0)
        ug_max   = known_nd_data.max(axis=0)
        ug_basis = [
            np.arange(min_ - (step_ * pad_steps), max_ + (step_ * (pad_steps + 1)), step_)
            for min_, max_, step_ in zip(ug_min, ug_max, ug_steps)
        ]
        ug_shape = tuple([basis.size for basis in ug_basis][::-1])
        # ig = interpolated grid
        unknown_nd_data = np.vstack([_pts.flatten() for _pts in np.meshgrid(*ug_basis)]).T
        return unknown_nd_data, ug_shape

    def interpolate_error(known_nd_data, known_target_points, unknown_nd_data):
        """
        References:
            http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.griddata.html
        """
        #method = 'cubic'  # {'linear', 'nearest', 'cubic'}
        method = 'linear'  # {'linear', 'nearest', 'cubic'}
        import scipy as sp
        interpolated_targets = sp.interpolate.griddata(known_nd_data, known_target_points, unknown_nd_data, method=method)
        #interpolated_targets[np.isnan(interpolated_targets)] = known_target_points.max() * 2
        interpolated_targets[np.isnan(interpolated_targets)] = known_target_points.min()
        return interpolated_targets

    # Interpolate uniform grid positions
    if len(known_nd_data.T) == 1 or ut.list_allsame(known_nd_data.T[1]):
        xdata = known_nd_data.T[0]
        ydata = known_target_points
        pt.plot(xdata, ydata)
        ax = pt.gca()
        if len(known_nd_data.T) == 2:
            ax.set_xlabel(nd_labels[0] + ' (const:' + nd_labels[1] + '=%r)' % (known_nd_data.T[1][0],))
        else:
            ax.set_xlabel(nd_labels[0])
        ax.set_ylabel(target_label)
    else:
        unknown_nd_data, ug_shape = compute_interpolation_grid(known_nd_data, 0 * 5)
        interpolated_error = interpolate_error(known_nd_data, known_target_points, unknown_nd_data)
        import matplotlib as mpl

        label_fontprop = mpl.font_manager.FontProperties(weight='light', size=8)
        title_fontprop = mpl.font_manager.FontProperties(weight='light', size=10)
        labelkw = dict(labelpad=1000, fontproperties=label_fontprop)
        titlekw = dict(fontproperties=title_fontprop)

        ax = pt.plot_surface3d(
            unknown_nd_data.T[0].reshape(ug_shape),
            unknown_nd_data.T[1].reshape(ug_shape),
            interpolated_error.reshape(ug_shape),
            xlabel=nd_labels[0],
            ylabel=nd_labels[1],
            zlabel=target_label,
            labelkw=labelkw,
            titlekw=titlekw,
            rstride=1, cstride=1,
            pnum=pnum,
            #cmap=pt.plt.get_cmap('jet'),
            cmap=pt.plt.get_cmap('coolwarm'),
            #wire=True,
            #mode='wire',
            title=title,
            mode='surface',
            alpha=.7,
            contour=True,
            #mode='contour',
            #norm=pt.mpl.colors.Normalize(0, 1),
            #shade=False,
            #dark=False,
        )
        #ax.scatter(known_nd_data.T[0], known_nd_data.T[1], known_target_points, s=100, c=pt.YELLOW)
        ax.scatter(known_nd_data.T[0], known_nd_data.T[1], known_target_points, s=10, c=pt.YELLOW)
        ax.set_aspect('auto')
        #given_data_dims = [0]
        #assert len(given_data_dims) == 1, 'can only plot 1 given data dim'
        #xdim = given_data_dims[0]
        #xdim = 0
        #ydim = (xdim + 1) % (len(known_nd_data.T))
        #known_nd_min = known_nd_data.min(axis=0)
        #known_nd_max = known_nd_data.max(axis=0)
        #xmin, xmax = known_nd_min[xdim], known_nd_max[xdim]
        #ymin, ymax = known_nd_min[ydim], known_nd_max[ydim]
        #zmin, zmax = known_target_points.min(), known_target_points.max()

        ##ax.set_xlim(xmin, xmax * 1.05)
        ##ax.set_ylim(ymin, ymax * 1.05)
        ##ax.set_zlim(zmin, zmax * 1.05)
        ##ax.set_xlim(0, xmax + 1)
        ##ax.set_ylim(0, ymax + 1)
        ##ax.set_zlim(0, zmax + 1)
        for label in ax.get_xticklabels():
            label.set_fontsize(6)
        for label in ax.get_yticklabels():
            label.set_fontsize(6)
        for label in ax.get_zticklabels():
            label.set_fontsize(6)
        #import matplotlib.ticker as mtick
        #ax.zaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
        #ax.zaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
        #ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
        #ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
    return ax


if __name__ == '__main__':
    """
    CommandLine:
        python -m plottool.plots
        python -m plottool.plots --allexamples
        python -m plottool.plots --allexamples --noface --nosrc
    """
    import multiprocessing
    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA
    ut.doctest_funcs()
