import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

# ---------------------- Salary Dashboard-related functions  ----------------------
def load_salary_data(file_path="modified_data.xlsx"):
    @st.cache_data
    def _load_data():
        try:
            df = pd.read_excel(file_path, sheet_name="Sheet1")
            df_plot = df.set_index('Occupation').T
            df_plot.index = pd.to_numeric(df_plot.index)
            df_plot = df_plot.sort_index()
            all_years = sorted(df_plot.index.tolist())
            all_occupations = [col for col in df_plot.columns if "Average" not in col]
            average_col = [col for col in df_plot.columns if "Average" in col][0]
            return df_plot, all_years, all_occupations, average_col
        except Exception as e:
            st.error(f"❌ Employment data loading failed: {str(e)}")
            return None, [], [], None
    return _load_data()

def create_salary_filters(all_years, all_occupations):
    st.sidebar.header("🔍 Filter Options (Median Salary Trends of Positions in Singapore(Aged 25-29))")
    
    # Check the validity of the year data
    if not all_years or len(all_years) < 2:
        st.sidebar.warning("❌ Insufficient salary data years to generate the slider.")
        return (None, None), []  
    
    selected_years = st.sidebar.slider(
        "Select Year Range (Salary)",
        min_value=min(all_years),
        max_value=max(all_years),
        value=(min(all_years), max(all_years)),
        step=1,
        key="salary_year_slider"
    )
    st.sidebar.subheader("Job Roles")
    if 'selected_occupations' not in st.session_state:
        st.session_state.selected_occupations = all_occupations
    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("✅ Select All (Salary)", key="salary_select_all"):
            st.session_state.selected_occupations = all_occupations
    with col_btn2:
        if st.button("❌ Clear All (Salary)", key="salary_clear_all"):
            st.session_state.selected_occupations = []
    selected_occupations = st.sidebar.multiselect(
        "Select Job Roles",
        options=all_occupations,
        default=st.session_state.selected_occupations,
        key="salary_occupation_multiselect"
    )
    st.session_state.selected_occupations = selected_occupations
    return selected_years, selected_occupations

def filter_salary_data(df_plot, selected_years, selected_occupations, average_col):
    if df_plot is None:
        return None
    filtered_df = df_plot.loc[selected_years[0]:selected_years[1]]
    if not selected_occupations:
        filtered_df = filtered_df[[average_col]]
    else:
        filtered_df = filtered_df[selected_occupations + [average_col]]
    return filtered_df

def filter_salary_data(df_plot, selected_years, selected_occupations, average_col):
    if df_plot is None:
        return None
    filtered_df = df_plot.loc[selected_years[0]:selected_years[1]]
    if not selected_occupations:
        filtered_df = filtered_df[[average_col]]
    else:
        filtered_df = filtered_df[selected_occupations + [average_col]]
    return filtered_df

