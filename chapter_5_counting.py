import streamlit as st
import theme
import pandas as pd
import numpy as np
import graphviz
import math
import random

# ==========================================
# 1. Page configuration and styling (matching Chapter 6)
# ==========================================
theme.setup_page("Ch 5: Counting & Combinatorics", "🎲")

# ==========================================
# 2. Core utilities (backend logic)
# ==========================================

def factorial(n):
    return math.factorial(n)

def permutations(n, r):
    if r > n or n < 0 or r < 0: return 0
    return math.perm(n, r)

def combinations(n, r):
    if r > n or n < 0 or r < 0: return 0
    return math.comb(n, r)

def pascals_triangle(rows):
    triangle = []
    for i in range(rows):
        row = [1]
        if triangle:
            last_row = triangle[-1]
            row.extend([sum(pair) for pair in zip(last_row, last_row[1:])])
            row.append(1)
        triangle.append(row)
    return triangle

def birthday_probability(n):
    if n > 365:
        return 1.0
    prob_no_match = 1.0
    for i in range(n):
        prob_no_match *= (365 - i) / 365
    return 1.0 - prob_no_match

def inclusion_exclusion_2(a, b, a_and_b):
    return a + b - a_and_b

def inclusion_exclusion_3(a, b, c, ab, ac, bc, abc):
    return a + b + c - ab - ac - bc + abc

def euler_totient(n):
    # compute phi(n) using prime factorization and inclusion-exclusion logic implicitly
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def simulate_pigeonhole(pigeons, holes):
    assignment = {}
    for i in range(1, holes + 1):
        assignment[i] = []
    
    for p in range(1, pigeons + 1):
        hole = random.randint(1, holes)
        assignment[hole].append(p)
        
    return assignment

def display_latex_or_table(items, label, max_latex=20):
    st.markdown(f"#### {label}")
    if len(items) <= max_latex:
        expr = "\\{ " + ", ".join(map(str, items)) + " \\}"
        st.latex(expr)
    else:
        df = pd.DataFrame(items, columns=["Item"])
        df.index += 1
        st.dataframe(df, use_container_width=True)

# ==========================================
# 3. Module rendering functions
# ==========================================

def render_overview():
    st.header("Chapter 5: Counting & Combinatorics")
    st.markdown("""
    ### From Textbook to Interactive Tool
    This chapter explores the mathematics of counting, which forms the bedrock of algorithm analysis, cryptography, and probability theory.
    
    1.  **Basic Principles (Sum/Product Rules)**: 
        * *Concept*: Breaking complex counting problems into simpler OR / AND conditions.
        * *CS Bridge*: Branching factors, loops, and conditional statements in algorithm complexity.
    2.  **Permutations & Combinations**: 
        * *Concept*: Counting arrangements with and without order.
        * *CS Bridge*: Password security, test case generation, combination locks.
    3.  **Pigeonhole Principle**: 
        * *Concept*: Guaranteed collisions when space is limited.
        * *CS Bridge*: Hash collisions, birthday attacks.
    4.  **Inclusion-Exclusion Principle**: 
        * *Concept*: Counting exactly without double-counting overlapping sets.
        * *CS Bridge*: Database deduplication, tracking unique visitors.
    """)
    st.info("👈 Select a module from the tabs above to start experimenting.")


