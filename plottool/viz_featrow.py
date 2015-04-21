from __future__ import absolute_import, division, print_function
import utool as ut  # NOQA
import six
import plottool.draw_func2 as df2
from plottool import plot_helpers as ph
from plottool import custom_constants
from plottool import custom_figure
#(print, print_, printDBG, rrr, profile) = ut.inject(
#    __name__, '[viz_featrow]', DEBUG=False)
ut.noinject(__name__, '[viz_featrow]')


def precisionstr(c='E', pr=2):
    return '%.' + str(pr) + c


def formatdist(val):
    pr = 3
    if val > 1000:
        return precisionstr('E', pr) % val
    elif val > .01 or val == 0:
        return precisionstr('f', pr) % val
    else:
        return precisionstr('e', pr) % val


#@ut.indent_func
def draw_feat_row(chip, fx, kp, sift, fnum, nRows, nCols, px, prevsift=None,
                  origsift=None, aid=None, info='', type_=None,
                  shape_labels=False, vecfield=False, multicolored_arms=False,
                  draw_warped=True, draw_unwarped=True, rect=True, ori=True, pts=False):
    """
    draw_feat_row

    SeeAlso:
        ibeis.viz.viz_nearest_descriptors
        ~/code/ibeis/ibeis/viz/viz_nearest_descriptors.py

    CommandLine:
        python -m plottool.viz_featrow --test-draw_feat_row --show
        python -m plottool.viz_featrow --test-draw_feat_row --dpath figures --save ~/latex/crall-candidacy-2015/figures/viz_featrow.jpg

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.viz_featrow import *  # NOQA
        >>> import plottool as pt
        >>> # build test data
        >>> kpts, vecs, imgBGR = pt.viz_keypoints.testdata_kpts()
        >>> chip = imgBGR
        >>> fx = 0
        >>> kp = kpts[fx]
        >>> sift = vecs[fx]
        >>> fnum = 1
        >>> nRows = 1
        >>> nCols = 2
        >>> px = 0
        >>> prevsift = None
        >>> origsift = None
        >>> aid = None
        >>> info = ''
        >>> type_ = None
        >>> shape_labels = False
        >>> vecfield = False
        >>> multicolored_arms = True
        >>> draw_unwarped = False
        >>> draw_warped = True
        >>> # execute function
        >>> result = draw_feat_row(chip, fx, kp, sift, fnum, nRows, nCols, px, prevsift, origsift, aid, info, type_, shape_labels, vecfield, multicolored_arms, draw_warped, draw_unwarped, rect=False, ori=False, pts=False)
        >>> # verify results
        >>> print(result)
        >>> pt.show_if_requested()
    """
    import itertools

    pnum_ = df2.get_pnum_func(nRows, nCols, base=1)
    countgen = itertools.count(1)

    #pnumgen_ = df2.make_pnum_nextgen(nRows, nCols, base=1)

    def _draw_patch(**kwargs):
        return df2.draw_keypoint_patch(chip, kp, sift, rect=rect, ori=ori, pts=pts,
                                       ori_color=custom_constants.DEEP_PINK,
                                       multicolored_arms=multicolored_arms,
                                       **kwargs)

    # Feature strings
    xy_str, shape_str, scale, ori_str = ph.kp_info(kp)

    if draw_unwarped:
        # Draw the unwarped selected feature
        ax = _draw_patch(fnum=fnum, pnum=pnum_(px + six.next(countgen)))
        ph.set_plotdat(ax, 'viztype', 'unwarped')
        ph.set_plotdat(ax, 'aid', aid)
        ph.set_plotdat(ax, 'fx', fx)
        if shape_labels:
            unwarped_lbl = 'affine feature invV =\n' + shape_str + '\n' + ori_str
            custom_figure.set_xlabel(unwarped_lbl, ax)

    if draw_warped:
        # Draw the warped selected feature
        ax = _draw_patch(fnum=fnum, pnum=pnum_(px + six.next(countgen)), warped=True)
        ph.set_plotdat(ax, 'viztype', 'warped')
        ph.set_plotdat(ax, 'aid', aid)
        ph.set_plotdat(ax, 'fx', fx)
        if shape_labels:
            warped_lbl = ('warped feature\n' +
                          'fx=%r scale=%.1f\n' +
                          '%s') % (fx, scale, xy_str)
        else:
            warped_lbl = ''
        warped_lbl += info
        custom_figure.set_xlabel(warped_lbl, ax)

    border_color = {None: None,
                    'query': None,
                    'match': custom_constants.BLUE,
                    'norm': custom_constants.ORANGE}[type_]
    if border_color is not None:
        df2.draw_border(ax, color=border_color)

    # Draw the SIFT representation
    pnum = pnum_(px + six.next(countgen))
    if ph.SIFT_OR_VECFIELD or vecfield:
        custom_figure.figure(fnum=fnum, pnum=pnum)
        df2.draw_keypoint_gradient_orientations(chip, kp, sift=sift)
    else:
        sigtitle =  'sift histogram' if (px % 3) == 0 else ''
        ax = df2.plot_sift_signature(sift, sigtitle, fnum=fnum, pnum=pnum)
        ax._hs_viztype = 'histogram'
    #dist_list = ['L1', 'L2', 'hist_isect', 'emd']
    #dist_list = ['L2', 'hist_isect']
    #dist_list = ['L2']
    #dist_list = ['bar_L2_sift', 'cos_sift']
    dist_list = ['L2_sift', 'bar_cos_sift']
    dist_str_list = []
    if origsift is not None:
        distmap_orig = ut.compute_distances(sift, origsift, dist_list)
        dist_str_list.append(
            'query_dist: ' + ', '.join(['(%s, %s)' % (key, formatdist(val))
                                        for key, val in six.iteritems(distmap_orig)])
        )
    if prevsift is not None:
        distmap_prev = ut.compute_distances(sift, prevsift, dist_list)
        dist_str_list.append(
            'prev_dist: ' + ', '.join(['(%s, %s)' % (key, formatdist(val))
                                       for key, val in six.iteritems(distmap_prev)])
        )
    dist_str = '\n'.join(dist_str_list)
    custom_figure.set_xlabel(dist_str)
    return px + nCols


if __name__ == '__main__':
    """
    CommandLine:
        python -m plottool.viz_featrow
        python -m plottool.viz_featrow --allexamples
        python -m plottool.viz_featrow --allexamples --noface --nosrc
    """
    import multiprocessing
    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA
    ut.doctest_funcs()
