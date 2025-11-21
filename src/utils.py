"""
Utility Functions for Marketing Campaign Causal Analysis
=========================================================

Author: Tomasz Solis
Purpose: Helper functions for data preprocessing and visualization

"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def reconstruct_contact_date(df, additional_info=False, start_year=2008):
    """
    Reconstruct full contact dates from month column using sequential logic.
    
    The dataset lacks explicit year information. Years are inferred by detecting
    month wrap-around: when month decreases from one row to the next (e.g., 
    November→March), the year increments.
    
    Parameters
    ----------
    df : pd.DataFrame
        Must contain 'month' column with three-letter month abbreviations.
        Optionally contains 'day' column.
    additional_info : bool, default False
        If True, adds 'quarter' and 'year_quarter' columns.
    start_year : int, default 2008
        Starting year for first observation.
        
    Returns
    -------
    pd.DataFrame
        Copy of input with added columns:
        - 'year': Inferred year
        - 'contact_date': Full datetime
        - 'quarter', 'year_quarter': If additional_info=True
        
    Raises
    ------
    ValueError
        If 'month' column is missing or contains invalid values.
        
    Examples
    --------
    >>> df = pd.DataFrame({'month': ['may', 'jun', 'dec', 'jan']})
    >>> df_dated = reconstruct_contact_date(df)
    >>> df_dated[['month', 'year', 'contact_date']]
       month  year contact_date
    0    may  2008   2008-05-01
    1    jun  2008   2008-06-01
    2    dec  2008   2008-12-01
    3    jan  2009   2009-01-01
    """
    df = df.copy()
    
    # Validate input
    if 'month' not in df.columns:
        raise ValueError("DataFrame must contain 'month' column.")
    
    # Month name to number mapping
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
        'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
        'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    # Convert month names to numbers
    df['month_num'] = df['month'].str.lower().map(month_map)
    
    if df['month_num'].isna().any():
        invalid_months = df.loc[df['month_num'].isna(), 'month'].unique()
        raise ValueError(f"Invalid month values found: {invalid_months}")
    
    # Infer years from month sequence
    years = []
    current_year = start_year
    prev_month = df['month_num'].iloc[0]
    
    for month_num in df['month_num']:
        # If month decreased, assume new year
        if month_num < prev_month:
            current_year += 1
        years.append(current_year)
        prev_month = month_num
    
    df['year'] = years
    
    # Handle day: use existing 'day' column or default to 1
    day_col = df['day'] if 'day' in df.columns else 1
    
    # Construct full datetime
    df['contact_date'] = pd.to_datetime({
        'year': df['year'],
        'month': df['month_num'],
        'day': day_col
    })
    
    # Add quarter information if requested
    if additional_info:
        df['quarter'] = df['contact_date'].dt.quarter
        df['year_quarter'] = (
            df['year'].astype(str) + '-Q' + df['quarter'].astype(str)
        )
    
    # Cleanup temporary column
    df = df.drop(columns=['month_num'])
    
    return df


def create_pseudo_customer_id(df, id_cols=None):
    """
    Create pseudo-customer identifier from stable demographic features.
    
    Since the dataset lacks explicit customer IDs, we construct a composite
    identifier from demographic and account attributes that are stable over time.
    
    Parameters
    ----------
    df : pd.DataFrame
        Customer contact data.
    id_cols : list of str, optional
        Columns to use for pseudo-ID creation. If None, uses default set:
        ['age', 'job', 'marital', 'education', 'housing', 'loan', 'contact']
        
    Returns
    -------
    pd.DataFrame
        Copy of input with added 'pseudo_id' column.
        
    Notes
    -----
    Pseudo-ID quality depends on demographic granularity. Using 7 demographic
    features typically yields ~34% unique IDs from contact events, implying
    ~3 contacts per customer on average.
    
    Examples
    --------
    >>> df_with_id = create_pseudo_customer_id(df)
    >>> print(f"Unique customers: {df_with_id['pseudo_id'].nunique()}")
    """
    df = df.copy()
    
    if id_cols is None:
        id_cols = ['age', 'job', 'marital', 'education', 'housing', 'loan', 'contact']
    
    # Validate columns exist
    missing_cols = set(id_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
    
    # Create composite ID by concatenating string representations
    df['pseudo_id'] = df[id_cols].astype(str).agg('_'.join, axis=1)
    
    return df


def plot_time_series(df, date_col, value_col, title, yaxis_title, 
                     color='#636EFA', show_crisis=True):
    """
    Create interactive time series plot with optional crisis period shading.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data containing time series.
    date_col : str
        Column name containing dates.
    value_col : str
        Column name containing values to plot.
    title : str
        Plot title.
    yaxis_title : str
        Y-axis label.
    color : str, default '#636EFA'
        Line color (hex or named color).
    show_crisis : bool, default True
        If True, shade September 2008-March 2009 period (financial crisis).
        
    Returns
    -------
    plotly.graph_objects.Figure
        Interactive plot object.
    """
    fig = go.Figure()
    
    # Add main line
    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df[value_col],
        mode='lines',
        line=dict(color=color, width=2),
        name=value_col
    ))
    
    # Add crisis period shading
    if show_crisis:
        fig.add_vrect(
            x0="2008-09-01", x1="2009-03-31",
            fillcolor="red", opacity=0.1,
            layer="below", line_width=0,
            annotation_text="Financial Crisis",
            annotation_position="top left"
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_covariate_balance(balance_df, title="Covariate Balance Check"):
    """
    Visualize covariate balance between treatment and control groups.
    
    Parameters
    ----------
    balance_df : pd.DataFrame
        Balance table with columns ['Wave 1', 'Wave 2', 'Abs % Diff'].
        Index should contain covariate names.
    title : str, default "Covariate Balance Check"
        Plot title.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Interactive bar chart showing standardized differences.
        
    Notes
    -----
    Rule of thumb: Absolute standardized differences <10% indicate good balance,
    >20% may indicate problematic imbalance.
    """
    fig = go.Figure()
    
    # Color bars by balance quality
    colors = ['green' if x < 10 else 'orange' if x < 20 else 'red' 
              for x in balance_df['Abs % Diff']]
    
    fig.add_trace(go.Bar(
        y=balance_df.index,
        x=balance_df['Abs % Diff'],
        orientation='h',
        marker=dict(color=colors),
        text=balance_df['Abs % Diff'].round(1).astype(str) + '%',
        textposition='outside'
    ))
    
    # Add reference lines
    fig.add_vline(x=10, line_dash="dash", line_color="green", 
                  annotation_text="Good (<10%)")
    fig.add_vline(x=20, line_dash="dash", line_color="red",
                  annotation_text="Concerning (>20%)")
    
    fig.update_layout(
        title=title,
        xaxis_title="Absolute % Difference",
        yaxis_title="Covariate",
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    return fig


def create_sample_flow_diagram(sample_counts):
    """
    Create Sankey diagram showing sample selection flow.
    
    Parameters
    ----------
    sample_counts : dict
        Dictionary with keys:
        - 'total_contacts'
        - 'wave_1_and_2'
        - 'single_wave'
        - 'cross_wave'
        - 'final_wave_1'
        - 'final_wave_2'
        
    Returns
    -------
    plotly.graph_objects.Figure
        Sankey diagram showing attrition.
    """
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            label=[
                "All Contacts",
                "Wave 1 or 2",
                "Other Periods",
                "Single-Wave",
                "Cross-Wave",
                "Final Wave 1",
                "Final Wave 2"
            ],
            color=["lightgray", "lightblue", "lightgray", 
                   "lightgreen", "salmon", "green", "green"]
        ),
        link=dict(
            source=[0, 0, 1, 1, 3, 3],
            target=[1, 2, 3, 4, 5, 6],
            value=[
                sample_counts['wave_1_and_2'],
                sample_counts['total_contacts'] - sample_counts['wave_1_and_2'],
                sample_counts['single_wave'],
                sample_counts['cross_wave'],
                sample_counts['final_wave_1'],
                sample_counts['final_wave_2']
            ]
        )
    )])
    
    fig.update_layout(
        title="Sample Selection Flow",
        font_size=12,
        height=400
    )
    
    return fig
