import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import tempfile
import warnings

warnings.filterwarnings("ignore")

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="💼 Advanced Accounting Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("💼 Advanced Accounting Analytics Dashboard")
st.write(
    "Upload your accounting data (CSV or Excel) to analyze KPIs, trends, and financial performance."
)


# --------------------------------------------------
# CACHED DATA LOADING
# --------------------------------------------------
@st.cache_data(ttl=3600)
def load_data(file, file_type):
    try:
        if file_type == "csv":
            return pd.read_csv(file, encoding="utf-8", low_memory=False)
        elif file_type == "excel":
            return pd.read_excel(file, engine="openpyxl")
        else:
            return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


@st.cache_data(ttl=3600)
def process_large_data(df, sample_frac=0.05):
    """Sample large datasets for plotting"""
    if len(df) > 100000:
        return df.sample(frac=sample_frac, random_state=42)
    return df


# --------------------------------------------------
# ENHANCED COLUMN DETECTION
# --------------------------------------------------
def detect_columns(df):
    detected = {
        "date_cols": [],
        "amount_cols": [],
        "client_cols": [],
        "status_cols": [],
        "category_cols": [],
        "revenue_cols": [],
        "expense_cols": [],
    }

    for col in df.columns:
        c = col.lower()

        # Date columns
        if any(x in c for x in ["date", "time", "period", "invoice", "transaction"]):
            detected["date_cols"].append(col)

        # Amount columns
        if any(x in c for x in ["amount", "total", "value", "price"]):
            detected["amount_cols"].append(col)

        # Revenue specific
        if any(x in c for x in ["revenue", "income", "sales"]):
            detected["revenue_cols"].append(col)

        # Expense specific
        if any(x in c for x in ["expense", "cost", "debit", "spend"]):
            detected["expense_cols"].append(col)

        # Client columns
        if any(
            x in c
            for x in ["client", "customer", "vendor", "supplier", "company", "name"]
        ):
            detected["client_cols"].append(col)

        # Status columns
        if any(x in c for x in ["status", "state", "condition", "payment"]):
            detected["status_cols"].append(col)

        # Category columns
        if any(x in c for x in ["category", "type", "account", "department"]):
            detected["category_cols"].append(col)

    return detected


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------
def clean_data(df, cols):
    df = df.copy()

    # Clean date columns
    for d in cols["date_cols"]:
        df[d] = pd.to_datetime(df[d], errors="coerce")

    # Clean amount columns
    for a in cols["amount_cols"] + cols["revenue_cols"] + cols["expense_cols"]:
        df[a] = pd.to_numeric(df[a], errors="coerce")
        # Remove extreme outliers (top and bottom 0.5%)
        if df[a].notna().sum() > 0:
            q_low, q_high = df[a].quantile(0.005), df[a].quantile(0.995)
            df[a] = df[a].clip(q_low, q_high)

    # Clean text columns
    for t in cols["client_cols"] + cols["status_cols"] + cols["category_cols"]:
        df[t] = df[t].astype(str).str.strip().str.title()

    return df


# --------------------------------------------------
# FORMATTING FUNCTIONS
# --------------------------------------------------
def format_currency(value):
    """Format currency values consistently"""
    if pd.isna(value) or value == 0:
        return "$0.00"
    elif abs(value) < 1000:
        return f"${value:,.2f}"
    elif abs(value) < 1000000:
        return f"${value / 1000:,.1f}K"
    else:
        return f"${value / 1000000:,.2f}M"


def format_percentage(value):
    """Format percentage values"""
    return f"{value:.1f}%"


