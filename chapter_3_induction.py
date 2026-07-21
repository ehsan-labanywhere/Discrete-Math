import streamlit as st
import pandas as pd
import numpy as np
import graphviz
from collections import deque

# ==========================================
# 1. Page configuration and styling
# ==========================================
st.set_page_config(page_title="Ch 3: Proofs, Induction & Recursion", layout="wide")

st.markdown("""
<style>
    .math-tag { background-color: #e3f2fd; color: #0d47a1; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    .db-tag { background-color: #fce4ec; color: #880e4f; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    .highlight-box { background-color: #f0f2f6; border-left: 5px solid #4caf50; padding: 15px; margin: 10px 0; border-radius: 5px; }
    h3 { color: #1f77b4; }
    .stButton>button { width: 100%; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Core utilities (backend logic)
# ==========================================

def verify_sum_formula(n):
    left = sum(range(1, n+1))
    right = n * (n + 1) // 2
    return left, right

def verify_sum_squares(n):
    left = sum(i**2 for i in range(1, n+1))
    right = n * (n + 1) * (2*n + 1) // 6
    return left, right

def fibonacci(n):
    if n <= 0: return 0
    elif n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

def factorial(n):
    if n == 0: return 1
    return n * factorial(n-1)

def prime_factorization(n):
    if n <= 1: return []
    factors = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def build_recursion_tree(func_name, n):
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='TB')
    
    counter = [0]
    
    def add_node(label):
        node_id = f"node_{counter[0]}"
        dot.node(node_id, label, style='filled', fillcolor='#e3f2fd')
        counter[0] += 1
        return node_id
    
    if func_name == "fib":
        def build_fib(k):
            u = add_node(f"fib({k})")
            if k <= 1:
                return u
            v1 = build_fib(k-1)
            v2 = build_fib(k-2)
            dot.edge(u, v1)
            dot.edge(u, v2)
            return u
        build_fib(n)
        
    elif func_name == "fact":
        def build_fact(k):
            u = add_node(f"{k}!")
            if k == 0:
                return u
            v = build_fact(k-1)
            dot.edge(u, v)
            return u
        build_fact(n)
        
    elif func_name == "hanoi":
        def build_hanoi(k):
            u = add_node(f"T({k})")
            if k == 1:
                return u
            v1 = build_hanoi(k-1)
            v2 = build_hanoi(k-1)
            dot.edge(u, v1)
            dot.edge(u, v2)
            return u
        build_hanoi(n)
        
    return dot

def solve_linear_recurrence(c1, c2, a0, a1, n_max):
    seq = [a0, a1]
    for i in range(2, n_max + 1):
        seq.append(c1 * seq[-1] + c2 * seq[-2])
    return seq

def tower_of_hanoi(n):
    return 2**n - 1

def display_smart_table(data, cols, max_len=25):
    if len(data) <= max_len:
        st.dataframe(pd.DataFrame(data, columns=cols), use_container_width=True)
    else:
        st.dataframe(pd.DataFrame(data, columns=cols), use_container_width=True)
        st.caption(f"Showing {len(data)} rows.")

# ==========================================
# 3. Module rendering functions
# ==========================================

def render_overview():
    st.header("Chapter 3: Proofs, Induction & Recursion")
    st.markdown("""
    ### From Base Cases to Universal Truths
    This chapter connects mathematical proofs to computational recursive structures:
    
    1.  **Mathematical Induction**: 
        * *Concept*: Proving statements for all integers by establishing a base case and a domino effect.
        * *Bridge*: Loop Invariants in algorithms.
    2.  **Strong Induction**: 
        * *Concept*: Assuming truth for all previous cases, not just the immediate predecessor.
        * *Bridge*: Correctness of Divide-and-Conquer algorithms.
    3.  **Recursive Definitions**: 
        * *Concept*: Defining objects in terms of themselves.
        * *Bridge*: Recursive functions and Call Stacks.
    4.  **Solving Recurrences**: 
        * *Concept*: Finding closed-form formulas for recursive sequences.
        * *Bridge*: Algorithm complexity analysis (Big-O).
    """)
    st.info("👈 Select a module from the tabs above to start experimenting.")

# --- Tab 1: Mathematical Induction ---
def render_induction():
    st.subheader("1. Mathematical Induction")
    st.markdown("Focus: **The Domino Effect** & **Loop Invariants**.")
    
    with st.expander("🛠️ Interactive Induction Playground", expanded=True):
        st.markdown("Verify formulas for a chosen $n$. Note how the left-hand side (computation) matches the right-hand side (formula).")
        example = st.selectbox("Choose an Example", [
            "Sum of First n Integers", 
            "Sum of Squares", 
            "Inequality: 2^n > n"
        ])
        n_val = st.slider("Select n", 1, 50, 5, key="ind_slider")
        
    c_math, c_cs = st.columns([1, 1])
    
    with c_math:
        st.markdown("#### 📐 Mathematical View")
        if example == "Sum of First n Integers":
            st.latex(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}")
            l, r = verify_sum_formula(n_val)
            st.write(f"**Left Side (Computation):** 1 + 2 + ... + {n_val} = {l}")
            st.write(f"**Right Side (Formula):** {n_val}({n_val}+1)/2 = {r}")
            
            st.markdown("**Proof Structure:**")
            st.markdown("- **Base Case (n=1):** $1 = 1(2)/2 = 1$ ✅")
            st.markdown(f"- **Inductive Hypothesis (n=k):** Assume $1 + ... + k = k(k+1)/2$")
            st.markdown(f"- **Inductive Step (n=k+1):** Add $(k+1)$ to both sides and simplify.")
            
        elif example == "Sum of Squares":
            st.latex(r"\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}")
            l, r = verify_sum_squares(n_val)
            st.write(f"**Left Side (Computation):** 1² + 2² + ... + {n_val}² = {l}")
            st.write(f"**Right Side (Formula):** {n_val}({n_val}+1)(2({n_val})+1)/6 = {r}")
            
        elif example == "Inequality: 2^n > n":
            st.latex(r"2^n > n \quad \text{for } n \ge 1")
            l, r = 2**n_val, n_val
            st.write(f"**Left Side:** 2^{n_val} = {l}")
            st.write(f"**Right Side:** {r}")
            st.write("✅ Holds true" if l > r else "❌ Failed")

    with c_cs:
        st.markdown("#### 💻 CS Bridge: Loop Invariants")
        st.markdown("""<div class='highlight-box'>Math <span class='math-tag'>Inductive Hypothesis</span> = CS <span class='db-tag'>Loop Invariant</span></div>""", unsafe_allow_html=True)
        st.markdown("In CS, we prove a loop works by finding an invariant: a condition true before and after each iteration.")
        
        st.code("""
# Computing sum = 1 + 2 + ... + n
sum = 0
i = 1
while i <= n:
    # Loop Invariant: sum == i(i-1)/2
    sum = sum + i
    i = i + 1
# Postcondition: sum == n(n+1)/2
        """, language="python")
        st.caption("The invariant is the inductive hypothesis, maintaining truth at every step.")

    st.divider()
    st.markdown("### 🧪 Quick Check")
    q1 = st.radio(
        "In a proof by mathematical induction, what is the 'Inductive Step'?",
        ["Proving P(1) is true.", "Assuming P(k) is true to prove P(k+1) is true.", "Checking P(k) for all possible values of k."],
        key="qc_ind_1"
    )
    if st.button("Check Answer", key="btn_ind_1"):
        if q1 == "Assuming P(k) is true to prove P(k+1) is true.":
            st.success("Correct! This creates the infinite 'domino effect'.")
        else:
            st.error("Incorrect. The inductive step bridges P(k) to P(k+1).")

# --- Tab 2: Strong Induction ---
def render_strong_induction():
    st.subheader("2. Strong Induction")
    st.markdown("Focus: **Multiple Base Cases & Assuming All Previous Steps**.")
    
    with st.expander("📘 Theory: Strong vs Weak Induction", expanded=True):
        st.markdown("""
        - **Weak Induction:** Assume $P(k)$ is true, use it to prove $P(k+1)$.
        - **Strong Induction:** Assume $P(1), P(2), \dots, P(k)$ are ALL true, use them to prove $P(k+1)$.
        """)

    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("#### 🔢 Example 1: Prime Factorization")
        st.markdown("Every integer $n \ge 2$ can be written as a product of primes.")
        n_prime = st.number_input("Enter n (≥ 2):", min_value=2, max_value=10000, value=60, key="si_prime")
        factors = prime_factorization(n_prime)
        
        st.latex(f"{n_prime} = " + " \\times ".join(map(str, factors)))
        st.caption("Proof uses Strong Induction because if n is composite (n = a × b), we need the assumption for a and b, which are smaller than n but not necessarily n-1.")
        
    with c2:
        st.markdown("#### 💻 CS Bridge: Divide and Conquer")
        st.markdown("""<div class='highlight-box'>Math <span class='math-tag'>Strong Induction</span> = CS <span class='db-tag'>Divide & Conquer Recursion</span></div>""", unsafe_allow_html=True)
        st.markdown("Algorithms like Merge Sort split data into pieces of size $k < n$, not exactly $n-1$. Their correctness relies on strong induction.")
        
        st.markdown("#### Example 2: Fibonacci Growth")
        st.markdown("Prove $F(n) < 2^n$ for all $n \ge 1$. Strong induction is needed because $F(n) = F(n-1) + F(n-2)$ relies on TWO previous terms.")
        
        n_fib = st.slider("Select n for Fibonacci", 1, 20, 10, key="si_fib")
        fib_val = fibonacci(n_fib)
        st.write(f"**F({n_fib})** = {fib_val}")
        st.write(f"**2^{n_fib}** = {2**n_fib}")
        st.success(f"Clearly, {fib_val} < {2**n_fib}")

    st.divider()
    st.markdown("### 🧪 Quick Check")
    q2 = st.radio(
        "Why does proving properties about the Fibonacci sequence often require Strong Induction?",
        ["Because the numbers grow very fast.", "Because F(n) depends on both F(n-1) and F(n-2).", "Because it has no base case."],
        key="qc_si_1"
    )
    if st.button("Check Answer", key="btn_si_1"):
        if q2 == "Because F(n) depends on both F(n-1) and F(n-2).":
            st.success("Correct! Weak induction only gives you F(n-1), which isn't enough.")
        else:
            st.error("Incorrect. It's because the recursive definition looks back two steps.")

# --- Tab 3: Recursive Definitions ---
def render_recursion():
    st.subheader("3. Recursive Definitions & Sequences")
    
    st.markdown("Functions, sets, and sequences can be defined recursively (in terms of themselves).")
    
    c_def, c_tree = st.columns([1, 1.5])
    
    with c_def:
        func_choice = st.selectbox("Select Recursive Function", ["Factorial (n!)", "Fibonacci (F(n))", "Tower of Hanoi (T(n))"])
        n_rec = st.slider("Select n to visualize", 1, 6, 4, key="rec_slider")
        
        st.markdown("#### 📜 Mathematical Definition")
        if func_choice == "Factorial (n!)":
            st.latex(r"0! = 1 \quad \text{(Base Step)}")
            st.latex(r"n! = n \times (n-1)! \quad \text{(Recursive Step)}")
            result = factorial(n_rec)
            st.metric("Result", result)
            dot_type = "fact"
            
        elif func_choice == "Fibonacci (F(n))":
            st.latex(r"F(0) = 0, \ F(1) = 1 \quad \text{(Base Step)}")
            st.latex(r"F(n) = F(n-1) + F(n-2) \quad \text{(Recursive Step)}")
            result = fibonacci(n_rec)
            st.metric("Result", result)
            dot_type = "fib"
            
        elif func_choice == "Tower of Hanoi (T(n))":
            st.latex(r"T(1) = 1 \quad \text{(Base Step)}")
            st.latex(r"T(n) = 2T(n-1) + 1 \quad \text{(Recursive Step)}")
            result = tower_of_hanoi(n_rec)
            st.metric("Total Moves", result)
            dot_type = "hanoi"
            
        st.markdown("#### 💻 Iterative vs Recursive")
        if func_choice == "Factorial (n!)":
            st.code("def fact(n):\n  if n == 0: return 1\n  return n * fact(n-1)", language="python")
            st.code("def fact_iter(n):\n  res = 1\n  for i in range(1, n+1):\n    res *= i\n  return res", language="python")

    with c_tree:
        st.markdown("#### 🌳 Recursion Tree (Call Stack Visualization)")
        try:
            dot = build_recursion_tree(dot_type, n_rec)
            st.graphviz_chart(dot)
            st.caption("Each node represents a function call. Overlapping subproblems in Fibonacci make the tree grow exponentially!")
        except Exception as e:
            st.error("Graphviz rendering failed. Ensure graphviz is installed in your environment.")

    st.divider()
    st.markdown("### 🧪 Quick Check")
    q3 = st.radio(
        "What happens if a recursive function is missing its base case?",
        ["It returns 0.", "Infinite recursion (Stack Overflow).", "It becomes an iterative loop."],
        key="qc_rec_1"
    )
    if st.button("Check Answer", key="btn_rec_1"):
        if q3 == "Infinite recursion (Stack Overflow).":
            st.success("Correct! Without a base case to terminate, the call stack grows until memory runs out.")
        else:
            st.error("Incorrect. The function will call itself forever.")

# --- Tab 4: Solving Recurrences ---
def render_recurrences():
    st.subheader("4. Solving Recurrences")
    
    st.markdown("A recurrence relation expresses $a_n$ in terms of previous terms. How do we find a non-recursive (closed-form) formula for $a_n$?")
    
    with st.expander("🛠️ Linear Homogeneous Recurrence Solver", expanded=True):
        st.markdown("Define a relation of the form: $a_n = c_1 a_{n-1} + c_2 a_{n-2}$")
        col1, col2, col3, col4 = st.columns(4)
        c1_val = col1.number_input("c1 (coef of a_{n-1})", value=1.0, step=1.0)
        c2_val = col2.number_input("c2 (coef of a_{n-2})", value=1.0, step=1.0)
        a0_val = col3.number_input("a0 (Initial condition)", value=0.0, step=1.0)
        a1_val = col4.number_input("a1 (Initial condition)", value=1.0, step=1.0)
        
        n_terms = st.slider("Number of terms to generate", 5, 50, 20)
        
    seq = solve_linear_recurrence(c1_val, c2_val, a0_val, a1_val, n_terms)
    
    c_math, c_plot = st.columns([1, 2])
    
    with c_math:
        st.latex(f"a_n = {c1_val} a_{{n-1}} + {c2_val} a_{{n-2}}")
        st.latex(f"a_0 = {a0_val}, a_1 = {a1_val}")
        
        df = pd.DataFrame({"n": range(len(seq)), "a_n": seq})
        st.dataframe(df.set_index("n"), height=300)
        
    with c_plot:
        st.markdown("#### Sequence Growth")
        st.line_chart(df.set_index("n"))
        st.caption("Notice the growth rate. E.g., Fibonacci (c1=1, c2=1) grows exponentially. Arithmetic progressions grow linearly.")
        
    st.divider()
    st.markdown("#### 💻 CS Bridge: Algorithm Complexity")
    st.markdown("""<div class='highlight-box'>Math <span class='math-tag'>Solving Recurrences</span> = CS <span class='db-tag'>Big-O Time Complexity</span></div>""", unsafe_allow_html=True)
    st.markdown("In Computer Science, we use recurrence relations to analyze the running time of recursive algorithms.")
    
    st.latex(r"T(n) = 2T(n/2) + O(n) \implies T(n) = O(n \log n) \quad \text{(Merge Sort)}")
    st.latex(r"T(n) = T(n-1) + O(1) \implies T(n) = O(n) \quad \text{(Linear Search)}")
    
    st.divider()
    st.markdown("### 🧪 Quick Check")
    q4 = st.radio(
        "For the recurrence $T(n) = 2T(n-1) + 1$, what is the growth rate?",
        ["Linear $O(n)$", "Quadratic $O(n^2)$", "Exponential $O(2^n)$"],
        key="qc_rec_sol_1"
    )
    if st.button("Check Answer", key="btn_rec_sol_1"):
        if q4 == "Exponential $O(2^n)$":
            st.success("Correct! This is the Tower of Hanoi recurrence, which doubles every step.")
        else:
            st.error("Incorrect. Look at the multiplier (2). The size doubles at each level.")

# ==========================================
# 4. Main entry point
# ==========================================
def main():
    st.title("Chapter 3: Proofs, Induction & Recursion")
    tabs = st.tabs([
        "Overview", 
        "1. Math Induction", 
        "2. Strong Induction", 
        "3. Recursive Definitions", 
        "4. Solving Recurrences"
    ])
    
    with tabs[0]: render_overview()
    with tabs[1]: render_induction()
    with tabs[2]: render_strong_induction()
    with tabs[3]: render_recursion()
    with tabs[4]: render_recurrences()

if __name__ == "__main__":
    main()
