Report
==========

### Floyd Warshall Assignment

The main issue I had with this assignment was figuring out how to write the final result back to the file. If the result was being written to the file outside of the calculate_path function and outside of thread 0, the result would be written multiple times. To fix this I created an if statement inside of the calculate_path function that would execute if the current rank was 0. I assume my program is not running the way I believe it to be, even though the final results after calling calculate_path matched the expected result file. The program will run successfully as long as the amount of threads provided in the command line is below 6 threads. The time did lower each call with the increase in number of threads to perform the Floyd Warshall algorithm.

Overall, this assignment took about 2 1/2 days to complete.

- 1 thread: 0.2539 
- 2 thread: 0.1320
- 4 thread: 0.0852

model name : Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz 4 36 216