def plot_salary_trend_chart(filtered_df, all_occupations, average_col):
    if filtered_df is None or filtered_df.empty:
        return
    
    fig = go.Figure()
    
    highlight_colors = plt.cm.tab20(np.linspace(0, 1, len(all_occupations)))
    markers = ['circle', 'square', 'triangle-up', 'diamond', 'triangle-down', 
               'triangle-left', 'triangle-right', 'pentagon', 'star', 'hexagram'] * 2
    
    for column in filtered_df.columns:
        if column == average_col:
            fig.add_trace(go.Scatter(
                x=filtered_df.index,
                y=filtered_df[column],
                name="Employment Market Baseline",
                line=dict(color='#888888', dash='dash', width=1.8),
                hovertemplate="Year: %{x}<br>Salary: %{y:.2f}<extra></extra>",
                zorder=1
            ))
        else:
            occ_index = all_occupations.index(column)
            fig.add_trace(go.Scatter(
                x=filtered_df.index,
                y=filtered_df[column],
                name=column,
                line=dict(
                    color=f'rgba({highlight_colors[occ_index][0]*255:.0f}, {highlight_colors[occ_index][1]*255:.0f}, {highlight_colors[occ_index][2]*255:.0f}, 1)',
                    width=2.5
                ),
                marker=dict(
                    symbol=markers[occ_index % len(markers)],
                    size=6,
                    line=dict(
                        color='#333333',
                        width=1.2
                    )
                ),
                hovertemplate="Year: %{x}<br>%{fullData.name} Salary: %{y:.2f}<extra></extra>",
                zorder=2
            ))
    
    fig.update_layout(

        xaxis_title="Year",
        yaxis_title="Median Monthly Salary",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=9),
            bgcolor="white",
            bordercolor="#cccccc",
            borderwidth=1
        ),
        hovermode="x unified",  
        template="plotly_white",
        margin=dict(t=80, b=100),  
        height=500
    )
    
    fig.update_xaxes(
        tickangle=45,
        tickfont=dict(size=9),
        gridcolor='#dddddd'
    )
    fig.update_yaxes(
        tickfont=dict(size=9),
        gridcolor='#dddddd'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_salary_data_preview_and_download(filtered_df, selected_years, selected_occupations, all_occupations):
    if filtered_df is None:
        return
    st.subheader("📊 Filtered Salary Data Preview")
    preview_df = filtered_df.T
    st.dataframe(
        preview_df.style.format("{:.2f}")
        .background_gradient(cmap="viridis", axis=1)
        .set_properties(**{'color': '#FFFFFF', 'font-size': '10px'}),
        height=min(500, len(preview_df)*30)
    )
    csv_data = filtered_df.to_csv(index=True, encoding='utf-8')
    if not selected_occupations:
        file_name = f"Salary_Trends_Only_Baseline_{selected_years[0]}_{selected_years[1]}.csv"
    elif len(selected_occupations) == len(all_occupations):
        file_name = f"Salary_Trends_All_Roles_{selected_years[0]}_{selected_years[1]}.csv"
    else:
        file_name = f"Salary_Trends_{selected_years[0]}_{selected_years[1]}.csv"
    st.download_button(
        label="💾 Download Salary Data (CSV)",
        data=csv_data,
        file_name=file_name,
        mime="text/csv",
        key="salary_download_btn"
    )

# ---------------------- Employment Dashboard-related function  ----------------------
def load_employment_data(file_path="modified_data.xlsx"):
    @st.cache_data
    def _load_excel_data():
        try:
            df = pd.read_excel(file_path, sheet_name="Sheet2")
            df = df.set_index(df.columns[0])
            df = df.T
            df.index = pd.to_numeric(df.index, errors='coerce')
            df = df.dropna(axis=0)
            df = df.sort_index()
            base_category = "Employed Residents Aged 25 - 29 Years"
            base_data = df[base_category] if base_category in df.columns else None
            all_years = sorted(df.index.tolist())
            all_categories = df.columns.tolist()
            return df, all_years, all_categories, base_data
        except Exception as e:
            st.error(f"❌ Employment data loading failed: {str(e)}")
            return None, [], [], None
    return _load_excel_data()

def create_employment_filters(all_years, all_categories):
    st.sidebar.header("🔍 Filter Options (Distribution of positions in Singapore(Aged 25-29))")
    

    if not all_years or len(all_years) < 2:
        st.sidebar.warning("❌ Insufficient salary data years to generate the slider.")
        return (None, None), []  
    
    selected_years = st.sidebar.slider(
        "Select Year Range (Employment)",
        min_value=int(min(all_years)),
        max_value=int(max(all_years)),
        value=(int(min(all_years)), int(max(all_years))),
        step=1,
        key="employment_year_slider"
    )
    st.sidebar.subheader("Categories")
    if 'selected_categories' not in st.session_state:
        st.session_state.selected_categories = [cat for cat in all_categories if cat != "Employed Residents Aged 25 - 29 Years"]
    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("✅ Select All (Employment)", key="employment_select_all"):
            st.session_state.selected_categories = [cat for cat in all_categories if cat != "Employed Residents Aged 25 - 29 Years"]
    with col_btn2:
        if st.button("❌ Clear All (Employment)", key="employment_clear_all"):
            st.session_state.selected_categories = []
    selected_categories = st.sidebar.multiselect(
        "Select Categories to Display",
        options=all_categories,
        default=st.session_state.selected_categories,
        key="employment_category_multiselect"
    )
    st.session_state.selected_categories = selected_categories
    return selected_years, selected_categories

def filter_employment_data(df, selected_years, selected_categories):
    if df is None:
        return None
    filtered_df = df.loc[selected_years[0]:selected_years[1]]
    if selected_categories:
        filtered_df = filtered_df[selected_categories]
    return filtered_df

def plot_stacked_chart(filtered_df, all_categories):
    if filtered_df is None:
        return
    fig = go.Figure()
    highlight_colors = [
        '#a6cee3', '#1f78b4', '#b2df8a',
        '#33a02c', '#fb9a99', '#e31a1c',
        '#fdbf6f', '#ff7f00'
    ]
    for i, category in enumerate(filtered_df.columns):
        fig.add_trace(go.Scatter(
            x=filtered_df.index,
            y=filtered_df[category],
            name=category,
            stackgroup='one',
            line=dict(width=0.5, color='white'),
            fillcolor=highlight_colors[i % len(highlight_colors)],
            hovertemplate=f'{category}<br>Year: %{{x}}<br>Value: %{{y:,.2f}}<extra></extra>'
        ))
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Number',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        height=600,
        margin=dict(b=120),
        xaxis=dict(
            tick0=filtered_df.index.min(),
            dtick=1,
            tickmode='linear'
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_proportion_pie_chart(df, selected_year, selected_categories, base_data, all_categories):
    if df is None:
        return
    year_data = df.loc[selected_year]
    if selected_categories:
        category_data = year_data[selected_categories]
    else:
        category_data = year_data[[cat for cat in all_categories if cat != "Employed Residents Aged 25 - 29 Years"]]
    total = base_data.loc[selected_year] if base_data is not None else category_data.sum()
    proportions = (category_data / total) * 100
    fig = go.Figure(data=[go.Pie(
        labels=proportions.index,
        values=proportions,
        textinfo='percent',
        hoverinfo='label+percent+value',
        insidetextorientation='radial',
        marker=dict(
            colors=[
                '#a6cee3', '#1f78b4', '#b2df8a',
                '#33a02c', '#fb9a99', '#e31a1c',
                '#fdbf6f', '#ff7f00'
            ][:len(proportions)],
            line=dict(color='white', width=1)
        )
    )])
    fig.update_layout(
        title=f'Proportion of Job Categories in Total Employment (Age 25-29) - {selected_year}',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        margin=dict(b=120)
    )
    st.plotly_chart(fig, use_container_width=True)

def show_employment_data_preview_and_download(filtered_df, selected_years, selected_categories):
    if filtered_df is None:
        return
    st.subheader("📊 Filtered Employment Data Preview")
    preview_df = filtered_df.T
    st.dataframe(
        preview_df.style.format("{:.2f}")
        .background_gradient(cmap="viridis", axis=1)
        .set_properties(**{'color': '#000000', 'font-size': '10px'}),
        height=min(500, len(preview_df)*30)
    )
    csv_data = filtered_df.to_csv(index=True, encoding='utf-8')
    if not selected_categories:
        file_name = f"Employment_All_Categories_{selected_years[0]}-{selected_years[1]}.csv"
    else:
        file_name = f"Employment_{selected_years[0]}-{selected_years[1]}.csv"
    st.download_button(
        label="💾 Download Employment Data (CSV)",
        data=csv_data,
        file_name=file_name,
        mime="text/csv",
        key="employment_download_btn"
    )

# ---------------------- The overall trend of the employment market in Singapore + The proportion of young people in various industries  ----------------------
def load_market_trend_data(file_path="modified_data.xlsx"):
    @st.cache_data
    def _load_data():
        try:
            # Read Sheet6 (original data) and Sheet7 (data on the proportion of young people)
            df_emp = pd.read_excel(file_path, sheet_name="Sheet6")
            df_youth = pd.read_excel(file_path, sheet_name="Sheet7")
            
            # Base year and range calculation
            min_year = int(df_emp["Year"].min()) if not df_emp.empty else 2007
            max_year = int(df_emp["Year"].max()) if not df_emp.empty else 2023
            BASE_YEAR = 2007
            base_val = float(df_emp.loc[df_emp["Year"] == BASE_YEAR, "Total_Employed"].iloc[0]) if (not df_emp.empty and BASE_YEAR in df_emp["Year"].values) else 1
            
            # Base year youth data year extraction
            years_y = sorted([int(y) for y in df_youth["Year"].dropna().unique()]) if not df_youth.empty else []
            
            return df_emp, df_youth, min_year, max_year, BASE_YEAR, base_val, years_y
        except Exception as e:
            st.error(f"❌ Failed to load job market trend data: {str(e)}")
            return pd.DataFrame(), pd.DataFrame(), 2007, 2023, 2007, 1, []
    return _load_data()

def create_market_trend_filters(min_year, max_year, years_y):
    """Create simplified filters (only for expanded services)"""
    st.sidebar.header("🔍 Filter Options (Overall Singapore Market Employment Trend & Youth Share by Industry)")
    
    # Employment year range
    if min_year >= max_year:
        st.sidebar.warning("Invalid employment year range.")
        selected_emp_years = (min_year, max_year)
    else:
        selected_emp_years = st.sidebar.slider(
            "Select Employment Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1,
            key="market_emp_year_slider"
        )
    
    # Display options
    show_rate = st.sidebar.checkbox("Show YoY Growth Rate (%)", value=True, key="market_show_rate")
    show_total = st.sidebar.checkbox("Show Total Employed Residents", value=True, key="market_show_total")
    show_base2007 = st.sidebar.checkbox("Show Growth vs 2007 (Base=2007)", value=False, key="market_show_base2007")
    
    # Youth share year selection (kept, but no service mode)
    st.sidebar.header("🧭 Youth Share Data (Expanded Services)")
    if not years_y:
        st.sidebar.warning("No valid youth share data available.")
        selected_youth_year = None
    else:
        selected_youth_year = st.sidebar.selectbox(
            "Select Year (for Treemap)",
            years_y,
            index=len(years_y)-1 if years_y else 0,
            key="market_youth_year_select"
        )
    
    return selected_emp_years, show_rate, show_total, show_base2007, selected_youth_year



def filter_market_trend_data(df_emp, selected_emp_years):
    if df_emp.empty:
        return pd.DataFrame()
    start_year, end_year = selected_emp_years
    mask = (df_emp["Year"] >= start_year) & (df_emp["Year"] <= end_year)
    return df_emp.loc[mask].sort_values("Year").reset_index(drop=True)


def filter_youth_share_data(df_youth, selected_year):
    """Filter youth share data (expanded services only)"""
    if df_youth.empty or selected_year is None:
        return pd.DataFrame()
    
    d = df_youth[df_youth["Year"] == selected_year].copy()
    if d.empty:
        return pd.DataFrame()
    
    # Keep only expanded service subsectors (exclude aggregate 'Services')
    is_services_agg = d["Series"].str.strip().str.lower().eq("services")
    d = d[~is_services_agg]
    
    # Keep valid rows
    return d[(d["Total"] > 0) & d["Youth"].notna()]


def plot_market_trend_chart(filtered_emp, show_rate, show_total, show_base2007, BASE_YEAR):
    """Draw a chart showing the employment trend (total employment + growth rate)"""
    if filtered_emp.empty:
        st.warning("There are currently no employment market trend data available for display.")
        return None
    
    # Create a dual-axis graph (primary and secondary axes)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # total employment figures (bar chart)
    if show_total:
        fig.add_trace(go.Bar(
            x=filtered_emp["Year"], 
            y=filtered_emp["Total_Employed"],
            name="Total Employed Residents", 
            marker_color="darkorange",
            hovertemplate="Year: %{x}<br>Total: %{y:,.2f}<extra></extra>"
        ), secondary_y=False)
    
    # Year-on-year growth rate (line graph)
    if show_rate and "YoY_Growth_Rate" in filtered_emp.columns:
        fig.add_trace(go.Scatter(
            x=filtered_emp["Year"], 
            y=filtered_emp["YoY_Growth_Rate"],
            mode="lines+markers", 
            name="YoY Growth Rate (%)",
            line=dict(color="steelblue", width=3),
            hovertemplate="Year: %{x}<br>YoY: %{y:.2f}%<extra></extra>"
        ), secondary_y=True)
        fig.add_hline(
            y=0, 
            line=dict(color="gray", dash="dash", width=1),
            secondary_y=True, 
            annotation_text="0% baseline",
            annotation_position="top right"
        )
    
    # Add the 2007 benchmark growth rate (line graph)
    if show_base2007 and "Growth_vs_2007_%" in filtered_emp.columns:
        fig.add_trace(go.Scatter(
            x=filtered_emp["Year"], 
            y=filtered_emp["Growth_vs_2007_%"],
            mode="lines+markers", 
            name=f"Growth vs {BASE_YEAR} (%)",
            line=dict(width=2, dash="dot"),
            hovertemplate=f"Year: %{{x}}<br>Growth vs {BASE_YEAR}: %{{y:.2f}}%<extra></extra>"
        ), secondary_y=True)
    
    # Chart layout
    fig.update_layout(
        title="Employment Trends (Bar = Total, Line = YoY)",
        barmode="group", 
        plot_bgcolor="white",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    return fig

def plot_youth_share_treemap(filtered_youth, selected_year):
    if filtered_youth.empty or selected_year is None:
        st.warning("There are currently no youth share data available for display.")
        return None
    

    fig_t = px.treemap(
        filtered_youth, 
        path=["Series"], 
        values="Youth_Share(%)", 
        color="Youth_Share(%)",
        color_continuous_scale="viridis"
    )
    
#Custom hover information
    fig_t.update_traces(
        customdata=np.stack([
            filtered_youth["Total"], 
            filtered_youth["Youth"], 
            filtered_youth["Youth_Share(%)"]
        ], axis=-1),
        texttemplate="%{label}<br>%{customdata[2]:.2f}%",
        hovertemplate="<b>%{label}</b><br>"
                      f"Year: {int(selected_year)}<br>"
                      "Total: %{customdata[0]:,.2f}<br>"
                      "Youth (25–29): %{customdata[1]:,.2f}<br>"
                      "Youth Share: %{customdata[2]:.2f}%<extra></extra>"
    )
    
    st.plotly_chart(fig_t, use_container_width=True)
    return fig_t

def show_market_trend_data_preview_and_download(filtered_emp, filtered_youth, show_rate, show_total, show_base2007, selected_year, market_emp_fig, market_youth_fig):
    """Preview and download of employment trends and data on the proportion of young people"""
    st.subheader("📊 Employment Trend Data Preview")
    if not filtered_emp.empty:
        with st.expander("📋 Show Employment Data Table (with Gradient)", expanded=False):
            cols = ["Year"]
            if show_total: cols.append("Total_Employed")
            if show_rate and "YoY_Growth_Rate" in filtered_emp.columns: cols.append("YoY_Growth_Rate")
            if show_base2007 and "Growth_vs_2007_%" in filtered_emp.columns: cols.append("Growth_vs_2007_%")
            
            preview_df = filtered_emp[cols].set_index("Year")
            fmt = {c: "{:,.2f}" if not c.endswith("%") else "{:.2f}%" for c in preview_df.columns}
            styler = preview_df.style.format(fmt)
            for c in preview_df.columns:
                styler = styler.background_gradient(cmap="viridis", subset=[c])
            st.dataframe(styler.set_properties(**{"color": "#FFFFFF", "font-size": "14px"}))
        
        # Download of employment trend data
        col1, col2 = st.columns(2)
        csv_emp = filtered_emp.round(2).to_csv(index=False).encode("utf-8")
        with col1:
            st.download_button(
                "💾 Download Employment Data (CSV)", 
                csv_emp, 
                file_name="employment_filtered.csv",
                key="market_emp_download"
            )
        with col2:
            try:
                from plotly.io import to_image
                if market_emp_fig is not None:
                    png_emp = to_image(market_emp_fig, format="png", width=1400, height=600, scale=2)
                    st.download_button(
                        "🖼️ Download Employment Chart (PNG)", 
                        png_emp, 
                        file_name="employment_chart.png", 
                        mime="image/png",
                        key="market_emp_chart_download"
                    )
            except ImportError:
                st.warning("Missing 'kaleido' library. Install with: pip install kaleido")
            except Exception as e:
                st.warning(f"Failed to export chart: {str(e)}")
    else:
        st.info("There are no employment trend data available for preview.")
    
    # Preview and download of the data on the proportion of young people
    st.subheader(f"🧭 Youth Share Data Preview ({selected_year})")
    if not filtered_youth.empty and selected_year is not None:
        col3, col4 = st.columns(2)
        csv_y = filtered_youth.round(2).to_csv(index=False).encode("utf-8")
        with col3:
            st.download_button(
                "💾 Download Youth Data (CSV)", 
                csv_y, 
                file_name="youth_share_filtered.csv",
                key="market_youth_download"
            )
        with col4:
            try:
                from plotly.io import to_image
                if market_youth_fig is not None:
                    png_y = to_image(market_youth_fig, format="png", width=1000, height=800, scale=2)
                    st.download_button(
                        "🖼️ Download Treemap Chart (PNG)", 
                        png_y, 
                        file_name="youth_treemap.png", 
                        mime="image/png",
                        key="market_youth_chart_download"
                    )
            except ImportError:
                st.warning("Missing 'kaleido' library. Install with: pip install kaleido")
            except Exception as e:
                st.warning(f"Failed to export chart: {str(e)}")
    else:
        st.info("There is no data available for the proportion of young people to preview.")

# ---------------------- Employment Trends for Individuals Aged 25-29 ----------------------
def load_age2529_employment_data(file_path="modified_data.xlsx"):
    @st.cache_data
    def _load_data():
        try:
            # Read Sheet 4 of Excel
            df = pd.read_excel(file_path, sheet_name="Sheet3")
            # Data preprocessing
            df.columns = ["Industry"] + [f"Year_{i}" for i in range(1, len(df.columns))]
            df_melt = df.melt(id_vars="Industry", var_name="Year", value_name="Employment").dropna()
            
            # Year conversion (starting from 2007)）
            year_s = df_melt["Year"].astype(str)
            if year_s.str.startswith("Year_").all():
                df_melt["Year"] = year_s.str.replace("Year_", "", regex=False).astype(int) + 2006
            else:
                df_melt["Year"] = year_s.astype(int)
            
            # Distinguish between the main industry and the sub-industries of the service sector
            main_groups = ["Manufacturing", "Construction", "Services", "Others"]
            exclude_items = ["Employed Residents Aged 25 - 29 Years"] + main_groups
            df_services = df_melt[~df_melt["Industry"].isin(exclude_items)].copy()
            
            # Extract key parameters
            years = sorted(df_melt["Year"].unique().tolist())
            main_industries = [g for g in main_groups if g in df_melt["Industry"].unique().tolist()]
            service_subsectors = sorted(df_services["Industry"].unique().tolist())
            
            return df_melt, df_services, years, main_industries, service_subsectors
        except Exception as e:
            st.error(f"Data loading for employment of individuals aged 25-29 has failed.: {str(e)}")
            return pd.DataFrame(), pd.DataFrame(), [], [], []
    return _load_data()

def create_age2529_filters(all_years, all_main, all_services):
    st.sidebar.header("🔍 Filter Options (Singapore Employment Trend(Aged 25-29))")
    # Year Slider (with unique key)
    if not all_years or len(all_years) < 2:
        st.sidebar.warning("The employment data for the age group of 25-29 is insufficient for the year, so the slider cannot be generated.")
        return (None, None), [], []
    
    selected_years = st.sidebar.slider(
        "Select Year Range (Age 25-29)",
        min_value=min(all_years),
        max_value=max(all_years),
        value=(min(all_years), max(all_years)),
        step=1,
        key="age2529_year_slider"
    )
    yr0, yr1 = selected_years
    
    # Main Industry Filtering (Session State + Unique Key)
    st.sidebar.subheader("🏭 Main Industries")
    if "selected_age2529_main" not in st.session_state:
        st.session_state["selected_age2529_main"] = all_main
    
    col_m1, col_m2 = st.sidebar.columns(2)
    with col_m1:
        if st.button("✅ Select All (Main-Age2529)", key="age2529_main_select_all"):
            st.session_state["selected_age2529_main"] = all_main
    with col_m2:
        if st.button("❌ Clear All (Main-Age2529)", key="age2529_main_clear_all"):
            st.session_state["selected_age2529_main"] = []
    
    selected_main = st.sidebar.multiselect(
        "Select Main Industries",
        options=all_main,
        default=st.session_state["selected_age2529_main"],
        key="age2529_main_multiselect"
    )
    st.session_state["selected_age2529_main"] = selected_main
    
    # Service industry sub-industry screening (session status + unique key)
    st.sidebar.subheader("🧩 Service Subsectors")
    if "selected_age2529_services" not in st.session_state:
        st.session_state["selected_age2529_services"] = all_services
    
    col_s1, col_s2 = st.sidebar.columns(2)
    with col_s1:
        if st.button("✅ Select All (Services-Age2529)", key="age2529_serv_select_all"):
            st.session_state["selected_age2529_services"] = all_services
    with col_s2:
        if st.button("❌ Clear All (Services-Age2529)", key="age2529_serv_clear_all"):
            st.session_state["selected_age2529_services"] = []
    
    selected_services = st.sidebar.multiselect(
        "Select Service Subsectors",
        options=all_services,
        default=st.session_state["selected_age2529_services"],
        key="age2529_serv_multiselect"
    )
    st.session_state["selected_age2529_services"] = selected_services
    
    return selected_years, selected_main, selected_services

def filter_age2529_data(df_melt, df_services, selected_years, selected_main, selected_services):
    if df_melt.empty or selected_years[0] is None:
        return pd.DataFrame(), pd.DataFrame()
    yr0, yr1 = selected_years
    # Filter the main industry data
    df_main_range = df_melt[df_melt["Year"].between(yr0, yr1) & df_melt["Industry"].isin(selected_main)]
    # Filter data of the sub-industry of the service industry
    df_serv_range = df_services[df_services["Year"].between(yr0, yr1) & df_services["Industry"].isin(selected_services)]
    return df_main_range, df_serv_range

def plot_age2529_charts(df_main_range, df_serv_range, selected_main, selected_services, selected_years):
    if df_main_range.empty and df_serv_range.empty:
        st.warning("There are no employment data available for the age group of 25-29.")
        return
    
    yr0, yr1 = selected_years
    plt.style.use('default')  
    c1, c2 = st.columns(2)
    
    # Left: Main industry trend chart
    with c1:
        st.subheader("🏭 Employment Trend — Main Industries")
        fig1, ax1 = plt.subplots(figsize=(12, 7))
        plot_main = selected_main if selected_main else []
        if not plot_main:
            ax1.text(0.5, 0.5, "No main industries selected",
                     transform=ax1.transAxes, ha='center', va='center',
                     fontsize=14, fontweight='bold', color='gray')
        else:
            for name in plot_main:
                g = df_main_range[df_main_range["Industry"] == name].sort_values("Year")
                if not g.empty:
                    ax1.plot(g["Year"], g["Employment"], marker='o', linewidth=2, label=name)
        
        ax1.set_title(f"Employment Trend (25–29 Years, {yr0}-{yr1})", fontsize=15, fontweight='bold')
        ax1.set_ylabel("Number of Employed Residents (Thousands)", fontsize=12)
        ax1.set_xlabel("Year", fontsize=12)
        ax1.grid(True, alpha=0.3)
        if plot_main:
            ax1.legend(fontsize=9, loc='best')
            ax1.set_xticks(sorted(df_main_range["Year"].unique()))
            plt.setp(ax1.get_xticklabels(), rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)
    
    # Right side: Service subsector trend chart
    with c2:
        st.subheader("🧩 Employment Trend — Service Subsectors")
        fig2, ax2 = plt.subplots(figsize=(12, 7))
        plot_services = selected_services if selected_services else []
        if not plot_services:
            ax2.text(0.5, 0.5, "No service subsectors selected",
                     transform=ax2.transAxes, ha='center', va='center',
                     fontsize=14, fontweight='bold', color='gray')
        else:
            for name in plot_services:
                g = df_serv_range[df_serv_range["Industry"] == name].sort_values("Year")
                if not g.empty:
                    ax2.plot(g["Year"], g["Employment"], marker='o', linewidth=2, label=name)
        
        ax2.set_title(f"Employment Trend of Service Subsectors (25–29 Years, {yr0}-{yr1})", fontsize=15, fontweight='bold')
        ax2.set_ylabel("Employment (Thousands)", fontsize=12)
        ax2.set_xlabel("Year", fontsize=12)
        ax2.grid(True, alpha=0.3)
        if plot_services:
            ax2.legend(fontsize=9, loc='best')
            ax2.set_xticks(sorted(df_serv_range["Year"].unique()))
            plt.setp(ax2.get_xticklabels(), rotation=45)
        plt.tight_layout()
        st.pyplot(fig2)

def show_age2529_data_preview_and_download(df_main_range, df_serv_range, selected_years, selected_main, selected_services):
    st.subheader("📊 Filtered Age 25-29 Employment Data Preview")
    yr0, yr1 = selected_years
    
    # Main industry data preview and download
    with st.expander("Main Industries — Pivot Table & Download", expanded=True):
        if selected_main and not df_main_range.empty:
            pivot_main = df_main_range.pivot_table(
                index="Industry", columns="Year", values="Employment", aggfunc="sum"
            ).sort_index()
            st.dataframe(
                pivot_main.style.format("{:.2f}")
                .background_gradient(cmap="YlGnBu", axis=1)
                .set_properties(**{'font-size': '10px'}),
                height=min(500, 35 * len(pivot_main))
            )
            # Download function (add unique key)
            csv_bytes = pivot_main.to_csv(encoding="utf-8").encode("utf-8")
            st.download_button(
                label="💾 Download CSV — Main Industries",
                data=csv_bytes,
                file_name=f"Age2529_Employment_MainIndustries_{yr0}_{yr1}.csv",
                mime="text/csv",
                key="age2529_main_download"
            )
        else:
            st.info("No data to display for Main Industries. Please select at least one.")
    
    # Service sub-sector data preview and download
    with st.expander("Service Subsectors — Pivot Table & Download", expanded=True):
        if selected_services and not df_serv_range.empty:
            pivot_serv = df_serv_range.pivot_table(
                index="Industry", columns="Year", values="Employment", aggfunc="sum"
            ).sort_index()
            st.dataframe(
                pivot_serv.style.format("{:.2f}")
                .background_gradient(cmap="YlGnBu", axis=1)
                .set_properties(**{'font-size': '10px'}),
                height=min(500, 35 * len(pivot_serv))
            )
            # Download function (add unique key)
            csv_bytes2 = pivot_serv.to_csv(encoding="utf-8").encode("utf-8")
            st.download_button(
                label="💾 Download CSV — Service Subsectors",
                data=csv_bytes2,
                file_name=f"Age2529_Employment_ServiceSubsectors_{yr0}_{yr1}.csv",
                mime="text/csv",
                key="age2529_serv_download"
            )
        else:
            st.info("No data to display for Service Subsectors. Please select at least one.")

# ---------------------- The correlation function of the dashboard for the number of people with degrees  ----------------------
def load_education_pop_data(file_path="modified_data.xlsx"):
    """Load Sheet5's educational headcount data (replace the original CSV read)）"""
    @st.cache_data
    def _load_data():
        try:
            # Read Sheet5 in Excel
            df = pd.read_excel(file_path, sheet_name="Sheet5", index_col=0)
            # Extract the valid year column in numeric format）
            year_columns = [col for col in df.columns if str(col).isdigit()]
            return df, year_columns
        except Exception as e:
            st.error(f"The data of the number of educated people failed to load: {str(e)}")
            return pd.DataFrame(), []
    return _load_data()

def create_education_pop_filters(year_columns):
    """Create a filter for the number of degrees module (year slider)）"""
    st.sidebar.header("🔍 Filter Options (Singapore Residents Education Level Distribution(Aged 25-29))")
    if not year_columns:
        st.sidebar.warning("There are no valid years for the educational data to generate a filter")
        return (None, None)
    
    # Convert the year to an integer and get the range
    years_int = [int(col) for col in year_columns]
    min_year = min(years_int)
    max_year = max(years_int)
    
    # Year slider (add unique key)
    selected_years = st.sidebar.slider(
        "Select Year Range (Education)",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        key="education_year_slider"
    )
    st.sidebar.write(f"Selected years: {selected_years[0]} - {selected_years[1]}")
    return selected_years

def preprocess_education_pop_data(df):
    """Pre-process educational data (extract classification, rename index)"""
    if df.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    # Extract data of different educational levels
    HQA_total = df.iloc[0:2] if len(df) >= 2 else pd.DataFrame()
    HQA_Below_Secondary = df.iloc[10:12] if len(df) >= 12 else pd.DataFrame()
    HQA_Secondary = df.iloc[20:22] if len(df) >= 22 else pd.DataFrame()
    HQA_Post_Secondary = df.iloc[30:32] if len(df) >= 32 else pd.DataFrame()
    HQA_Diploma_PQ = df.iloc[40:42] if len(df) >= 42 else pd.DataFrame()
    HQA_University = df.iloc[50:52] if len(df) >= 52 else pd.DataFrame()

    # Rename the index
    if not HQA_total.empty:
        HQA_total.index = ['Total', '25-29_Years_Total']
    if not HQA_Below_Secondary.empty:
        HQA_Below_Secondary.index = ['Total_Below_Secondary', '25-29_Below_Secondary'] 
    if not HQA_Secondary.empty:
        HQA_Secondary.index = ['Total_Secondary', '25-29_Secondary']
    if not HQA_Post_Secondary.empty:
        HQA_Post_Secondary.index = ['Total_Post_Secondary', '25-29_Post_Secondary']
    if not HQA_Diploma_PQ.empty:
        HQA_Diploma_PQ.index = ['Total_Diploma_Professional', '25-29_Diploma_PQ']
    if not HQA_University.empty:
        HQA_University.index = ['Total_University', '25-29_University']

    # The relevant data of 25-29 years old are merged
    HQA_combined = pd.concat([
        HQA_total.iloc[1:2] if not HQA_total.empty else pd.DataFrame(),
        HQA_Below_Secondary.iloc[1:2] if not HQA_Below_Secondary.empty else pd.DataFrame(),
        HQA_Secondary.iloc[1:2] if not HQA_Secondary.empty else pd.DataFrame(),
        HQA_Post_Secondary.iloc[1:2] if not HQA_Post_Secondary.empty else pd.DataFrame(),
        HQA_Diploma_PQ.iloc[1:2] if not HQA_Diploma_PQ.empty else pd.DataFrame(),
        HQA_University.iloc[1:2] if not HQA_University.empty else pd.DataFrame()
    ])

    # Year column in reverse order (old → new)
    if not HQA_combined.empty:
        HQA_combined = HQA_combined.iloc[:, ::-1]

    # Extraction of educational trend data for 25-29 years old (excluding the summary line)
    HQA_25_29_comb = HQA_combined.iloc[1:] if len(HQA_combined) > 1 else pd.DataFrame()
    if not HQA_25_29_comb.empty:
        HQA_25_29_comb.index = ['Below_Secondary', 'Secondary', 'Post_Secondary', 'Diploma_&_Professional_Qualification', 'University']

    # Calculate the proportion of each degree (relative to the total number of 25-29 years old)
    HQA_proportion = pd.DataFrame()
    if len(HQA_combined) > 1:
        HQA_proportion = HQA_combined.iloc[1:] / HQA_combined.iloc[0]
        HQA_proportion.index = HQA_25_29_comb.index if not HQA_25_29_comb.empty else HQA_proportion.index

    return HQA_25_29_comb, HQA_proportion

def filter_education_pop_data(HQA_25_29_comb, HQA_proportion, selected_years):
    """Filtering educational data by selected year"""
    if HQA_25_29_comb.empty or selected_years[0] is None:
        return pd.DataFrame(), pd.DataFrame()
    
    start_year, end_year = selected_years
    year_columns = [col for col in HQA_25_29_comb.columns if start_year <= int(col) <= end_year]
    filtered_2529 = HQA_25_29_comb[year_columns] if year_columns else pd.DataFrame()
    filtered_proportion = HQA_proportion[year_columns] if year_columns and not HQA_proportion.empty else pd.DataFrame()
    
    return filtered_2529, filtered_proportion

def plot_education_pop_chart(filtered_2529, filtered_proportion):
    """Draw the double chart of the trend + proportion of the number of educated people"""
    if filtered_2529.empty:
        st.warning("The data of the number of people without academic qualifications can be displayed")
        return
    
    # Create a twin graph
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f"Educational Trends for 25-29 Year Olds ({filtered_2529.columns[0]}-{filtered_2529.columns[-1]})", 
            f"Educational Proportion Trends for 25-29 Year Olds ({filtered_2529.columns[0]}-{filtered_2529.columns[-1]})"
        ),
        horizontal_spacing=0.05
    )

    # define color
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    # Add trend line (left panel: headcount, right panel: share)
    for i, education_level in enumerate(filtered_2529.index):
        # Left panel: Number of 25-29 year olds with various degrees
        fig.add_trace(
            go.Scatter(
                x=filtered_2529.columns,
                y=filtered_2529.loc[education_level],
                mode='lines+markers',
                name=education_level,
                line=dict(color=colors[i % len(colors)]),
                marker=dict(color=colors[i % len(colors)]),
                showlegend=True
            ),
            row=1, col=1
        )
        # Right panel: Proportion of 25-29 year olds with different degrees
        if not filtered_proportion.empty:
            fig.add_trace(
                go.Scatter(
                    x=filtered_proportion.columns,
                    y=filtered_proportion.loc[education_level],
                    mode='lines+markers',
                    name=education_level,
                    line=dict(color=colors[i % len(colors)]),
                    marker=dict(color=colors[i % len(colors)]),
                    showlegend=False
                ),
                row=1, col=2
            )

    # Chart layout adjustment
    fig.update_layout(
        height=500,
        template="plotly_white",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.2
        )
    )
    # The axis label
    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="Year", row=1, col=2)
    fig.update_yaxes(title_text="Number of People", row=1, col=1)
    fig.update_yaxes(title_text="Proportion", row=1, col=2)

    st.plotly_chart(fig, use_container_width=True)

