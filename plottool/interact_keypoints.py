from __future__ import absolute_import, division, print_function
import utool as ut
from plottool import draw_func2 as df2
from plottool import plot_helpers as ph
from plottool import interact_helpers as ih
from plottool.viz_featrow import draw_feat_row
from plottool.viz_keypoints import show_keypoints

(print, print_, printDBG, rrr, profile) = ut.inject(__name__, '[interact_kpts]', DEBUG=False)


def ishow_keypoints(chip, kpts, desc, fnum=0, figtitle=None, nodraw=False, **kwargs):
    """

    CommandLine:
        python -m plottool.interact_keypoints --test-ishow_keypoints --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from plottool.interact_keypoints import *  # NOQA
        >>> import numpy as np
        >>> import plottool as pt
        >>> import utool as ut
        >>> import pyhesaff
        >>> import vtool as vt
        >>> kpts, vecs, imgBGR = pt.viz_keypoints.testdata_kpts()
        >>> ut.quit_if_noshow()
        >>> pt.interact_keypoints.ishow_keypoints(imgBGR, kpts, vecs, ori=True, ell_alpha=.4, color='distinct')
        >>> pt.show_if_requested()
    """
    fig = ih.begin_interaction('keypoint', fnum)
    annote_ptr = [1]

    self = ut.DynStruct()  # MOVE TO A CLASS INTERACTION
    self.kpts = kpts
    self.desc = desc

    def _select_ith_kpt(fx):
        print_('[interact] viewing ith=%r keypoint' % fx)
        # Get the fx-th keypiont
        kp, sift = kpts[fx], desc[fx]
        # Draw the image with keypoint fx highlighted
        _viz_keypoints(fnum, (2, 1, 1), sel_fx=fx, **kwargs)  # MAYBE: remove kwargs
        # Draw the selected feature
        nRows, nCols, px = (2, 3, 3)
        draw_feat_row(chip, fx, kp, sift, fnum, nRows, nCols, px, None)

    def _viz_keypoints(fnum, pnum=(1, 1, 1), **kwargs):
        df2.figure(fnum=fnum, docla=True, doclf=True)
        show_keypoints(chip, kpts, fnum=fnum, pnum=pnum, **kwargs)
        if figtitle is not None:
            df2.set_figtitle(figtitle)

    def _on_keypoints_click(event):
        print_('[viz] clicked keypoint view')
        if event is None  or event.xdata is None or event.inaxes is None:
            annote_ptr[0] = (annote_ptr[0] + 1) % 3
            mode = annote_ptr[0]
            draw_ell = mode == 1
            draw_pts = mode == 2
            print('... default kpts view mode=%r' % mode)
            _viz_keypoints(fnum, draw_ell=draw_ell, draw_pts=draw_pts, **kwargs)    # MAYBE: remove kwargs
        else:
            ax = event.inaxes
            viztype = ph.get_plotdat(ax, 'viztype', None)
            print_('[ik] viztype=%r' % viztype)
            if viztype == 'keypoints':
                kpts = ph.get_plotdat(ax, 'kpts', [])
                if len(kpts) == 0:
                    print('...nokpts')
                else:
                    print('...nearest')
                    x, y = event.xdata, event.ydata
                    fx = ut.nearest_point(x, y, kpts)[0]
                    _select_ith_kpt(fx)
            elif viztype == 'warped':
                hs_fx = ph.get_plotdat(ax, 'fx', None)
                #kpts = ph.get_plotdat(ax, 'kpts', [])
                if hs_fx is not None:
                    # Ugly. Interactions should be changed to classes.
                    kp = self.kpts[hs_fx]  # FIXME
                    sift = self.desc[hs_fx]
                    df2.draw_keypoint_gradient_orientations(chip, kp, sift=sift, mode='vec',
                                                            fnum=df2.next_fnum())
            else:
                print('...unhandled')
        ph.draw()

    # Draw without keypoints the first time
    _viz_keypoints(fnum, **kwargs)   # MAYBE: remove kwargs
    ih.connect_callback(fig, 'button_press_event', _on_keypoints_click)
    if not nodraw:
        ph.draw()


if __name__ == '__main__':
    """
    CommandLine:
        python -m plottool.interact_keypoints
        python -m plottool.interact_keypoints --allexamples
        python -m plottool.interact_keypoints --allexamples --noface --nosrc
    """
    import multiprocessing
    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA
    ut.doctest_funcs()
