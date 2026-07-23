import streamlit as st
import theme
import pandas as pd
import numpy as np
import graphviz
import itertools

# ==========================================
# 1. Page configuration and styling
# ==========================================
theme.setup_page("Ch 2: Sets & Set Operations", "🧮")

# ==========================================
# 2. Core utility functions (backend logic)
# ==========================================
def parse_set_input(input_str):
    """Parse comma-separated values into a sorted list of unique integers."""
    try:
        return sorted(list(set([int(x.strip()) for x in input_str.split(',') if x.strip()])))
    except:
        return []

def format_set_display(s):
    """Format a list as a set string."""
    if not s:
        return r"\emptyset"
    return r"\{" + ", ".join(map(str, s)) + r"\}"

def power_set(s):
    """Compute power set of a list s."""
    s_list = list(s)
    return list(itertools.chain.from_iterable(itertools.combinations(s_list, r) for r in range(len(s_list)+1)))

def format_powerset_display(ps):
    """Format powerset elements for display."""
    items = []
    for subset in ps:
        if not subset:
            items.append(r"\emptyset")
        else:
            items.append(r"\{" + ", ".join(map(str, subset)) + r"\}")
    return r"\{" + ", ".join(items) + r"\}"

def cartesian_product(a, b):
    """Compute A x B."""
    return list(itertools.product(a, b))

# ==========================================
# 3. Module rendering functions
# ==========================================

def render_overview():
    st.header("Chapter 2: Sets & Set Operations")
    st.markdown("""
    ### Sets: The Building Blocks
    Sets are fundamental to both discrete mathematics and computer science. In this module, we will explore:
    
    1.  **Set Basics**: Elements, membership, subsets, and cardinality.
    2.  **Operations**: Union, intersection, difference, symmetric difference.
    3.  **Power Sets & Cartesian Products**: Combinatorics and relations foundations.
    4.  **Set Identities & Laws**: Equivalence rules (De Morgan's, Distributive, etc.).
    
    **The CS Bridge**: 
    Sets directly map to data structures like Python's `set()`, Java's `HashSet`, and database operations like SQL `JOIN`s or `DISTINCT` queries.
    """)
    st.info("👈 Select a tab above to explore each topic interactively.")

def render_basics():
    st.subheader("1. Set Basics")
    st.markdown("Focus: **Membership, Subsets, Cardinality, and Notations**.")
    
    with st.expander("🛠️ Define Sets", expanded=True):
        c1, c2 = st.columns(2)
        A = parse_set_input(c1.text_input("Set A (comma-separated integers)", "1, 2, 3, 4, 5", key="basics_a"))
        B = parse_set_input(c2.text_input("Set B (comma-separated integers)", "3, 4, 5, 6, 7", key="basics_b"))
    
    c_math, c_cs = st.columns(2)
    
    with c_math:
        st.markdown("#### 📐 Mathematical Notation")
        st.latex(f"A = {format_set_display(A)}")
        st.latex(f"B = {format_set_display(B)}")
        
        st.markdown("**Cardinality (Size):**")
        st.latex(f"|A| = {len(A)}, \\quad |B| = {len(B)}")
        
        st.markdown("**Subset Check:**")
        is_subset = set(A).issubset(set(B))
        st.latex(f"A \\subseteq B \\implies \\text{{{is_subset}}}")
        
    with c_cs:
        st.markdown("#### 💻 Python Set Equivalent")
        st.code(f'''
A = set({A})
B = set({B})

# Cardinality
len_A = len(A)  # {len(A)}
len_B = len(B)  # {len(B)}

# Subset Check
is_subset = A.issubset(B)  # {set(A).issubset(set(B))}
        ''', language='python')
        
    st.divider()
    
    st.markdown("### 🔎 Membership Testing")
    col_x, col_test = st.columns([1, 2])
    x_val = col_x.number_input("Enter a value x:", value=3, step=1, key="x_val")
    in_a = x_val in A
    in_b = x_val in B
    
    with col_test:
        st.markdown("<br>", unsafe_allow_html=True)
        if in_a: st.success(f"✅ x ∈ A : {x_val} is in Set A")
        else: st.error(f"❌ x ∉ A : {x_val} is NOT in Set A")
        
        if in_b: st.success(f"✅ x ∈ B : {x_val} is in Set B")
        else: st.error(f"❌ x ∉ B : {x_val} is NOT in Set B")

    st.markdown("### 🧪 Quick Check")
    q1 = st.radio(
        "What is the mathematical meaning of A ⊆ B?",
        ["Every element in A is also in B", "A and B have the same elements", "Every element in B is also in A"],
        key="qc_basics"
    )
    if st.button("Check", key="btn_qc_basics"):
        if q1 == "Every element in A is also in B":
            st.success("Correct! That is the definition of a subset.")
        else:
            st.error("Incorrect. A ⊆ B means all elements of A exist in B.")