def show_education_pop_data_preview_and_download(filtered_2529, filtered_proportion, selected_years):
    """Academic data preview and download"""
    st.subheader("📊 Filtered Education Population Data Preview")
    if filtered_2529.empty:
        st.info("There is no filtered educational data to show")
        return
    
    start_year, end_year = selected_years
    # Headcount data preview
    with st.expander("Educational Attainment Data for the 25-29 Age Group", expanded=True):
        st.dataframe(
            filtered_2529.style.format("{:.2f}")
            .background_gradient(cmap="Blues", axis=1)
            .set_properties(**{'font-size': '10px'}),
            height=min(400, 35 * len(filtered_2529))
        )
        # Download number of people (unique key)
        csv_2529 = filtered_2529.to_csv(encoding="utf-8").encode("utf-8")
        st.download_button(
            label="💾 Download 25-29 Education Population CSV",
            data=csv_2529,
            file_name=f"Education_2529_Population_{start_year}_{end_year}.csv",
            mime="text/csv",
            key="education_pop_download"
        )
    
    # Preview of percentage data (if any)
    if not filtered_proportion.empty:
        with st.expander("Educational Attainment Proportion Data for the 25-29 Age Group", expanded=True):
            st.dataframe(
                filtered_proportion.style.format("{:.4f}")  # The proportion is reserved for 4 decimal places
                .background_gradient(cmap="Greens", axis=1)
                .set_properties(**{'font-size': '10px'}),
                height=min(400, 35 * len(filtered_proportion))
            )
            # Download percentage data (unique key)
            csv_proportion = filtered_proportion.to_csv(encoding="utf-8").encode("utf-8")
            st.download_button(
                label="💾 Download 25-29 Education Proportion CSV",
                data=csv_proportion,
                file_name=f"Education_2529_Proportion_{start_year}_{end_year}.csv",
                mime="text/csv",
                key="education_proportion_download"
            )

