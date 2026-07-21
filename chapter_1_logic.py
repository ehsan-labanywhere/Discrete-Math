import streamlit as st
import pandas as pd
import numpy as np
import graphviz
import itertools
from collections import deque

# ==========================================
# 1. Page configuration and styling 
# ==========================================
st.set_page_config(page_title="Ch 1: Logic & Proofs", layout="wide")

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
# 2. Core logic utilities (Backend logic)
# ==========================================

class _Bool:
    """Boolean wrapper so that logical symbols map to Python operators with the
    correct precedence: ¬ (~) binds tightest, then ∧ (&), then ∨ (|), and
    finally → (<=) and ↔ (==) bind loosest.

    Using plain `not`/`and`/`or` with `<=` breaks precedence: e.g. `not p <= q`
    parses as `not (p <= q)` and `p <= not q` is a syntax error.
    """
    def __init__(self, v):
        self.v = bool(v)
    def __invert__(self):            # ¬p
        return _Bool(not self.v)
    def __and__(self, other):        # p ∧ q
        return _Bool(self.v and other.v)
    def __or__(self, other):         # p ∨ q
        return _Bool(self.v or other.v)
    def __le__(self, other):         # p → q
        return _Bool((not self.v) or other.v)
    def __eq__(self, other):         # p ↔ q
        return _Bool(self.v == other.v)
    def __bool__(self):
        return self.v

def eval_logic(expr_str, env):
    """Evaluate a logical expression string given an environment dictionary of boolean values."""
    if not expr_str:
        return False
    # Replace math symbols with Python operators (evaluated on _Bool wrappers)
    s = expr_str.replace('∧', ' & ')
    s = s.replace('∨', ' | ')
    s = s.replace('¬', ' ~ ')
    s = s.replace('→', ' <= ')
    s = s.replace('↔', ' == ')
    wrapped_env = {k: _Bool(v) for k, v in env.items()}
    try:
        return bool(eval(s, {"__builtins__": None}, wrapped_env))
    except Exception:
        return None

def generate_truth_table(variables, expr_str):
    """Generate all rows for a truth table for the given expression."""
    rows = []
    # Generate all combinations of True/False for the variables
    for vals in itertools.product([True, False], repeat=len(variables)):
        env = dict(zip(variables, vals))
        res = eval_logic(expr_str, env)
        row = dict(env)
        row['Result'] = res
        rows.append(row)
    return rows

def classify_expression(rows):
    """Classify based on truth table result column."""
    if not rows: return "Unknown"
    results = [r['Result'] for r in rows if r['Result'] is not None]
    if not results: return "Invalid Expression"
    if all(results): return "Tautology"
    if not any(results): return "Contradiction"
    return "Contingency"

def check_equivalence(expr1, expr2, variables):
    """Compare two expressions column by column."""
    table1 = generate_truth_table(variables, expr1)
    table2 = generate_truth_table(variables, expr2)
    
    res1 = [r['Result'] for r in table1]
    res2 = [r['Result'] for r in table2]
    
    if None in res1 or None in res2:
        return False, pd.DataFrame()
        
    is_equiv = (res1 == res2)
    
    df_data = []
    for i, r in enumerate(table1):
        row = {var: r[var] for var in variables}
        row['Expr 1'] = res1[i]
        row['Expr 2'] = res2[i]
        row['Match'] = "✅" if res1[i] == res2[i] else "❌"
        df_data.append(row)
        
    return is_equiv, pd.DataFrame(df_data)

def evaluate_predicate(predicate_rule, domain):
    """Evaluate a predicate function over a finite domain."""
    results = {}
    for x in domain:
        try:
            results[x] = bool(eval(predicate_rule, {"__builtins__": None}, {'x': x}))
        except:
            results[x] = False
    return results

def draw_logic_gate(op_type):
    """Returns a graphviz Digraph for a logic gate."""
    g = graphviz.Digraph(format='png')
    g.attr(rankdir='LR')
    if "NOT" in op_type:
        g.node('p', 'p')
        g.node('op', 'NOT Gate', shape='invtriangle')
        g.node('out', 'Output')
        g.edge('p', 'op')
        g.edge('op', 'out')
    else:
        g.node('p', 'p')
        g.node('q', 'q')
        gate_name = op_type.split(' ')[0] + ' Gate'
        g.node('op', gate_name, shape='box')
        g.node('out', 'Output')
        g.edge('p', 'op')
        g.edge('q', 'op')
        g.edge('op', 'out')
    return g

# ==========================================
# 3. Module rendering functions
# ==========================================

