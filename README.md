# Greedy Randomized Adaptive Search Procedure (GRASP)
### For finding _ballanced groups of higher value_ in a graph
---

* **How to run**

    Go to root folder and run the following command
    
    ```console
    python3 grasp.py filename_of_instance I N K
    ```

    Where
    - **I** : Number of GRASP iterations
    - **N** : Restricted Candidate List size
    - **K** : Number of neighbors generated in local search

* **Observations**
    * The instances should be in "instances" folder

    * The results will be written in "results" folder, each one named with the *name of the instance + I_N_K*

    * The format of the results should be equal to the one described in "format.txt" file, in "results" folder
    