import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="WayneTech | Traffic Intelligence",
    page_icon="🦇",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / "data" / "traffic_data.csv"
ROAD_FILE = BASE_DIR / "output" / "road_totals.tsv"
HOURLY_FILE = BASE_DIR / "output" / "hourly_totals.tsv"

BG = "#090B10"
PANEL = "#131720"
BORDER = "#292F3B"
GOLD = "#F5C518"
BLUE = "#38BDF8"
TEXT = "#F0F3F8"
MUTED = "#929BAD"

# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #090B10;
    --panel: #131720;
    --panel-hover: #191F2B;
    --border: #292F3B;
    --gold: #F5C518;
    --blue: #38BDF8;
    --text: #F0F3F8;
    --muted: #929BAD;
}

/* Main application */
.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(9, 11, 16, 0.96);
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #10131A;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div {
    background: transparent;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text) !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #B0B9C9 !important;
}

/* Headings and general text */
h1, h2, h3, h4 {
    color: var(--text) !important;
    letter-spacing: -0.4px;
}

p {
    color: #A5ADBD;
}

/* WayneTech hero */
.hero {
    background: linear-gradient(120deg, #171B24, #101722, #17202B);
    border: 1px solid #343A46;
    border-left: 4px solid var(--gold);
    border-radius: 14px;
    padding: 28px 30px;
    margin: 10px 0 25px;
}

.brand,
.section-label {
    color: var(--gold);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* KPI cards */
.metric {
    background: linear-gradient(145deg, #171B24, #11151D);
    border: 1px solid #2C3340;
    border-radius: 13px;
    padding: 19px;
    min-height: 130px;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

.metric:hover {
    border-color: var(--gold);
    transform: translateY(-2px);
}

.metric-label {
    color: #9AA5B8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.1px;
    text-transform: uppercase;
}

.metric-value {
    color: #F5F7FB;
    font-size: 29px;
    font-weight: 800;
    margin-top: 12px;
}

.metric-accent {
    color: var(--gold);
}

/* Dark select boxes */
div[data-baseweb="select"] > div {
    background-color: #171C26 !important;
    border-color: #343C4C !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] input {
    color: var(--text) !important;
}

div[data-baseweb="select"] span {
    color: var(--text);
}

div[data-baseweb="popover"] {
    background: #171C26 !important;
}

div[data-baseweb="menu"] {
    background: #171C26 !important;
}

div[role="option"] {
    background: #171C26 !important;
    color: var(--text) !important;
}

div[role="option"]:hover {
    background: #252D3B !important;
}

/* Text and number inputs */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background: #171C26 !important;
    color: var(--text) !important;
    border: 1px solid #343C4C !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: #F5C518 !important;
    color: #090B10 !important;
    border: 1px solid #F5C518 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #FFD84D !important;
    border-color: #FFD84D !important;
    color: #090B10 !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #A5ADBD !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold) !important;
}

div[data-baseweb="tab-highlight"] {
    background: var(--gold) !important;
}

/* Data tables */
div[data-testid="stDataFrame"] {
    background: #131720 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px;
    overflow: hidden;
}

/* Metrics and alerts */
div[data-testid="stMetric"] {
    background: #131720;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 15px;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Separators */
hr {
    border-color: #292F3B !important;
}

/* Hide Streamlit footer and menu */
footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

/* Responsive layout */
@media (max-width: 768px) {
    .hero {
        padding: 20px;
    }

    .hero h1 {
        font-size: 25px;
    }

    .metric {
        padding: 14px;
        min-height: 110px;
    }

    .metric-value {
        font-size: 23px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    traffic = pd.read_csv(DATA_FILE)

    required = {"timestamp", "road", "vehicle_count"}
    if not required.issubset(traffic.columns):
        raise ValueError("Traffic CSV is missing required columns.")

    traffic["timestamp"] = pd.to_datetime(
        traffic["timestamp"], errors="coerce"
    )
    traffic["vehicle_count"] = pd.to_numeric(
        traffic["vehicle_count"], errors="coerce"
    )
    traffic["road"] = traffic["road"].astype("string").str.strip()

    traffic = traffic.dropna(
        subset=["timestamp", "road", "vehicle_count"]
    )
    traffic = traffic[
        (traffic["road"] != "") &
        (traffic["vehicle_count"] >= 0)
    ].copy()

    traffic["hour"] = traffic["timestamp"].dt.strftime("%H:00")
    traffic["date"] = traffic["timestamp"].dt.date.astype(str)

    road_totals = pd.read_csv(
        ROAD_FILE, sep="\t", names=["road", "total_vehicles"]
    )
    hourly_totals = pd.read_csv(
        HOURLY_FILE, sep="\t", names=["hour", "total_vehicles"]
    )

    road_totals["road"] = road_totals["road"].astype(str).str.strip()
    road_totals["total_vehicles"] = pd.to_numeric(
        road_totals["total_vehicles"], errors="raise"
    )
    hourly_totals["total_vehicles"] = pd.to_numeric(
        hourly_totals["total_vehicles"], errors="raise"
    )

    # Validate the MapReduce road totals against the source data.
    calculated_roads = (
        traffic.groupby("road")["vehicle_count"]
        .sum()
        .sort_index()
    )
    reported_roads = (
        road_totals.groupby("road")["total_vehicles"]
        .sum()
        .sort_index()
    )

    if not calculated_roads.equals(reported_roads):
        raise ValueError(
            "Hadoop road totals do not match the current CSV. "
            "Rerun the road-wise MapReduce job."
        )

    return traffic, road_totals, hourly_totals


try:
    traffic, road_totals, hourly_totals = load_data()
except Exception as error:
    st.error("The dashboard could not load or validate its data.")
    st.code(str(error))
    st.info(
        "Check that the CSV and Hadoop output files exist and "
        "that the output files were generated from this dataset."
    )
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown('<div class="brand">🦇 WAYNETECH</div>', unsafe_allow_html=True)
    st.markdown("## Traffic Intelligence")
    st.caption("ANALYTICS COMMAND CENTER")

    st.divider()

    st.markdown("### Filters")

    all_roads = sorted(traffic["road"].unique().tolist())

    selected_roads = st.multiselect(
        "Road selection",
        options=all_roads,
        default=all_roads
    )

    all_dates = sorted(traffic["date"].unique().tolist())

    selected_dates = st.multiselect(
        "Observation dates",
        options=all_dates,
        default=all_dates
    )

    st.divider()

    if st.button("↻ Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("### System information")
    st.markdown("**Processing:** Hadoop Streaming")
    st.markdown("**Storage:** HDFS")
    st.markdown("**Interface:** Streamlit")

    st.divider()
    st.caption("ABA PROJECT • ACADEMIC DEMONSTRATION")

# =========================================================
# FILTER DATA
# =========================================================

filtered = traffic[
    traffic["road"].isin(selected_roads) &
    traffic["date"].isin(selected_dates)
].copy()

filtered_roads = road_totals[
    road_totals["road"].isin(selected_roads)
].copy()

# Use the selected source records for interactive hour calculations.
filtered_hours = (
    filtered.groupby("hour", as_index=False)["vehicle_count"]
    .sum()
    .rename(columns={"vehicle_count": "total_vehicles"})
    .sort_values("hour")
)

total_vehicles = int(filtered["vehicle_count"].sum())
record_count = len(filtered)
road_count = filtered["road"].nunique()

if not filtered_hours.empty:
    peak = filtered_hours.loc[
        filtered_hours["total_vehicles"].idxmax()
    ]
    peak_hour = peak["hour"]
    peak_count = int(peak["total_vehicles"])
else:
    peak_hour = "N/A"
    peak_count = 0

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="brand">WAYNETECH • INTELLIGENCE DIVISION</div>
    <h1>Traffic Intelligence Center</h1>
    <p>
        Urban mobility insights powered by Apache Hadoop,
        HDFS and MapReduce.
    </p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([3, 1])

with left:
    st.markdown("### Operational Overview")
    st.caption("Traffic indicators for the currently selected records.")

with right:
    st.markdown(
        f"<div style='text-align:right;color:{MUTED};font-size:12px'>"
        f"LOCAL SESSION<br><b style='color:{GOLD}'>● DATA LOADED</b>"
        f"</div>",
        unsafe_allow_html=True
    )

# =========================================================
# KPI CARDS
# =========================================================

def metric_card(label, value, note):
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div style="color:#F5C518;font-size:12px;margin-top:9px">
                {note}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


m1, m2, m3, m4 = st.columns(4)

with m1:
    metric_card("Total vehicles", f"{total_vehicles:,}", "Selected records")

with m2:
    metric_card("Roads analyzed", f"{road_count}", "Selected road network")

with m3:
    metric_card("Traffic records", f"{record_count:,}", "Valid observations")

with m4:
    metric_card("Peak traffic hour", peak_hour, f"{peak_count:,} vehicles")

st.write("")
st.divider()

# =========================================================
# ROAD INTELLIGENCE
# =========================================================

st.markdown('<div class="section-label">01 / ROAD INTELLIGENCE</div>',
            unsafe_allow_html=True)
st.markdown("## Road Network Analysis")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Vehicle volume by road")

    if not filtered_roads.empty:
        road_chart = px.bar(
            filtered_roads.sort_values("total_vehicles"),
            x="total_vehicles",
            y="road",
            orientation="h",
            text="total_vehicles",
            color="total_vehicles",
            color_continuous_scale=["#25415A", "#38BDF8", "#F5C518"],
            labels={
                "road": "Road",
                "total_vehicles": "Total vehicles"
            }
        )

        road_chart.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            cliponaxis=False
        )
        road_chart.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=TEXT,
            coloraxis_showscale=False,
            margin=dict(l=10, r=45, t=15, b=15),
            height=350
        )
        st.plotly_chart(road_chart, use_container_width=True)
    else:
        st.info("Select roads to view the comparison.")

with c2:
    st.markdown("#### Traffic share by road")

    if not filtered_roads.empty:
        share_chart = px.pie(
            filtered_roads,
            names="road",
            values="total_vehicles",
            hole=0.68,
            color_discrete_sequence=[GOLD, BLUE, "#8794AA"]
        )

        share_chart.update_traces(
            textposition="outside",
            textinfo="label+percent"
        )
        share_chart.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=TEXT,
            margin=dict(l=15, r=15, t=15, b=15),
            height=350,
            showlegend=False
        )
        st.plotly_chart(share_chart, use_container_width=True)
    else:
        st.info("Select roads to view the distribution.")

st.divider()

# =========================================================
# BUSIEST ROADS LEADERBOARD
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">02 / ROAD RANKINGS</div>',
    unsafe_allow_html=True
)

st.markdown("## 🏆 Busiest Roads Leaderboard")

st.caption(
    "Road rankings based on vehicle totals calculated by Hadoop MapReduce."
)

if not filtered_roads.empty:
    leaderboard = filtered_roads.copy()

    leaderboard = leaderboard.sort_values(
        "total_vehicles",
        ascending=False
    ).reset_index(drop=True)

    total_road_traffic = leaderboard["total_vehicles"].sum()

    if total_road_traffic > 0:
        leaderboard["traffic_share"] = (
            leaderboard["total_vehicles"]
            / total_road_traffic
            * 100
        )
    else:
        leaderboard["traffic_share"] = 0.0

    leaderboard["rank"] = leaderboard.index + 1

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for _, row in leaderboard.iterrows():
        rank = int(row["rank"])
        road_name = row["road"]
        vehicle_count = int(row["total_vehicles"])
        share = float(row["traffic_share"])

        rank_label = medals.get(rank, f"#{rank}")

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(100deg, #171B24, #11151D);
                border: 1px solid #292F3B;
                border-left: 4px solid {'#F5C518' if rank == 1 else '#343C4C'};
                border-radius: 12px;
                padding: 17px 20px;
                margin-bottom: 12px;
            ">
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 12px;
                ">
                    <div>
                        <span style="
                            color: #F5C518;
                            font-size: 19px;
                            font-weight: 800;
                        ">{rank_label}</span>
                        <span style="
                            color: #F0F3F8;
                            font-size: 17px;
                            font-weight: 700;
                            margin-left: 12px;
                        ">{road_name}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="
                            color: #F0F3F8;
                            font-size: 20px;
                            font-weight: 800;
                        ">{vehicle_count:,}</span>
                        <span style="
                            color: #929BAD;
                            font-size: 12px;
                            margin-left: 6px;
                        ">vehicles</span>
                    </div>
                </div>
                <div style="
                    background: #292F3B;
                    border-radius: 20px;
                    height: 7px;
                    margin-top: 15px;
                    overflow: hidden;
                ">
                    <div style="
                        background: {'#F5C518' if rank == 1 else '#38BDF8'};
                        width: {share:.2f}%;
                        height: 7px;
                        border-radius: 20px;
                    "></div>
                </div>
                <div style="
                    color: #929BAD;
                    font-size: 12px;
                    margin-top: 8px;
                ">{share:.1f}% of the selected roads' total traffic</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Note: Rankings use the Hadoop-generated road totals. "
        "Date filters affect source-record charts but do not "
        "recalculate the existing Hadoop output."
    )

else:
    st.info("Select at least one road to display the leaderboard.")

# =========================================================
# PEAK-HOUR ANALYSIS
# =========================================================

st.markdown('<div class="section-label">02 / TEMPORAL ANALYSIS</div>',
            unsafe_allow_html=True)
st.markdown("## Peak-Hour Intelligence")

if not filtered_hours.empty:
    hour_chart = px.area(
        filtered_hours,
        x="hour",
        y="total_vehicles",
        markers=True,
        labels={
            "hour": "Hour of day",
            "total_vehicles": "Total vehicles"
        }
    )

    hour_chart.update_traces(
        line=dict(color=GOLD, width=3),
        marker=dict(color=BLUE, size=8),
        fillcolor="rgba(245,197,24,0.12)"
    )

    hour_chart.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=TEXT,
        margin=dict(l=10, r=20, t=20, b=10),
        height=370,
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#292F3B")
    )

    st.plotly_chart(hour_chart, use_container_width=True)

    st.success(
        f"Peak observed hour: {peak_hour} — "
        f"{peak_count:,} vehicles across the selected records."
    )
else:
    st.info("No hourly observations match the selected filters.")

st.divider()

# =========================================================
# DAILY TRAFFIC COMPARISON
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">03 / DAILY INTELLIGENCE</div>',
    unsafe_allow_html=True
)

st.markdown("## 📅 Daily Traffic Comparison")

st.caption(
    "Compare vehicle counts across the selected dates "
    "using the available traffic records."
)

if not filtered.empty:

    daily_totals = (
        filtered.groupby("date", as_index=False)["vehicle_count"]
        .sum()
        .rename(columns={"vehicle_count": "total_vehicles"})
        .sort_values("date")
    )

    daily_totals["total_vehicles"] = (
        daily_totals["total_vehicles"].astype(int)
    )

    busiest_day = daily_totals.loc[
        daily_totals["total_vehicles"].idxmax()
    ]

    c1, c2 = st.columns([2, 1])

    with c1:
        daily_chart = px.bar(
            daily_totals,
            x="date",
            y="total_vehicles",
            text="total_vehicles",
            color="total_vehicles",
            color_continuous_scale=["#25415A", "#38BDF8", "#F5C518"],
            labels={
                "date": "Observation date",
                "total_vehicles": "Total vehicles"
            },
            title="Daily Vehicle Volume"
        )

        daily_chart.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            cliponaxis=False
        )

        daily_chart.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#F0F3F8",
            coloraxis_showscale=False,
            margin=dict(l=10, r=25, t=55, b=15),
            height=350
        )

        st.plotly_chart(
            daily_chart,
            use_container_width=True
        )

    with c2:
        st.markdown("#### Busiest day")

        st.metric(
            label="Highest recorded total",
            value=f"{int(busiest_day['total_vehicles']):,}",
            help=f"Observation date: {busiest_day['date']}"
        )

        st.caption(
            f"Busiest observation date: {busiest_day['date']}"
        )
    st.markdown("#### Daily summary")

    st.dataframe(
        daily_totals.rename(
            columns={
                "date": "Observation Date",
                "total_vehicles": "Total Vehicles"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download daily comparison CSV",
        data=daily_totals.to_csv(index=False).encode("utf-8"),
        file_name="daily_traffic_comparison.csv",
        mime="text/csv"
    )

else:
    st.info("Select at least one road and one date to compare traffic.")

# =========================================================
# DATA EXPLORER
# =========================================================

st.markdown('<div class="section-label">03 / DATA EXPLORER</div>',
            unsafe_allow_html=True)
st.markdown("## Traffic Records & Hadoop Results")

tab1, tab2, tab3 = st.tabs([
    "Road totals",
    "Hourly analysis",
    "Source records"
])

with tab1:
    st.caption("Road-wise totals produced by the Hadoop MapReduce job.")
    st.dataframe(
        filtered_roads.sort_values("total_vehicles", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download road totals CSV",
        data=filtered_roads.to_csv(index=False).encode("utf-8"),
        file_name="road_totals.csv",
        mime="text/csv"
    )

with tab2:
    st.caption(
        "Hourly totals calculated from source records matching the filters."
    )
    st.dataframe(
        filtered_hours,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download hourly analysis CSV",
        data=filtered_hours.to_csv(index=False).encode("utf-8"),
        file_name="hourly_analysis.csv",
        mime="text/csv"
    )

with tab3:
    st.dataframe(
        filtered.sort_values("timestamp"),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download filtered traffic records",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="traffic_records.csv",
        mime="text/csv"
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    f"""
    <div style="text-align:center;padding:15px 0;color:{MUTED};font-size:12px">
        <span style="color:{GOLD};font-weight:800;letter-spacing:2px">
            WAYNETECH
        </span>
        &nbsp; | &nbsp; TRAFFIC INTELLIGENCE PLATFORM<br><br>
        ABA PROJECT • APACHE HADOOP • HDFS • MAPREDUCE<br>
        Academic demonstration using simulated traffic data.
    </div>
    """,
    unsafe_allow_html=True
)

