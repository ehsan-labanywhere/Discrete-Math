import streamlit as st
import theme
import pandas as pd
import numpy as np
import graphviz
from collections import deque

# ==========================================
# 1. Page configuration and styling
# ==========================================
theme.setup_page("Ch 8: Trees", "🌳")

# ==========================================
# 2. Core algorithm utilities
# ==========================================

def parse_set_input(input_str):
    try: return [x.strip() for x in input_str.split(',') if x.strip()]
    except: return ['A', 'B', 'C']

def is_valid_tree(nodes, edges):
    if len(edges) != len(nodes) - 1:
        return False, f"A tree with n={len(nodes)} nodes must have exactly n-1={len(nodes)-1} edges. You have {len(edges)} edges."
    adj = {n: [] for n in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if not nodes:
        return True, "Empty tree."
    visited = set()
    q = deque([nodes[0]])
    visited.add(nodes[0])
    while q:
        curr = q.popleft()
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    if len(visited) == len(nodes):
        return True, "Valid tree (connected, n-1 edges, no cycles)."
    return False, "Graph is not connected (or contains cycles and disjoint parts)."

def compute_tree_properties(nodes, edges, root):
    adj = {n: [] for n in nodes}
    undirected_adj = {n: [] for n in nodes}
    for u, v in edges:
        undirected_adj[u].append(v)
        undirected_adj[v].append(u)
    if root not in nodes:
        return None
    visited = set([root])
    q = deque([root])
    depth = {root: 0}
    parent = {root: None}
    while q:
        curr = q.popleft()
        for neighbor in undirected_adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                depth[neighbor] = depth[curr] + 1
                adj[curr].append(neighbor)
                q.append(neighbor)
    height = max(depth.values()) if depth else 0
    leaves = [n for n in nodes if len(adj[n]) == 0]
    internal = [n for n in nodes if len(adj[n]) > 0]
    is_binary = all(len(adj[n]) <= 2 for n in nodes)
    return {
        'height': height, 'depth': depth, 'leaves': leaves,
        'internal': internal, 'is_binary': is_binary, 'directed_adj': adj
    }

def preorder(tree_adj, root, result=None):
    if result is None: result = []
    if root is None: return result
    result.append(root)
    children = tree_adj.get(root, [])
    if len(children) > 0: preorder(tree_adj, children[0], result)
    if len(children) > 1: preorder(tree_adj, children[1], result)
    return result

def inorder(tree_adj, root, result=None):
    if result is None: result = []
    if root is None: return result
    children = tree_adj.get(root, [])
    if len(children) > 0: inorder(tree_adj, children[0], result)
    result.append(root)
    if len(children) > 1: inorder(tree_adj, children[1], result)
    return result

def postorder(tree_adj, root, result=None):
    if result is None: result = []
    if root is None: return result
    children = tree_adj.get(root, [])
    if len(children) > 0: postorder(tree_adj, children[0], result)
    if len(children) > 1: postorder(tree_adj, children[1], result)
    result.append(root)
    return result

def levelorder(tree_adj, root):
    if root is None: return []
    result = []
    q = deque([root])
    while q:
        curr = q.popleft()
        result.append(curr)
        for child in tree_adj.get(curr, []):
            q.append(child)
    return result

def find_parent(parent, i):
    if parent[i] == i: return i
    parent[i] = find_parent(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    xroot = find_parent(parent, x)
    yroot = find_parent(parent, y)
    if rank[xroot] < rank[yroot]: parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]: parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

def kruskal_mst(nodes, weighted_edges):
    result = []
    i = 0
    e = 0
    sorted_edges = sorted(weighted_edges, key=lambda item: item[2])
    parent = {n: n for n in nodes}
    rank = {n: 0 for n in nodes}
    steps = []
    while e < len(nodes) - 1 and i < len(sorted_edges):
        u, v, w = sorted_edges[i]
        i += 1
        x = find_parent(parent, u)
        y = find_parent(parent, v)
        if x != y:
            e += 1
            result.append((u, v, w))
            union(parent, rank, x, y)
            steps.append(f"✅ Added ({u}-{v}, w={w})")
        else:
            steps.append(f"❌ Skipped ({u}-{v}, w={w}) - creates cycle")
    return result, steps

def prim_mst(nodes, weighted_edges, start):
    adj = {n: [] for n in nodes}
    for u, v, w in weighted_edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    visited = set([start])
    mst_edges = []
    steps = []
    while len(visited) < len(nodes):
        min_edge = None
        min_weight = float('inf')
        for u in visited:
            for v, w in adj[u]:
                if v not in visited and w < min_weight:
                    min_weight = w
                    min_edge = (u, v, w)
        if min_edge:
            u, v, w = min_edge
            visited.add(v)
            mst_edges.append((u, v, w))
            steps.append(f"✅ Added ({u}-{v}, w={w})")
        else:
            break
    return mst_edges, steps

def check_winner(board):
    win_states = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    for s in win_states:
        if board[s[0]] == board[s[1]] == board[s[2]] and board[s[0]] != ' ': return board[s[0]]
    if ' ' not in board: return 'Tie'
    return None

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O': return 10 - depth
    if winner == 'X': return depth - 10
    if winner == 'Tie': return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

# ==========================================
# 3. Module rendering functions
# ==========================================

def render_overview():
    st.header("Chapter 8: Trees as Hierarchical Structures")
    st.markdown("""
    ### From Textbook to Interactive Tool
    In this module, we explore **Trees**—a specialized type of graph that models hierarchies.
    
    1.  **Basics & Properties**: 
        * *Concept*: A connected graph with no cycles.
        * *Bridge*: File systems, DOM structure, organizational charts.
    2.  **Tree Traversals**: 
        * *Concept*: Pre-order, in-order, post-order, level-order.
        * *Bridge*: Expression evaluation, compiler parsing, prefix/postfix notation.
    3.  **Spanning Trees & MST**: 
        * *Concept*: Kruskal's and Prim's Algorithms.
        * *Bridge*: Network design, minimum cost cabling, clustering.
    4.  **Decision & Game Trees**: 
        * *Concept*: Modeling decisions and game states.
        * *Bridge*: AI game playing (Minimax), classification in Machine Learning.
    """)
    st.info("👈 Select a module from the tabs above to start experimenting.")

def render_basics():
    st.subheader("1. Tree Basics & Properties")
    st.markdown("Focus: **Hierarchical Structure**, **Root**, **Leaves**, and **Height**.")
    
    if "tb_nodes" not in st.session_state:
        st.session_state.tb_nodes = ["A", "B", "C", "D", "E"]
    if "tb_edges" not in st.session_state:
        st.session_state.tb_edges = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")]
    
    with st.expander("🛠️ Define Tree Nodes and Root", expanded=True):
        c1, c2 = st.columns([2, 1])
        nodes_input = c1.text_input("Nodes (comma-separated)", ", ".join(st.session_state.tb_nodes), key="tb_nodes_input")
        nodes = parse_set_input(nodes_input)
        if nodes != st.session_state.tb_nodes:
            st.session_state.tb_nodes = nodes
            st.session_state.tb_edges = []
        
        root = c2.selectbox("Select Root", nodes, key="tb_root")
        
    with st.expander("🔗 Add Edges (Parent-Child)"):
        c_from, c_to, c_btn = st.columns([2, 2, 1])
        parent_node = c_from.selectbox("Parent", nodes, key="tb_parent")
        child_node = c_to.selectbox("Child", nodes, key="tb_child")
        if c_btn.button("Add Edge", key="tb_add_edge"):
            if parent_node != child_node and (parent_node, child_node) not in st.session_state.tb_edges and (child_node, parent_node) not in st.session_state.tb_edges:
                st.session_state.tb_edges.append((parent_node, child_node))
            else:
                st.warning("Invalid edge or edge already exists.")
        
        if st.button("Reset Edges", key="tb_reset_edges"):
            st.session_state.tb_edges = []
            
    edges = st.session_state.tb_edges
    
    is_valid, msg = is_valid_tree(nodes, edges)
    
    c_graph, c_props = st.columns([1, 1])
    
    with c_graph:
        st.markdown("#### 🌳 Tree Visualization")
        try:
            g = graphviz.Digraph(format='png'); g.attr(rankdir='TB')
            for n in nodes: 
                color = '#ffcccc' if n == root else '#e3f2fd'
                g.node(str(n), style='filled', fillcolor=color)
            for u, v in edges: g.edge(str(u), str(v))
            st.graphviz_chart(g)
        except: st.error("Graphviz not installed.")
        
        if is_valid: st.success(msg)
        else: st.error(msg)
        
    with c_props:
        st.markdown("#### 📏 Properties")
        if is_valid:
            props = compute_tree_properties(nodes, edges, root)
            if props:
                m1, m2 = st.columns(2)
                m1.metric("Height", props['height'])
                m2.metric("Is Binary Tree?", "Yes" if props['is_binary'] else "No")
                st.write(f"**Leaves:** {', '.join(props['leaves'])}")
                st.write(f"**Internal Nodes:** {', '.join(props['internal'])}")
                
                with st.expander("View Node Depths"):
                    depth_df = pd.DataFrame(list(props['depth'].items()), columns=["Node", "Depth"])
                    st.dataframe(depth_df, use_container_width=True)
            else:
                st.warning("Root not found in nodes.")
        else:
            st.info("Complete the tree to see properties.")
            
        st.markdown("<div class='highlight-box'>Math <span class='math-tag'>Acyclic Connected Graph</span> = CS <span class='db-tag'>Hierarchical Data Structure (DOM, File System)</span></div>", unsafe_allow_html=True)
        
    st.divider()
    st.markdown("### 🧪 Quick Check")
    q1 = st.radio(
        "A tree with 10 nodes must have exactly how many edges?",
        ["9", "10", "11"],
        key="qc_basics_1"
    )
    if st.button("Check", key="check_qc_basics_1"):
        if q1 == "9":
            st.success("Correct. A tree with n nodes always has n-1 edges.")
        else:
            st.error("Not quite. Remember the n-1 rule for trees.")

def render_traversals():
    st.subheader("2. Tree Traversals")
    st.markdown("Focus: **Visiting nodes in specific orders** and their applications.")
    
    st.info("Using a predefined Binary Expression Tree for (3 + 4) * 5")
    
    nodes = ["*", "+", "5", "3", "4"]
    adj = {
        "*": ["+", "5"],
        "+": ["3", "4"],
        "5": [],
        "3": [],
        "4": []
    }
    root = "*"
    
    c_graph, c_trav = st.columns([1, 1])
    
    with c_graph:
        st.markdown("#### 🌳 Expression Tree")
        try:
            g = graphviz.Digraph(format='png'); g.attr(rankdir='TB')
            for n in nodes: g.node(n)
            g.edge("*", "+", label="left")
            g.edge("*", "5", label="right")
            g.edge("+", "3", label="left")
            g.edge("+", "4", label="right")
            st.graphviz_chart(g)
        except: pass
        
    with c_trav:
        st.markdown("#### 🚶 Traversal Sequences")
        pre_res = preorder(adj, root)
        in_res = inorder(adj, root)
        post_res = postorder(adj, root)
        level_res = levelorder(adj, root)
        
        st.write("**Pre-order (Root, Left, Right) [Prefix notation]**")
        st.code(" ".join(pre_res))
        st.caption("Used for copying trees.")
        
        st.write("**In-order (Left, Root, Right) [Infix notation]**")
        st.code(" ".join(in_res))
        st.caption("Standard math evaluation format.")
        
        st.write("**Post-order (Left, Right, Root) [Postfix notation]**")
        st.code(" ".join(post_res))
        st.caption("Used for deleting trees or postfix evaluation.")
        
        st.write("**Level-order (BFS) [Level-by-level]**")
        st.code(" ".join(level_res))
        st.caption("Used for breadth-first searching.")
        
    st.divider()
    
    st.markdown("### 🎯 Try-it Prompts")
    guess_trav = st.radio("What would the Post-order traversal be for a subtree with root '+' and children '3' and '4'?", 
                          ["+ 3 4", "3 4 +", "3 + 4"], key="prompt_trav")
    if st.button("Check Guess", key="chk_guess_trav"):
        if guess_trav == "3 4 +": st.success("✅ Correct! Left, Right, Root.")
        else: st.error("❌ Not quite. Post-order means the root comes last.")
        
    st.markdown("### 🧪 Quick Check")
    q2 = st.radio(
        "Which traversal gives the standard math notation (with parentheses) for an expression tree?",
        ["Pre-order", "In-order", "Post-order"],
        key="qc_trav_1"
    )
    if st.button("Check", key="check_qc_trav_1"):
        if q2 == "In-order":
            st.success("Correct. In-order traversal gives standard infix notation.")
        else:
            st.error("Not quite. In-order places the operator between the operands.")

def render_mst():
    st.subheader("3. Spanning Trees & MST")
    st.markdown("Focus: Finding the minimum cost to connect all nodes.")
    
    st.latex(r"MST = \arg\min_{T} \sum_{e \in T} w(e)")
    
    st.info("Preset Example: City Network (Nodes=Cities, Edges=Distances/Cost)")
    
    nodes = ["A", "B", "C", "D", "E"]
    weighted_edges = [
        ("A", "B", 4), ("A", "C", 2),
        ("B", "C", 1), ("B", "D", 5),
        ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2)
    ]
    
    c_graph, c_algos = st.columns([1, 1])
    
    with c_graph:
        st.markdown("#### 🌐 Original Graph")
        try:
            g = graphviz.Graph(format='png')
            for n in nodes: g.node(n)
            for u, v, w in weighted_edges: g.edge(u, v, label=str(w))
            st.graphviz_chart(g)
        except: pass
        
    with c_algos:
        tab_k, tab_p = st.tabs(["Kruskal's Algorithm", "Prim's Algorithm"])
        
        with tab_k:
            st.markdown("#### Kruskal's (Greedy by Edge)")
            k_edges, k_steps = kruskal_mst(nodes, weighted_edges)
            st.write("**Total Cost:**", sum(w for u, v, w in k_edges))
            with st.expander("View Steps"):
                for step in k_steps: st.write(step)
            try:
                gk = graphviz.Graph(format='png')
                for n in nodes: gk.node(n)
                for u, v, w in k_edges: gk.edge(u, v, label=str(w), color='green', penwidth='2')
                st.graphviz_chart(gk)
            except: pass
            
        with tab_p:
            st.markdown("#### Prim's (Greedy by Vertex)")
            start_node = st.selectbox("Start Node", nodes, key="prim_start")
            p_edges, p_steps = prim_mst(nodes, weighted_edges, start_node)
            st.write("**Total Cost:**", sum(w for u, v, w in p_edges))
            with st.expander("View Steps"):
                for step in p_steps: st.write(step)
            try:
                gp = graphviz.Graph(format='png')
                for n in nodes: gp.node(n)
                for u, v, w in p_edges: gp.edge(u, v, label=str(w), color='blue', penwidth='2')
                st.graphviz_chart(gp)
            except: pass
            
    st.divider()
    st.markdown("### 🧪 Quick Check")
    q3 = st.radio(
        "Kruskal's algorithm sorts all edges by weight and adds them sequentially, unless:",
        ["The edge weight is negative", "The edge creates a cycle", "The edge connects to a leaf"],
        key="qc_mst_1"
    )
    if st.button("Check", key="check_qc_mst_1"):
        if q3 == "The edge creates a cycle":
            st.success("Correct. We skip edges that form a cycle to ensure the result is a tree.")
        else:
            st.error("Not quite. Cycle detection is key in Kruskal's.")

