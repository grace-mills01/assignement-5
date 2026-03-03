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

Placeholder text.

# Summary

Placeholder text.