def format_number(value):
    """Format large numbers"""
    if value < 1000:
        return f"{value:,}"
    elif value < 1000000:
        return f"{value / 1000:,.1f}K"
    else:
        return f"{value / 1000000:,.2f}M"


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------
uploaded_file = st.file_uploader("📤 Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    file_type = "csv" if uploaded_file.name.endswith(".csv") else "excel"

    with st.spinner("Loading and processing data..."):
        df = load_data(uploaded_file, file_type)
        if df is None:
            st.stop()

        cols = detect_columns(df)
        df = clean_data(df, cols)
        df_viz = process_large_data(df)

        # Column selection with fallbacks
        date_col = (
            cols["date_cols"][0]
            if cols["date_cols"]
            else st.selectbox("Select Date Column", df.columns)
        )
        amount_col = (
            cols["amount_cols"][0]
            if cols["amount_cols"]
            else st.selectbox("Select Amount Column", df.columns)
        )
        client_col = cols["client_cols"][0] if cols["client_cols"] else None
        status_col = cols["status_cols"][0] if cols["status_cols"] else None
        category_col = cols["category_cols"][0] if cols["category_cols"] else None

    # --------------------------------------------------
    # SIDEBAR FILTERS
    # --------------------------------------------------
    st.sidebar.header("🔍 Filters")

    if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
        min_d, max_d = df[date_col].min(), df[date_col].max()
        start_d, end_d = st.sidebar.date_input("Date Range", [min_d, max_d])
        df = df[
            (df[date_col] >= pd.Timestamp(start_d))
            & (df[date_col] <= pd.Timestamp(end_d))
        ]
        df_viz = df_viz[
            (df_viz[date_col] >= pd.Timestamp(start_d))
            & (df_viz[date_col] <= pd.Timestamp(end_d))
        ]

    if client_col:
        clients = st.sidebar.multiselect(
            "Filter by Client",
            sorted([c for c in df[client_col].unique() if str(c) != "NaN"]),
            default=[],
        )
        if clients:
            df = df[df[client_col].isin(clients)]
            df_viz = df_viz[df_viz[client_col].isin(clients)]

    if status_col:
        statuses = st.sidebar.multiselect(
            "Filter by Status",
            sorted([s for s in df[status_col].unique() if str(s) != "NaN"]),
            default=[],
        )
        if statuses:
            df = df[df[status_col].isin(statuses)]
            df_viz = df_viz[df_viz[status_col].isin(statuses)]

    # --------------------------------------------------
    # ENHANCED KPI CALCULATIONS
    # --------------------------------------------------
    st.subheader("📊 Key Financial KPIs")

    # Calculate KPIs
    total_records = len(df)

    # Enhanced revenue/expense detection
    if amount_col:
        # Try to detect revenue vs expense based on column names first
        revenue_col = cols["revenue_cols"][0] if cols["revenue_cols"] else amount_col
        expense_col = cols["expense_cols"][0] if cols["expense_cols"] else amount_col

        # If we have separate columns, use them
        if revenue_col != expense_col:
            total_revenue = df[revenue_col].sum() if revenue_col in df.columns else 0
            total_expense = df[expense_col].sum() if expense_col in df.columns else 0
        else:
            # Single amount column - assume positive is revenue, negative is expense
            total_revenue = df[df[amount_col] > 0][amount_col].sum()
            total_expense = abs(df[df[amount_col] < 0][amount_col].sum())
    else:
        total_revenue = 0
        total_expense = 0

    profit = total_revenue - total_expense
    margin = (profit / total_revenue * 100) if total_revenue != 0 else 0
    avg_txn = df[amount_col].mean() if amount_col else 0
    num_clients = df[client_col].nunique() if client_col else 0

    # ROI calculation (assuming initial investment is total expenses)
    roi = (profit / total_expense * 100) if total_expense != 0 else 0

    # Additional KPIs
    total_positive_txns = len(df[df[amount_col] > 0]) if amount_col else 0
    total_negative_txns = len(df[df[amount_col] < 0]) if amount_col else 0
    max_transaction = df[amount_col].max() if amount_col else 0
    min_transaction = df[amount_col].min() if amount_col else 0

    # --------------------------------------------------
    # IMPROVED KPI DISPLAY
    # --------------------------------------------------

    # First row - Main financial KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🧾 Total Records",
            value=format_number(total_records),
            help="Total number of transactions",
        )

    with col2:
        st.metric(
            label="💰 Total Revenue",
            value=format_currency(total_revenue),
            delta=None,
            help="Sum of all positive transactions",
        )

    with col3:
        st.metric(
            label="💸 Total Expenses",
            value=format_currency(total_expense),
            delta=None,
            help="Sum of all expenses/negative transactions",
        )

    with col4:
        st.metric(
            label="📈 Net Profit",
            value=format_currency(profit),
            delta=f"{margin:+.1f}%",
            delta_color="normal" if profit >= 0 else "inverse",
            help="Revenue minus expenses",
        )

    # Second row - Performance KPIs
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            label="💹 Profit Margin",
            value=format_percentage(margin),
            help="(Profit / Revenue) × 100",
        )

    with col6:
        st.metric(
            label="📊 ROI", value=format_percentage(roi), help="Return on Investment"
        )

    with col7:
        st.metric(
            label="👥 Total Clients",
            value=format_number(num_clients),
            help="Number of unique clients",
        )

    with col8:
        st.metric(
            label="⚖️ Avg Transaction",
            value=format_currency(avg_txn),
            help="Average transaction value",
        )

    # Third row - Additional metrics
    if amount_col:
        col9, col10, col11, col12 = st.columns(4)

        with col9:
            st.metric(
                label="📥 Income Transactions",
                value=format_number(total_positive_txns),
                help="Number of revenue transactions",
            )

        with col10:
            st.metric(
                label="📤 Expense Transactions",
                value=format_number(total_negative_txns),
                help="Number of expense transactions",
            )

        with col11:
            st.metric(
                label="⬆️ Largest Transaction",
                value=format_currency(max_transaction),
                help="Maximum transaction value",
            )

        with col12:
            st.metric(
                label="⬇️ Smallest Transaction",
                value=format_currency(min_transaction),
                help="Minimum transaction value",
            )

    # --------------------------------------------------
    # ENHANCED VISUALIZATIONS
    # --------------------------------------------------
    st.subheader("📈 Analytics & Trends")

    # Create tabs for different visualization categories
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📅 Trends", "📊 Distributions", "👥 Clients", "📋 Categories"]
    )

    with tab1:
        if date_col and amount_col:
            # Monthly trend
            monthly = (
                df.groupby(df[date_col].dt.to_period("M"))[amount_col]
                .sum()
                .reset_index()
            )
            monthly[date_col] = monthly[date_col].dt.to_timestamp()

            fig1 = px.line(
                monthly,
                x=date_col,
                y=amount_col,
                title="📈 Monthly Financial Trend",
                labels={date_col: "Month", amount_col: "Amount ($)"},
            )
            fig1.update_traces(line=dict(width=3), marker=dict(size=8))
            st.plotly_chart(fig1, use_container_width=True)

            # Cumulative revenue
            cumulative_data = df.sort_values(date_col).assign(
                cumulative=df[amount_col].cumsum()
            )
            fig2 = px.area(
                cumulative_data,
                x=date_col,
                y="cumulative",
                title="📊 Cumulative Amount Over Time",
            )
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        if amount_col:
            # Amount distribution
            fig3 = px.histogram(
                df_viz,
                x=amount_col,
                nbins=50,
                title="📊 Transaction Amount Distribution",
                labels={amount_col: "Amount ($)"},
            )
            st.plotly_chart(fig3, use_container_width=True)

        if status_col and amount_col:
            # Status breakdown
            status_summary = df.groupby(status_col)[amount_col].sum().reset_index()
            fig4 = px.pie(
                status_summary,
                names=status_col,
                values=amount_col,
                title="🔄 Payment Status Breakdown",
                hole=0.4,
            )
            st.plotly_chart(fig4, use_container_width=True)

    with tab3:
        if client_col and amount_col:
            # Top clients
            top_clients = (
                df.groupby(client_col)[amount_col].sum().nlargest(10).reset_index()
            )
            fig5 = px.bar(
                top_clients,
                x=client_col,
                y=amount_col,
                title="🏆 Top 10 Clients by Value",
                labels={client_col: "Client", amount_col: "Total Amount ($)"},
            )
            fig5.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig5, use_container_width=True)

    with tab4:
        if category_col and amount_col:
            # Category breakdown
            category_summary = (
                df.groupby(category_col)[amount_col].sum().nlargest(15).reset_index()
            )
            fig6 = px.bar(
                category_summary,
                x=category_col,
                y=amount_col,
                title="📂 Amount by Category",
                labels={category_col: "Category", amount_col: "Total Amount ($)"},
            )
            fig6.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig6, use_container_width=True)

    # --------------------------------------------------
    # ENHANCED PDF REPORT GENERATION
    # --------------------------------------------------
    st.subheader("🧾 Generate Financial Report")

    report_type = st.radio(
        "Report Type:",
        ["Summary Report", "Client Report", "Period Report"],
        horizontal=True,
    )

    if report_type == "Client Report" and client_col:
        selected_client = st.selectbox(
            "Select Client:", sorted(df[client_col].dropna().unique())
        )
        report_data = df[df[client_col] == selected_client]
    elif report_type == "Period Report" and date_col:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", df[date_col].min())
        with col2:
            end_date = st.date_input("End Date", df[date_col].max())
        report_data = df[
            (df[date_col] >= pd.Timestamp(start_date))
            & (df[date_col] <= pd.Timestamp(end_date))
        ]
    else:
        report_data = df

    if st.button("📄 Generate PDF Report"):
        with st.spinner("Generating professional PDF report..."):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = styles["Title"]
            title_style.alignment = 1  # Center alignment
            story.append(Paragraph("FINANCIAL ANALYTICS REPORT", title_style))
            story.append(Spacer(1, 12))

            # Report details
            details = [
                f"Report Type: {report_type}",
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Total Records Analyzed: {len(report_data):,}",
                f"Date Range: {report_data[date_col].min().strftime('%Y-%m-%d') if date_col else 'N/A'} to {report_data[date_col].max().strftime('%Y-%m-%d') if date_col else 'N/A'}",
            ]

            for detail in details:
                story.append(Paragraph(detail, styles["Normal"]))

            story.append(Spacer(1, 24))

            # Financial Metrics Table
            metrics_data = [
                ["Financial Metric", "Value"],
                ["Total Records", format_number(len(report_data))],
                ["Total Revenue", format_currency(total_revenue)],
                ["Total Expenses", format_currency(total_expense)],
                ["Net Profit", format_currency(profit)],
                ["Profit Margin", format_percentage(margin)],
                ["ROI", format_percentage(roi)],
                ["Unique Clients", format_number(num_clients)],
                ["Average Transaction", format_currency(avg_txn)],
            ]

            metrics_table = Table(metrics_data, colWidths=[200, 150])
            metrics_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E86AB")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F0F3F5")),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ]
                )
            )
            story.append(metrics_table)
            story.append(Spacer(1, 24))

            # Summary
            story.append(Paragraph("Summary", styles["Heading2"]))
            summary_text = f"""
            This financial report provides a comprehensive analysis of {len(report_data):,} transactions. 
            The organization achieved a net profit of {format_currency(profit)} with a {format_percentage(margin)} profit margin. 
            Revenue totaled {format_currency(total_revenue)} against expenses of {format_currency(total_expense)}.
            """
            story.append(Paragraph(summary_text, styles["Normal"]))
            story.append(Spacer(1, 12))

            # Footer
            story.append(Paragraph("---", styles["Normal"]))
            story.append(
                Paragraph(
                    "Generated by Advanced Accounting Analytics Dashboard",
                    styles["Italic"],
                )
            )
            story.append(Paragraph("Confidential Business Report", styles["Italic"]))

            doc.build(story)
            buffer.seek(0)

            # Download button
            st.download_button(
                label="⬇️ Download Professional PDF Report",
                data=buffer,
                file_name=f"Financial_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
            )
            st.success("✅ Professional PDF report generated successfully!")

    # --------------------------------------------------
    # DATA EXPORT
    # --------------------------------------------------
    st.subheader("📥 Export Data")

    col1, col2 = st.columns(2)

    with col1:
        # Export filtered data
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📊 Download Filtered Data (CSV)",
            data=csv_data,
            file_name="filtered_financial_data.csv",
            mime="text/csv",
            help="Download the currently filtered dataset",
        )

    with col2:
        # Export summary statistics
        if amount_col:
            summary_stats = df[amount_col].describe().reset_index()
            summary_stats.columns = ["Metric", "Value"]
            summary_csv = summary_stats.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📈 Download Summary Statistics",
                data=summary_csv,
                file_name="financial_summary_stats.csv",
                mime="text/csv",
                help="Download statistical summary of the data",
            )

else:
    st.info("👆 Upload your accounting data file to begin analysis.")

    # Demo information
    with st.expander("📋 Expected Data Format"):
        st.markdown("""
        ### Recommended Column Names:
        - **Date Columns**: `date`, `invoice_date`, `transaction_date`
        - **Amount Columns**: `amount`, `total`, `value`, `price`
        - **Client Columns**: `client`, `customer`, `vendor`
        - **Status Columns**: `status`, `payment_status`
        - **Category Columns**: `category`, `type`, `account`
        
        ### Features:
        - ✅ Handles large datasets (1M+ records)
        - ✅ Smart column detection
        - ✅ Professional KPI dashboards
        - ✅ Interactive visualizations
        - ✅ PDF report generation
        - ✅ Data export options
        """)

# --------------------------------------------------
# PERFORMANCE OPTIMIZATION
# --------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Performance Tips")
st.sidebar.markdown("""
- Use CSV format for large files
- Apply filters to reduce data size
- Close other browser tabs for better performance
- Sampling is auto-applied for visualizations
""")