# ---------------------- The education unemployment rate dashboard correlation function  ----------------------
def load_unemployment_data(file_path="modified_data.xlsx"):
    @st.cache_data
    def _load_data():
        try:
            df = pd.read_excel(file_path, sheet_name="Sheet4")
            # Ensure that the year column format is uniform (convert to string for easy filtering)
            year_cols = [col for col in df.columns if str(col).isdigit()]
            df[year_cols] = df[year_cols].astype(float)
            return df, year_cols
        except Exception as e:
            st.error(f"The unemployment data failed to load: {str(e)}")
            return None, []
    return _load_data()

def create_unemployment_filters(df, year_cols):
    st.sidebar.header("🔍 Filter Options (Singapore Unemployment Rate Analysis by Education Level(Aged 25-29))")
    if df is None or not year_cols:
        st.sidebar.warning("Unemployment data is abnormal and a filter cannot be generated")
        return [], ("", ""), "Line Chart"
    
# Education level screening
    education_levels = df['Data Series'].tolist()
    selected_educations = st.sidebar.multiselect(
        "Select Education Levels",
        options=education_levels,
        default=education_levels,
        key="unemployment_education_multiselect"
    )
    
    # Year range filter
    if len(year_cols) < 2:
        st.sidebar.warning("There are not enough years of unemployment data to generate a slider")
        selected_years = (year_cols[0] if year_cols else "", year_cols[0] if year_cols else "")
    else:
        selected_years = st.sidebar.select_slider(
            "Select Year Range (Unemployment)",
            options=year_cols,
            value=(year_cols[0], year_cols[-1]),
            key="unemployment_year_slider"
        )
    
    # Chart type selection
    chart_type = st.sidebar.radio(
        "Select Chart Type (Unemployment)",
        ["Line Chart", "Bar Chart"],
        key="unemployment_chart_type"
    )
    
    return selected_educations, selected_years, chart_type

