simplex_solver
==============

Explanatory implementation of the simplex method.  Uses only standard python library and makes some WILD assumptions about solvability, so be gentle.  

Usage
=====
The file can be run using the `main` function.  Edit the coefficients there.  All coefficients should be integers.  Didn't finish implementing the method for the case of equality constraints.


```
$ python simplex.py 
We seek to minimize the function

Z = -2x - 3y - 4z

Subject to the constraints

3x + 2y + z <= 10
2x + 5y + 3z <= 15

and the constraint that each variable must be nonnegative.


The canonical tableaux is

|   1   2   3   4   0   0   0   |   
|   0   3   2   1   1   0   10  |   
|   0   2   5   3   0   1   15  |   

Select row 2, column 2 as the pivot and reduce to get

|      1      0      5/3    10/3   -2/3   0      -20/3  |      
|      0      1      2/3    1/3    1/3    0      10/3   |      
|      0      0      11/3   7/3    -2/3   1      25/3   |      

Select row 3, column 3 as the pivot and reduce to get

|        1        0        0        25/11    -4/11    -5/11    -115/11  |        
|        0        1        0        -1/11    5/11     -2/11    20/11    |        
|        0        0        1        7/11     -2/11    3/11     25/11    |        

Select row 3, column 4 as the pivot and reduce to get

|       1       0       -25/7   0       2/7     -10/7   -130/7  |       
|       0       1       1/7     0       3/7     -1/7    15/7    |       
|       0       0       11/7    1       -2/7    3/7     25/7    |       

Select row 2, column 5 as the pivot and reduce to get

|      1      -2/3   -11/3  0      0      -4/3   -20    |      
|      0      7/3    1/3    0      1      -1/3   5      |      
|      0      2/3    5/3    1      0      1/3    5      |      

Now the first row is entirely nonpositive, so the minimum value of Z is -20
```
