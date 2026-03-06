# Assignment 5

# Team Members:

- Grace Mills
-

# Expected Data Structures

Focusing on line or method coverage tests I would expect data structures such as bst's, stacks, priority queues and linked lists to be utilized. I think that a bst and priority queue would be helpful for a method coverage tester because the methods could be stored in a priority queue where their priority is increased by hoe many times the method is called. This could pull from a bst that is organized with all the methods based on their priority to make sure the most frequently called methods, the ones at the top of the tree and beginning of the priority queue, are tested thoroughly. For a line based coverage tested you could simply use a linked list or stack. A stack would be helpful to see what the last line accessed by the tester was and both have a quick length operation in order to find the total amount of lines tested.

# Initial Code Examination

The read me is very helpful as it shows how to edit the project as well as use it with the documentation linked. There are a lot of tests which are broken up into files to have cleaner organization. The source code mainly deals with parsing through code being tested or run and running the hook to see which lines are actually tested.
I looked through the test_coverage and test_report files. Test_coverage mainly tests if the code is knowing what lines are being covered and which arn't. I mainly read through the comments and headers of each of the tests because those are what describe the purpose of each test the best.
Test_report tests the reporting feature of the tool after it is run. I noticed the tests would check for what is in or not in the report because it is easier to know certain things the report should contain rather than making mock reports on mock files which would be too much manual work.
Then I looked into parser.py, report.py, tracer.pyi, numbits.py and results.py.
parser.py creates a parser object that handles checking if a line is exactable, a raw parse function that finds basic information on the file and its formatting and following functions to process comments, output messages and exception errors while the code runs.
report.py is the code that writes the summery report after coverage is run on a certain file reporting which lines/branches run or didn't run and the overall percent of the code that ran.
tracer.pyi seems to be a description of the typing constraints listed in another file that the tool follows when run.
numbits.py is a function to handle the set data structure that holds line numbers and their corresponding status of executed or ignored into 'blobs' in the data base.
results.py contains and analysis and analysis narrower class that hold the results as an object while the narrower class only looks at the relevant lines to improve the time complexities of its functions. the numbers class holds the raw data of the coverage run.

# Detailed Code Examination

I focused on `coverage/results.py`, which centralizes the data structures for “what was run” versus “what was possible.” The main type is the `Analysis` dataclass: it holds sets of line numbers (`statements`, `excluded`, `executed`) and, when branch coverage is enabled, sets of arcs—pairs `(from_line, to_line)`—and a dict of exit counts per line.

I traced arcs_executed_set, a set of executed (from, to) arc pairs. It is created in analysis_from_file_reporter. That function gets raw arcs from `data.arcs(filename)` and from the file reporter’s `arcs()` (possible arcs). It builds a `defaultdict(set)` mapping each “from” line to its “to” lines, then builds dests (defaultdict of "from" line to set of "to" lines) and single_dests for lines with one exit; it fills new_arcs by keeping (fromno, tono) when fromno != tono, and when fromno == tono only if that line is in single_dests. The result is stored in the `Analysis` instance as `arcs_executed_set` (and a sorted list `arcs_executed` in `__post_init__` for stable iteration). So creation happens in one place: the factory that builds Analysis from coverage data and the file reporter.

The set is only read after that, never mutated. arcs_missing() yields possible arcs that are not in arcs_executed_set (and not in no_branch/excluded); missing_branch_arcs() turns that into a dict mapping branch lines to lists of missing destination lines. branch_stats() then uses exit_counts and missing_branch_arcs to produce (total_exits, taken_exits) per line for HTML/XML reports. executed_branch_arcs() iterates over arcs_executed and groups by source line. So the values flow from raw coverage data to one canonical set per file, then to read-only use for missing and executed branch reporting.

To verify this behavior I ran a small test script. It exercised the Numbers dataclass (creation, n_executed, pc_covered, __add__), format_lines with sample statement/line sets, and should_fail_under for fail-under logic. It also ran a live coverage run on a tiny file with branches: after start/stop/import, cov._analyze(filename) returns an Analysis whose arcs_executed_set and branch_stats() behave as above. Finally it built an Analysis by hand and used AnalysisNarrower.add_regions() then narrow() to confirm the narrowed Analysis gets the correct subset of statements and arcs. All checks passed.

When the same logic is applied to a subset of lines (e.g., one region), `AnalysisNarrower` avoids re-scanning the whole analysis. In add_regions it precomputes, for each region (a frozenset of lines), the sets of arcs that touch that region, and stores them in region2arc_possibilities and region2arc_executed. Later, narrow(lines) does set intersection for statements, excluded, and executed, looks up the precomputed arc sets keyed by frozenset(lines), and builds a new Analysis with those smaller sets. So the flow is: original `arcs_executed_set` → split by region into `region2arc_executed` → each narrowed `Analysis` gets the subset of arcs for that region. The design keeps one source of truth (the full Analysis) and uses dicts keyed by region to reuse work and avoid quadratic behavior when narrowing many regions.

# Summary

Placeholder text.
