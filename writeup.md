# Assignment 5

# Team Members:

- Grace Mills
- Chris Hamel

# Expected Data Structures

Focusing on line or method coverage tests I would expect data structures such as bst's, stacks, priority queues and linked lists to be utilized. I think that a bst and priority queue would be helpful for a method coverage tester because the methods could be stored in a priority queue where their priority is increased by hoe many times the method is called. This could pull from a bst that is organized with all the methods based on their priority to make sure the most frequently called methods, the ones at the top of the tree and beginning of the priority queue, are tested thoroughly. For a line based coverage tested you could simply use a linked list or stack. A stack would be helpful to see what the last line accessed by the tester was and both have a quick length operation in order to find the total amount of lines tested.

# Initial Code Examination

The README provides helpful guidance on editing and using the project, with linked documentation. Tests are organized across multiple files for clarity. 'test_coverage' verifies that the tool correctly identiies covered and uncovered lines, while 'test_report' checks the reporting feature by asserting what the output contains rather than generating mock reports manually.
The core source files each handle a distinct responsibility. 'parser.py' creates a parser object that checks line executability, parses file formatting, and handles comments, output messages, and exceptions. 'report.py' generates the summary report after a coverage run, detailing which lines or branches executed and the overall coverage percentage. 'tracer.pyi' describes the type constraints the tool follows at runtime. 'numbits.py' manages the set data structure that stores line numbers and their executed/ignored status as compressed blobs in the database. Finally, 'results.py' contains an Analysis class and a narrowed subclass that holds coverage results as objects, the narrower class focuses only on relevant lines to improve time complexity, while a separate Numbers class stores the raw coverage data.

# Detailed Code Examination

I focused on `coverage/results.py`, which centralizes “what was run” versus “what was possible.” The main type is the `Analysis` dataclass: sets of line numbers (`statements`, `excluded`, `executed`) and, when branch coverage is on, sets of arcs—pairs `(from_line, to_line)`—and a dict of exit counts per line.

I traced `arcs_executed_set`, a set of executed (from, to) arc pairs (one arc = one control-flow step, e.g. which branch of an if was taken). It is created in `analysis_from_file_reporter`. That function gets executed arcs from `data.arcs(filename)` (then translated) and possible arcs from the file reporter’s `arcs()`. It builds a `defaultdict(set)` mapping each “from” line to its “to” lines, then builds dests from possible arcs and single_dests for lines with one exit, fills new_arcs (keeping (fromno, tono) when fromno != tono, or when fromno == tono only if in single_dests). The result is run through `file_reporter.translate_arcs()` and stored as `arcs_executed_set` (and a sorted list `arcs_executed` in `__post_init__`). Creation is in one place: the factory building Analysis from coverage data and the file reporter.

After construction the set is only read, never mutated. `arcs_missing()` returns possible arcs not in `arcs_executed_set`, excluding from-lines in no_branch and to-lines in excluded; `missing_branch_arcs()` turns that into a dict from branch lines to lists of missing destinations; `branch_stats()` uses that and exit_counts to produce (total_exits, taken_exits) per line; `executed_branch_arcs()` iterates `arcs_executed` and groups by source line. Values flow from raw coverage data to one set per file, to read-only use for missing and executed branch reporting.

For subsets of lines, `AnalysisNarrower` precomputes in `add_regions` arc sets touching each region (frozenset of lines), storing them in region2arc_possibilities and region2arc_executed. `narrow(lines)` does set intersection for statements/excluded/executed, looks up precomputed sets by frozenset(lines), and builds a new Analysis. One source of truth plus dicts keyed by region avoids quadratic behavior when narrowing many regions.

# Summary

The coverage.py source code is notably high quality and well-organized. The files I analyzed had a clear organization and ordering of functions. The use of dataclasses like Analysis and Numbers makes the data structures self-documenting, and the factory pattern for building Analysis from coverage data keeps construction logic in one place, avoiding scattered mutation.
The AnalysisNarrower design is particularly thoughtful, precomputing arc sets per region avoids quadratic behavior when narrowing many regions, showing attention to time complexity. Comments and naming conventions are clear to enhance readability and maintainability. I found the comments particularly helpful when defining the use cases of the code.
Compared to my own code, this project is significantly more intricate, especially around making the whole project generalizable. Maintaining this codebase would feel approachable given its consistent patterns. One challenge would be the arc-tracking logic, which requires careful understanding of the branch coverage data flow before making changes.