def render_overview():
    st.header("Chapter 1: Logic & Proofs")
    st.markdown("""
    ### From Textbook to Interactive Tool
    This app transforms static logic concepts into an **active CS playground** connecting 4 key areas:
    
    1.  **Propositions & Connectives**: 
        * *Concept*: Basic statements and logical operations (AND, OR, NOT).
        * *CS Bridge*: **Logic Gates** (Hardware) & **Boolean Expressions** (Programming).
    2.  **Truth Tables & Equivalences**: 
        * *Concept*: Exhaustive evaluation and De Morgan's Laws.
        * *CS Bridge*: **Data validation rules** and **optimizing conditional logic**.
    3.  **Predicate Logic & Quantifiers**: 
        * *Concept*: Statements about collections of objects (For All, Exists).
        * *CS Bridge*: **SQL WHERE clauses** and **Loop conditions** (`all()` / `any()`).
    4.  **Proof Methods**: 
        * *Concept*: Establishing universal truths (Direct, Contradiction, Induction).
        * *CS Bridge*: **Algorithm correctness verification**.
    """)
    st.info("👈 Select a module from the tabs above to start experimenting.")

def render_propositions():
    st.subheader("1. Propositions & Connectives")
    st.markdown("Focus: **Basic statements** & **Logical combinations**.")
    
    with st.expander("🛠️ Define Propositions", expanded=True):
        c1, c2, c3 = st.columns(3)
        p_text = c1.text_input("Proposition p:", "It is raining", key="prop_p")
        q_text = c2.text_input("Proposition q:", "I carry an umbrella", key="prop_q")
        r_text = c3.text_input("Proposition r:", "I stay dry", key="prop_r")
        
    st.markdown("#### The Connectives & Logic Gates")
    
    op = st.selectbox("Select Connective to Explore", ["AND (∧)", "OR (∨)", "NOT (¬)", "IMPLIES (→)", "IFF (↔)"], key="conn_select")
    
    c_math, c_cs = st.columns(2)
    
    with c_math:
        st.markdown("#### 📐 Math Notation & Truth Table")
        if "AND" in op:
            st.latex(r"p \land q")
            st.caption(f"Statement: {p_text} AND {q_text}")
            expr = "p ∧ q"
            vars_list = ['p', 'q']
        elif "OR" in op:
            st.latex(r"p \lor q")
            st.caption(f"Statement: {p_text} OR {q_text}")
            expr = "p ∨ q"
            vars_list = ['p', 'q']
        elif "NOT" in op:
            st.latex(r"\lnot p")
            st.caption(f"Statement: It is NOT the case that {p_text}")
            expr = "¬p"
            vars_list = ['p']
        elif "IMPLIES" in op:
            st.latex(r"p \rightarrow q")
            st.caption(f"Statement: IF {p_text}, THEN {q_text}")
            expr = "p → q"
            vars_list = ['p', 'q']
        elif "IFF" in op:
            st.latex(r"p \leftrightarrow q")
            st.caption(f"Statement: {p_text} IF AND ONLY IF {q_text}")
            expr = "p ↔ q"
            vars_list = ['p', 'q']
            
        tt = generate_truth_table(vars_list, expr)
        st.dataframe(pd.DataFrame(tt), use_container_width=True)
        
    with c_cs:
        st.markdown("#### 💻 CS Bridge: Logic Gates")
        st.markdown("""<div class='highlight-box'>Math <span class='math-tag'>Connective</span> = CS <span class='db-tag'>Logic Gate</span></div>""", unsafe_allow_html=True)
        try:
            g = draw_logic_gate(op)
            st.graphviz_chart(g)
        except:
            st.error("Graphviz not installed.")
            
    st.divider()
    st.markdown("### 🎯 Build a Compound Expression")
    comp_c1, comp_c2, comp_c3 = st.columns(3)
    var1 = comp_c1.selectbox("Var 1", ['p', 'q', 'r', '¬p', '¬q', '¬r'], key="b_var1")
    conn = comp_c2.selectbox("Connective", ['∧', '∨', '→', '↔'], key="b_conn")
    var2 = comp_c3.selectbox("Var 2", ['p', 'q', 'r', '¬p', '¬q', '¬r'], index=1, key="b_var2")
    
    compound_expr = f"({var1} {conn} {var2})"
    st.latex(compound_expr.replace('∧', r'\land').replace('∨', r'\lor').replace('¬', r'\lnot').replace('→', r'\rightarrow').replace('↔', r'\leftrightarrow'))
    
    st.markdown("### 🧪 Quick Check")
    q1 = st.radio(
        "Which logic gate outputs True ONLY when all inputs are True?",
        ["OR Gate", "AND Gate", "NOT Gate", "XOR Gate"],
        key="qc_prop_1"
    )
    if st.button("Check", key="check_qc_prop_1"):
        if q1 == "AND Gate":
            st.success("Correct. The AND gate corresponds to the logical conjunction (∧).")
        else:
            st.error("Not quite. AND is the only gate that requires ALL inputs to be True.")

