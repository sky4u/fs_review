import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Page Config ---
st.set_page_config(page_title="Financial Review", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #1e3d59; }

    /* Hide empty index header */
    [data-testid="stDataFrame"] thead th:nth-child(1) { display: none; }

    /* Line items column */
    [data-testid="stDataFrame"] table {
        table-layout: auto !important;
        width: 100%;
    }
    [data-testid="stDataFrame"] tbody th {
        min-width: 0 !important;
        max-width: none !important;
        width: 1% !important;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        text-align: left !important;
        font-weight: normal;
    }

    /* Numeric columns */
    [data-testid="stDataFrame"] td {
        text-align: right !important;
        white-space: nowrap !important;
    }

    /* === VERTICAL DIVIDER LINE BETWEEN COLUMNS === */
    /* This targets the right edge of the left column */
    div[data-testid="column"]:nth-child(1) {
        border-right: 2px solid #ddd;  /* Light gray line */
        padding-right: 20px;           /* Space after the line */
    }

    /* Optional: Add some left padding to the right column for balance */
    div[data-testid="column"]:nth-child(2) {
        padding-left: 20px;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 12px;
        align-items: stretch;
    }
    .metric-card {
        text-align: center;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    .metric-label {
        margin: 0;
        font-size: 1.1em;
        font-weight: bold;
    }
    .metric-value {
        margin: 5px 0 0 0;
        font-size: 1.6em;
        font-weight: bold;
        color: #1e3d59;
    }
    .metric-delta {
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Yearly Financials: Actuals vs. Finalization")
st.markdown("---")

# --- 1. Base Data ---
suppliers = ["Supplier 1", "Supplier 2", "Supplier 3", "Supplier 4"]
opex_items = [
    "Sales and Branding Expenses", "Licenses/Subscriptions", "Management Salaries",
    "Legal and Professional Charges", "Project Subscription Cost", "Other Admin Expenses"
]

base_revenue_24 = 1_200_000.0
base_suppliers_24 = [180_000.0] * 4
base_opex_24 = [60_000.0, 35_000.0, 85_000.0, 25_000.0, 20_000.0, 15_000.0]

# --- 2. Sidebar Controls ---
st.sidebar.header("👁️ View Previous Data")
show_2023 = st.sidebar.checkbox("Show 2023", value=True)
show_2024 = st.sidebar.checkbox("Show 2024", value=True)

st.sidebar.header("🕹️ 2025 Variance Adjustments")
rev_change = st.sidebar.slider("Revenue Change (%)", -30, 50, 0, key="rev_change") / 100

with st.sidebar.expander("🛠️ Adjust Individual Suppliers", expanded=False):
    supp_changes = [st.slider(f"{s} (%)", -30, 50, 0, key=f"supp_{i}") / 100
                    for i, s in enumerate(suppliers)]

with st.sidebar.expander("🛠️ Adjust Individual OPEX Items", expanded=False):
    opex_changes = [st.slider(f"{o} (%)", -30, 50, 0, key=f"opex_{i}") / 100
                    for i, o in enumerate(opex_items)]

# --- 3. Calculation Logic ---
def generate_column(revenue, supplier_vals, opex_vals, is_2023=False):
    total_cogs = sum(supplier_vals)
    gp = revenue - total_cogs
    gp_pct = (gp / revenue * 100) if revenue != 0 else 0
    total_opex = sum(opex_vals)
    ebitda = gp - total_opex
    threshold_usd = 375_000 / 3.6725
    tax = max(ebitda - threshold_usd, 0) * 0.09 if not is_2023 else 0.0
    net_profit = ebitda - tax
    net_profit_pct = (net_profit / revenue * 100) if revenue != 0 else 0
    return ([revenue, None] + supplier_vals + [total_cogs, None, gp, gp_pct, None] +
            opex_vals + [None, ebitda, None, tax, None, net_profit, net_profit_pct])

# Row labels
indented_suppliers = ["  " + s for s in suppliers]
blank_rows = ['blank_1', 'blank_2', 'blank_3', 'blank_4', 'blank_5', 'blank_6']

labels = (["Revenue", "blank_1"] + indented_suppliers +
          ["Total COGS", "blank_2", "Gross Profit", "Gross Profit %", "blank_3"] +
          opex_items + ["blank_4", "EBITDA", "blank_5", "Corporate Tax", "blank_6",
                        "Net Profit", "Net Profit %"])

# Build data
data_map = {
    "Line Item": labels,
    "2023 Actual": generate_column(base_revenue_24 * 0.9,
                                   [v * 0.9 for v in base_suppliers_24],
                                   [v * 0.9 for v in base_opex_24], is_2023=True),
    "2024 Actual": generate_column(base_revenue_24, base_suppliers_24, base_opex_24),
    "2025 Original": generate_column(base_revenue_24, base_suppliers_24, base_opex_24)
}

final_rev = base_revenue_24 * (1 + rev_change)
final_supps = [v * (1 + c) for v, c in zip(base_suppliers_24, supp_changes)]
final_opex = [v * (1 + c) for v, c in zip(base_opex_24, opex_changes)]
data_map["2025 Finalized"] = generate_column(final_rev, final_supps, final_opex)

df = pd.DataFrame(data_map)

# --- 4. Column Selection ---
cols_to_show = ["Line Item"]
if show_2023: cols_to_show.append("2023 Actual")
if show_2024: cols_to_show.append("2024 Actual")
cols_to_show += ["2025 Original", "2025 Finalized"]

display_df = df[cols_to_show].set_index("Line Item")

# --- 5. Styling ---
def style_financial_table(styler):
    pct_rows = ["Gross Profit %", "Net Profit %"]
    supplier_rows = indented_suppliers
    key_rows = ["Gross Profit", "EBITDA", "Net Profit"]
    blank_rows = ['blank_1', 'blank_2', 'blank_3', 'blank_4', 'blank_5', 'blank_6']
    currency_rows = [row for row in styler.index if row not in pct_rows + blank_rows]

    styler.format("${:,.0f}", subset=(currency_rows, slice(None)), na_rep="")
    styler.format("{:.2f}%", subset=(pct_rows, slice(None)), na_rep="")
    styler.format("", subset=(blank_rows, slice(None)))

    def highlight_rows(row):
            if row.name in blank_rows:
                return [''] * len(row)
            elif row.name in supplier_rows:
                return ['background-color: #000000; color: #6c757d; font-style: italic'] * len(row)
            elif row.name == "Gross Profit":
                return ['background-color: #1e3d59; color: white; font-weight: bold'] * len(row)
            elif row.name == "Gross Profit %":
                return ['background-color: #e3f2fd; color: #1565c0; font-weight: bold'] * len(row)
            elif row.name in ["EBITDA", "Net Profit"]:
                return ['background-color: #214469; color: white; font-weight: bold'] * len(row)
            elif row.name == "Net Profit %":
                return ['background-color: #e3f2fd; color: #1565c0; font-weight: bold'] * len(row)
            elif row.name in key_rows:
                return ['font-weight: bold; background-color: #f8f9fa'] * len(row)
            return [''] * len(row)

    styler.apply(highlight_rows, axis=1)
    return styler

# Prepare chart data
chart_data = pd.DataFrame({
    col: display_df.loc[["Revenue", "Total COGS", "Gross Profit %", "Net Profit %"], col]
    for col in display_df.columns
}).T

chart_data["Total OPEX"] = display_df.loc["Gross Profit", :] - display_df.loc["EBITDA", :]
chart_data = chart_data[["Revenue", "Total COGS", "Total OPEX", "Gross Profit %", "Net Profit %"]]
chart_data = chart_data.rename_axis("Year/Plan").reset_index()

# Create Plotly figure
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(name="Revenue", x=chart_data["Year/Plan"], y=chart_data["Revenue"], marker_color="#003f5c"), secondary_y=False)
fig.add_trace(go.Bar(name="Total COGS", x=chart_data["Year/Plan"], y=chart_data["Total COGS"], marker_color="#bc5090"), secondary_y=False)
fig.add_trace(go.Bar(name="Total OPEX", x=chart_data["Year/Plan"], y=chart_data["Total OPEX"], marker_color="#ffa600"), secondary_y=False)

fig.add_trace(go.Scatter(name="Gross Profit %", x=chart_data["Year/Plan"], y=chart_data["Gross Profit %"],
                         mode='lines+markers', line=dict(width=4, color="#1e88e5")), secondary_y=True)
fig.add_trace(go.Scatter(name="Net Profit %", x=chart_data["Year/Plan"], y=chart_data["Net Profit %"],
                         mode='lines+markers', line=dict(width=4, color="#43a047")), secondary_y=True)

fig.update_xaxes(title_text="Year / Plan")
fig.update_yaxes(title_text="Amount (USD)", secondary_y=False)
fig.update_yaxes(title_text="Percentage (%)", secondary_y=True, range=[0, 50])

fig.update_layout(
    barmode='group',
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=40, t=60, b=40)
)

# --- Side-by-Side Layout (Equal Width Columns) ---
left_col, col2, right_col = st.columns([10.9, 0.2, 10.9])
# left_col, right_col = st.columns(2)  # Equal width: both get 50% of available space

with left_col:
    st.subheader("Comparative Financial Statement (Values in USD)")
    styled_df = style_financial_table(display_df.style)
    # use_container_width=True makes the table fill its column fully
    st.dataframe(styled_df, use_container_width=True, hide_index=False, height=900)

with col2:
    st.html(
        """
        <div class="divider-vertical-line"></div>
        <style>
        .divider-vertical-line {
            border-left: 2px solid rgba(49, 51, 63, 0.2);
            height: 1000px; /* Adjust height as needed */
            margin: auto;
        }
        </style>
        """
    )

with right_col:
    st.subheader("📈 Profitability Trend Analysis")
    
    # Center the chart and make it fill the column nicely
    st.plotly_chart(fig, use_container_width=True)
    
    # --- 2025 Finalized Key Metrics (Zero gap, colored labels) ---
    st.markdown("---")
    st.subheader("2025 Finalized Key Metrics")

    final_col = data_map["2025 Finalized"]
    org_col = data_map["2025 Original"]

    def fmt_currency(val):
        if val is None or pd.isna(val):
            return "$ 0"
        return f"$ {val:,.0f}"

    def fmt_pct(val):
        if val is None or pd.isna(val):
            return "0.00%"
        return f"{val:.2f}%"

    # Custom metric HTML template
    def custom_metric(label_text, label_color, value, delta=None):
        delta_html = f"<br><span class='metric-delta' style='color:{'#43a047' if delta and '+' in delta else '#d81b60'}'>{delta}</span>" if delta else ""
        return (
            "<div class='metric-card'>"
            f"<p class='metric-label' style='color: {label_color};'>{label_text}</p>"
            f"<p class='metric-value'>{value}</p>"
            f"{delta_html}"
            "</div>"
        )

    # Layout with equal columns
    metrics_html = "".join([
        custom_metric("Revenue", "#1565c0", fmt_currency(final_rev), f"{rev_change*100:+.1f}%"),
        custom_metric("Net Profit", "#43a047", fmt_currency(final_col[-2]), f"{((final_col[-2]/org_col[-2])-1)*100:+.1f}%"),
        custom_metric("Net Profit Margin", "#43a047", fmt_pct(final_col[-1]), f"{((final_col[-1]/org_col[-1])-1)*100:+.1f}%"),
        custom_metric("Corporate Tax", "#d81b60", fmt_currency(final_col[-4]), f"{((final_col[-4]/org_col[-4])-1)*100:+.1f}%"),
    ])
    st.markdown(f"<div class='metrics-grid'>{metrics_html}</div>", unsafe_allow_html=True)

st.info("💡 **Tip:** Use sidebar controls to dynamically update table, chart, and metrics in real-time.")
