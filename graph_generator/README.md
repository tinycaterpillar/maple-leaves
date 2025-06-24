# Self-Complementary Graph Degree Sequence Generator

This program is designed to generate **degree sequences** corresponding to **self-complementary graphs**.  

※ Only **simple graphs** are considered — multiple edges and loops are not allowed.

---

## Program: `degree_sequences_generator`

- **Input**  
  An integer `n`, representing the number of vertices. It must be of the form `4k` or `4k + 1`.

- **Output**  
  A list of **graphic degree sequences** satisfying all of the following conditions:

  1. **Graphic Sequence**  
     The sequence satisfies the **Erdős–Gallai theorem**, i.e., it corresponds to some simple graph.

  2. **Half Edge Count**  
     The sum of the degrees is  
     
     $$ \sum d_i = \binom{n}{2} $$  
     meaning the corresponding graph has exactly **half the number of edges** of a complete graph of order `n`.

  3. **Complement Symmetry**  
     The sequence is symmetric with respect to the complement:  
     $$ d_i + d_{n + 1 - i} = n - 1 \quad \text{for all } i = 1, 2, \dots, n $$
     This ensures that the graph and its complement have the **same degree sequence**,  
     a necessary condition for self-complementarity.

## Ref
1. https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Gallai_theorem
2. https://en.wikipedia.org/wiki/Havel%E2%80%93Hakimi_algorithm