def render_truth_tables():
    st.subheader("2. Truth Tables & Equivalences")
    
    tab_gen, tab_equiv = st.tabs(["Truth Table Generator", "De Morgan's & Equivalences"])
    
    with tab_gen:
        st.markdown("Evaluate any expression up to 4 variables.")
        with st.expander("📝 Enter Expression", expanded=True):
            user_expr = st.text_input("Expression (use p, q, r, s and symbols ∧, ∨, ¬, →, ↔):", "p ∧ (q ∨ ¬r)", key="user_expr")
            st.caption("Copy symbols if needed: ∧  ∨  ¬  →  ↔")
        
        if user_expr:
            vars_found = sorted(list(set([c for c in user_expr if c in 'pqrs'])))
            if not vars_found:
                st.warning("No variables (p, q, r, s) found.")
            else:
                tt = generate_truth_table(vars_found, user_expr)
                df = pd.DataFrame(tt)
                
                if df['Result'].isnull().any():
                    st.error("Invalid expression format. Please check your syntax.")
                else:
                    classification = classify_expression(tt)
                    
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        def highlight_result(val):
                            color = '#d1e7dd' if val is True else '#f8d7da'
                            return f'background-color: {color}'
                        st.dataframe(df.style.map(highlight_result, subset=['Result']), use_container_width=True)
                    with c2:
                        st.markdown(f"**Classification:**")
                        if classification == "Tautology":
                            st.success(classification + "\n\nAlways True!")
                        elif classification == "Contradiction":
                            st.error(classification + "\n\nAlways False!")
                        else:
                            st.info(classification + "\n\nMixed True/False.")
                        
                        st.markdown("#### CS Bridge")
                        st.markdown("In programming, a **Tautology** in a `if` statement means the condition is useless (always runs), and a **Contradiction** means dead code (never runs).")
    
    with tab_equiv:
        st.markdown("### Logical Equivalence Checker")
        st.markdown("Two expressions are logically equivalent ($A \equiv B$) if their truth tables match exactly.")
        
        with st.expander("📘 Theory Notes: De Morgan's Laws"):
            st.latex(r"\lnot (p \land q) \equiv \lnot p \lor \lnot q")
            st.latex(r"\lnot (p \lor q) \equiv \lnot p \land \lnot q")
            st.caption("De Morgan's laws show how to distribute negation inside parentheses.")
            
        col1, col2 = st.columns(2)
        expr1 = col1.text_input("Expression 1", "¬(p ∧ q)", key="equiv_1")
        expr2 = col2.text_input("Expression 2", "¬p ∨ ¬q", key="equiv_2")
        
        if expr1 and expr2:
            vars1 = set([c for c in expr1 if c in 'pqrs'])
            vars2 = set([c for c in expr2 if c in 'pqrs'])
            all_vars = sorted(list(vars1.union(vars2)))
            
            if not all_vars:
                st.warning("No variables found.")
            else:
                is_equiv, df_compare = check_equivalence(expr1, expr2, all_vars)
                
                if df_compare.empty:
                    st.error("Error evaluating expressions.")
                else:
                    if is_equiv:
                        st.success(f"✅ They are Equivalent! (Truth values match for all rows)")
                    else:
                        st.error(f"❌ Not Equivalent. (Found mismatches)")
                        
                    st.dataframe(df_compare, use_container_width=True)
        
        st.markdown("### 🧪 Quick Check")
        q2 = st.radio(
            "By De Morgan's Law, ¬(p ∨ q) is equivalent to:",
            ["¬p ∨ ¬q", "¬p ∧ ¬q", "p ∧ q", "p ∨ ¬q"],
            key="qc_tt_1"
        )
        if st.button("Check", key="check_qc_tt_1"):
            if q2 == "¬p ∧ ¬q":
                st.success("Correct! The negation of a disjunction is the conjunction of the negations.")
            else:
                st.error("Not quite. Remember that De Morgan's flips the operator (∨ becomes ∧).")

