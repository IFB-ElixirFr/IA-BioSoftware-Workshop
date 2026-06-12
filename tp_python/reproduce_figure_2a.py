"""Reproduce Figure 2A from Kelliher et al. 2016.

This module reads the supplementary Excel file ``pgen.1006453.s002.xlsx`` and
recreates the Saccharomyces cerevisiae periodic-gene heatmap shown in Figure 2A.
"""

from __future__ import annotations

import argparse
import warnings
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from pandas.api.types import is_numeric_dtype

DEFAULT_INPUT_PATH = Path("data/pgen.1006453.s002.xlsx")
DEFAULT_OUTPUT_PATH = Path("results/figure_2A_reproduced.png")
DEFAULT_SHEET_NAME = "Sheet1"
DEFAULT_HEADER_ROW = 2
DEFAULT_ORDER_COLUMN = "Figure2A_order_peaktime"
DEFAULT_VMIN = -1.5
DEFAULT_VMAX = 1.5
DEFAULT_DPI = 300
DEFAULT_XTICK_TIMES = (0, 50, 100, 150, 200)


def read_expression_table(
    input_path: Path,
    sheet_name: str = DEFAULT_SHEET_NAME,
    header_row: int = DEFAULT_HEADER_ROW,
) -> pd.DataFrame:
    """Read the supplementary Excel expression table.

    Parameters
    ----------
    input_path:
        Path to the Excel file.
    sheet_name:
        Name of the sheet to read.
    header_row:
        Zero-based row index containing column names.

    Returns
    -------
    pandas.DataFrame
        Expression and annotation table.

    Raises
    ------
    FileNotFoundError
        If the Excel file does not exist.
    ValueError
        If ``header_row`` is negative.
    """
    if header_row < 0:
        msg = "header_row must be a non-negative integer."
        raise ValueError(msg)
    if not input_path.exists():
        msg = f"Input Excel file not found: {input_path.resolve()}"
        raise FileNotFoundError(msg)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return pd.read_excel(input_path, sheet_name=sheet_name, header=header_row)


def get_time_columns(dataframe: pd.DataFrame) -> list[int | float]:
    """Identify numeric time-point columns and sort them by time.

    Parameters
    ----------
    dataframe:
        Input expression table.

    Returns
    -------
    list[int | float]
        Sorted time-point columns.

    Raises
    ------
    ValueError
        If no numeric time-point columns are found.
    """
    time_columns: list[int | float] = []
    for column_name in dataframe.columns:
        if isinstance(column_name, int | float | np.integer | np.floating):
            time_columns.append(column_name)
        elif is_numeric_dtype(dataframe[column_name]) and str(column_name).isdigit():
            time_columns.append(float(column_name))

    time_columns = sorted(time_columns, key=float)
    if not time_columns:
        msg = "No numeric time columns were found in the expression table."
        raise ValueError(msg)
    return time_columns


def select_and_order_periodic_genes(
    dataframe: pd.DataFrame,
    order_column: str = DEFAULT_ORDER_COLUMN,
) -> pd.DataFrame:
    """Select genes used in Figure 2A and order them as in the paper.

    The published visual orientation is reproduced by sorting
    ``Figure2A_order_peaktime`` in decreasing order.

    Parameters
    ----------
    dataframe:
        Input expression table.
    order_column:
        Column containing the Figure 2A order index.

    Returns
    -------
    pandas.DataFrame
        Filtered and ordered table.

    Raises
    ------
    ValueError
        If ``order_column`` is missing or contains no valid value.
    """
    if order_column not in dataframe.columns:
        msg = f"Required order column is missing: {order_column}"
        raise ValueError(msg)

    periodic_genes = dataframe.loc[dataframe[order_column].notna()].copy()
    periodic_genes[order_column] = pd.to_numeric(
        periodic_genes[order_column],
        errors="coerce",
    )
    periodic_genes = periodic_genes.loc[periodic_genes[order_column].notna()].copy()
    if periodic_genes.empty:
        msg = f"Column {order_column} does not contain valid Figure 2A order values."
        raise ValueError(msg)

    return periodic_genes.sort_values(order_column, ascending=False)