def preprocess_unemployment_data(df, selected_educations, selected_years):
    if df is None or not selected_educations:
        return pd.DataFrame(), pd.DataFrame()
    
    # Data perspective
    df_melted = df.melt(id_vars=['Data Series'], 
                        var_name='Year', 
                        value_name='Unemployment Rate')
    
    # Filter data
    filtered_df = df_melted[
        (df_melted['Data Series'].isin(selected_educations)) & 
        (df_melted['Year'] >= selected_years[0]) & 
        (df_melted['Year'] <= selected_years[1])
    ]
    
    # Export data in wide format
    export_df = df[df['Data Series'].isin(selected_educations)]
    year_cols = [col for col in df.columns if col == 'Data Series' or (selected_years[0] <= col <= selected_years[1])]
    export_df = export_df[year_cols]
    
    return filtered_df, export_df

def plot_unemployment_chart(filtered_df, selected_years, chart_type):
    if filtered_df.empty:
        st.warning("There are no eligible unemployment data to show")
        return
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    if chart_type == "Line Chart":
        fig = px.line(
            filtered_df, 
            x='Year', 
            y='Unemployment Rate', 
            color='Data Series',
            title=f'Unemployment Rate Trends ({selected_years[0]}-{selected_years[1]})',
            color_discrete_sequence=colors
        )
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Unemployment Rate (%)',
            legend_title='Education Level',
            hovermode='x unified',
            height=700,
            xaxis=dict(
                tickmode='array',
                tickvals=filtered_df['Year'].unique(),
                tickangle=45
            )
        )
        fig.update_traces(mode='lines+markers')
    else:
        fig = px.bar(
            filtered_df,
            x='Year',
            y='Unemployment Rate',
            color='Data Series',
            title=f'Unemployment Rate Comparison ({selected_years[0]}-{selected_years[1]})',
            barmode='group',
            color_discrete_sequence=colors
        )
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Unemployment Rate (%)',
            legend_title='Education Level',
            hovermode='x unified',
            height=700,
            xaxis=dict(
                tickmode='array',
                tickvals=filtered_df['Year'].unique(),
                tickangle=45
            )
        )
    st.plotly_chart(fig, use_container_width=True)

