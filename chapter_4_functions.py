import streamlit as st
import pandas as pd
import numpy as np
import graphviz
import math

# ==========================================
# 1. Page configuration and styling
# ==========================================
st.set_page_config(page_title="Ch 4: Functions", layout="wide")

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
# 2. Core algorithm utilities
# ==========================================
def parse_set_input(input_str):
    try: return sorted(list(set([int(x.strip()) for x in input_str.split(',') if x.strip()])))
    except: return [1, 2, 3, 4]

def format_set_display(s):
    return "{" + ", ".join(map(str, s)) + "}"

def apply_function_rule(rule, x, mod_val=5):
    if rule == "f(x) = x + 1":
        return x + 1
    elif rule == "f(x) = x²":
        return x ** 2
    elif rule == "f(x) = x mod n":
        return x % mod_val
    elif rule == "f(x) = 2x":
        return 2 * x
    elif rule == "f(x) = x":
        return x
    return x

def compute_function_pairs(A, rule, mod_val=5):
    pairs = []
    for a in A:
        pairs.append((a, apply_function_rule(rule, a, mod_val)))
    return pairs

def display_function_smart(pairs, label, prefix=None, max_latex=25):
    st.markdown(f"#### {label}")
    if not pairs:
        if prefix: st.latex(prefix + r"\ \{\}")
        else: st.latex(r"\{\}")
        return
    
    if len(pairs) <= max_latex:
        items = ", ".join([f"({a},{b})" for a, b in pairs])
        expr = f"\\{{ {items} \\}}"
        if prefix: st.latex(prefix + r"\ " + expr)
        else: st.latex(expr)
        st.caption(f"Displayed as math notation ({len(pairs)} pairs).")
    else:
        df = pd.DataFrame(pairs, columns=["Domain", "Codomain"])
        df.index += 1
        st.dataframe(df, use_container_width=True)
        st.caption(f"Displayed as a table because there are {len(pairs)} pairs.")

def check_injective(pairs):
    seen = set()
    for _, b in pairs:
        if b in seen:
            return False
        seen.add(b)
    return True

def check_surjective(pairs, codomain):
    image = set(b for _, b in pairs)
    return image.issuperset(codomain)

def compose_functions(f_pairs, g_pairs):
    g_dict = {a: b for a, b in g_pairs}
    g_of_f = []
    for a, b in f_pairs:
        if b in g_dict:
            g_of_f.append((a, g_dict[b]))
    return g_of_f

def compute_inverse(pairs):
    return [(b, a) for a, b in pairs]

def floor_val(x):
    return math.floor(x)

def ceil_val(x):
    return math.ceil(x)

def mod_val_func(x, n):
    return x % n

def draw_arrow_diagram(A, B, pairs, label_A="A", label_B="B"):
    try:
        g = graphviz.Digraph(format='png')
        g.attr(rankdir='LR')
        
        with g.subgraph(name='cluster_A') as c:
            c.attr(label=label_A, color='blue')
            for a in A:
                c.node(f"A_{a}", str(a))
                
        with g.subgraph(name='cluster_B') as c:
            c.attr(label=label_B, color='red')
            for b in B:
                c.node(f"B_{b}", str(b))
                
        for a, b in pairs:
            if b in B:
                g.edge(f"A_{a}", f"B_{b}")
            else:
                g.node(f"B_out_{b}", str(b), color='gray')
                g.edge(f"A_{a}", f"B_out_{b}", color='gray', style='dashed')
                
        return g
    except:
        return None

# ==========================================
# 3. Module rendering functions
# ==========================================

def render_overview():
    st.header("Chapter 4: Functions")
    st.markdown("""
    ### From Math to Code: Functions
    Functions are a fundamental mathematical mapping concept. In this module, we bridge the gap between abstract mappings and real-world Computer Science applications.
    
    1.  **Function Basics**: 
        * *Concept*: Mapping elements from a Domain A to a Codomain B.
        * *CS Bridge*: Python `def`, APIs, method signatures.
    2.  **Properties**: 
        * *Concept*: Injective, Surjective, and Bijective functions.
        * *CS Bridge*: Hash collisions, encryption invertibility.
    3.  **Composition & Inverse**: 
        * *Concept*: Combining functions ($g \circ f$) and reversing them ($f^{-1}$).
        * *CS Bridge*: Function pipelines, middleware, Unix pipes.
    4.  **Special Functions**: 
        * *Concept*: Floor, ceiling, modular arithmetic.
        * *CS Bridge*: Array indexing, hash functions, cryptography.
    """)
    st.info("👈 Select a module from the tabs above to start experimenting.")