def compute_row_z_scores(
    expression_values: npt.ArrayLike,
    vmin: float = DEFAULT_VMIN,
    vmax: float = DEFAULT_VMAX,
) -> npt.NDArray[np.float64]:
    """Compute row-wise z-scores and clip values to the plotting range.

    Parameters
    ----------
    expression_values:
        Two-dimensional matrix with genes in rows and time points in columns.
    vmin:
        Lower clipping bound.
    vmax:
        Upper clipping bound.

    Returns
    -------
    numpy.ndarray
        Row-wise normalized expression matrix.

    Raises
    ------
    ValueError
        If bounds are invalid or the expression matrix is not two-dimensional.
    """
    if vmin >= vmax:
        msg = "vmin must be lower than vmax."
        raise ValueError(msg)

    matrix = np.asarray(expression_values, dtype=float)
    if matrix.ndim != 2:
        msg = "expression_values must be a two-dimensional matrix."
        raise ValueError(msg)

    row_means = np.nanmean(matrix, axis=1, keepdims=True)
    row_standard_deviations = np.nanstd(matrix, axis=1, ddof=0, keepdims=True)
    row_standard_deviations[row_standard_deviations == 0] = np.nan

    z_scores = (matrix - row_means) / row_standard_deviations
    z_scores = np.nan_to_num(z_scores, nan=0.0, posinf=vmax, neginf=vmin)
    return np.clip(z_scores, vmin, vmax)


def build_expression_matrix(
    periodic_genes: pd.DataFrame,
    time_columns: Sequence[int | float],
    vmin: float = DEFAULT_VMIN,
    vmax: float = DEFAULT_VMAX,
) -> npt.NDArray[np.float64]:
    """Build the normalized heatmap matrix from ordered genes.

    Parameters
    ----------
    periodic_genes:
        Ordered periodic-gene table.
    time_columns:
        Time-point columns to extract.
    vmin:
        Lower clipping bound for z-scores.
    vmax:
        Upper clipping bound for z-scores.

    Returns
    -------
    numpy.ndarray
        Normalized expression matrix.
    """
    expression_dataframe = periodic_genes.loc[:, list(time_columns)].apply(
        pd.to_numeric,
        errors="coerce",
    )
    return compute_row_z_scores(expression_dataframe.to_numpy(dtype=float), vmin, vmax)


def make_heatmap_colormap() -> LinearSegmentedColormap:
    """Create the cyan-black-yellow colormap used for the heatmap.

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Colormap where low values are cyan and high values are yellow.
    """
    return LinearSegmentedColormap.from_list(
        "cyan_black_yellow",
        ["#00d5e8", "#111111", "#ffea00"],
        N=256,
    )


