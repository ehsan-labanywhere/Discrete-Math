import streamlit as st
import theme
import pandas as pd
import numpy as np
import graphviz
from collections import deque

# ==========================================
# 1. Page configuration and styling
# ==========================================
theme.setup_page("Ch 7: Graph Theory", "🕸️")

# ==========================================
# 2. Core algorithm utilities
# ==========================================

def parse_set_input(input_str):
    try: return sorted(list(set([x.strip() for x in input_str.split(',') if x.strip()])))
    except: return ["A", "B", "C", "D"]

def build_adjacency_list(nodes, edges, directed=False):
    adj = {n: [] for n in nodes}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].append(v)
            if not directed and u != v:
                adj[v].append(u)
    return adj

def get_adjacency_matrix(nodes, edges, directed=False):
    size = len(nodes)
    matrix = np.zeros((size, size), dtype=int)
    idx_map = {val: i for i, val in enumerate(nodes)}
    for u, v in edges:
        if u in idx_map and v in idx_map:
            matrix[idx_map[u]][idx_map[v]] += 1
            if not directed and u != v:
                matrix[idx_map[v]][idx_map[u]] += 1
    return matrix, idx_map

def compute_degrees(nodes, edges, directed=False):
    if not directed:
        degrees = {n: 0 for n in nodes}
        for u, v in edges:
            if u in nodes and v in nodes:
                degrees[u] += 1
                if u != v:
                    degrees[v] += 1
                else:
                    degrees[u] += 1 # Loop adds 2 to degree
        return degrees, None
    else:
        in_deg = {n: 0 for n in nodes}
        out_deg = {n: 0 for n in nodes}
        for u, v in edges:
            if u in nodes and v in nodes:
                out_deg[u] += 1
                in_deg[v] += 1
        return in_deg, out_deg

def is_connected(nodes, edges, directed=False):
    if not nodes: return True
    adj = build_adjacency_list(nodes, edges, directed=False) # Undirected for weak connectivity
    visited = set()
    q = deque([nodes[0]])
    visited.add(nodes[0])
    while q:
        curr = q.popleft()
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return len(visited) == len(nodes)

def is_bipartite(nodes, edges, directed=False):
    if not nodes: return True
    adj = build_adjacency_list(nodes, edges, directed=False)
    color = {}
    for node in nodes:
        if node not in color:
            q = deque([node])
            color[node] = 0
            while q:
                curr = q.popleft()
                for neighbor in adj[curr]:
                    if neighbor not in color:
                        color[neighbor] = 1 - color[curr]
                        q.append(neighbor)
                    elif color[neighbor] == color[curr]:
                        return False
    return True

def bfs(nodes, edges, start, directed=False):
    adj = build_adjacency_list(nodes, edges, directed)
    visited = set()
    q = deque([start])
    visited.add(start)
    order = []
    while q:
        curr = q.popleft()
        order.append(curr)
        for neighbor in adj.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return order

def dfs(nodes, edges, start, directed=False):
    adj = build_adjacency_list(nodes, edges, directed)
    visited = set()
    order = []
    def dfs_recursive(node):
        visited.add(node)
        order.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                dfs_recursive(neighbor)
    if start in nodes:
        dfs_recursive(start)
    return order

def find_euler_path(nodes, edges, directed=False):
    if directed: return None
    if not is_connected(nodes, edges): return None
    deg, _ = compute_degrees(nodes, edges, directed)
    odds = [n for n in nodes if deg[n] % 2 != 0]
    if len(odds) > 2: return None
    
    # Hierholzer's algorithm roughly
    adj = build_adjacency_list(nodes, edges, directed=False)
    start_node = odds[0] if odds else nodes[0]
    
    path = []
    def visit(u):
        while adj[u]:
            v = adj[u].pop()
            if u in adj[v]: adj[v].remove(u)
            visit(v)
        path.append(u)
    
    visit(start_node)
    return path[::-1]

def greedy_coloring(nodes, edges):
    adj = build_adjacency_list(nodes, edges, directed=False)
    color_map = {}
    for node in nodes:
        used_colors = {color_map[neighbor] for neighbor in adj[node] if neighbor in color_map}
        color = 0
        while color in used_colors:
            color += 1
        color_map[node] = color
    return color_map

def check_valid_coloring(nodes, edges, colors):
    adj = build_adjacency_list(nodes, edges, directed=False)
    for u, v in edges:
        if colors.get(u) == colors.get(v):
            return False, (u, v)
    return True, None

def shortest_path_bfs(nodes, edges, start, end, directed=False):
    adj = build_adjacency_list(nodes, edges, directed)
    q = deque([start])
    prev = {start: None}
    while q:
        curr = q.popleft()
        if curr == end:
            break
        for neighbor in adj.get(curr, []):
            if neighbor not in prev:
                prev[neighbor] = curr
                q.append(neighbor)
    
    if end not in prev: return []
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    return path[::-1]


