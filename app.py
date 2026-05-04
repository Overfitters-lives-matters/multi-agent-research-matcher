import streamlit as st
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Page setup
st.set_page_config(
    page_title="AI Research Collaboration Dashboard",
    layout="wide"
)

# Load data
df = pd.read_csv("final_results.csv")

# Header
st.title("🤖 AI Research Collaboration Dashboard")
st.markdown("Interactive dashboard for AI-generated research collaboration recommendations.")

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Collaborations", len(df))
col2.metric("Accepted Collaborations", (df["decision"] == "ACCEPTED").sum())
col3.metric("Average Score", round(df["score"].mean(), 2))

# Sidebar filters
st.sidebar.header("Filters")

decision_filter = st.sidebar.selectbox(
    "Filter by Decision",
    ["ALL", "ACCEPTED", "REJECTED"]
)

top_n = st.sidebar.slider(
    "Number of Top Results",
    min_value=5,
    max_value=min(50, len(df)),
    value=10
)

# Apply filter
filtered_df = df.copy()

if decision_filter != "ALL":
    filtered_df = filtered_df[filtered_df["decision"] == decision_filter]

filtered_df = filtered_df.sort_values(by="score", ascending=False)

# Top collaborations table
st.subheader("🔝 Top Collaboration Recommendations")
st.dataframe(filtered_df.head(top_n), use_container_width=True)

# AI explanation
st.subheader("🧠 AI Explanation")

if len(filtered_df) > 0:
    top = filtered_df.iloc[0]

    st.info(f"""
    The top recommended collaboration is between **{top['r1']}** and **{top['r2']}**.

    This pair received a collaboration score of **{round(top['score'], 2)}**.

    The score is based on semantic similarity, research impact, and collaboration potential.
    """)
else:
    st.warning("No results found for this filter.")

# Score distribution chart
st.subheader("📊 Collaboration Score Distribution")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(filtered_df["score"], bins=10)
ax.set_xlabel("Collaboration Score")
ax.set_ylabel("Number of Collaborations")
ax.set_title("Distribution of Collaboration Scores")
st.pyplot(fig)

# Network graph
st.subheader("🌐 Collaboration Network")

G = nx.Graph()

for _, row in filtered_df.head(30).iterrows():
    if row["decision"] == "ACCEPTED":
        G.add_edge(row["r1"], row["r2"], weight=row["score"])

fig, ax = plt.subplots(figsize=(10, 7))

if len(G.nodes) > 0:
    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1200,
        font_size=8,
        ax=ax
    )

    ax.set_title("Accepted Collaboration Network")
    st.pyplot(fig)
else:
    st.warning("No accepted collaborations available to display in the network.")

# Full dataset
st.subheader("📄 Full Results")
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "Built using Multi-Agent Systems, Semantic AI, Collaboration Scoring, and Game Theory."
)