def plot_figure_2a(
    z_scores: npt.NDArray[np.float64],
    time_columns: Sequence[int | float],
    output_path: Path,
    *,
    add_panel_label: bool = True,
    dpi: int = DEFAULT_DPI,
    vmin: float = DEFAULT_VMIN,
    vmax: float = DEFAULT_VMAX,
) -> Figure:
    """Plot and save the Figure 2A heatmap.

    Parameters
    ----------
    z_scores:
        Normalized expression matrix.
    time_columns:
        Time-point columns matching the matrix columns.
    output_path:
        Destination PNG path.
    add_panel_label:
        Whether to draw the large ``A.`` panel label.
    dpi:
        Figure resolution.
    vmin:
        Lower color-scale bound.
    vmax:
        Upper color-scale bound.

    Returns
    -------
    matplotlib.figure.Figure
        The generated Matplotlib figure.

    Raises
    ------
    ValueError
        If matrix and time-column dimensions do not match.
    """
    if z_scores.ndim != 2:
        msg = "z_scores must be a two-dimensional matrix."
        raise ValueError(msg)
    if z_scores.shape[1] != len(time_columns):
        msg = "Number of matrix columns must match number of time columns."
        raise ValueError(msg)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    number_of_genes = z_scores.shape[0]

    figure, axis = plt.subplots(figsize=(3.05, 5.55), dpi=dpi)
    axis.imshow(
        z_scores,
        aspect="auto",
        interpolation="nearest",
        cmap=make_heatmap_colormap(),
        vmin=vmin,
        vmax=vmax,
        origin="upper",
    )

    tick_positions = [
        list(time_columns).index(time) for time in DEFAULT_XTICK_TIMES if time in time_columns
    ]
    tick_labels = [str(time) for time in DEFAULT_XTICK_TIMES if time in time_columns]
    axis.set_xticks(tick_positions)
    axis.set_xticklabels(tick_labels)
    axis.set_yticks([])

    axis.set_xlabel("time (minutes)", fontsize=12, labelpad=13)
    axis.set_ylabel(f"Top Periodic Genes ({number_of_genes})", fontsize=12, labelpad=10)
    axis.set_title(r"$\it{Saccharomyces\ cerevisiae}$", fontsize=12, pad=8)

    for spine in axis.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.2)
        spine.set_color("black")

    axis.tick_params(axis="x", labelsize=11, length=5, width=1)
    axis.tick_params(axis="y", length=0)

    if add_panel_label:
        axis.text(
            -0.23,
            1.04,
            "A.",
            transform=axis.transAxes,
            fontsize=30,
            fontweight="bold",
            va="top",
            ha="left",
        )

    figure.tight_layout()
    figure.savefig(output_path, bbox_inches="tight")
    return figure


def reproduce_figure_2a(
    input_path: Path,
    output_path: Path,
    *,
    sheet_name: str = DEFAULT_SHEET_NAME,
    header_row: int = DEFAULT_HEADER_ROW,
    order_column: str = DEFAULT_ORDER_COLUMN,
    add_panel_label: bool = True,
) -> Path:
    """Run the complete Figure 2A reproduction workflow.

    Parameters
    ----------
    input_path:
        Path to the supplementary Excel file.
    output_path:
        Destination path for the PNG figure.
    sheet_name:
        Excel sheet to read.
    header_row:
        Zero-based row index containing column names.
    order_column:
        Column containing the Figure 2A order index.
    add_panel_label:
        Whether to draw the large ``A.`` panel label.

    Returns
    -------
    pathlib.Path
        Path to the generated figure.
    """
    expression_table = read_expression_table(input_path, sheet_name, header_row)
    time_columns = get_time_columns(expression_table)
    periodic_genes = select_and_order_periodic_genes(expression_table, order_column)
    z_scores = build_expression_matrix(periodic_genes, time_columns)
    figure = plot_figure_2a(
        z_scores,
        time_columns,
        output_path,
        add_panel_label=add_panel_label,
    )
    plt.close(figure)
    return output_path


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser.

    Returns
    -------
    argparse.ArgumentParser
        Configured parser.
    """
    parser = argparse.ArgumentParser(
        description="Reproduce Figure 2A from Kelliher et al. 2016.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to pgen.1006453.s002.xlsx.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output PNG path.",
    )
    parser.add_argument(
        "--sheet-name",
        default=DEFAULT_SHEET_NAME,
        help="Excel sheet name to read.",
    )
    parser.add_argument(
        "--header-row",
        type=int,
        default=DEFAULT_HEADER_ROW,
        help="Zero-based Excel header row index.",
    )
    parser.add_argument(
        "--no-panel-label",
        action="store_true",
        help="Do not draw the large A. label.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface.

    Parameters
    ----------
    argv:
        Optional command-line arguments. ``None`` uses ``sys.argv``.

    Returns
    -------
    int
        Process exit status.
    """
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    output_path = reproduce_figure_2a(
        input_path=args.input,
        output_path=args.output,
        sheet_name=args.sheet_name,
        header_row=args.header_row,
        add_panel_label=not args.no_panel_label,
    )
    print(f"Figure saved to: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