def show_unemployment_summary(df, filtered_df, selected_educations, selected_years):
    st.subheader("📊 Unemployment Data Summary")
    
    # Latest year data
    if df is not None and not df.empty:
        latest_year = df.columns[-1]
        st.write(f"**{latest_year} Unemployment Rate by Education Level:**")
        latest_data = df[['Data Series', latest_year]].copy()
        latest_data.columns = ['Education Level', 'Unemployment Rate']
        latest_data = latest_data.sort_values('Unemployment Rate', ascending=False)
        st.dataframe(latest_data.style.format({'Unemployment Rate': '{:.1f}%'}), height=300)
    
    # Statistical information
    st.write("**Statistics for Selected Data:**")
    if not filtered_df.empty:
        avg_unemployment = filtered_df['Unemployment Rate'].mean()
        max_unemployment = filtered_df['Unemployment Rate'].max()
        min_unemployment = filtered_df['Unemployment Rate'].min()
        st.metric("Average Unemployment Rate", f"{avg_unemployment:.2f}%")
        st.metric("Highest Unemployment Rate", f"{max_unemployment:.2f}%")
        st.metric("Lowest Unemployment Rate", f"{min_unemployment:.2f}%")
    else:
        st.warning("No data available for the selected filters.")
    
    # Screening status
    st.write("**Current Filter:**")
    st.write(f"Education Levels: {', '.join(selected_educations)}")
    st.write(f"Year Range: {selected_years[0]} - {selected_years[1]}")