def render_predicates():
    st.subheader("3. Predicate Logic & Quantifiers")
    
    with st.expander("🌐 Define Domain and Predicate", expanded=True):
        c1, c2 = st.columns([1, 2])
        domain_str = c1.text_input("Domain (integers):", "1, 2, 3, 4, 5", key="pred_domain")
        try:
            domain = sorted(list(set([int(x.strip()) for x in domain_str.split(',') if x.strip()])))
        except:
            domain = [1,2,3,4,5]
            
        pred_rule = c2.selectbox("Predicate P(x):", ["x > 3", "x % 2 == 0", "x * x < 20", "x == 3"], key="pred_rule")
        st.caption(f"Domain D = {domain}")
    
    eval_results = evaluate_predicate(pred_rule, domain)
    
    col_u, col_e = st.columns(2)
    
    with col_u:
        st.markdown("#### Universal Quantifier $\\forall x P(x)$")
        st.markdown("For ALL x in the domain, P(x) is true.")
        all_true = all(eval_results.values())
        if all_true:
            st.success("✅ True! Every element satisfies the predicate.")
        else:
            counterexamples = [x for x, val in eval_results.items() if not val]
            st.error(f"❌ False! Counterexample found: x = {counterexamples[0]}")
            
        st.markdown("**CS Bridge (Python):**")
        st.code(f"all(P(x) for x in {domain})")

    with col_e:
        st.markdown("#### Existential Quantifier $\\exists x P(x)$")
        st.markdown("There EXISTS at least one x in the domain where P(x) is true.")
        any_true = any(eval_results.values())
        if any_true:
            witnesses = [x for x, val in eval_results.items() if val]
            st.success(f"✅ True! Witness found: x = {witnesses[0]}")
        else:
            st.error("❌ False! No element satisfies the predicate.")
            
        st.markdown("**CS Bridge (Python):**")
        st.code(f"any(P(x) for x in {domain})")
        
    st.divider()
    st.markdown("### Nested Quantifiers")
    st.markdown("Evaluate $\\forall x \\exists y (x + y = 6)$ over the same domain.")
    
    st.write("Let's test each $x$ to see if there is a corresponding $y$:")
    results_nested = []
    overall_nested = True
    for x in domain:
        found_y = False
        matching_y = None
        for y in domain:
            if x + y == 6:
                found_y = True
                matching_y = y
                break
        results_nested.append({"x": x, "∃y (x+y=6)": found_y, "Witness y": matching_y if found_y else "None"})
        if not found_y:
            overall_nested = False
            
    st.dataframe(pd.DataFrame(results_nested), use_container_width=True)
    if overall_nested:
        st.success("The nested statement $\\forall x \\exists y (x + y = 6)$ is **True** for this domain.")
    else:
        st.error("The nested statement $\\forall x \\exists y (x + y = 6)$ is **False** for this domain.")
        
    st.markdown("### 🧪 Quick Check")
    q3 = st.radio(
        "In SQL, which clause acts most like a filter based on a Predicate P(x)?",
        ["SELECT", "FROM", "WHERE", "ORDER BY"],
        key="qc_pred_1"
    )
    if st.button("Check", key="check_qc_pred_1"):
        if q3 == "WHERE":
            st.success("Correct! WHERE filters rows based on whether they satisfy a logical predicate.")
        else:
            st.error("Not quite. WHERE is the clause that evaluates a logical condition (predicate).")

