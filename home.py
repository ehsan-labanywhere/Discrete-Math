import streamlit as st

st.set_page_config(
    page_title="Discrete Math Bridge",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Discrete Math Learning System")
st.markdown("### Bridging Mathematics & Computer Science")

st.info("👈 Please select a Chapter from the sidebar to begin.")

st.markdown("""
### Course Roadmap

#### 🟢 **Chapter 1: Logic & Proofs**
* **Propositions & Connectives**: Truth tables, AND/OR/NOT gates.
* **Equivalences**: De Morgan's Laws, tautologies & contradictions.
* **Predicate Logic**: ∀ and ∃ quantifiers over finite domains.
* **Proof Methods**: Direct, contrapositive, contradiction & induction.

#### 🟢 **Chapter 2: Sets & Set Operations**
* **Set Basics**: Membership, subsets, cardinality.
* **Operations**: Union, intersection, difference & Venn diagrams.
* **Power Sets & Cartesian Products**: Combinatorial test generation.
* **Set Identities**: De Morgan's, distributive & absorption laws.

#### 🟢 **Chapter 3: Proofs, Induction & Recursion**
* **Mathematical Induction**: Step-through proofs with loop invariants.
* **Strong Induction**: Prime factorization & Fibonacci bounds.
* **Recursive Definitions**: Recursion trees & call stack visualization.
* **Solving Recurrences**: Linear recurrences & algorithm complexity.

#### 🟢 **Chapter 4: Functions**
* **Function Basics**: Domain, codomain, range & arrow diagrams.
* **Properties**: Injective, surjective, bijective & hash collisions.
* **Composition & Inverse**: Function pipelines & middleware chains.
* **Special Functions**: Floor, ceiling, modular arithmetic & hashing.

#### 🟢 **Chapter 5: Counting & Combinatorics**
* **Basic Counting**: Sum rule, product rule & decision trees.
* **Permutations & Combinations**: Pascal's Triangle & password strength.
* **Pigeonhole Principle**: Birthday paradox & hash collisions.
* **Inclusion-Exclusion**: Survey analysis & Euler's Totient.

#### 🟢 **Chapter 6: Relations**
* **The Bridge**: Why `Relation` ≈ `SQL Table`.
* **Modeling**: Visualizing Social Networks with Digraphs & Matrices.
* **Operations**: How `Composition` explains "Friends of Friends".
* **Applications**: 
    * **Task Scheduling** (using Topological Sort on DAGs).
    * **Data Clustering** (using Equivalence Relations).

#### 🟢 **Chapter 7: Graph Theory**
* **Graph Basics**: Vertices, edges, degrees & adjacency representations.
* **Graph Types**: Bipartite, complete, connected & Eulerian checks.
* **Paths & Traversal**: BFS, DFS & shortest path algorithms.
* **Graph Coloring**: Chromatic number & exam scheduling game.

#### 🟢 **Chapter 8: Trees**
* **Tree Basics**: Rooted trees, binary trees & tree properties.
* **Traversals**: Pre-order, in-order, post-order & level-order.
* **Spanning Trees**: Kruskal's & Prim's MST algorithms.
* **Decision & Game Trees**: Tic-Tac-Toe with Minimax AI.
""")