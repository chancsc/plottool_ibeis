from typing import Union
from typing import Tuple
import matplotlib as mpl
from typing import Any
import matplotlib as mpl
from _typeshed import Incomplete
from typing import Any


def customize_figure(fig, docla):
    ...


def gcf():
    ...


def gca():
    ...


def cla():
    ...


def clf():
    ...


def get_fig(fnum: Incomplete | None = ...):
    ...


def ensure_fig(fnum: Incomplete | None = ...):
    ...


def get_ax(fnum: Incomplete | None = ..., pnum: Incomplete | None = ...):
    ...


def figure(fnum: Union[int, None] = None,
           pnum: Union[int, str, Tuple[int, int, int]] = ...,
           docla: bool = False,
           title: Union[str, None] = None,
           figtitle: None = None,
           doclf: bool = False,
           projection: None = None,
           **kwargs) -> mpl.figure.Figure:
    ...


def prepare_figure_for_save(fnum,
                            dpi: Incomplete | None = ...,
                            figsize: Incomplete | None = ...,
                            fig: Incomplete | None = ...):
    ...


def sanitize_img_fname(fname):
    ...


def sanitize_img_ext(ext, defaultext: Incomplete | None = ...):
    ...


def prepare_figure_fpath(fig,
                         fpath,
                         fnum,
                         usetitle,
                         defaultext,
                         verbose,
                         dpath: Incomplete | None = ...):
    ...


def get_image_from_figure(fig):
    ...


def save_figure(fnum: Union[int, None] = None,
                fpath: Union[str, None] = None,
                fpath_strict: Union[str, None] = None,
                usetitle: bool = False,
                overwrite: bool = True,
                defaultext: Union[str, None] = None,
                verbose: int = 1,
                dpi: Union[int, None] = None,
                figsize: Union[tuple[int, int], None] = None,
                saveax: Union[bool, mpl.axes.Axes, None] = None,
                fig: Incomplete | None = ...,
                dpath: Incomplete | None = ...):
    ...


def set_ticks(xticks, yticks) -> None:
    ...


def set_xticks(tick_set) -> None:
    ...


def set_yticks(tick_set) -> None:
    ...


def customize_fontprop(font_prop, **fontkw):
    ...


def set_title(title: str = ..., ax: Incomplete | None = ..., **fontkw) -> None:
    ...


def set_xlabel(lbl: Any, ax: None = None, **kwargs) -> None:
    ...


def set_ylabel(lbl, ax: Incomplete | None = ..., **kwargs) -> None:
    ...


def set_figtitle(figtitle: Any,
                 subtitle: str = '',
                 forcefignum: bool = True,
                 incanvas: bool = True,
                 size: None = None,
                 fontfamily: None = None,
                 fontweight: None = None,
                 fig: None = None,
                 font: Incomplete | None = ...) -> None:
    ...