def render_basics():
    st.subheader("1. Function Basics")
    st.markdown("Focus: **Domain, Codomain, Mappings**, and the **Python `def`** parallel.")
    
    with st.expander("🛠️ Define Function f: A → B", expanded=True):
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        A = parse_set_input(c1.text_input("Domain A (comma-separated)", "1, 2, 3, 4", key="b_dom"))
        B = parse_set_input(c2.text_input("Codomain B (comma-separated)", "1, 2, 3, 4, 5, 6, 7, 8", key="b_codom"))
        
        rule = c3.selectbox("Function Rule f(x)", [
            "f(x) = x + 1", "f(x) = x²", "f(x) = x mod n", "f(x) = 2x", "f(x) = x"
        ], key="b_rule")
        
        mod_v = 5
        if rule == "f(x) = x mod n":
            mod_v = c4.number_input("n for modulo", 2, 20, 5, key="b_mod")
            
    if A and B:
        pairs = compute_function_pairs(A, rule, mod_v)
        image = sorted(list(set([b for a, b in pairs])))
        
        c_math, c_cs = st.columns([1, 1])
        with c_math:
            st.markdown("#### 📐 Math Notation")
            st.latex(f"A = {format_set_display(A)}")
            st.latex(f"B = {format_set_display(B)}")
            st.markdown("**Function f (Ordered Pairs):**")
            display_function_smart(pairs, "Set of Pairs", prefix="f =", max_latex=20)
            st.latex(f"\\text{{Image}} = {format_set_display(image)}")
            
            st.markdown("#### 🏹 Arrow Diagram")
            g = draw_arrow_diagram(A, B, pairs)
            if g:
                st.graphviz_chart(g)
            else:
                st.error("Graphviz not installed.")
                
        with c_cs:
            st.markdown("#### 💻 CS Bridge: Python `def`")
            st.markdown("""<div class='highlight-box'>Math <span class='math-tag'>f: A → B</span> = CS <span class='db-tag'>def f(x: int) -> int:</span></div>""", unsafe_allow_html=True)
            code = f"""def f(x):
    # Rule: {rule}
"""
            if rule == "f(x) = x + 1":
                code += "    return x + 1"
            elif rule == "f(x) = x²":
                code += "    return x ** 2"
            elif rule == "f(x) = x mod n":
                code += f"    return x % {mod_v}"
            elif rule == "f(x) = 2x":
                code += "    return 2 * x"
            else:
                code += "    return x"
                
            code += f"\n\n# Mapping Domain A\nA = {A}\nimage = list(map(f, A))\nprint(image) # {image}"
            st.code(code, language="python")
            
            st.markdown("### 🧪 Quick Check")
            q1 = st.radio(
                "If an element in Domain A maps to a value NOT in Codomain B, what happens?",
                ["It's perfectly fine", "It's no longer a valid function from A to B", "It becomes a surjective function"],
                key="qc_basics"
            )
            if st.button("Check", key="btn_qc_basics"):
                if q1 == "It's no longer a valid function from A to B":
                    st.success("Correct! A function f: A → B must map every element in A to some element specifically in B.")
                else:
                    st.error("Not quite. A valid function from A to B requires all outputs to be in B.")