def render_basics():
    st.subheader("1. Basic Counting Principles")
    st.markdown("Focus: The **Sum Rule** (OR) and **Product Rule** (AND).")
    
    with st.expander("🍔 Restaurant Menu Example", expanded=True):
        st.markdown("Configure a meal that requires choosing exactly 1 Appetizer, 1 Entree, and 1 Dessert.")
        c1, c2, c3 = st.columns(3)
        apps = c1.number_input("Number of Appetizers", 1, 10, 3)
        entrees = c2.number_input("Number of Entrees", 1, 20, 5)
        desserts = c3.number_input("Number of Desserts", 1, 10, 2)
        
        st.divider()
        col_m, col_db = st.columns([1, 1])
        with col_m:
            st.markdown("#### Product Rule (AND)")
            total_meals = apps * entrees * desserts
            st.latex(f"|A \\times B \\times C| = {apps} \\times {entrees} \\times {desserts} = {total_meals}")
            st.caption("Total distinct 3-course meals.")
        
        with col_db:
            st.markdown("#### Sum Rule (OR)")
            total_items = apps + entrees + desserts
            st.latex(f"|A| + |B| + |C| = {apps} + {entrees} + {desserts} = {total_items}")
            st.caption("Total items if you can only order ONE thing.")
            
        st.markdown("""<div class='highlight-box'>CS <span class='math-tag'>Decision Trees</span> = Math <span class='db-tag'>Product Rule</span></div>""", unsafe_allow_html=True)
        
        with st.expander("🌳 View Decision Tree (Partial)"):
            st.caption("Shows branching for the first 2 appetizers, 2 entrees, and 2 desserts to avoid visual clutter.")
            try:
                g = graphviz.Digraph(format='png'); g.attr(rankdir='LR')
                g.node('Start')
                for a in range(min(2, apps)):
                    aname = f'App{a+1}'
                    g.node(aname)
                    g.edge('Start', aname)
                    for e in range(min(2, entrees)):
                        ename = f'{aname}_Ent{e+1}'
                        g.node(ename, label=f'Ent{e+1}')
                        g.edge(aname, ename)
                        for d in range(min(2, desserts)):
                            dname = f'{ename}_Des{d+1}'
                            g.node(dname, label=f'Des{d+1}')
                            g.edge(ename, dname)
                st.graphviz_chart(g)
            except: st.error("Graphviz not available.")
            
    st.markdown("### 🧪 Quick Check")
    q1 = st.radio(
        "A password requires 1 letter followed by 1 digit. How many total possibilities? (Assume 26 letters, 10 digits)",
        ["36", "260", "2610"],
        key="qc_basic_1"
    )
    if st.button("Check", key="check_qc_basic_1"):
        if q1 == "260":
            st.success("Correct! Product rule: 26 (letters) × 10 (digits) = 260.")
        else:
            st.error("Incorrect. Remember we are picking a letter AND a digit, so we multiply.")


def render_perms_combs():
    st.subheader("2. Permutations & Combinations")
    
    tab_calc, tab_pascal, tab_apps = st.tabs(["Calculator", "Pascal's Triangle", "Applications"])
    
    with tab_calc:
        st.markdown("Explore arrangements where **order matters** (Permutations) vs **order doesn't matter** (Combinations).")
        col1, col2 = st.columns(2)
        n = col1.number_input("n (Total pool size)", 1, 100, 10)
        r = col2.number_input("r (Number to select)", 0, n, 3)
        
        c_p, c_c = st.columns(2)
        with c_p:
            st.markdown("#### Permutations $P(n, r)$")
            st.latex(r"P(n, r) = \frac{n!}{(n-r)!}")
            p_val = permutations(n, r)
            st.success(f"**{p_val:,}** arrangements")
        with c_c:
            st.markdown("#### Combinations $C(n, r)$")
            st.latex(r"C(n, r) = \frac{n!}{r!(n-r)!}")
            c_val = combinations(n, r)
            st.success(f"**{c_val:,}** selections")
            
        st.markdown("### 🎯 Try-it Prompts")
        st.info(f"Notice that $P({n}, {r}) / C({n}, {r}) = {math.factorial(r) if r <= 10 else '...'} = {r}!$. This represents the number of ways to order the {r} selected items.")
        
    with tab_pascal:
        st.markdown("#### Pascal's Triangle Visualizer")
        rows = st.slider("Number of rows", 1, 15, 8)
        triangle = pascals_triangle(rows)
        
        html = "<div style='text-align: center; font-family: monospace;'>"
        for i, row in enumerate(triangle):
            html += f"n={i}: &nbsp;&nbsp;" + "&nbsp;&nbsp;&nbsp;&nbsp;".join(map(str, row)) + "<br>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        st.caption("Each number is the sum of the two numbers directly above it. Entry at row $n$, position $r$ is exactly $C(n, r)$.")
        
    with tab_apps:
        st.markdown("#### Real-world Examples")
        app_choice = st.selectbox("Select Scenario", ["Password Strength", "Committee Selection", "Lottery Odds"])
        
        if app_choice == "Password Strength":
            st.markdown("How many 8-character passwords from 62 possible characters (A-Z, a-z, 0-9)?")
            st.latex(r"62 \times 62 \times \dots \times 62 = 62^8")
            st.metric("Total Passwords", f"{62**8:,}")
            st.caption("This uses the Product Rule with repetition allowed.")
            
        elif app_choice == "Committee Selection":
            st.markdown("Choose a committee of 3 from 10 people.")
            st.latex(r"C(10, 3) = \frac{10!}{3!7!} = 120")
            st.metric("Total Committees", "120")
            st.caption("Combinations, since committee member order doesn't matter.")
            
        elif app_choice == "Lottery Odds":
            st.markdown("Pick 6 numbers correctly out of 49.")
            st.latex(r"C(49, 6) = 13,983,816")
            st.metric("Odds of winning", f"1 in {combinations(49, 6):,}")
            
    st.markdown("### 🧪 Quick Check")
    q2 = st.radio(
        "For forming a line of 5 students from a class of 20, do we use Permutations or Combinations?",
        ["Permutations", "Combinations"],
        key="qc_pc"
    )
    if st.button("Check", key="check_qc_pc"):
        if q2 == "Permutations":
            st.success("Correct! Order matters in a line (A-B-C is different from C-B-A).")
        else:
            st.error("Incorrect. Since order in line matters, we use Permutations.")


