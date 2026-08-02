"""
████████████████████████████████████
Student Marks Analyzer Pro
AI-Powered Academic Performance Analytics
████████████████████████████████████
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
import os

# Page config MUST be first
st.set_page_config(
    page_title="Marks Analyzer Pro - Academic Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS STYLING
# ============================================

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    .glass-card {
        background: rgba(30, 27, 75, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
    }
    
    [data-testid="stMetric"] {
        background: rgba(30, 27, 75, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
    }
    
    [data-testid="stMetric"] label {
        color: #818cf8 !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 27, 75, 0.5);
        border-radius: 12px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #a5b4fc;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #6366f120, #8b5cf620);
        color: #818cf8;
        font-weight: 600;
    }
    
    h1, h2, h3 { color: #ffffff !important; font-weight: 700 !important; }
    
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #6366f140; border-radius: 4px; }
    
    .gradient-text {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .topper-badge {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: #000;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .rank-1 { background: linear-gradient(135deg, #ffd700, #ffb700); }
    .rank-2 { background: linear-gradient(135deg, #c0c0c0, #a0a0a0); }
    .rank-3 { background: linear-gradient(135deg, #cd7f32, #b8700a); }
    
    .stDataFrame {
        background: rgba(30, 27, 75, 0.6);
        border-radius: 15px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# DATA GENERATION & PROCESSING
# ============================================

def generate_sample_data():
    """Generate sample student marks data"""
    np.random.seed(42)
    
    students = [
        'Alice Johnson', 'Bob Smith', 'Charlie Brown', 'David Wilson',
        'Eva Martinez', 'Frank Lee', 'Grace Kim', 'Henry Davis',
        'Isabella Garcia', 'Jack Turner', 'Karen White', 'Leo Thompson',
        'Mia Rodriguez', 'Noah Anderson', 'Olivia Taylor', 'Peter Chen',
        'Quinn Murphy', 'Rachel Green', 'Sam Patel', 'Tina Williams'
    ]
    
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'Computer Science']
    
    data = {'Name': students}
    
    for subject in subjects:
        # Generate realistic marks with different distributions per subject
        if subject == 'Mathematics':
            marks = np.random.normal(72, 15, len(students))
        elif subject == 'Physics':
            marks = np.random.normal(68, 18, len(students))
        elif subject == 'Chemistry':
            marks = np.random.normal(70, 16, len(students))
        elif subject == 'Biology':
            marks = np.random.normal(75, 12, len(students))
        elif subject == 'English':
            marks = np.random.normal(78, 10, len(students))
        else:
            marks = np.random.normal(65, 20, len(students))
        
        # Clip to valid range and round
        marks = np.clip(marks, 35, 100).astype(int)
        data[subject] = marks
    
    df = pd.DataFrame(data)
    
    # Calculate totals and averages
    df['Total'] = df[subjects].sum(axis=1)
    df['Average'] = df[subjects].mean(axis=1).round(2)
    df['Percentage'] = (df['Total'] / (len(subjects) * 100) * 100).round(2)
    
    # Assign grades
    def get_grade(pct):
        if pct >= 90: return 'A+'
        elif pct >= 80: return 'A'
        elif pct >= 70: return 'B+'
        elif pct >= 60: return 'B'
        elif pct >= 50: return 'C+'
        elif pct >= 40: return 'C'
        else: return 'F'
    
    df['Grade'] = df['Percentage'].apply(get_grade)
    
    # Add rank
    df['Rank'] = df['Total'].rank(ascending=False, method='min').astype(int)
    
    # Sort by total marks
    df = df.sort_values('Total', ascending=False).reset_index(drop=True)
    
    return df, subjects

def analyze_data(df, subjects):
    """Perform comprehensive data analysis with error handling"""
    
    # Ensure Percentage column exists
    if 'Percentage' not in df.columns:
        if 'Total' in df.columns and subjects:
            df['Percentage'] = (df['Total'] / (len(subjects) * 100) * 100).round(2)
        else:
            df['Percentage'] = 0
    
    # Calculate pass percentage with safety check
    pass_percentage = 0
    if len(df) > 0:
        pass_count = df[df['Percentage'] >= 40].shape[0]
        pass_percentage = (pass_count / len(df) * 100).round(2)
    
    # Ensure all required keys exist
    subject_averages = {subj: df[subj].mean().round(2) if subj in df.columns else 0 for subj in subjects}
    
    # Get top 3 safely
    top_3 = []
    if len(df) > 0:
        top_3 = df.head(3)[['Name', 'Total', 'Percentage', 'Grade']].to_dict('records')
    
    # Get subject toppers safely
    subject_toppers = {}
    for subj in subjects:
        if subj in df.columns and len(df) > 0:
            subject_toppers[subj] = df.loc[df[subj].idxmax(), 'Name']
        else:
            subject_toppers[subj] = 'N/A'
    
    # Get subject highest safely
    subject_highest = {}
    for subj in subjects:
        if subj in df.columns:
            subject_highest[subj] = df[subj].max()
        else:
            subject_highest[subj] = 0
    
    # Get weakest and strongest subjects
    weakest_subject = subjects[0] if subjects else 'None'
    strongest_subject = subjects[0] if subjects else 'None'
    if subject_averages:
        weakest_subject = min(subject_averages, key=subject_averages.get)
        strongest_subject = max(subject_averages, key=subject_averages.get)
    
    analysis = {
        'total_students': len(df),
        'subjects': subjects,
        'class_average': df['Average'].mean().round(2) if 'Average' in df.columns and len(df) > 0 else 0,
        'class_highest': df['Total'].max() if 'Total' in df.columns and len(df) > 0 else 0,
        'class_lowest': df['Total'].min() if 'Total' in df.columns and len(df) > 0 else 0,
        'pass_percentage': pass_percentage,
        
        # Overall topper
        'overall_topper': df.iloc[0]['Name'] if len(df) > 0 else 'N/A',
        'topper_marks': df.iloc[0]['Total'] if len(df) > 0 else 0,
        'topper_percentage': df.iloc[0]['Percentage'] if len(df) > 0 else 0,
        
        # Top 3
        'top_3': top_3,
        
        # Subject-wise toppers
        'subject_toppers': subject_toppers,
        'subject_highest': subject_highest,
        'subject_average': subject_averages,
        
        # Grade distribution
        'grade_distribution': df['Grade'].value_counts().to_dict() if 'Grade' in df.columns else {},
        
        # Weakest and strongest subjects
        'weakest_subject': weakest_subject,
        'strongest_subject': strongest_subject,
    }
    
    return analysis

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================

def create_subject_comparison(df, subjects):
    """Create subject-wise comparison chart"""
    fig = go.Figure()
    
    colors = ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd', '#818cf8', '#6366f1']
    
    for i, subject in enumerate(subjects):
        if subject in df.columns:
            fig.add_trace(go.Box(
                y=df[subject],
                name=subject,
                marker_color=colors[i % len(colors)],
                boxmean='sd'
            ))
    
    fig.update_layout(
        title=dict(text='📊 Subject-wise Performance Distribution', font=dict(color='white', size=20), x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(title='Marks', gridcolor='rgba(255,255,255,0.1)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        height=500,
        margin=dict(t=60, b=40, l=60, r=40),
        showlegend=True,
        legend=dict(font=dict(color='white'))
    )
    
    return fig

def create_student_performance(df, subjects):
    """Create student performance heatmap"""
    # Prepare data for heatmap
    heatmap_data = df.set_index('Name')[subjects]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=subjects,
        y=heatmap_data.index,
        colorscale='Viridis',
        text=heatmap_data.values,
        texttemplate='%{text}',
        textfont={"size": 10, "color": "white"},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=dict(text='🔥 Student Performance Heatmap', font=dict(color='white', size=20), x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600,
        margin=dict(t=60, b=40, l=100, r=40),
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10))
    )
    
    return fig

def create_radar_chart(df, subjects, student_name):
    """Create radar chart for individual student"""
    student_data = df[df['Name'] == student_name]
    
    if student_data.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=student_data[subjects].values[0],
        theta=subjects,
        fill='toself',
        name=student_name,
        line_color='#818cf8',
        fillcolor='rgba(99, 102, 241, 0.3)'
    ))
    
    # Add class average
    avg_values = df[subjects].mean().values
    fig.add_trace(go.Scatterpolar(
        r=avg_values,
        theta=subjects,
        fill='toself',
        name='Class Average',
        line_color='#fbbf24',
        fillcolor='rgba(251, 191, 36, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='white')
            ),
            angularaxis=dict(
                tickfont=dict(color='white')
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title=dict(text=f'🎯 {student_name} - Performance Radar', font=dict(color='white', size=16), x=0.5),
        height=450,
        showlegend=True,
        legend=dict(font=dict(color='white'))
    )
    
    return fig

def create_grade_distribution(df):
    """Create grade distribution pie chart"""
    if 'Grade' not in df.columns or df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=dict(text='📈 Grade Distribution', font=dict(color='white', size=20), x=0.5),
            paper_bgcolor='rgba(0,0,0,0)',
            height=450
        )
        return fig
    
    grade_counts = df['Grade'].value_counts()
    
    colors = {
        'A+': '#10b981', 'A': '#34d399', 'B+': '#fbbf24',
        'B': '#f59e0b', 'C+': '#f97316', 'C': '#ef4444', 'F': '#dc2626'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=grade_counts.index,
        values=grade_counts.values,
        hole=0.4,
        marker=dict(colors=[colors.get(g, '#6366f1') for g in grade_counts.index]),
        textinfo='label+percent',
        textfont=dict(color='white', size=14)
    )])
    
    fig.update_layout(
        title=dict(text='📈 Grade Distribution', font=dict(color='white', size=20), x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        showlegend=True,
        legend=dict(font=dict(color='white'))
    )
    
    return fig

def create_rank_chart(df):
    """Create ranking bar chart"""
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=dict(text='🏆 Top 10 Students Ranking', font=dict(color='white', size=20), x=0.5),
            paper_bgcolor='rgba(0,0,0,0)',
            height=450
        )
        return fig
    
    top_10 = df.head(10).sort_values('Total')
    
    fig = go.Figure(go.Bar(
        x=top_10['Total'],
        y=top_10['Name'],
        orientation='h',
        marker=dict(
            color=top_10['Percentage'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Percentage', tickfont=dict(color='white'))
        ),
        text=top_10['Total'],
        textposition='outside',
        textfont=dict(color='white')
    ))
    
    fig.update_layout(
        title=dict(text='🏆 Top 10 Students Ranking', font=dict(color='white', size=20), x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(title='Total Marks', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        height=450,
        margin=dict(t=60, b=40, l=150, r=40)
    )
    
    return fig

# ============================================
# STREAMLIT UI
# ============================================

def main():
    load_css()
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df, st.session_state.subjects = generate_sample_data()
    if 'analysis' not in st.session_state:
        st.session_state.analysis = analyze_data(st.session_state.df, st.session_state.subjects)
    
    df = st.session_state.df
    subjects = st.session_state.subjects
    analysis = st.session_state.analysis
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:20px 0;">
            <h1 style="font-size:1.8rem; margin:0;">
                <span style="color:#818cf8;">🎓 Marks</span><span style="color:#ffffff;"> Analyzer</span>
            </h1>
            <p style="color:#a5b4fc; font-size:0.85rem; margin-top:5px;">
                Academic Performance Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data upload
        st.markdown("### 📁 Data Source")
        
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="CSV with columns: Name, Subject1, Subject2, ..."
        )
        
        if uploaded_file:
            try:
                new_df = pd.read_csv(uploaded_file)
                # Identify subject columns
                name_col = new_df.columns[0]
                subject_cols = [col for col in new_df.columns[1:] if new_df[col].dtype in ['int64', 'float64']]
                
                new_df['Total'] = new_df[subject_cols].sum(axis=1)
                new_df['Average'] = new_df[subject_cols].mean(axis=1).round(2)
                new_df['Percentage'] = (new_df['Total'] / (len(subject_cols) * 100) * 100).round(2)
                
                def get_grade(pct):
                    if pct >= 90: return 'A+'
                    elif pct >= 80: return 'A'
                    elif pct >= 70: return 'B+'
                    elif pct >= 60: return 'B'
                    elif pct >= 50: return 'C+'
                    elif pct >= 40: return 'C'
                    else: return 'F'
                
                new_df['Grade'] = new_df['Percentage'].apply(get_grade)
                new_df['Rank'] = new_df['Total'].rank(ascending=False, method='min').astype(int)
                new_df = new_df.sort_values('Total', ascending=False).reset_index(drop=True)
                
                st.session_state.df = new_df
                st.session_state.subjects = subject_cols
                st.session_state.analysis = analyze_data(new_df, subject_cols)
                st.success(f"✅ Loaded {len(new_df)} students")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        
        if st.button("🔄 Reset to Sample Data", use_container_width=True):
            st.session_state.df, st.session_state.subjects = generate_sample_data()
            st.session_state.analysis = analyze_data(st.session_state.df, st.session_state.subjects)
            st.rerun()
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 🔍 Filters")
        selected_subject = st.selectbox("Select Subject", ['All'] + subjects)
        
        grade_filter = st.multiselect(
            "Filter by Grade",
            ['A+', 'A', 'B+', 'B', 'C+', 'C', 'F'],
            default=['A+', 'A', 'B+', 'B', 'C+', 'C', 'F']
        )
        
        # Apply filters
        filtered_df = df[df['Grade'].isin(grade_filter)]
        if selected_subject != 'All':
            filtered_df = filtered_df.nlargest(10, selected_subject)
        
        st.markdown("---")
        
        # Export options
        st.markdown("### 📥 Export")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📄 Download CSV",
            csv,
            "student_marks.csv",
            "text/csv",
            use_container_width=True
        )
        
        # Excel export
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Student Marks', index=False)
        excel_data = output.getvalue()
        
        st.download_button(
            "📊 Download Excel",
            excel_data,
            "student_marks.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    # Main content
    st.markdown("""
    <div style="text-align:center; padding:20px 0;">
        <h1 style="font-size:3rem; font-weight:900; margin:0;">
            <span style="color:#818cf8;">🎓 Student Marks</span>
            <span style="color:#ffffff;"> Analyzer Pro</span>
        </h1>
        <p style="font-size:1.2rem; color:#a78bfa; margin:10px 0;">
            AI-Powered Academic Performance Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("👨‍🎓 Total Students", analysis['total_students'])
    with col2:
        st.metric("📊 Class Average", f"{analysis['class_average']:.1f}%")
    with col3:
        st.metric("🏆 Highest", f"{analysis['class_highest']}")
    with col4:
        st.metric("✅ Pass Rate", f"{analysis['pass_percentage']}%")
    with col5:
        st.metric("📈 Subjects", len(subjects))
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "🏆 Rankings", "📈 Analysis", "🔍 Individual", "📋 Data Table"
    ])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            box_plot = create_subject_comparison(df, subjects)
            st.plotly_chart(box_plot, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🏆 Overall Topper")
            st.markdown(f"""
            <div style="text-align:center; padding:20px;">
                <h2 style="color:#fbbf24; margin:0;">🥇 {analysis['overall_topper']}</h2>
                <p style="color:#a5b4fc; font-size:1.2rem; margin:10px 0;">
                    {analysis['topper_marks']} / {len(subjects) * 100}
                </p>
                <p style="color:#10b981; font-size:1.5rem; font-weight:700;">
                    {analysis['topper_percentage']}%
                </p>
                <span class="topper-badge rank-1">Rank #1</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            pie_chart = create_grade_distribution(df)
            st.plotly_chart(pie_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Subject-wise toppers
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Subject-wise Toppers")
        
        cols = st.columns(len(subjects))
        for i, subject in enumerate(subjects):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align:center; padding:15px; background:rgba(99,102,241,0.1); border-radius:12px;">
                    <p style="color:#818cf8; font-weight:600; margin:0;">{subject}</p>
                    <p style="color:#fbbf24; font-size:1.1rem; margin:5px 0;">🥇 {analysis['subject_toppers'].get(subject, 'N/A')}</p>
                    <p style="color:#10b981; font-weight:700;">{analysis['subject_highest'].get(subject, 0)}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        rank_chart = create_rank_chart(df)
        st.plotly_chart(rank_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Top 3 podium
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Top 3 Performers")
        
        col1, col2, col3 = st.columns([1, 1.2, 1])
        medals = ['🥇', '🥈', '🥉']
        rank_classes = ['rank-1', 'rank-2', 'rank-3']
        
        for i, (col, medal, rank_class) in enumerate(zip([col2, col1, col3], medals, rank_classes)):
            if i < len(analysis['top_3']):
                student = analysis['top_3'][i]
                with col:
                    st.markdown(f"""
                    <div style="text-align:center; padding:20px; background:rgba(30,27,75,0.8); border-radius:15px; border:2px solid rgba(99,102,241,0.3);">
                        <h2 style="margin:0;">{medal}</h2>
                        <h3 style="color:#fbbf24; margin:10px 0;">{student['Name']}</h3>
                        <p style="color:#a5b4fc;">{student['Total']} marks</p>
                        <p style="color:#10b981; font-weight:700;">{student['Percentage']}%</p>
                        <span class="topper-badge {rank_class}">Rank #{i+1}</span>
                        <p style="color:#a78bfa; margin-top:10px;">Grade: {student['Grade']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Subject Averages")
            
            avg_data = pd.DataFrame({
                'Subject': subjects,
                'Average': [analysis['subject_average'][s] for s in subjects]
            })
            
            fig = px.bar(avg_data, x='Subject', y='Average', color='Average',
                        color_continuous_scale='Viridis', title='Subject-wise Average Marks')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'), height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            heatmap = create_student_performance(df, subjects)
            st.plotly_chart(heatmap, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Insights
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 💡 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="padding:15px; background:rgba(99,102,241,0.1); border-radius:10px;">
                <h4 style="color:#818cf8;">📈 Strongest Subject</h4>
                <p style="color:#10b981; font-size:1.2rem; font-weight:700;">{analysis['strongest_subject']}</p>
                <p style="color:#a5b4fc;">Avg: {analysis['subject_average'][analysis['strongest_subject']]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="padding:15px; background:rgba(239,68,68,0.1); border-radius:10px;">
                <h4 style="color:#ef4444;">📉 Weakest Subject</h4>
                <p style="color:#fbbf24; font-size:1.2rem; font-weight:700;">{analysis['weakest_subject']}</p>
                <p style="color:#a5b4fc;">Avg: {analysis['subject_average'][analysis['weakest_subject']]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="padding:15px; background:rgba(16,185,129,0.1); border-radius:10px;">
                <h4 style="color:#10b981;">✅ Class Performance</h4>
                <p style="color:#a78bfa; font-size:1.2rem; font-weight:700;">{analysis['pass_percentage']}% Pass Rate</p>
                <p style="color:#a5b4fc;">{analysis['total_students']} Students</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Individual Student Analysis")
        
        selected_student = st.selectbox("Select Student", df['Name'].tolist())
        
        if selected_student:
            student_data = df[df['Name'] == selected_student].iloc[0]
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.markdown(f"""
                <div style="padding:20px; background:rgba(99,102,241,0.1); border-radius:15px;">
                    <h3 style="color:#fbbf24; margin:0;">{student_data['Name']}</h3>
                    <p style="color:#a5b4fc;">Rank: <span style="color:#fbbf24; font-weight:700;">#{int(student_data['Rank'])}</span></p>
                    <p style="color:#a5b4fc;">Total: <span style="color:#10b981; font-weight:700;">{int(student_data['Total'])}/{len(subjects)*100}</span></p>
                    <p style="color:#a5b4fc;">Percentage: <span style="color:#a78bfa; font-weight:700;">{student_data['Percentage']}%</span></p>
                    <p style="color:#a5b4fc;">Grade: <span style="color:#fbbf24; font-weight:700; font-size:1.2rem;">{student_data['Grade']}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Subject-wise marks
                st.markdown("### Subject-wise Marks")
                for subject in subjects:
                    marks = int(student_data[subject])
                    pct = marks
                    color = '#10b981' if pct >= 75 else '#fbbf24' if pct >= 60 else '#ef4444'
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; 
                                padding:8px; margin:5px 0; background:rgba(99,102,241,0.05); border-radius:8px;">
                        <span style="color:#a5b4fc;">{subject}</span>
                        <span style="color:{color}; font-weight:600;">{marks}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                radar = create_radar_chart(df, subjects, selected_student)
                if radar:
                    st.plotly_chart(radar, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Complete Data Table")
        
        # Search
        search = st.text_input("🔍 Search student...", placeholder="Type student name...")
        
        display_df = df.copy()
        if search:
            display_df = display_df[display_df['Name'].str.contains(search, case=False)]
        
        # Style the dataframe
        def highlight_topper(s):
            return ['background-color: rgba(251,191,36,0.2); color: #fbbf24; font-weight: bold' if s.name == 0 else '' for _ in s]
        
        styled_df = display_df.style.apply(highlight_topper, axis=0)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Name': 'Student Name',
                'Total': st.column_config.NumberColumn('Total', format="%d"),
                'Average': st.column_config.NumberColumn('Average', format="%.1f"),
                'Percentage': st.column_config.NumberColumn('Percentage', format="%.1f%%"),
                'Grade': 'Grade',
                'Rank': st.column_config.NumberColumn('Rank', format="#%d")
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <p style="color:#818cf8; font-size:1rem; font-weight:600;">
            🎓 Student Marks Analyzer Pro v2.0
        </p>
        <p style="color:#a5b4fc; font-size:0.8rem;">
            AI-Powered Academic Analytics | Built with Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