def render_operations():
    st.subheader("2. Set Operations")
    
    with st.expander("🛠️ Define Sets & Universe", expanded=True):
        c1, c2, c3 = st.columns(3)
        A_input = parse_set_input(c1.text_input("Set A", "1, 2, 3", key="op_a"))
        B_input = parse_set_input(c2.text_input("Set B", "3, 4, 5", key="op_b"))
        U_input = parse_set_input(c3.text_input("Universe U", "1, 2, 3, 4, 5, 6, 7, 8", key="op_u"))
        
        A = set(A_input)
        B = set(B_input)
        U = set(U_input)
        # Ensure U contains A and B
        U = U.union(A).union(B)

    st.markdown("#### 📐 Operations vs. 💾 SQL Equivalence")
    
    ops_tabs = st.tabs(["Union (∪)", "Intersection (∩)", "Difference (−)", "Sym. Diff (⊕)", "Complement (¯)"])
    
    with ops_tabs[0]:
        c_m, c_c = st.columns(2)
        res = A.union(B)
        with c_m:
            st.markdown("**Union** combines all elements.")
            st.latex(f"A \\cup B = {format_set_display(sorted(list(res)))}")
        with c_c:
            st.markdown("**SQL Equivalent: `FULL OUTER JOIN` / `UNION`**")
            st.code("SELECT * FROM A UNION SELECT * FROM B;")
            
    with ops_tabs[1]:
        c_m, c_c = st.columns(2)
        res = A.intersection(B)
        with c_m:
            st.markdown("**Intersection** finds common elements.")
            st.latex(f"A \\cap B = {format_set_display(sorted(list(res)))}")
        with c_c:
            st.markdown("**SQL Equivalent: `INNER JOIN`**")
            st.code("SELECT A.val FROM A INNER JOIN B ON A.val = B.val;")
            
    with ops_tabs[2]:
        c_m, c_c = st.columns(2)
        res = A.difference(B)
        with c_m:
            st.markdown("**Difference** (A − B) keeps elements in A but not in B.")
            st.latex(f"A - B = {format_set_display(sorted(list(res)))}")
        with c_c:
            st.markdown("**SQL Equivalent: `LEFT JOIN` (with NULL check)**")
            st.code("SELECT A.val FROM A LEFT JOIN B ON A.val = B.val WHERE B.val IS NULL;")
            
    with ops_tabs[3]:
        c_m, c_c = st.columns(2)
        res = A.symmetric_difference(B)
        with c_m:
            st.markdown("**Symmetric Difference** (A ⊕ B) keeps elements in A or B, but not both.")
            st.latex(f"A \\oplus B = {format_set_display(sorted(list(res)))}")
        with c_c:
            st.markdown("**SQL Equivalent: (A−B) UNION (B−A)**")
            st.code("SELECT * FROM (A - B) UNION SELECT * FROM (B - A);")
            
    with ops_tabs[4]:
        c_m, c_c = st.columns(2)
        res = U.difference(A)
        with c_m:
            st.markdown("**Complement** (Ā) keeps elements in U but not in A.")
            st.latex(f"\\bar{{A}} = U - A = {format_set_display(sorted(list(res)))}")
        with c_c:
            st.markdown("**SQL Equivalent: `NOT IN`**")
            st.code("SELECT val FROM U WHERE val NOT IN (SELECT val FROM A);")
            
    st.divider()
    
    st.markdown("### 🧪 Quick Check")
    q_op = st.radio(
        "Which SQL operation corresponds to Set Intersection (A ∩ B)?",
        ["FULL OUTER JOIN", "INNER JOIN", "LEFT JOIN"],
        key="qc_ops"
    )
    if st.button("Check", key="btn_qc_ops"):
        if q_op == "INNER JOIN":
            st.success("Correct! INNER JOIN returns only records with matches in both tables (A and B).")
        else:
            st.error("Incorrect. Remember, intersection means elements must be in BOTH sets.")