def render_properties():
    st.subheader("2. Properties: Injective, Surjective, Bijective")
    
    with st.expander("🛠️ Define Function to Test Properties", expanded=True):
        c1, c2, c3 = st.columns([1, 1, 2])
        A = parse_set_input(c1.text_input("Domain A", "1, 2, 3, 4", key="p_dom"))
        B = parse_set_input(c2.text_input("Codomain B", "1, 2, 3, 4", key="p_codom"))
        
        rule = c3.selectbox("Function Rule f(x)", [
            "f(x) = x", "f(x) = x + 1", "f(x) = x²", "f(x) = x mod n", "f(x) = 2x"
        ], key="p_rule")
        
        mod_v = 3
        if rule == "f(x) = x mod n":
            mod_v = st.number_input("n for modulo", 2, 20, 3, key="p_mod")

    pairs = compute_function_pairs(A, rule, mod_v)
    is_valid = all(b in B for a, b in pairs)
    
    if not is_valid:
        st.warning("⚠️ Warning: Some outputs are NOT in the Codomain B. This is not a valid function f: A → B.")
        
    is_inj = check_injective(pairs)
    is_surj = check_surjective(pairs, B)
    is_bij = is_inj and is_surj and is_valid
    
    c_m1, c_m2, c_m3 = st.columns(3)
    c_m1.metric("Injective (One-to-One)", "Yes" if is_inj else "No")
    c_m2.metric("Surjective (Onto)", "Yes" if (is_surj and is_valid) else "No")
    c_m3.metric("Bijective (One-to-One Correspondence)", "Yes" if is_bij else "No")
    
    st.divider()
    c_viz, c_cs = st.columns([1, 1])
    
    with c_viz:
        st.markdown("#### 🏹 Visualization")
        g = draw_arrow_diagram(A, B, pairs)
        if g:
            st.graphviz_chart(g)
            
        if not is_inj:
            st.info("💡 **Not Injective:** Notice how multiple arrows point to the same element in B (collision).")
        if not is_surj:
            st.info("💡 **Not Surjective:** Notice how some elements in B have no arrows pointing to them.")
            
    with c_cs:
        st.markdown("#### 💻 CS Bridge: Collisions & Encryption")
        st.markdown("""
        **Injective ↔ Hash Collisions**
        If a hash function is NOT injective, two different keys map to the same bucket. This is called a **collision**.
        
        **Bijective ↔ Encryption**
        For encryption to work, the mapping from plaintext to ciphertext MUST be **bijective**, so we can reliably decrypt it (invert it).
        """)
        
        st.markdown("### 🧪 Quick Check")
        q_prop = st.radio(
            "If a function is used to assign unique student IDs to students, what property MUST it have?",
            ["Surjective", "Injective", "None of these"],
            key="qc_prop"
        )
        if st.button("Check", key="btn_qc_prop"):
            if q_prop == "Injective":
                st.success("Correct! No two students should get the same ID.")
            else:
                st.error("Incorrect. It must be Injective so IDs are unique.")

def render_composition():
    st.subheader("3. Composition & Inverse")
    
    with st.expander("🛠️ Define f: A → B and g: B → C", expanded=True):
        c1, c2, c3 = st.columns(3)
        A = parse_set_input(c1.text_input("Set A", "1, 2, 3", key="c_A"))
        B = parse_set_input(c2.text_input("Set B", "2, 3, 4", key="c_B"))
        C = parse_set_input(c3.text_input("Set C", "4, 9, 16", key="c_C"))
        
        c4, c5 = st.columns(2)
        rule_f = c4.selectbox("Function f(x) [A → B]", [
            "f(x) = x + 1", "f(x) = x²", "f(x) = 2x"
        ], key="c_rule_f")
        rule_g = c5.selectbox("Function g(x) [B → C]", [
            "g(x) = x²", "g(x) = x + 1", "g(x) = 2x"
        ], key="c_rule_g")
        
    f_pairs = compute_function_pairs(A, rule_f)
    g_pairs = compute_function_pairs(B, rule_g)
    g_of_f = compose_functions(f_pairs, g_pairs)
    
    c_math, c_cs = st.columns([1, 1])
    
    with c_math:
        st.markdown("#### 📐 Composition: (g ∘ f)(x) = g(f(x))")
        display_function_smart(f_pairs, "f: A → B", prefix="f =")
        display_function_smart(g_pairs, "g: B → C", prefix="g =")
        display_function_smart(g_of_f, "g ∘ f: A → C", prefix="g \\circ f =")
        
        st.markdown("#### 🏹 Pipeline View")
        try:
            g_chart = graphviz.Digraph(format='png')
            g_chart.attr(rankdir='LR')
            
            with g_chart.subgraph(name='cluster_A') as ca:
                ca.attr(label='A')
                for a in A: ca.node(f"A_{a}", str(a))
            with g_chart.subgraph(name='cluster_B') as cb:
                cb.attr(label='B')
                for b in B: cb.node(f"B_{b}", str(b))
            with g_chart.subgraph(name='cluster_C') as cc:
                cc.attr(label='C')
                for c in C: cc.node(f"C_{c}", str(c))
                
            for a, b in f_pairs:
                g_chart.edge(f"A_{a}", f"B_{b}", label="f")
            for b, c in g_pairs:
                g_chart.edge(f"B_{b}", f"C_{c}", label="g")
                
            st.graphviz_chart(g_chart)
        except:
            st.error("Graphviz not installed.")
            
    with c_cs:
        st.markdown("#### 💻 CS Bridge: Function Pipelines")
        st.markdown("In Python, composition is simply passing the result of one function into another.")
        st.code("result = g(f(x))", language="python")
        st.markdown("Or using lambdas:")
        st.code("g_of_f = lambda x: g(f(x))", language="python")
        st.markdown("Unix pipes work exactly the same way: `cat file.txt | grep 'error'` is like `grep(cat('file.txt'))`.")
        
        st.markdown("### 🔄 Inverse Function $f^{-1}$")
        is_inj = check_injective(f_pairs)
        is_surj = check_surjective(f_pairs, B)
        is_bij = is_inj and is_surj and all(b in B for a, b in f_pairs)
        
        if is_bij:
            st.success("Function f is Bijective! We can compute its inverse.")
            inv_pairs = compute_inverse(f_pairs)
            display_function_smart(inv_pairs, "Inverse $f^{-1}: B \\rightarrow A$", prefix="f^{-1} =")
        else:
            st.warning("Function f is NOT Bijective, so it does not have a well-defined inverse mapping B entirely to A uniquely.")
            
        st.markdown("### 🧪 Quick Check")
        q_comp = st.radio(
            "If f(x) = x + 1 and g(x) = 2x, what is (g ∘ f)(3)?",
            ["7", "8", "6"],
            key="qc_comp"
        )
        if st.button("Check", key="btn_qc_comp"):
            if q_comp == "8":
                st.success("Correct! f(3) = 4, then g(4) = 8.")
            else:
                st.error("Incorrect. Remember to evaluate f(3) first, then pass the result to g.")

