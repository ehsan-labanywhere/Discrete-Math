import streamlit as st
import theme

theme.setup_page("Discrete Math Bridge", "📚")


# --------------------------------------------------------------------------- #
#  Course metadata — drives the roadmap grid
# --------------------------------------------------------------------------- #
CHAPTERS = [
    ("01", "🔣", "Logic & Proofs",
     "Truth tables, De Morgan's laws, quantifiers and the four proof methods.",
     "Logic gates · boolean expressions · data validation", theme.INDIGO,
     "chapter_1_logic.py"),
    ("02", "🧮", "Sets & Set Operations",
     "Membership, unions, power sets and Venn diagrams over finite domains.",
     "Python sets · SQL JOINs · test generation", theme.TEAL,
     "chapter_2_sets.py"),
    ("03", "🔁", "Induction & Recursion",
     "Weak & strong induction, recursive definitions and solving recurrences.",
     "Loop invariants · recursion trees · call stacks", theme.INDIGO,
     "chapter_3_induction.py"),
    ("04", "🎯", "Functions",
     "Domain/codomain, injective/surjective/bijective, composition and inverses.",
     "Hash functions · APIs · middleware pipelines", theme.TEAL,
     "chapter_4_functions.py"),
    ("05", "🎲", "Counting & Combinatorics",
     "Sum/product rules, permutations, pigeonhole and inclusion–exclusion.",
     "Password strength · birthday paradox · Pascal's triangle", theme.AMBER,
     "chapter_5_counting.py"),
    ("06", "🔗", "Relations",
     "Digraphs, matrices, composition, equivalence classes and orderings.",
     "SQL tables · topological sort · clustering", theme.INDIGO,
     "chapter_6_relations.py"),
    ("07", "🕸️", "Graph Theory",
     "Degrees, connectivity, BFS/DFS, shortest paths and graph coloring.",
     "Social networks · routing · exam scheduling", theme.TEAL,
     "chapter_7_graphs.py"),
    ("08", "🌳", "Trees",
     "Rooted & binary trees, traversals, spanning trees and game trees.",
     "File systems · MST · Minimax AI", theme.AMBER,
     "chapter_8_trees.py"),
]



def overview():
    theme.hero(
        'Discrete Math Learning System <span class="cs-version-badge">v2.0</span>',
        "An interactive bridge between mathematical structures and the computer "
        "science they power — every concept shown in LaTeX and in code, with "
        "live playgrounds and Socratic checks.",
        kicker="University of Michigan–Flint",
    )

    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Chapters", "8")
    c2.metric("Interactive modules", "32+")
    c3.metric("Math ↔ CS bridges", "24+")

    # Feature highlights
    st.write("")
    f1, f2, f3, f4 = st.columns(4)
    features = [
        (f1, "📐", "LaTeX Notation", "Side-by-side math and code"),
        (f2, "🧪", "What-If Labs", "Interactive playgrounds"),
        (f3, "🧑\u200d🏫", "Socratic Checks", "Guided self-assessment"),
        (f4, "📊", "Visualizations", "Graphviz diagrams & charts"),
    ]
    for col, emoji, feat_title, feat_desc in features:
        with col:
            st.markdown(
                f'<div style="text-align:center;padding:12px 8px;">'
                f'<div style="font-size:1.8rem;margin-bottom:4px;">{emoji}</div>'
                f'<div style="font-weight:600;font-size:.88rem;color:#1E293B;">'
                f'{feat_title}</div>'
                f'<div style="font-size:.78rem;color:#64748B;">{feat_desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="cs-hint">👈 Pick a chapter from the sidebar to start '
        'experimenting, or browse the roadmap below.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Course Roadmap")
    for row in range(0, len(CHAPTERS), 2):
        cols = st.columns(2, gap="medium")
        for col, ch in zip(cols, CHAPTERS[row:row + 2]):
            num, icon, title, desc, bridge, accent, page_file = ch
            with col:
                if st.button(
                    f"{icon}  CHAPTER {num}  ·  {title}\n\n"
                    f"{desc}\n\n"
                    f"↳ {bridge}",
                    key=f"nav_{num}",
                    use_container_width=True,
                    type="tertiary",
                ):
                    st.switch_page(page_file)
        st.write("")

    st.divider()
    st.markdown(
        '<div style="text-align:center;padding:8px 0;">'
        '<p style="color:#64748B;font-size:.85rem;margin:0;">'
        'Built with the <b>Cognitive Scaffolding System</b> — clarity, tactile '
        'logic, and Socratic guidance to manage cognitive load.</p>'
        '<p style="margin:6px 0 0;font-size:.75rem;">'
        '<span style="background:linear-gradient(135deg,#4F46E5,#0D9488);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'font-weight:600;">v2.0 Premium Edition</span>'
        ' · University of Michigan–Flint</p></div>',
        unsafe_allow_html=True,
    )


pages = [
    st.Page(overview, title="Home", icon="🏠", default=True),
    st.Page("chapter_1_logic.py", title="Ch 1: Logic & Proofs", icon="🔣"),
    st.Page("chapter_2_sets.py", title="Ch 2: Sets & Set Operations", icon="🧮"),
    st.Page("chapter_3_induction.py", title="Ch 3: Induction & Recursion", icon="🔁"),
    st.Page("chapter_4_functions.py", title="Ch 4: Functions", icon="🎯"),
    st.Page("chapter_5_counting.py", title="Ch 5: Counting & Combinatorics", icon="🎲"),
    st.Page("chapter_6_relations.py", title="Ch 6: Relations", icon="🔗"),
    st.Page("chapter_7_graphs.py", title="Ch 7: Graph Theory", icon="🕸️"),
    st.Page("chapter_8_trees.py", title="Ch 8: Trees", icon="🌳"),
]

nav = st.navigation(pages)
nav.run()