def render_power_cartesian():
    st.subheader("3. Power Sets & Cartesian Products")
    
    with st.expander("🛠️ Define Sets", expanded=True):
        c1, c2 = st.columns(2)
        A = parse_set_input(c1.text_input("Set A", "1, 2, 3", key="pow_a"))
        B = parse_set_input(c2.text_input("Set B", "4, 5", key="pow_b"))
        
    tab_pow, tab_cart = st.tabs(["Power Set P(A)", "Cartesian Product (A × B)"])
    
    with tab_pow:
        if len(A) > 6:
            st.warning("⚠️ Cardinality of A > 6. Displaying the power set might take too much space. Truncating.")
            A = A[:6]
        
        pset = power_set(A)
        st.markdown("#### 📐 The Power Set")
        st.markdown("The power set $P(A)$ is the set of all subsets of $A$.")
        
        st.latex(f"|A| = {len(A)}")
        st.latex(f"|P(A)| = 2^{{|A|}} = {len(pset)}")
        
        if len(pset) <= 32:
            st.latex(f"P(A) = {format_powerset_display(pset)}")
        else:
            st.caption(f"Skipping latex display as size > 32 (size is {len(pset)}).")
            
        st.markdown("""<div class='highlight-box'>
        <b>CS Application:</b> Generating all subsets is used in <b>exhaustive search</b> algorithms (like the Knapsack problem) and computing feature combinations.
        </div>""", unsafe_allow_html=True)
        
    with tab_cart:
        cart_prod = cartesian_product(A, B)
        st.markdown("#### 📐 The Cartesian Product")
        st.markdown("$A \\times B$ generates all ordered pairs $(a,b)$ where $a \\in A$ and $b \\in B$.")
        
        st.latex(f"|A \\times B| = |A| \\cdot |B| = {len(A)} \\cdot {len(B)} = {len(cart_prod)}")
        
        items = ", ".join([f"({a},{b})" for a, b in cart_prod])
        
        if len(cart_prod) <= 40:
            st.latex(f"A \\times B = \\{{ {items} \\}}")
        else:
            st.caption(f"Cartesian product has {len(cart_prod)} elements.")
            
        st.markdown("""<div class='highlight-box'>
        <b>CS Application:</b> Cartesian products are the basis for a <b>CROSS JOIN</b> in SQL, combining every row of one table with every row of another. Combinatorial testing uses this to test all input parameter combinations.
        </div>""", unsafe_allow_html=True)
        
        if st.checkbox("Show as Data Table"):
            df = pd.DataFrame(cart_prod, columns=["A", "B"])
            df.index += 1
            st.dataframe(df, use_container_width=True)
            
    st.divider()
    st.markdown("### 🧪 Quick Check")
    q_pow = st.radio(
        "If a set A has 5 elements, how many subsets does it have?",
        ["5", "10", "32", "64"],
        key="qc_pow"
    )
    if st.button("Check", key="btn_qc_pow"):
        if q_pow == "32":
            st.success("Correct! |P(A)| = 2^5 = 32.")
        else:
            st.error("Incorrect. The power set size is 2^|A|.")