def render_special_functions():
    st.subheader("4. Special Functions")
    
    tab1, tab2 = st.tabs(["Floor & Ceiling", "Modular Arithmetic"])
    
    with tab1:
        st.markdown("### Floor $\\lfloor x \\rfloor$ and Ceiling $\\lceil x \\rceil$")
        val = st.number_input("Enter a real number x:", value=3.7, step=0.1)
        
        f_val = floor_val(val)
        c_val = ceil_val(val)
        
        c1, c2 = st.columns(2)
        c1.metric("Floor ⌊x⌋", f_val, help="Greatest integer ≤ x")
        c2.metric("Ceiling ⌈x⌉", c_val, help="Least integer ≥ x")
        
        st.markdown("#### 💻 CS Bridge")
        st.code(f'''import math\nmath.floor({val}) # Returns {f_val}\nmath.ceil({val})  # Returns {c_val}''', language="python")
        st.caption("Often used in UI layout calculations and pagination (e.g. `total_pages = ceil(total_items / items_per_page)`).")
        
    with tab2:
        st.markdown("### Modular Arithmetic: $a \\pmod n$")
        c1, c2 = st.columns(2)
        a_val = c1.number_input("Enter a:", value=17, step=1)
        n_val = c2.number_input("Enter n (modulus):", value=5, step=1, min_value=1)
        
        rem = mod_val_func(a_val, n_val)
        st.metric(f"{a_val} mod {n_val}", rem)
        
        st.markdown("#### 💻 CS Bridge: Hash Tables & Circular Buffers")
        st.write("Modulo is frequently used to constrain values within array bounds.")
        
        with st.expander("Interactive Hash Table Demo"):
            keys = st.text_input("Enter keys to insert (comma-separated):", "12, 44, 59, 32, 10")
            key_list = parse_set_input(keys)
            
            buckets = {i: [] for i in range(n_val)}
            for k in key_list:
                buckets[k % n_val].append(k)
                
            st.write(f"Hash function: `h(k) = k % {n_val}`")
            st.json(buckets)
            st.caption("Notice how keys mapping to the same bucket cause collisions!")
            
        st.markdown("### 🧪 Quick Check")
        q_mod = st.radio(
            "What is -2 mod 5 in standard mathematics?",
            ["-2", "3", "2"],
            key="qc_mod"
        )
        if st.button("Check", key="btn_qc_mod"):
            if q_mod == "3":
                st.success("Correct! -2 = -1*(5) + 3.")
            else:
                st.error("Incorrect. Standard math modulo results in a positive remainder 0 ≤ r < n.")

# ==========================================
# 4. Main entry point
# ==========================================
def main():
    st.title("Chapter 4: Functions")
    tabs = st.tabs(["Overview", "1. Basics", "2. Properties", "3. Composition & Inverse", "4. Special Functions"])
    with tabs[0]: render_overview()
    with tabs[1]: render_basics()
    with tabs[2]: render_properties()
    with tabs[3]: render_composition()
    with tabs[4]: render_special_functions()

if __name__ == "__main__":
    main()