def render_pigeonhole():
    st.subheader("3. Pigeonhole Principle")
    
    with st.expander("🕊️ Theorem Statement", expanded=True):
        st.markdown("**Basic:** If $n+1$ objects are placed in $n$ boxes, at least one box contains $\ge 2$ objects.")
        st.markdown("**Generalized:** If $N$ objects are placed in $k$ boxes, at least one box contains $\ge \\lceil N/k \\rceil$ objects.")
        
    tab_sim, tab_bday, tab_hash = st.tabs(["Interactive Simulator", "Birthday Paradox", "Hash Collisions"])
    
    with tab_sim:
        st.markdown("#### Assign pigeons to holes")
        c1, c2 = st.columns(2)
        holes = c1.number_input("Holes (k)", 1, 20, 5)
        pigeons = c2.number_input("Pigeons (N)", 1, 50, 6)
        
        st.latex(f"\\text{{Guaranteed max in one hole: }} \\lceil {pigeons}/{holes} \\rceil = {math.ceil(pigeons/holes)}")
        
        if st.button("Assign Randomly"):
            assignment = simulate_pigeonhole(pigeons, holes)
            max_in_hole = max([len(v) for v in assignment.values()])
            
            st.markdown("#### Assignment Result")
            cols = st.columns(min(holes, 10))
            for i in range(holes):
                col_idx = i % 10
                with cols[col_idx]:
                    st.markdown(f"**Hole {i+1}**")
                    st.write(assignment[i+1])
                    
            if max_in_hole >= math.ceil(pigeons/holes):
                st.success(f"Theorem holds! The most crowded hole has {max_in_hole} pigeons.")
                
    with tab_bday:
        st.markdown("#### The Birthday Paradox")
        st.markdown("How large must a group be to have a >50% chance of a shared birthday?")
        
        group_size = st.slider("Group Size", 1, 100, 23)
        prob = birthday_probability(group_size)
        
        st.metric(f"Probability of shared birthday for {group_size} people", f"{prob*100:.2f}%")
        
        # Plot curve
        sizes = list(range(1, 70))
        probs = [birthday_probability(s) for s in sizes]
        df_bday = pd.DataFrame({"Group Size": sizes, "Probability": probs})
        st.line_chart(df_bday, x="Group Size", y="Probability")
        st.caption("Notice how quickly the probability rises, passing 50% at just 23 people.")
        
    with tab_hash:
        st.markdown("#### CS Application: Hash Collisions")
        st.markdown("Inserting $N$ keys into a hash table of size $M$. If $N > M$, collisions are guaranteed (Pigeonhole). Even for $N < M$, collisions are highly likely (Birthday paradox).")
        
        M = st.slider("Table Size (M)", 10, 100, 50)
        N = st.slider("Keys Inserted (N)", 1, 150, 20)
        
        if st.button("Simulate Hash Insertions"):
            table = {i: [] for i in range(M)}
            for key in range(N):
                # Simple random hash
                hash_val = random.randint(0, M-1)
                table[hash_val].append(key)
                
            collisions = sum(1 for v in table.values() if len(v) > 1)
            empty = sum(1 for v in table.values() if len(v) == 0)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Collisions (Buckets > 1)", collisions)
            c2.metric("Empty Buckets", empty)
            c3.metric("Max in one bucket", max([len(v) for v in table.values()]))

    st.markdown("### 🧪 Quick Check")
    q3 = st.radio(
        "If you have 10 pairs of black socks and 10 pairs of white socks in a drawer, how many individual socks must you pull to guarantee a matching pair?",
        ["2", "3", "11", "21"],
        key="qc_pigeon"
    )
    if st.button("Check", key="check_qc_pigeon"):
        if q3 == "3":
            st.success("Correct! There are only 2 colors (holes). By Pigeonhole, picking 3 socks (pigeons) guarantees at least ceil(3/2)=2 of the same color.")
        else:
            st.error("Incorrect. Think of colors as holes. How many holes are there?")