def render_identities():
    st.subheader("4. Set Identities & Laws")
    
    st.markdown("Explore how set operations obey algebraic laws, allowing us to simplify expressions (just like boolean logic).")
    
    with st.expander("🛠️ Define Sets A, B, C & Universe", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        A = set(parse_set_input(c1.text_input("Set A", "1, 2, 3", key="id_a")))
        B = set(parse_set_input(c2.text_input("Set B", "3, 4, 5", key="id_b")))
        C = set(parse_set_input(c3.text_input("Set C", "2, 3, 6", key="id_c")))
        U = set(parse_set_input(c4.text_input("Universe U", "1, 2, 3, 4, 5, 6, 7", key="id_u")))
        
        U = U.union(A).union(B).union(C) # Ensure U contains everything
        
    law = st.selectbox("Select a Set Identity to Verify:", [
        "De Morgan's Law 1: (A ∪ B)' = A' ∩ B'",
        "De Morgan's Law 2: (A ∩ B)' = A' ∪ B'",
        "Distributive Law 1: A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)",
        "Distributive Law 2: A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)",
        "Absorption Law: A ∪ (A ∩ B) = A"
    ])
    
    st.markdown(f"### Verifying: **{law.split(':')[0]}**")
    
    col_l, col_r = st.columns(2)
    
    def comp(s): return U.difference(s)
    
    lhs = set()
    rhs = set()
    lhs_str = ""
    rhs_str = ""
    
    if "De Morgan's Law 1" in law:
        lhs = comp(A.union(B))
        rhs = comp(A).intersection(comp(B))
        lhs_str = r"\overline{(A \cup B)}"
        rhs_str = r"\overline{A} \cap \overline{B}"
    elif "De Morgan's Law 2" in law:
        lhs = comp(A.intersection(B))
        rhs = comp(A).union(comp(B))
        lhs_str = r"\overline{(A \cap B)}"
        rhs_str = r"\overline{A} \cup \overline{B}"
    elif "Distributive Law 1" in law:
        lhs = A.intersection(B.union(C))
        rhs = A.intersection(B).union(A.intersection(C))
        lhs_str = r"A \cap (B \cup C)"
        rhs_str = r"(A \cap B) \cup (A \cap C)"
    elif "Distributive Law 2" in law:
        lhs = A.union(B.intersection(C))
        rhs = A.union(B).intersection(A.union(C))
        lhs_str = r"A \cup (B \cap C)"
        rhs_str = r"(A \cup B) \cap (A \cup C)"
    elif "Absorption Law" in law:
        lhs = A.union(A.intersection(B))
        rhs = A
        lhs_str = r"A \cup (A \cap B)"
        rhs_str = r"A"

    with col_l:
        st.markdown("#### Left Hand Side (LHS)")
        st.latex(f"{lhs_str} = {format_set_display(sorted(list(lhs)))}")
        
    with col_r:
        st.markdown("#### Right Hand Side (RHS)")
        st.latex(f"{rhs_str} = {format_set_display(sorted(list(rhs)))}")
        
    if lhs == rhs:
        st.success("✅ **Identity Verified!** Both sides evaluate to the same set.")
    else:
        st.error("❌ Mismatch detected. Please check your Universe definition.")
        
    st.markdown("""<div class='highlight-box'>
    <b>CS Bridge:</b> Set identities are crucial for <b>Query Optimization</b>. Database query planners use laws like De Morgan's to rewrite SQL conditions (e.g., <code>NOT (A OR B)</code> rewritten to <code>NOT A AND NOT B</code>), reducing execution time and speeding up database responses.
    </div>""", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🧪 Quick Check")
    q_id = st.radio(
        "According to De Morgan's Law, what is the equivalent of the complement of a union?",
        ["The intersection of the complements", "The union of the complements", "The set itself"],
        key="qc_id"
    )
    if st.button("Check", key="btn_qc_id"):
        if q_id == "The intersection of the complements":
            st.success("Correct! (A ∪ B)' = A' ∩ B'")
        else:
            st.error("Incorrect. Complementing a union flips the operator to intersection.")

def main():
    theme.chapter_header("SETS", "Chapter 2: Sets & Set Operations", "Membership, unions, power sets and Venn diagrams — the algebra of collections.")
    tabs = st.tabs(["Overview", "1. Set Basics", "2. Set Operations", "3. Power Sets & Products", "4. Identities & Laws"])
    
    with tabs[0]: render_overview()
    with tabs[1]: render_basics()
    with tabs[2]: render_operations()
    with tabs[3]: render_power_cartesian()
    with tabs[4]: render_identities()

if __name__ == "__main__":
    main()
