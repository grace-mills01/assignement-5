#!/usr/bin/env python3
"""
Script to test coverage/results.py behavior for the Detailed Code Examination.
Run from project root: python3 test_results_examination.py
"""
import sys
import os
import tempfile
import shutil

# Run from assignment root; need coverage from coveragepy-main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "coveragepy-main"))

import coverage
from coverage.results import (
    Analysis,
    Numbers,
    format_lines,
    display_covered,
    should_fail_under,
    AnalysisNarrower,
)

def test_numbers():
    """Test Numbers dataclass: creation, addition, percentages."""
    n1 = Numbers(n_files=1, n_statements=200, n_missing=20)
    assert n1.n_statements == 200 and n1.n_executed == 180 and n1.pc_covered == 90
    n2 = Numbers(n_files=1, n_statements=10, n_missing=8)
    n3 = n1 + n2
    assert n3.n_files == 2 and n3.n_statements == 210 and n3.n_missing == 28
    print("Numbers: creation, n_executed, pc_covered, __add__ OK")

def test_format_lines():
    """Test format_lines (statements vs lines -> formatted string)."""
    statements = {1, 2, 3, 4, 5, 10, 11, 12, 13, 14}
    lines = {1, 2, 5, 10, 11, 13, 14}
    got = format_lines(statements, lines)
    assert got == "1-2, 5-11, 13-14"
    print("format_lines(statements, lines) OK:", repr(got))

def test_should_fail_under():
    """Test fail_under logic."""
    assert should_fail_under(42.1, 42, 0) is False
    assert should_fail_under(42.1, 43, 0) is True
    assert should_fail_under(100.0, 100, 0) is False
    assert should_fail_under(99.8, 100, 0) is True
    print("should_fail_under OK")

def test_analysis_and_arcs():
    """Run coverage on a small file with branches and inspect Analysis."""
    tmp = tempfile.mkdtemp()
    try:
        os.chdir(tmp)
        with open("branchy.py", "w") as f:
            f.write("""\
def fun(x):
    if x == 1:
        print("one")
    else:
        print("not one")
    print("done")
fun(1)
fun(2)
""")
        cov = coverage.Coverage(branch=True, source=[tmp])
        cov.start()
        import importlib.util
        spec = importlib.util.spec_from_file_location("branchy", os.path.join(tmp, "branchy.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cov.stop()
        cov.save()

        analysis = cov._analyze(os.path.join(tmp, "branchy.py"))
        # Analysis holds sets; arcs_executed_set is the set we traced
        assert hasattr(analysis, "arcs_executed_set")
        assert hasattr(analysis, "arcs_executed")  # sorted list from __post_init__
        assert analysis.has_arcs
        # branch_stats uses arcs_executed_set via missing_branch_arcs
        stats = analysis.branch_stats()
        assert isinstance(stats, dict)
        # missing_formatted uses statements, missing, and optionally arcs
        mf = analysis.missing_formatted(branches=False)
        mf_branches = analysis.missing_formatted(branches=True)
        assert isinstance(mf, str)
        # Numbers is derived in __post_init__ from the sets
        assert analysis.numbers.n_statements >= 1
        assert analysis.numbers.n_branches >= 0
        print("Analysis from live coverage: arcs_executed_set, branch_stats, missing_formatted, numbers OK")
    finally:
        os.chdir(os.path.dirname(__file__))
        shutil.rmtree(tmp, ignore_errors=True)

def test_analysis_narrower():
    """Test AnalysisNarrower: add_regions then narrow yields smaller Analysis."""
    from coverage.types import TLineNo
    # Build a minimal Analysis-like we get from analysis_from_file_reporter
    statements = {1, 2, 3, 4, 5}
    executed = {1, 2, 4}
    excluded = set()
    arc_poss = {(1, 2), (2, 3), (2, 4), (4, 5)}
    arcs_exec = {(1, 2), (2, 4)}
    exit_counts = {2: 2}
    no_branch = set()
    a = Analysis(
        precision=0,
        filename="fake.py",
        has_arcs=True,
        statements=statements,
        excluded=excluded,
        executed=executed,
        arc_possibilities_set=arc_poss,
        arcs_executed_set=arcs_exec,
        exit_counts=exit_counts,
        no_branch=no_branch,
    )
    narrower = AnalysisNarrower(a)
    narrower.add_regions([{1, 2}, {4, 5}])
    small = narrower.narrow({1, 2})
    assert small.statements == {1, 2}
    assert small.executed == {1, 2}
    assert small.arc_possibilities_set <= arc_poss
    assert small.arcs_executed_set <= arcs_exec
    print("AnalysisNarrower add_regions + narrow OK")

if __name__ == "__main__":
    test_numbers()
    test_format_lines()
    test_should_fail_under()
    test_analysis_and_arcs()
    test_analysis_narrower()
    print("All checks passed.")
