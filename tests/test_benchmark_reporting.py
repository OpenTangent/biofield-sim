"""Regression checks for benchmark score/edge reporting semantics."""
import ast
from pathlib import Path
import numpy as np
from types import SimpleNamespace
from benchmark_setpoint_v070 import selectivity_sparsity

def test_score_selectivity_has_no_edge_sparsity():
    world = SimpleNamespace(con=[np.array([0, 1])], hubs=np.array([2, 3]))
    selectivity, sparsity = selectivity_sparsity(np.array([2., 4., 1., 2.]), world, 0, is_scores=True)
    assert np.isclose(selectivity, 2.)
    assert sparsity is None

def test_no_stale_graph_sparsity_append_after_setpoint_read():
    # AST guard: the last three (Setpoint) sparsity appends must be None,
    # not the preceding FLUX graph's local variable sp.
    tree = ast.parse((Path(__file__).parents[1] / "benchmark_setpoint_v070.py").read_text())
    values = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "append":
            target = node.func.value
            if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant) and target.slice.value == "sparsity":
                values.append((node.lineno, node.args[0]))
    values.sort(key=lambda item: item[0])
    assert len(values) == 5
    assert all(isinstance(value, ast.Constant) and value.value is None for _, value in values[-3:])


def test_export_refuses_to_overwrite(tmp_path):
    import pytest
    from benchmark_setpoint_v070 import write_results
    path = tmp_path / "baseline.json"
    path.write_text("original")
    with pytest.raises(FileExistsError):
        write_results({"new": True}, path)
    assert path.read_text() == "original"


def test_export_new_file_round_trip(tmp_path):
    import json
    from benchmark_setpoint_v070 import write_results
    path = tmp_path / "fresh.json"
    result = {"raw": {"sparsity": [None]}, "summary": {}}
    assert write_results(result, path) == path
    assert json.loads(path.read_text()) == result
