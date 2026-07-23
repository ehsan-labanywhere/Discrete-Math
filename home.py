import streamlit as st
import theme

theme.setup_page("Discrete Math Bridge", "📚")


# --------------------------------------------------------------------------- #
#  Course metadata — drives the roadmap grid
# --------------------------------------------------------------------------- #
CHAPTERS = [
    ("01", "🔣", "Logic & Proofs",
     "Truth tables, De Morgan's laws, quantifiers and the four proof methods.",
     "Logic gates · boolean expressions · data validation", theme.INDIGO),
    ("02", "🧮", "Sets & Set Operations",
     "Membership, unions, power sets and Venn diagrams over finite domains.",
     "Python sets · SQL JOINs · test generation", theme.TEAL),
    ("03", "🔁", "Induction & Recursion",
     "Weak & strong induction, recursive definitions and solving recurrences.",
     "Loop invariants · recursion trees · call stacks", theme.INDIGO),
    ("04", "🎯", "Functions",
     "Domain/codomain, injective/surjective/bijective, composition and inverses.",
     "Hash functions · APIs · middleware pipelines", theme.TEAL),
    ("05", "🎲", "Counting & Combinatorics",
     "Sum/product rules, permutations, pigeonhole and inclusion–exclusion.",
     "Password strength · birthday paradox · Pascal's triangle", theme.AMBER),
    ("06", "🔗", "Relations",
     "Digraphs, matrices, composition, equivalence classes and orderings.",
     "SQL tables · topological sort · clustering", theme.INDIGO),
    ("07", "🕸️", "Graph Theory",
     "Degrees, connectivity, BFS/DFS, shortest paths and graph coloring.",
     "Social networks · routing · exam scheduling", theme.TEAL),
    ("08", "🌳", "Trees",
     "Rooted & binary trees, traversals, spanning trees and game trees.",
     "File systems · MST · Minimax AI", theme.AMBER),
]


def _card(num, icon, title, desc, bridge, accent):
    return (
        f'<div class="cs-course-card" style="--accent:{accent};">'
        f'<div class="num">CHAPTER {num}</div>'
        f'<h4>{icon}&nbsp; {title}</h4>'
        f'<p>{desc}</p>'
        f'<p style="margin-top:10px;font-family:\'JetBrains Mono\',monospace;'
        f'font-size:.76rem;color:{accent};">↳ {bridge}</p>'
        f'</div>'
    )


def overview():
    theme.hero(
        "Discrete Math Learning System",
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

    st.markdown(
        '<div class="cs-hint">👈 Pick a chapter from the sidebar to start '
        'experimenting, or browse the roadmap below.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Course Roadmap")
    for row in range(0, len(CHAPTERS), 2):
        cols = st.columns(2, gap="medium")
        for col, ch in zip(cols, CHAPTERS[row:row + 2]):
            with col:
                st.markdown(_card(*ch), unsafe_allow_html=True)
        st.write("")

    st.divider()
    st.markdown(
        '<p style="text-align:center;color:#64748B;font-size:.85rem;">'
        'Built with the <b>Cognitive Scaffolding System</b> — clarity, tactile '
        'logic, and Socratic guidance to manage cognitive load.</p>',
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