# ==========================================
# 3. Module rendering functions
# ==========================================

def render_overview():
    st.header("Chapter 7: Graph Theory")
    st.markdown("""
    ### From Textbook to Interactive Tool
    Graphs are the **universal modeling tool in Computer Science**. This chapter connects discrete math theory to practical algorithms.
    
    1. **Graph Basics**: 
       * *Concept*: Vertices, edges, degrees, and matrices.
       * *Bridge*: Social networks, handshaking lemma.
    2. **Properties & Types**:
       * *Concept*: Bipartite, complete, connected graphs.
       * *Bridge*: Network topology classification.
    3. **Paths & Traversal**:
       * *Concept*: BFS, DFS, Euler circuits.
       * *Bridge*: GPS navigation, web crawling.
    4. **Graph Coloring**:
       * *Concept*: Assigning colors avoiding conflicts, chromatic number.
       * *Bridge*: Exam scheduling, register allocation.
    """)
    st.info("👈 Select a module from the tabs above to start experimenting.")

def render_basics():
    st.subheader("1. Graph Basics & Representation")
    
    with st.expander("🛠️ Build your graph", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        nodes_input = c1.text_input("Vertices V (comma-separated)", "A, B, C, D")
        nodes = parse_set_input(nodes_input)
        is_directed = c2.checkbox("Directed Graph", value=False, key="basics_directed")
        
        st.markdown("Add Edges")
        ec1, ec2, ec3 = st.columns(3)
        edge_u = ec1.selectbox("From", nodes, key="basics_u")
        edge_v = ec2.selectbox("To", nodes, key="basics_v")
        
        if "basics_edges" not in st.session_state:
            st.session_state.basics_edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
            
        if ec3.button("Add Edge", key="basics_add"):
            if (edge_u, edge_v) not in st.session_state.basics_edges:
                st.session_state.basics_edges.append((edge_u, edge_v))
        if st.button("Clear Edges", key="basics_clear"):
            st.session_state.basics_edges = []
            
    edges = [e for e in st.session_state.basics_edges if e[0] in nodes and e[1] in nodes]
    
    c_graph, c_rep = st.columns(2)
    with c_graph:
        st.markdown("#### 🕸️ Visualization")
        try:
            g = graphviz.Digraph(format='png') if is_directed else graphviz.Graph(format='png')
            for n in nodes: g.node(str(n))
            for u, v in edges: g.edge(str(u), str(v))
            st.graphviz_chart(g)
        except: st.error("Graphviz not installed.")
        
    with c_rep:
        st.markdown("#### 🔢 Adjacency Matrix")
        mat, _ = get_adjacency_matrix(nodes, edges, is_directed)
        st.dataframe(pd.DataFrame(mat, index=nodes, columns=nodes).style.highlight_max(axis=None, color="#d1e7dd"), use_container_width=True)
        
        st.markdown("#### 📜 Adjacency List")
        adj = build_adjacency_list(nodes, edges, is_directed)
        st.json(adj)

    st.divider()
    st.markdown("### 📊 Degrees & Handshaking Lemma")
    
    if not is_directed:
        deg, _ = compute_degrees(nodes, edges, False)
        sum_deg = sum(deg.values())
        st.write(f"**Degree Sequence:** {sorted(list(deg.values()), reverse=True)}")
        st.metric("Sum of Degrees", sum_deg)
        st.metric("2 × |E|", 2 * len(edges))
        if sum_deg == 2 * len(edges):
            st.success("The Handshaking Lemma holds: Sum of degrees = 2|E|.")
    else:
        in_deg, out_deg = compute_degrees(nodes, edges, True)
        sum_in = sum(in_deg.values())
        sum_out = sum(out_deg.values())
        
        c1, c2 = st.columns(2)
        c1.write("**In-degrees:**")
        c1.json(in_deg)
        c1.metric("Sum In-degrees", sum_in)
        
        c2.write("**Out-degrees:**")
        c2.json(out_deg)
        c2.metric("Sum Out-degrees", sum_out)
        
        if sum_in == sum_out == len(edges):
             st.success("For directed graphs: Sum of In-degrees = Sum of Out-degrees = |E|.")
             
    st.markdown("<div class='highlight-box'>CS Bridge: In a social network (undirected), the Handshaking Lemma proves there must be an even number of people with an odd number of friends.</div>", unsafe_allow_html=True)
    
    st.markdown("### 🧪 Quick Check")
    q1 = st.radio("In an undirected graph, what does the degree of a vertex represent?", 
                  ["Number of edges connected to it", "Number of other vertices in the graph", "Length of the longest path"], key="qc_basic_1")
    if st.button("Check", key="check_qc_basic_1"):
        if q1 == "Number of edges connected to it": st.success("Correct!")
        else: st.error("Incorrect. It's the number of incident edges.")


def render_properties():
    st.subheader("2. Graph Types & Properties")
    
    with st.expander("🕸️ Generate Special Graph", expanded=True):
        st.markdown("Choose a standard graph type to explore:")
        graph_type = st.selectbox("Type", ["Custom (from Tab 1)", "Complete (K_n)", "Cycle (C_n)", "Path (P_n)", "Bipartite (K_{m,n})"])
        
        if graph_type == "Complete (K_n)":
            n = st.slider("n", 1, 10, 5, key="prop_kn_n")
            nodes = [str(i) for i in range(n)]
            edges = [(nodes[i], nodes[j]) for i in range(n) for j in range(i+1, n)]
        elif graph_type == "Cycle (C_n)":
            n = st.slider("n", 3, 10, 5, key="prop_cn_n")
            nodes = [str(i) for i in range(n)]
            edges = [(nodes[i], nodes[(i+1)%n]) for i in range(n)]
        elif graph_type == "Path (P_n)":
            n = st.slider("n", 2, 10, 5, key="prop_pn_n")
            nodes = [str(i) for i in range(n)]
            edges = [(nodes[i], nodes[i+1]) for i in range(n-1)]
        elif graph_type == "Bipartite (K_{m,n})":
            m = st.slider("m", 1, 5, 2, key="prop_bip_m")
            n = st.slider("n", 1, 5, 3, key="prop_bip_n")
            nodes = [f"U{i}" for i in range(m)] + [f"V{j}" for j in range(n)]
            edges = [(f"U{i}", f"V{j}") for i in range(m) for j in range(n)]
        else:
            nodes = parse_set_input("A, B, C, D")
            edges = st.session_state.get("basics_edges", [])
            
    c_graph, c_props = st.columns([1, 1])
    with c_graph:
        try:
            g = graphviz.Graph(format='png')
            for n_id in nodes: g.node(n_id)
            for u, v in edges: g.edge(u, v)
            st.graphviz_chart(g)
        except: st.error("Graphviz issue")
        
    with c_props:
        st.markdown("### 🔍 Properties")
        p1, p2, p3 = st.columns(3)
        connected = is_connected(nodes, edges)
        bipartite = is_bipartite(nodes, edges)
        
        p1.metric("Connected", "Yes" if connected else "No")
        p2.metric("Bipartite", "Yes" if bipartite else "No")
        
        deg, _ = compute_degrees(nodes, edges, False)
        eulerian = connected and all(d % 2 == 0 for d in deg.values())
        p3.metric("Eulerian", "Yes" if eulerian else "No")
        
        st.caption("A graph is Eulerian if it's connected and every vertex has an even degree.")
        
    st.divider()
    st.markdown("### 🎯 Try-it Prompts")
    st.write("Does the graph have a path that uses every edge exactly once? (Euler Path)")
    if st.button("Find Euler Path", key="btn_find_euler"):
        path = find_euler_path(nodes, edges)
        if path:
            st.success("✅ Euler Path/Circuit found!")
            st.write(" → ".join(path))
        else:
            st.error("❌ No Euler Path exists for this graph.")

    st.markdown("### 🧪 Quick Check")
    q2 = st.radio("What makes a graph Bipartite?", ["Can be colored with 2 colors", "Has an even number of vertices", "Is fully connected"], key="qc_prop_1")
    if st.button("Check", key="check_qc_prop_1"):
        if q2 == "Can be colored with 2 colors": st.success("Correct!")
        else: st.error("Incorrect. Bipartite means its vertices can be divided into two disjoint sets.")


def render_traversal():
    st.subheader("3. Paths, Circuits & Traversal")
    
    nodes = parse_set_input("1, 2, 3, 4, 5, 6")
    default_edges = [("1","2"), ("1","3"), ("2","4"), ("2","5"), ("3","6")]
    
    if "trav_edges" not in st.session_state:
        st.session_state.trav_edges = default_edges.copy()
        
    edges = st.session_state.trav_edges
    
    c1, c2 = st.columns([1, 1])
    with c1:
        start_node = st.selectbox("Start Node", nodes, key="trav_start")
        end_node = st.selectbox("End Node", nodes, key="trav_end")
    with c2:
        try:
            g = graphviz.Graph(format='png')
            for n in nodes: g.node(n)
            for u, v in edges: g.edge(u, v)
            st.graphviz_chart(g)
        except: pass
        
    tab_bfs, tab_dfs, tab_sp = st.tabs(["BFS Traversal", "DFS Traversal", "Shortest Path"])
    
    with tab_bfs:
        st.write("Breadth-First Search explores level by level.")
        if st.button("Run BFS", key="btn_run_bfs"):
            order = bfs(nodes, edges, start_node)
            st.success(f"BFS Order: {' → '.join(order)}")
            
    with tab_dfs:
        st.write("Depth-First Search goes as deep as possible before backtracking.")
        if st.button("Run DFS", key="btn_run_dfs"):
            order = dfs(nodes, edges, start_node)
            st.success(f"DFS Order: {' → '.join(order)}")
            
    with tab_sp:
        st.write("Using BFS to find the shortest path (unweighted graph).")
        if st.button("Find Shortest Path", key="btn_run_sp"):
            path = shortest_path_bfs(nodes, edges, start_node, end_node)
            if path:
                st.success(f"Path: {' → '.join(path)}")
                st.metric("Distance (edges)", len(path)-1)
            else:
                st.error("No path exists.")

    st.markdown("<div class='highlight-box'>CS Bridge: BFS is used in network routing and shortest-path finding (like GPS routing on unweighted maps), while DFS is used in maze solving and topological sorting.</div>", unsafe_allow_html=True)
    
    st.markdown("### 🧪 Quick Check")
    q3 = st.radio("Which traversal algorithm uses a Queue data structure?", ["BFS", "DFS"], key="qc_trav")
    if st.button("Check", key="check_qc_trav"):
        if q3 == "BFS": st.success("Correct!")
        else: st.error("Incorrect. DFS uses a Stack (or recursion).")

def render_coloring():
    st.subheader("4. Graph Coloring & Scheduling")
    
    st.write("Assign a color to each vertex such that no two adjacent vertices share the same color.")
    
    nodes = ["Math", "Physics", "Chem", "Bio", "CS"]
    edges = [("Math", "Physics"), ("Physics", "Chem"), ("Chem", "Bio"), ("Bio", "CS"), ("CS", "Math"), ("Math", "Chem")]
    
    st.write("**Scenario: Exam Scheduling**")
    st.caption("Edges represent students taking both courses (a conflict). Conflicting courses cannot be scheduled in the same timeslot (color).")
    
    try:
        g = graphviz.Graph(format='png')
        for n in nodes: g.node(n)
        for u, v in edges: g.edge(u, v)
        st.graphviz_chart(g)
    except: pass
    
    st.markdown("### 🎨 Color the Graph")
    colors = ["Red", "Green", "Blue", "Yellow", "Purple"]
    
    user_colors = {}
    cols = st.columns(len(nodes))
    for i, node in enumerate(nodes):
        user_colors[node] = cols[i].selectbox(node, colors, key=f"col_{node}")
        
    if st.button("Check My Coloring", key="btn_chk_col"):
        valid, conflict = check_valid_coloring(nodes, edges, user_colors)
        if valid:
            used_count = len(set(user_colors.values()))
            st.success(f"✅ Valid! You used {used_count} colors.")
        else:
            st.error(f"❌ Conflict detected between {conflict[0]} and {conflict[1]}. They are adjacent but have the same color.")
            
    st.divider()
    st.markdown("### 🤖 Greedy Coloring Algorithm")
    if st.button("Run Greedy Algorithm", key="btn_run_greedy"):
        c_map = greedy_coloring(nodes, edges)
        st.write("Algorithm assigned:")
        st.json({k: f"Color {v}" for k,v in c_map.items()})
        st.metric("Total Colors Used", len(set(c_map.values())))
        
    st.markdown("<div class='highlight-box'>CS Bridge: Graph coloring is used in Compilers for Register Allocation, where variables (vertices) used at the same time (edges) cannot share the same CPU register (color).</div>", unsafe_allow_html=True)

    st.markdown("### 🧪 Quick Check")
    q4 = st.radio("What is the Chromatic Number of a graph?", ["The minimum number of colors needed", "The number of edges", "The maximum degree"], key="qc_col")
    if st.button("Check", key="check_qc_col"):
        if q4 == "The minimum number of colors needed": st.success("Correct!")
        else: st.error("Incorrect. It's the minimum colors for a valid coloring.")

# ==========================================
# 4. Main entry point
# ==========================================
def main():
    theme.chapter_header("GRAPHS", "Chapter 7: Graph Theory", "Degrees, connectivity, traversal, shortest paths and coloring.")
    tabs = st.tabs(["Overview", "1. Graph Basics", "2. Types & Properties", "3. Paths & Traversal", "4. Graph Coloring"])
    with tabs[0]: render_overview()
    with tabs[1]: render_basics()
    with tabs[2]: render_properties()
    with tabs[3]: render_traversal()
    with tabs[4]: render_coloring()

if __name__ == "__main__":
    main()