def render_proofs():
    st.subheader("4. Proof Methods")
    
    proof_type = st.radio(
        "Select a proof method to explore:",
        ["Direct Proof", "Contrapositive", "Contradiction", "Mathematical Induction"],
        horizontal=True,
        key="proof_type"
    )
    
    st.divider()
    
    if proof_type == "Direct Proof":
        st.markdown("### Direct Proof")
        st.markdown("**Theorem**: If $n$ is an even integer, then $n^2$ is even.")
        st.info("Assume the hypothesis ($p$) is true, and show that the conclusion ($q$) follows.")
        
        test_n = st.slider("Try it: Pick an even integer n", 2, 20, 4, step=2, key="dp_n")
        st.markdown(f"1. **Assume**: $n = {test_n}$ is even. (Meaning $n = 2k$ for some integer $k$)")
        st.markdown(f"2. Let's find $k$: $k = {test_n // 2}$")
        st.markdown(f"3. Calculate $n^2$: ${test_n}^2 = {test_n**2}$")
        st.markdown(f"4. **Show** $n^2$ is even: ${test_n**2} = 2 \\times {(test_n**2)//2}$")
        st.success(f"Since ${test_n**2}$ can be written as $2 \\times$ an integer, it is even. ✅")

    elif proof_type == "Contrapositive":
        st.markdown("### Proof by Contrapositive")
        st.markdown("Instead of proving $p \\rightarrow q$, we prove its logical equivalent: $\\lnot q \\rightarrow \\lnot p$.")
        st.markdown("**Theorem**: If $n^2$ is odd, then $n$ is odd.")
        
        st.markdown("**1. Form the Contrapositive:**")
        st.latex(r"\text{If } n \text{ is EVEN (not odd), then } n^2 \text{ is EVEN (not odd).}")
        
        st.info("Notice that this is exactly the same statement we proved in the Direct Proof section!")
        st.markdown("**CS Bridge:** Sometimes checking `if not condition_B` is computationally easier than checking `if condition_A` directly.")
        
    elif proof_type == "Contradiction":
        st.markdown("### Proof by Contradiction")
        st.markdown("**Theorem**: $\\sqrt{2}$ is irrational.")
        st.info("Assume the statement is FALSE, and show this leads to a logical impossibility (a contradiction).")
        
        st.markdown("""
        1. **Assume the opposite:** $\\sqrt{2}$ is rational.
        2. Then $\\sqrt{2} = \\frac{a}{b}$ for some integers $a, b$ with no common factors (lowest terms).
        3. Squaring both sides: $2 = \\frac{a^2}{b^2} \\implies a^2 = 2b^2$.
        4. This means $a^2$ is even, so $a$ must be even ($a = 2k$).
        5. Substitute $a$: $(2k)^2 = 2b^2 \\implies 4k^2 = 2b^2 \\implies b^2 = 2k^2$.
        6. This means $b^2$ is even, so $b$ must be even.
        7. **CONTRADICTION!** Both $a$ and $b$ are even, meaning they share a factor of 2. This contradicts our assumption in step 2 that they have no common factors.
        """)
        st.success("Therefore, our assumption must be false. $\\sqrt{2}$ is irrational. ✅")

    elif proof_type == "Mathematical Induction":
        st.markdown("### Mathematical Induction")
        st.markdown("**Theorem**: The sum of the first $n$ positive integers is $\\frac{n(n+1)}{2}$.")
        
        n_val = st.slider("Select n for demonstration:", 1, 10, 5, key="ind_n")
        
        st.markdown("#### Step 1: Base Case (n=1)")
        st.markdown(f"Left side: $1$")
        st.markdown(f"Right side: $\\frac{{1(1+1)}}{{2}} = 1$")
        st.success("Base case holds.")
        
        st.markdown("#### Step 2: Inductive Step")
        st.markdown("Assume true for $k$. Show true for $k+1$.")
        
        st.markdown(f"**Let's verify for $n={n_val}$:**")
        sum_actual = sum(range(1, n_val + 1))
        formula_val = (n_val * (n_val + 1)) // 2
        
        seq_str = " + ".join(map(str, range(1, n_val + 1)))
        st.markdown(f"**Actual Sum**: {seq_str} = **{sum_actual}**")
        st.markdown(f"**Formula**: $\\frac{{{n_val}({n_val}+1)}}{{2}} = \\frac{{{n_val * (n_val+1)}}}{{2}}$ = **{formula_val}**")
        
        if sum_actual == formula_val:
            st.success("Matches perfectly! ✅")
            
        st.markdown("**CS Bridge:** Induction is deeply connected to verifying **recursive functions**. Base cases map to recursion base cases, and inductive steps map to the recursive calls.")

    st.divider()
    st.markdown("### 🧪 Quick Check")
    q4 = st.radio(
        "Which proof method assumes the conclusion is FALSE to find a logical error?",
        ["Direct Proof", "Contrapositive", "Contradiction", "Induction"],
        key="qc_proof_1"
    )
    if st.button("Check", key="check_qc_proof_1"):
        if q4 == "Contradiction":
            st.success("Correct! Proof by contradiction assumes ¬q and derives a false statement.")
        else:
            st.error("Not quite. Proof by contradiction relies on finding a logical impossibility.")

# ==========================================
# 4. Main entry point
# ==========================================
def main():
    st.title("Chapter 1: Logic & Proofs")
    tabs = st.tabs(["Overview", "1. Propositions", "2. Truth Tables", "3. Predicates", "4. Proofs"])
    with tabs[0]: render_overview()
    with tabs[1]: render_propositions()
    with tabs[2]: render_truth_tables()
    with tabs[3]: render_predicates()
    with tabs[4]: render_proofs()

if __name__ == "__main__":
    main()