def render_decision():
    st.subheader("4. Decision Trees & Game Trees")
    
    tab_dt, tab_gt = st.tabs(["Decision Tree", "Minimax Game Tree"])
    
    with tab_dt:
        st.markdown("#### Simple Decision Tree Classification")
        st.write("Deciding whether to play tennis based on weather conditions.")
        try:
            g = graphviz.Digraph(format='png'); g.attr(rankdir='TB')
            g.node("O", "Outlook?", shape="diamond", style="filled", fillcolor="#fff3cd")
            g.node("H", "Humidity?", shape="diamond", style="filled", fillcolor="#fff3cd")
            g.node("W", "Wind?", shape="diamond", style="filled", fillcolor="#fff3cd")
            g.node("Yes1", "Play", shape="box", style="filled", fillcolor="#d4edda")
            g.node("No1", "Don't Play", shape="box", style="filled", fillcolor="#f8d7da")
            g.node("Yes2", "Play", shape="box", style="filled", fillcolor="#d4edda")
            g.node("No2", "Don't Play", shape="box", style="filled", fillcolor="#f8d7da")
            g.node("Yes3", "Play", shape="box", style="filled", fillcolor="#d4edda")
            
            g.edge("O", "H", label="Sunny")
            g.edge("O", "Yes1", label="Overcast")
            g.edge("O", "W", label="Rain")
            
            g.edge("H", "No1", label="High")
            g.edge("H", "Yes2", label="Normal")
            
            g.edge("W", "Yes3", label="Weak")
            g.edge("W", "No2", label="Strong")
            
            st.graphviz_chart(g)
        except: pass
        
        st.caption("Internal nodes = questions (features), Edges = answers, Leaves = classification outcomes.")
        
    with tab_gt:
        st.markdown("#### Tic-Tac-Toe Minimax Game Tree")
        st.write("Play as **X**. The computer (**O**) uses the Minimax algorithm to evaluate the game tree and choose the best move.")
        
        if "board" not in st.session_state:
            st.session_state.board = [' '] * 9
            st.session_state.game_over = False
            
        def reset_game():
            st.session_state.board = [' '] * 9
            st.session_state.game_over = False
            
        st.button("Reset Game", on_click=reset_game, key="btn_reset_game")
        
        board = st.session_state.board
        winner = check_winner(board)
        
        if winner:
            st.session_state.game_over = True
            if winner == 'Tie': st.info("It's a Tie!")
            else: st.success(f"{winner} Wins!")
            
        cols = st.columns([1,1,1, 3])
        
        def handle_click(i):
            if board[i] == ' ' and not st.session_state.game_over:
                board[i] = 'X'
                if not check_winner(board):
                    # Computer move
                    move = best_move(board)
                    if move != -1:
                        board[move] = 'O'
                        
        with cols[0]:
            for i in range(0, 3): st.button(board[i] if board[i] != ' ' else ' ', key=f"btn_{i}", on_click=handle_click, args=(i,), disabled=st.session_state.game_over or board[i] != ' ')
        with cols[1]:
            for i in range(3, 6): st.button(board[i] if board[i] != ' ' else ' ', key=f"btn_{i}", on_click=handle_click, args=(i,), disabled=st.session_state.game_over or board[i] != ' ')
        with cols[2]:
            for i in range(6, 9): st.button(board[i] if board[i] != ' ' else ' ', key=f"btn_{i}", on_click=handle_click, args=(i,), disabled=st.session_state.game_over or board[i] != ' ')
            
        with cols[3]:
            st.markdown("#### Minimax Logic (CS Bridge)")
            st.write("Minimax explores the entire game tree from the current state to the terminal leaves.")
            st.write("- **Maximizer (O):** Tries to maximize score (+10).")
            st.write("- **Minimizer (X):** Tries to minimize score (-10).")
            st.info("The computer evaluates all possible future states to ensure it never loses.")
            
    st.divider()
    st.markdown("### 🧪 Quick Check")
    q4 = st.radio(
        "In a decision tree, what do the leaf nodes represent?",
        ["Attributes to test", "Final decisions or classifications", "Branching conditions"],
        key="qc_dec_1"
    )
    if st.button("Check", key="check_qc_dec_1"):
        if q4 == "Final decisions or classifications":
            st.success("Correct. Leaves represent the final outcomes.")
        else:
            st.error("Not quite. Internal nodes are tests, leaves are outcomes.")

# ==========================================
# 4. Main entry point
# ==========================================
def main():
    theme.chapter_header("TREES", "Chapter 8: Trees", "Rooted & binary trees, traversals, spanning trees and game trees.")
    tabs = st.tabs(["Overview", "1. Basics & Properties", "2. Tree Traversals", "3. Spanning Trees & MST", "4. Decision & Game Trees"])
    with tabs[0]: render_overview()
    with tabs[1]: render_basics()
    with tabs[2]: render_traversals()
    with tabs[3]: render_mst()
    with tabs[4]: render_decision()

if __name__ == "__main__":
    main()