def render_inclusion_exclusion():
    st.subheader("4. Inclusion-Exclusion Principle")
    
    st.markdown("**Core Formula:** $|A \\cup B| = |A| + |B| - |A \\cap B|$")
    
    tab_2, tab_3, tab_euler = st.tabs(["2 Sets", "3 Sets", "Euler Totient"])
    
    with tab_2:
        c1, c2, c3 = st.columns(3)
        A = c1.number_input("|A| (e.g., Math students)", 0, 1000, 40)
        B = c2.number_input("|B| (e.g., CS students)", 0, 1000, 30)
        A_and_B = c3.number_input("|A ∩ B| (Both)", 0, min(A, B), 15)
        
        total = inclusion_exclusion_2(A, B, A_and_B)
        
        st.latex(f"|A \\cup B| = {A} + {B} - {A_and_B} = {total}")
        st.markdown(f"**Total unique students:** {total}")
        st.caption("We subtract the intersection once because it was counted twice (once in A, once in B).")
        
    with tab_3:
        st.markdown("**Formula:** $|A \\cup B \\cup C| = |A| + |B| + |C| - |A\\cap B| - |A\\cap C| - |B\\cap C| + |A\\cap B\\cap C|$")
        c1, c2, c3 = st.columns(3)
        sA = c1.number_input("|A|", 0, 100, 50, key='sa')
        sB = c2.number_input("|B|", 0, 100, 40, key='sb')
        sC = c3.number_input("|C|", 0, 100, 30, key='sc')
        
        d1, d2, d3 = st.columns(3)
        sAB = d1.number_input("|A ∩ B|", 0, min(sA, sB), 10, key='sab')
        sAC = d2.number_input("|A ∩ C|", 0, min(sA, sC), 15, key='sac')
        sBC = d3.number_input("|B ∩ C|", 0, min(sB, sC), 12, key='sbc')
        
        sABC = st.number_input("|A ∩ B ∩ C|", 0, min(sAB, sAC, sBC), 5, key='sabc')
        
        total3 = inclusion_exclusion_3(sA, sB, sC, sAB, sAC, sBC, sABC)
        
        st.latex(f"|A \\cup B \\cup C| = {sA} + {sB} + {sC} - {sAB} - {sAC} - {sBC} + {sABC} = {total3}")
        
    with tab_euler:
        st.markdown("#### CS Application: Euler's Totient Function $\\phi(n)$")
        st.markdown("Counts positive integers $\le n$ that are coprime to $n$. Crucial for RSA cryptography. Uses inclusion-exclusion internally on prime factors.")
        
        n_val = st.number_input("n", 2, 10000, 10)
        phi_n = euler_totient(n_val)
        
        st.latex(f"\\phi({n_val}) = {phi_n}")
        if n_val <= 100:
            coprimes = [i for i in range(1, n_val+1) if math.gcd(i, n_val) == 1]
            st.markdown(f"**Coprimes:** {coprimes}")

    st.markdown("### 🧪 Quick Check")
    q4 = st.radio(
        "If $|A|=10, |B|=10$, and $|A \\cup B|=15$, what is $|A \\cap B|$?",
        ["0", "5", "10", "20"],
        key="qc_ie"
    )
    if st.button("Check", key="check_qc_ie"):
        if q4 == "5":
            st.success("Correct! 15 = 10 + 10 - |A ∩ B|, so |A ∩ B| = 5.")
        else:
            st.error("Incorrect. Use the formula |A ∪ B| = |A| + |B| - |A ∩ B| and solve for the intersection.")


# ==========================================
# 4. Main entry point
# ==========================================
def main():
    theme.chapter_header("COUNTING", "Chapter 5: Counting & Combinatorics", "Sum & product rules, permutations, pigeonhole and inclusion–exclusion.")
    tabs = st.tabs(["Overview", "1. Basic Principles", "2. Permutations/Combinations", "3. Pigeonhole Principle", "4. Inclusion-Exclusion"])
    with tabs[0]: render_overview()
    with tabs[1]: render_basics()
    with tabs[2]: render_perms_combs()
    with tabs[3]: render_pigeonhole()
    with tabs[4]: render_inclusion_exclusion()

if __name__ == "__main__":
    main()