def show_unemployment_detailed_analysis(df, export_df):
    st.subheader("🔍 Unemployment Detailed Analysis")
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**Year Comparison Analysis**")
        if df is not None and len(df.columns) > 1:
            year_cols = [col for col in df.columns if str(col).isdigit()]
            col3a, col3b = st.columns(2)
            with col3a:
                year1 = st.selectbox("Select first year:", year_cols, index=0, key="unemployment_year1")
            with col3b:
                year2 = st.selectbox("Select second year:", year_cols, index=len(year_cols)-1, key="unemployment_year2")
            
            year1_data = df[['Data Series', year1]].set_index('Data Series')[year1]
            year2_data = df[['Data Series', year2]].set_index('Data Series')[year2]
            comparison_df = pd.DataFrame({
                f'{year1}': year1_data,
                f'{year2}': year2_data,
                'Change': year2_data - year1_data
            })
            st.dataframe(comparison_df.style.format({
                f'{year1}': '{:.1f}%',
                f'{year2}': '{:.1f}%',
                'Change': '{:+.1f}%'
            }))
    
    with col4:
        st.write("**Heatmap Analysis**")
        if not export_df.empty:
            heatmap_data = export_df.set_index('Data Series').T
            heatmap_data.index = heatmap_data.index.astype(int)
            fig_heat = px.imshow(
                heatmap_data,
                aspect="auto",
                color_continuous_scale='YlOrRd',
                title='Unemployment Rate Heatmap by Education Level',
                height=600
            )
            fig_heat.update_layout(
                xaxis_title='Education Level',
                yaxis_title='Year',
                yaxis=dict(tickmode='array', tickvals=heatmap_data.index.tolist())
            )
            fig_heat.update_coloraxes(colorbar_title="Unemployment Rate (%)")
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.warning("No data available for the heatmap.")

def show_unemployment_data_preview_and_download(df, export_df):
    st.subheader("📋 Unemployment Data Preview")
    if df is None or df.empty:
        st.warning("There is no unemployment data to show")
        return
    if export_df is None or export_df.empty:
        export_df = df 
    
    data_view_option = st.radio(
        "Select data to display:",
        ["Full Dataset", "Filtered Data (Current Selection)"],
        horizontal=True,
        key="unemployment_data_view"
    )
    if data_view_option == "Full Dataset":
        st.dataframe(df, use_container_width=True)
    else:
        st.dataframe(export_df, use_container_width=True)
    
    st.subheader("📥 Unemployment Data Export")
    export_option = st.radio(
        "Select data to export:",
        ["Full Dataset", "Filtered Data (Current Selection)"],
        horizontal=True,
        key="unemployment_export_option"
    )
    
    if export_option == "Full Dataset":
        csv_data = df.to_csv(index=False).encode('utf-8')
        file_name = "singapore_unemployment_full_data.csv"
    else:
        if export_df is None or export_df.empty:
            st.warning("Filter data is empty, the full data will be exported")
            csv_data = df.to_csv(index=False).encode('utf-8')
            file_name = "singapore_unemployment_full_data.csv"
        else:
            csv_data = export_df.to_csv(index=False).encode('utf-8')
            start_year = export_df.columns[1] if len(export_df.columns) > 1 else ""
            end_year = export_df.columns[-1] if len(export_df.columns) > 1 else ""
            file_name = f"singapore_unemployment_filtered_{start_year}_to_{end_year}.csv"
    
    st.download_button(
        label=f"💾 Download {export_option} as CSV",
        data=csv_data,
        file_name=file_name,
        mime="text/csv",
        key="unemployment_download_btn"
    )

