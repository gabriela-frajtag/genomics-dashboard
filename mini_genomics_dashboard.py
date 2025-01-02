import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Basic Streamlit configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Advanced Genomics Dashboard",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. Title and introduction
# -----------------------------------------------------------------------------
st.title("Advanced Genomics Dashboard")
st.markdown("""
An **enhanced** example of a genomics dashboard using **Streamlit**, featuring:
- Interactive **filters** (date range, region, variant),
- **Multiple** chart types (bar chart, scatter timeline, box plot),
- **Side panel** controls,
- A structure ready for **real data** integrations.

Currently, the data is **fictitious**, but you can easily swap in a real CSV file or any other data source.
""")

# -----------------------------------------------------------------------------
# 3. Create / Load data
# -----------------------------------------------------------------------------
# Example fictitious data (you can replace this with a CSV upload or something else)
@st.cache_data
def load_data():
    data = {
        'Sample_ID': ['BR001','BR002','BR003','MX001','MX002','US001','US002','US003'],
        'Date': [
            '2021-01-15','2021-02-10','2021-03-05','2021-02-20',
            '2021-03-12','2021-01-25','2021-02-15','2021-03-02'
        ],
        'Region': ['Brazil','Brazil','Brazil','Mexico','Mexico','USA','USA','USA'],
        'Variant': ['Gamma','Gamma','Delta','Delta','Omicron','Delta','Omicron','Gamma'],
        'Genome_Length': [29903, 29903, 29850, 29900, 29870, 29910, 29865, 29903]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 4. Sidebar filters
# -----------------------------------------------------------------------------
st.sidebar.header("Filters")

# 4.1 Date filter
min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 4.2 Region filter
all_regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=all_regions,
    default=all_regions  # all selected by default
)

# 4.3 Variant filter
all_variants = sorted(df['Variant'].unique())
selected_variants = st.sidebar.multiselect(
    "Select Variants",
    options=all_variants,
    default=all_variants  # all selected by default
)

# Apply filters to the DataFrame
start_date, end_date = date_range
df_filtered = df[
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date)) &
    (df['Region'].isin(selected_regions)) &
    (df['Variant'].isin(selected_variants))
]

st.markdown(f"**Current number of filtered samples**: {len(df_filtered)}")

# -----------------------------------------------------------------------------
# 5. Display filtered data
# -----------------------------------------------------------------------------
with st.expander("Show filtered data table"):
    st.dataframe(df_filtered)

# -----------------------------------------------------------------------------
# 6. Charts and analyses
# -----------------------------------------------------------------------------

# 6.1 Frequency of Variants (Bar Chart)
st.subheader("Frequency of Variants (Filtered)")
variant_counts = df_filtered['Variant'].value_counts().reset_index()
variant_counts.columns = ['Variant', 'Count']

if len(variant_counts) == 0:
    st.warning("No data available for the selected filters.")
else:
    fig_bar = px.bar(
        variant_counts,
        x='Variant',
        y='Count',
        color='Variant',
        title='Number of Samples per Variant (Filtered)'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 6.2 Timeline Scatter
st.subheader("Timeline of Sample Collection (Filtered)")
if len(df_filtered) > 0:
    fig_scatter = px.scatter(
        df_filtered,
        x='Date',
        y='Variant',
        color='Region',
        hover_data=['Sample_ID'],
        title='Collection Dates by Variant and Region'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("No data to display in timeline.")

# 6.3 Box Plot of Genome Length
st.subheader("Genome Length Distribution (Filtered)")
if len(df_filtered) > 0:
    fig_box = px.box(
        df_filtered,
        x='Variant',
        y='Genome_Length',
        color='Variant',
        title='Genome Length per Variant'
    )
    st.plotly_chart(fig_box, use_container_width=True)
else:
    st.warning("No data to display in box plot.")

# -----------------------------------------------------------------------------
# 7. Conclusions / Next Steps
# -----------------------------------------------------------------------------
st.markdown("""
---
### Conclusions & Next Steps
1. This **enhanced dashboard** demonstrates how to:
   - Implement **filtering** (dates, regions, variants) on the sidebar,
   - Create **multiple** types of visualizations (bar charts, scatter timelines, box plots),
   - Expand your interactive genomics dashboard functionality.

2. **Use real data**: Replace the fictitious dataset with a CSV or a connection to a remote database.
3. Integrate **phylogenetic trees** or **maps** to delve deeper into genomic insights.
4. Deploy your dashboard to [Streamlit Community Cloud](https://streamlit.io/cloud) to share it online easily.

**Enjoy exploring your genomic data with these new features!**
""")
