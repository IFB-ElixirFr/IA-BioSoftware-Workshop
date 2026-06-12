"""Unit tests for the Figure 2A reproduction module."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from reproduce_figure_2a import (  # noqa: E402
    build_expression_matrix,
    compute_row_z_scores,
    get_time_columns,
    plot_figure_2a,
    select_and_order_periodic_genes,
)


def make_test_dataframe() -> pd.DataFrame:
    """Create a small expression table with Figure 2A-like columns."""
    return pd.DataFrame(
        {
            "gene": ["gene_a", "gene_b", "gene_c"],
            "Figure2A_order_peaktime": [2, np.nan, 1],
            0: [1.0, 2.0, 4.0],
            5: [2.0, 3.0, 4.0],
            10: [3.0, 4.0, 4.0],
        },
    )


def test_get_time_columns_returns_sorted_numeric_columns() -> None:
    """Check that numeric time columns are detected and sorted."""
    dataframe = make_test_dataframe()
    assert get_time_columns(dataframe) == [0, 5, 10]


def test_get_time_columns_raises_without_numeric_columns() -> None:
    """Check that missing time columns raise a clear error."""
    dataframe = pd.DataFrame({"gene": ["gene_a"]})
    with pytest.raises(ValueError, match="No numeric time columns"):
        get_time_columns(dataframe)


def test_select_and_order_periodic_genes_uses_descending_order() -> None:
    """Check the descending sort needed to match the published orientation."""
    dataframe = make_test_dataframe()
    ordered = select_and_order_periodic_genes(dataframe)
    assert ordered["gene"].to_list() == ["gene_a", "gene_c"]


def test_select_and_order_periodic_genes_raises_for_missing_column() -> None:
    """Check that a missing order column is rejected."""
    dataframe = pd.DataFrame({"gene": ["gene_a"], 0: [1.0]})
    with pytest.raises(ValueError, match="Required order column"):
        select_and_order_periodic_genes(dataframe)


def test_compute_row_z_scores_nominal_case() -> None:
    """Check row-wise z-score normalization on non-constant rows."""
    result = compute_row_z_scores([[1.0, 2.0, 3.0]])
    expected = np.array([[-1.22474487, 0.0, 1.22474487]])
    np.testing.assert_allclose(result, expected)


def test_compute_row_z_scores_constant_row_becomes_zero() -> None:
    """Check that constant rows do not produce NaN values."""
    result = compute_row_z_scores([[4.0, 4.0, 4.0]])
    np.testing.assert_allclose(result, np.zeros((1, 3)))


def test_compute_row_z_scores_rejects_invalid_bounds() -> None:
    """Check that invalid plotting bounds raise an error."""
    with pytest.raises(ValueError, match="vmin must be lower"):
        compute_row_z_scores([[1.0, 2.0]], vmin=1.0, vmax=1.0)


def test_build_expression_matrix_shape() -> None:
    """Check that expression extraction returns the expected shape."""
    dataframe = make_test_dataframe()
    ordered = select_and_order_periodic_genes(dataframe)
    matrix = build_expression_matrix(ordered, [0, 5, 10])
    assert matrix.shape == (2, 3)


def test_plot_figure_2a_writes_png(tmp_path: Path) -> None:
    """Check that the plotting function creates an output file."""
    output_path = tmp_path / "figure.png"
    z_scores = np.array([[0.0, 1.0, -1.0], [1.0, 0.0, -1.0]])
    figure = plot_figure_2a(z_scores, [0, 50, 100], output_path, dpi=80)
    assert output_path.exists()
    assert figure.axes[0].get_ylabel() == "Top Periodic Genes (2)"


def test_plot_figure_2a_rejects_dimension_mismatch(tmp_path: Path) -> None:
    """Check that inconsistent matrix and time dimensions are rejected."""
    with pytest.raises(ValueError, match="Number of matrix columns"):
        plot_figure_2a(np.array([[1.0, 2.0]]), [0], tmp_path / "figure.png")

from reproduce_figure_2a import (  # noqa: E402
    build_argument_parser,
    main,
    read_expression_table,
    reproduce_figure_2a,
)


def test_read_expression_table_rejects_negative_header(tmp_path: Path) -> None:
    """Check that a negative header row is rejected before file reading."""
    with pytest.raises(ValueError, match="header_row"):
        read_expression_table(tmp_path / "missing.xlsx", header_row=-1)


def test_read_expression_table_rejects_missing_file(tmp_path: Path) -> None:
    """Check that a missing input file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="Input Excel file not found"):
        read_expression_table(tmp_path / "missing.xlsx")


def test_reproduce_figure_2a_end_to_end_with_small_excel(tmp_path: Path) -> None:
    """Check the complete workflow on a minimal Excel fixture."""
    input_path = tmp_path / "input.xlsx"
    output_path = tmp_path / "figure.png"
    dataframe = make_test_dataframe()
    with pd.ExcelWriter(input_path) as writer:
        dataframe.to_excel(writer, sheet_name="Sheet1", index=False, startrow=2)

    result_path = reproduce_figure_2a(input_path, output_path)

    assert result_path == output_path
    assert output_path.exists()


def test_build_argument_parser_defaults() -> None:
    """Check that the CLI parser has usable default arguments."""
    parser = build_argument_parser()
    args = parser.parse_args([])
    assert args.input.name == "pgen.1006453.s002.xlsx"
    assert args.output.name == "figure_2A_reproduced.png"
    assert not args.no_panel_label


def test_main_returns_zero_with_small_excel(tmp_path: Path) -> None:
    """Check that the command-line entry point succeeds on valid inputs."""
    input_path = tmp_path / "input.xlsx"
    output_path = tmp_path / "figure.png"
    dataframe = make_test_dataframe()
    with pd.ExcelWriter(input_path) as writer:
        dataframe.to_excel(writer, sheet_name="Sheet1", index=False, startrow=2)

    status = main(["--input", str(input_path), "--output", str(output_path)])

    assert status == 0
    assert output_path.exists()