# ---------------------- Main program entry ----------------------
def main():
    st.set_page_config(
        page_title="Comprehensive Salary & Employment Dashboard",
        page_icon=":bar_chart:",
        layout="wide"
    )
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.markdown("## <span style='font-size:2.5rem'>📋What traits shape a good career start: Industry, Occupation and Education Analysis for Young Singaporeans aged 25 to 29.</span>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid red; margin-top: 0.3rem;'>", unsafe_allow_html=True)

    # Load the module's data
    salary_df, salary_years, salary_occupations, salary_average_col = load_salary_data()
    employment_df, employment_years, employment_categories, employment_base_data = load_employment_data()
    market_emp_df, market_youth_df, market_min_year, market_max_year, market_BASE_YEAR, market_base_val, market_years_y = load_market_trend_data()
    age2529_df_melt, age2529_df_serv, age2529_years, age2529_all_main, age2529_all_serv = load_age2529_employment_data()
    edu_pop_df, edu_year_cols = load_education_pop_data()
    unemployment_df, unemployment_year_cols = load_unemployment_data()
    
    # Create all filters
    market_selected_emp_years, market_show_rate, market_show_total, market_show_base2007, market_selected_youth_year = create_market_trend_filters(
        market_min_year, market_max_year, market_years_y
    )
    age2529_selected_years, age2529_selected_main, age2529_selected_serv = create_age2529_filters(
        age2529_years, age2529_all_main, age2529_all_serv
    )
    selected_employment_years, selected_employment_categories = create_employment_filters(employment_years, employment_categories)
    selected_salary_years, selected_salary_occupations = create_salary_filters(salary_years, salary_occupations)
    selected_edu_years = create_education_pop_filters(edu_year_cols)
    selected_educations, selected_unemployment_years, selected_chart_type = create_unemployment_filters(unemployment_df, unemployment_year_cols)

    # Data preprocessing
    filtered_salary_df = filter_salary_data(salary_df, selected_salary_years, selected_salary_occupations, salary_average_col)
    filtered_employment_df = filter_employment_data(employment_df, selected_employment_years, selected_employment_categories)
    filtered_market_emp = filter_market_trend_data(market_emp_df, market_selected_emp_years)
    filtered_market_youth = filter_youth_share_data(market_youth_df, market_selected_youth_year)
    age2529_df_main_range, age2529_df_serv_range = filter_age2529_data(
        age2529_df_melt, age2529_df_serv, age2529_selected_years, age2529_selected_main, age2529_selected_serv
    )
    edu_2529_comb, edu_proportion = preprocess_education_pop_data(edu_pop_df)
    filtered_edu_2529, filtered_edu_proportion = filter_education_pop_data(edu_2529_comb, edu_proportion, selected_edu_years)
    filtered_unemployment_df, unemployment_export_df = preprocess_unemployment_data(unemployment_df, selected_educations, selected_unemployment_years)
    
    # Partition display Dashboard
        #-----------Market trends and talent share Dashboard------------
    st.divider()
    st.title("📊 Overall Singapore Market Employment Trends & 🧭 Youth Share by Industry")
    
    # Shows a chart of employment trends
    st.subheader("📈 Employment Trends")
    fig = plot_market_trend_chart(
        filtered_market_emp, 
        market_show_rate, 
        market_show_total, 
        market_show_base2007, 
        market_BASE_YEAR
    )
    
    # Employment Trend data preview and download
    if not filtered_market_emp.empty:
        with st.expander("📋 Show Employment Data Table (with Gradient)", expanded=False):
            cols = ["Year"]
            if market_show_total: cols.append("Total_Employed")
            if market_show_rate and "YoY_Growth_Rate" in filtered_market_emp.columns: cols.append("YoY_Growth_Rate")
            if market_show_base2007 and "Growth_vs_2007_%" in filtered_market_emp.columns: cols.append("Growth_vs_2007_%")
            
            preview_df = filtered_market_emp[cols].set_index("Year")
            fmt = {c: "{:,.2f}" if not c.endswith("%") else "{:.2f}%" for c in preview_df.columns}
            styler = preview_df.style.format(fmt)
            for c in preview_df.columns:
                styler = styler.background_gradient(cmap="viridis", subset=[c])
            st.dataframe(styler.set_properties(**{"color": "#FFFFFF", "font-size": "14px"}))
        
        # Employment Trends download button
        col1, col2 = st.columns(2)
        csv_emp = filtered_market_emp.round(2).to_csv(index=False).encode("utf-8")
        with col1:
            st.download_button(
                "💾 Download Employment Data (CSV)", 
                csv_emp, 
                file_name="employment_filtered.csv",
                key="market_emp_download"
            )
        with col2:
            try:
                from plotly.io import to_image
                if fig is not None:
                    png_emp = to_image(fig, format="png", width=1400, height=600, scale=2)
                    st.download_button(
                        "🖼️ Download Employment Chart (PNG)", 
                        png_emp, 
                        file_name="employment_chart.png", 
                        mime="image/png",
                        key="market_emp_chart_download"
                    )
            except Exception:
                st.warning("Install 'kaleido' to enable chart export: pip install kaleido")
    
    # Dendrogram showing the proportion of young people
    if market_selected_youth_year is not None:
        st.subheader(f"🧭 Youth Share by Industry — {market_selected_youth_year}")
        fig_t = plot_youth_share_treemap(filtered_market_youth, market_selected_youth_year)
        
        # Young people make up the download button
        if not filtered_market_youth.empty:
            col3, col4 = st.columns(2)
            csv_y = filtered_market_youth.round(2).to_csv(index=False).encode("utf-8")
            with col3:
                st.download_button(
                    "💾 Download Youth Data (CSV)", 
                    csv_y, 
                    file_name="youth_share_filtered.csv",
                    key="market_youth_download"
                )
            with col4:
                try:
                    from plotly.io import to_image
                    if fig_t is not None:
                        png_y = to_image(fig_t, format="png", width=1000, height=800, scale=2)
                        st.download_button(
                            "🖼️ Download Treemap Chart (PNG)", 
                            png_y, 
                            file_name="youth_treemap.png", 
                            mime="image/png",
                            key="market_youth_chart_download"
                        )
                except Exception:
                    st.warning("Install 'kaleido' to enable chart export: pip install kaleido")

    # ---------------Dashboard on Employment Trends for ages 25-29---------------
    st.divider()
    st.title("📈 Singapore Employment Trend (Aged 25–29)")
    # Display filter status
    if age2529_selected_years[0] is not None:
        yr0, yr1 = age2529_selected_years
        st.markdown(
            f"**Current Year Filter**: {yr0}–{yr1}  |  "
            f"Main: {'All' if len(age2529_selected_main)==len(age2529_all_main) else len(age2529_selected_main)} selected  |  "
            f"Services: {'All' if len(age2529_selected_serv)==len(age2529_all_serv) else len(age2529_selected_serv)} selected"
        )
    else:
        st.markdown("**Current Filter**: No valid year range selected")
    # Make a chart
    plot_age2529_charts(
        age2529_df_main_range, age2529_df_serv_range, 
        age2529_selected_main, age2529_selected_serv, 
        age2529_selected_years
    )
    # Data preview and download
    show_age2529_data_preview_and_download(
        age2529_df_main_range, age2529_df_serv_range, 
        age2529_selected_years, age2529_selected_main, 
        age2529_selected_serv
    )

    # --------------The Employment dashboard area------------------
    st.divider()
    st.title("📈 Distribution of positions in Singapore(Aged 25-29)")
    if not selected_employment_categories:
        st.markdown(f"**Current Filter**: Years {selected_employment_years[0]}-{selected_employment_years[1]} | All Categories")
    else:
        st.markdown(f"**Current Filter**: Years {selected_employment_years[0]}-{selected_employment_years[1]} | {len(selected_employment_categories)} Categories")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Stacked Area Chart")
        plot_stacked_chart(filtered_employment_df, employment_categories)
    with col2:
        st.subheader("Proportion by Year")
        if employment_base_data is not None:
            selected_pie_year = st.selectbox(
                "Select a year to view proportion:",
                options=employment_years,
                index=len(employment_years)-1 if employment_years else 0,
                key="employment_pie_year_select"
            )
            plot_proportion_pie_chart(employment_df, selected_pie_year, selected_employment_categories, employment_base_data, employment_categories)
    show_employment_data_preview_and_download(filtered_employment_df, selected_employment_years, selected_employment_categories)

    # -------------Payroll dashboard area-------------------
    st.divider()
    st.title("📈 Median Salary Trends of Positions in Singapore(Aged 25-29)")
    if not selected_salary_occupations:
        st.markdown(f"**Current Filter**: Years {selected_salary_years[0]}-{selected_salary_years[1]} | No Job Roles (Only Baseline)")
    elif len(selected_salary_occupations) == len(salary_occupations):
        st.markdown(f"**Current Filter**: Years {selected_salary_years[0]}-{selected_salary_years[1]} | All Job Roles")
    else:
        st.markdown(f"**Current Filter**: Years {selected_salary_years[0]}-{selected_salary_years[1]} | {len(selected_salary_occupations)} Job Roles")
    plot_salary_trend_chart(filtered_salary_df, salary_occupations, salary_average_col)
    show_salary_data_preview_and_download(filtered_salary_df, selected_salary_years, selected_salary_occupations, salary_occupations)

    # -------------Number of degrees dashboard area------------
    st.divider()
    st.title("🎓 Singapore Residents Education Level Distribution(Aged 25-29)")
    # Display filter status
    if selected_edu_years[0] is not None:
        st.markdown(f"**Current Filter**: Years {selected_edu_years[0]}-{selected_edu_years[1]}")
    else:
        st.markdown("**Current Filter**: No valid year range selected")
    # Chart the education trend + share
    plot_education_pop_chart(filtered_edu_2529, filtered_edu_proportion)
    # Data preview and download
    show_education_pop_data_preview_and_download(filtered_edu_2529, filtered_edu_proportion, selected_edu_years)

    # -----------Education and unemployment rate dashboard area------------
    st.divider()
    st.title("📊 Singapore Unemployment Rate Analysis by Education Level(Aged 25-29)")
    col_un1, col_un2 = st.columns([2, 1])
    with col_un1:
        st.subheader("📈 Unemployment Rate Trend Analysis")
        plot_unemployment_chart(filtered_unemployment_df, selected_unemployment_years, selected_chart_type)
    with col_un2:
        show_unemployment_summary(unemployment_df, filtered_unemployment_df, selected_educations, selected_unemployment_years)
    
    show_unemployment_detailed_analysis(unemployment_df, unemployment_export_df)
    show_unemployment_data_preview_and_download(unemployment_df, unemployment_export_df)
    st.caption("Data Source: Singapore Resident Unemployment Rate by Sex, Age and Highest Qualification Attained")

if __name__ == "__main__":
    main()