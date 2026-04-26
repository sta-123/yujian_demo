import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# -------------------------- 页面全局配置 --------------------------
st.set_page_config(
    page_title="预健·MED·AI | 中青年急重症智能预警系统",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- 深色高对比CSS（文字100%清晰） --------------------------
st.markdown("""
<style>
    /* 全局重置与基础样式 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'PingFang SC', 'Microsoft YaHei', 'Inter', sans-serif;
        color: #ffffff;
    }
    
    /* 主背景 - 专业深蓝黑 */
    .stApp {
        background: #0f172a;
    }
    
    /* 侧边栏 - 深灰 */
    [data-testid="stSidebar"] {
        background: #1e293b;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-brand {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    
    .sidebar-title {
        color: #165DFF;
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 0.3rem;
    }
    
    /* 主标题 - 白色高对比 */
    .main-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    
    /* 卡片模块 - 半透明深色，边框清晰 */
    .module-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    
    /* 指标卡片 - 深色+白色文字 */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 1rem;
        color: white;
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255, 255, 255, 0.6) !important;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    /* 按钮 - 蓝色主色，文字白色 */
    .stButton>button {
        background: #165DFF;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #0e4bcc;
    }
    
    /* 文本颜色统一 - 所有文字白色 */
    h1, h2, h3, h4, h5, h6, p, li, div {
        color: #ffffff !important;
    }
    
    /* 警告/信息框 - 深色背景+白色文字 */
    .stAlert {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px;
    }
    
    /* 分隔线 - 浅色 */
    hr {
        border: none;
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin: 1.5rem 0;
    }
    
    /* 标签页 - 选中状态清晰 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.03);
        border-radius: 6px;
        padding: 0.5rem 1rem;
        color: white;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #165DFF;
        color: white;
    }
    
    /* 进度条 - 蓝色 */
    .stProgress > div > div {
        background: #165DFF;
        border-radius: 4px;
    }
    
    /* 输入框/下拉框/文本框 - 深色背景+白色文字 */
    .stNumberInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.03) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 6px;
    }
    
    /* 下拉框选项文字 - 强制白色 */
    div[data-baseweb="popover"] div[role="listbox"] div[role="option"] {
        color: #000000 !important;
    }
    
    /* 单选按钮文字 - 强制白色 */
    .stRadio > label, .stRadio > div {
        color: #ffffff !important;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 表格文字 - 强制白色 */
    .stDataFrame {
        color: white !important;
    }
    .stDataFrame table {
        color: white !important;
    }
    .stDataFrame th, .stDataFrame td {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------- 异常指标解读知识库 --------------------------
ABNORMAL_ADVICE = {
    "收缩压": {
        "↑": "【血压升高】建议减少钠盐摄入（每日<5g），避免熬夜和情绪激动，每日监测血压2-3次，如持续高于140mmHg请及时就医心内科。",
        "↓": "【血压偏低】建议加强营养，适度增加蛋白质摄入，避免突然站立，如频繁头晕请就医检查。"
    },
    "舒张压": {
        "↑": "【舒张压升高】建议加强有氧运动（每日30分钟快走），减少高脂饮食，规律作息，2周后复查血压。",
        "↓": "【舒张压偏低】建议适度增加饮水量，避免长时间热水浴，定期监测血压变化。"
    },
    "总胆固醇": {
        "↑": "【胆固醇升高】建议严格控制高脂食物（动物内脏、肥肉），增加深海鱼、新鲜蔬果摄入，每日运动30分钟，3个月后复查血脂。",
        "↓": "【胆固醇偏低】建议适度增加优质蛋白和不饱和脂肪酸摄入（坚果、橄榄油），保持营养均衡。"
    },
    "甘油三酯": {
        "↑": "【甘油三酯升高】建议严格控制甜食、酒精和精制碳水，增加膳食纤维摄入，每周至少150分钟中等强度运动。",
        "↓": "【甘油三酯偏低】建议保持规律饮食，适度增加健康脂肪摄入。"
    },
    "空腹血糖": {
        "↑": "【血糖升高】建议控制精制糖和主食摄入，增加全谷物和蔬菜，规律监测血糖，必要时就医内分泌科。",
        "↓": "【血糖偏低】建议规律进餐，随身携带糖果，避免空腹剧烈运动。"
    },
    "心率": {
        "↑": "【心率加快】建议避免浓茶、咖啡，减少熬夜和精神紧张，每日进行冥想放松，如持续高于100次/分请就医。",
        "↓": "【心率偏慢】如无不适可继续观察，如伴随头晕、乏力请及时就医心内科。"
    },
    "肌酸激酶": {
        "↑": "【肌酸激酶升高】建议近期避免剧烈运动，休息1周后复查，如伴随胸痛、胸闷请立即就医。",
        "↓": "【肌酸激酶偏低】一般无特殊临床意义，保持规律运动即可。"
    },
    "低密度脂蛋白": {
        "↑": "【坏胆固醇升高】这是心脑血管疾病的高危因素！建议立即启动低脂饮食，增加运动，必要时就医心内科启动药物干预。",
        "↓": "【坏胆固醇偏低】这是好现象，继续保持健康生活方式。"
    },
    "同型半胱氨酸": {
        "↑": "【同型半胱氨酸升高】这是心脑血管疾病的独立危险因素！建议补充叶酸、维生素B6/B12，增加新鲜蔬果摄入，定期复查。",
        "↓": "【同型半胱氨酸偏低】这是好现象，继续保持。"
    }
}

# -------------------------- 侧边栏导航 --------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🩺</div>
        <div class="sidebar-title">预健·MED·AI</div>
        <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">中青年急重症智能预警系统</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 导航选项
    page = st.radio(
        "功能导航",
        ["🏠 系统首页", "📡 实时健康监测", "📊 数据同步中心", "⚠️ 风险预警中心", "💊 健康管理中心"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("© 2026 PREHEALTH MED·AI | All Rights Reserved")

# -------------------------- 全局数据初始化 --------------------------
# 用户基础数据（可编辑）
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "age": 32,
        "gender": "男",
        "family_history": "有心脑血管家族史",
        "lifestyle": "熬夜（日均睡眠6小时）、久坐、工作压力大",
        "health_score": 58
    }
st.session_state.user_data.setdefault("health_score", 58)

# 14天健康时序数据
if 'health_data' not in st.session_state:
    dates = [datetime.now() - timedelta(days=i) for i in range(14, 0, -1)]
    base_hr = np.random.randint(65, 75, 11)
    abnormal_hr = np.array([78, 82, 85])
    base_bp = np.random.randint(115, 130, 11)
    abnormal_bp = np.array([135, 140, 145])
    
    st.session_state.health_data = pd.DataFrame({
        "日期": dates,
        "静息心率": np.concatenate([base_hr, abnormal_hr]),
        "夜间心率": np.concatenate([base_hr - 8, abnormal_hr - 5]),
        "收缩压": np.concatenate([base_bp, abnormal_bp]),
        "舒张压": np.concatenate([np.random.randint(70, 80, 11), [82, 88, 92]]),
        "血氧饱和度": np.round(np.random.uniform(96, 99, 14), 1)
    })

# 风险评估结果
if 'risk_result' not in st.session_state:
    st.session_state.risk_result = (
        "极高危",
        "#ff4b4b",
        "近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。"
    )

# 体检报告数据（支持历史对比）
if 'physical_reports' not in st.session_state:
    # 初始化两份模拟报告
    report1 = pd.DataFrame({
        "指标名称": ["收缩压", "舒张压", "总胆固醇", "甘油三酯", "空腹血糖", "心率", "肌酸激酶", "低密度脂蛋白", "同型半胱氨酸"],
        "检测结果": ["128mmHg", "82mmHg", "5.1mmol/L", "1.6mmol/L", "5.2mmol/L", "76次/分", "165U/L", "3.1mmol/L", "11μmol/L"],
        "参考范围": ["90-140mmHg", "60-90mmHg", "2.8-5.2mmol/L", "0.45-1.7mmol/L", "3.9-6.1mmol/L", "60-100次/分", "25-200U/L", "0-3.4mmol/L", "0-15μmol/L"],
        "异常标识": ["正常", "正常", "正常", "正常", "正常", "正常", "正常", "正常", "正常"],
        "报告日期": ["2026-01-15"]*9
    })
    
    report2 = pd.DataFrame({
        "指标名称": ["收缩压", "舒张压", "总胆固醇", "甘油三酯", "空腹血糖", "心率", "肌酸激酶", "低密度脂蛋白", "同型半胱氨酸"],
        "检测结果": ["138mmHg", "88mmHg", "5.9mmol/L", "2.4mmol/L", "5.7mmol/L", "84次/分", "192U/L", "3.8mmol/L", "16μmol/L"],
        "参考范围": ["90-140mmHg", "60-90mmHg", "2.8-5.2mmol/L", "0.45-1.7mmol/L", "3.9-6.1mmol/L", "60-100次/分", "25-200U/L", "0-3.4mmol/L", "0-15μmol/L"],
        "异常标识": ["正常", "正常", "↑", "↑", "正常", "正常", "正常", "↑", "↑"],
        "报告日期": ["2026-04-20"]*9
    })
    
    st.session_state.physical_reports = [report1, report2]
    st.session_state.current_report_idx = 1

# -------------------------- 风险预测核心函数 --------------------------
def predict_risk(health_data, user_info):
    recent_hr = health_data["静息心率"].tail(3).values
    recent_bp = health_data["收缩压"].tail(3).values
    has_family_history = "心脑血管" in user_info["family_history"]
    age = user_info["age"]
    lifestyle = user_info["lifestyle"]
    
    base_risk = 0
    risk_reason = ""
    
    if has_family_history:
        base_risk += 40
        risk_reason += "结合心脑血管家族史，遗传风险较高；"
    if np.mean(recent_bp) > 140:
        base_risk += 35
        risk_reason += "近3天收缩压持续高于140mmHg，血压昼夜节律异常；"
    elif np.mean(recent_bp) > 135:
        base_risk += 20
        risk_reason += "近期收缩压持续处于高位，存在血压异常风险；"
    if np.all(np.diff(recent_hr) > 0) and np.mean(recent_hr) > 80:
        base_risk += 20
        risk_reason += "近3天静息心率持续升高15%以上，心率变异性异常；"
    elif np.mean(recent_hr) > 80:
        base_risk += 10
        risk_reason += "近期静息心率持续高于80次/分，存在心血管异常信号；"
    if age >= 40:
        base_risk += 5
        risk_reason += "年龄超过40岁，心脑血管疾病发病风险升高；"
    if "熬夜" in lifestyle or "久坐" in lifestyle or "压力大" in lifestyle:
        base_risk += 5
        risk_reason += "不良生活习惯进一步提升风险；"
    
    health_score = 100 - base_risk
    health_score = max(30, min(95, health_score))
    
    if base_risk >= 60:
        risk_level = "极高危"
        color = "#ff4b4b"
        full_reason = f"{risk_reason}综合判定心源性猝死、隐匿性冠心病风险显著升高。"
    elif base_risk >= 40:
        risk_level = "中危"
        color = "#ff9800"
        full_reason = f"{risk_reason}存在隐匿性心血管异常风险，建议加强监测。"
    else:
        risk_level = "低危"
        color = "#00c853"
        full_reason = "当前健康指标平稳，无显著异常风险，继续保持良好生活习惯。"
    
    return risk_level, color, full_reason, health_score

# -------------------------- 异常指标高亮表格函数 --------------------------
def highlight_abnormal(row):
    if row["异常标识"] in ["↑", "↓"]:
        return ['color: #ff4b4b; font-weight: bold;'] * len(row)
    else:
        return [''] * len(row)

# -------------------------- 1. 系统首页 --------------------------
if page == "🏠 系统首页":
    st.markdown('<p class="main-title">🩺 预健·MED·AI 中青年急重症智能预警系统</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">基于多模态时序大数据与深度学习，实现急重症的早发现、早预警、早干预</p>', unsafe_allow_html=True)
    
    # 顶部核心指标看板
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("当前风险等级", st.session_state.risk_result[0], delta="需紧急关注" if st.session_state.risk_result[0] in ["极高危", "中危"] else "正常", delta_color="inverse")
        with col2:
            st.metric("覆盖并发症", "5大类28项")
        with col3:
            st.metric("数据更新时间", datetime.now().strftime("%Y-%m-%d"))
        with col4:
            st.metric("模型准确率", "93.2%")

    st.divider()
    
    # 主体内容区
    col_main1, col_main2 = st.columns([1, 2])
    
    # 模块1：用户健康档案
    with col_main1:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">👤 用户健康档案（可编辑）</p>', unsafe_allow_html=True)
            
            # 健康评分进度条
            health_score = st.session_state.user_data['health_score']
            st.progress(health_score/100, text=f"健康评分：{health_score}/100")
            st.divider()
            
            # 可编辑基础信息 - 修复了控件文字显示问题
            col_a, col_b = st.columns(2)
            with col_a:
                new_age = st.number_input("年龄", min_value=25, max_value=50, value=st.session_state.user_data['age'], step=1)
                new_gender = st.radio("性别", options=["男", "女"], index=0 if st.session_state.user_data['gender'] == "男" else 1, horizontal=True)
            with col_b:
                new_family_history = st.selectbox("家族史", options=["有心脑血管家族史", "无相关家族史"], index=0 if "有心脑血管" in st.session_state.user_data['family_history'] else 1)
                new_lifestyle = st.text_area("生活习惯", value=st.session_state.user_data['lifestyle'], height=80)
            
            # 实时同步
            st.session_state.user_data.update({
                "age": new_age, "gender": new_gender,
                "family_history": new_family_history, "lifestyle": new_lifestyle
            })
            
            st.divider()
            st.write("✅ 已同步数据维度：")
            col_c, col_d = st.columns(2)
            col_c.write("• 可穿戴设备数据")
            col_c.write("• 体检报告数据")
            col_d.write("• 居家检测数据")
            col_d.write("• 病史数据")
            st.divider()
            
            if st.button("🚀 启动AI深度风险评估", type="primary"):
                with st.spinner("正在融合多源健康数据，AI模型分析中..."):
                    time.sleep(2)
                    risk_level, color, reason, score = predict_risk(st.session_state.health_data, st.session_state.user_data)
                    st.session_state.risk_result = (risk_level, color, reason)
                    st.session_state.user_data['health_score'] = score
                    st.success("✅ 风险评估完成！")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 模块2：健康趋势
    with col_main2:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">📈 核心健康指标趋势（近14天）</p>', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["血压变化趋势", "心率变化趋势"])
            with tab1:
                st.line_chart(
                    st.session_state.health_data.set_index("日期")[["收缩压", "舒张压"]],
                    color=["#ff4b4b", "#ff9800"],
                    height=300
                )
                st.caption("* 红色为收缩压，橙色为舒张压，正常参考值：90-140/60-90 mmHg")
            with tab2:
                st.line_chart(
                    st.session_state.health_data.set_index("日期")[["静息心率", "夜间心率"]],
                    color=["#165DFF", "#7b61ff"],
                    height=300
                )
                st.caption("* 蓝色为日间静息心率，紫色为夜间静息心率，正常参考值：60-100 次/分")
            st.markdown('</div>', unsafe_allow_html=True)

    # 模块3：风险概览
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">⚠️ 当前健康风险概览</p>', unsafe_allow_html=True)
        risk_level, color, reason = st.session_state.risk_result
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.markdown(f"<h2 style='text-align: center; color: {color}; font-weight: bold; font-size: 2.5rem;'>{risk_level}</h2>", unsafe_allow_html=True)
            risk_index = 85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15
            st.progress(risk_index/100)
            st.caption(f"风险指数：{risk_index}/100")
        with col_b:
            st.warning(reason)
            st.info("💡 提示：可点击左侧导航栏「风险预警中心」查看完整就医指导与干预方案")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 2. 实时健康监测 --------------------------
elif page == "📡 实时健康监测":
    st.markdown('<p class="main-title">📡 实时健康数据动态监测中心</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">模拟可穿戴设备7×24小时实时采集，AI自动识别异常并触发分级报警</p>', unsafe_allow_html=True)

    # 模块1：实时数据看板
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        hr_placeholder = col1.empty()
        bp_placeholder = col2.empty()
        spo2_placeholder = col3.empty()
        status_placeholder = col4.empty()

        hr_placeholder.metric("实时心率", "75 次/分", delta="正常", delta_color="off")
        bp_placeholder.metric("实时收缩压", "128 mmHg", delta="正常", delta_color="off")
        spo2_placeholder.metric("血氧饱和度", "98 %", delta="正常", delta_color="off")
        status_placeholder.markdown("<h3 style='color: #00c853; text-align: center;'>🟢 等待监测启动</h3>", unsafe_allow_html=True)

        chart_placeholder = st.empty()
        alert_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # 模块2：监测控制
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        if st.button("▶️ 启动实时监测", type="primary"):
            realtime_history = pd.DataFrame({"时间": [], "实时心率": [], "收缩压": [], "血氧饱和度": []})

            for i in range(60):
                if i < 30:
                    new_hr = np.random.randint(72, 78)
                    new_bp_s = np.random.randint(125, 132)
                    new_spo2 = round(np.random.uniform(97, 99), 1)
                    is_abnormal = False
                else:
                    new_hr = np.random.randint(95, 110)
                    new_bp_s = np.random.randint(145, 160)
                    new_spo2 = round(np.random.uniform(93, 95), 1)
                    is_abnormal = True

                new_row = pd.DataFrame({
                    "时间": [datetime.now().strftime("%H:%M:%S")],
                    "实时心率": [new_hr],
                    "收缩压": [new_bp_s],
                    "血氧饱和度": [new_spo2]
                })
                realtime_history = pd.concat([realtime_history, new_row], ignore_index=True).tail(20)

                hr_placeholder.metric("实时心率", f"{new_hr} 次/分", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                bp_placeholder.metric("实时收缩压", f"{new_bp_s} mmHg", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                spo2_placeholder.metric("血氧饱和度", f"{new_spo2} %", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                
                if is_abnormal:
                    status_placeholder.markdown("<h3 style='color: #ff4b4b; text-align: center;'>🔴 异常报警</h3>", unsafe_allow_html=True)
                    alert_placeholder.error("⚠️ 检测到心率、血压持续异常升高！已自动记录异常数据，建议立即停止活动，休息后复测，持续不适请立即就医！")
                else:
                    status_placeholder.markdown("<h3 style='color: #00c853; text-align: center;'>🟢 监测正常</h3>", unsafe_allow_html=True)
                    alert_placeholder.empty()

                chart_placeholder.line_chart(realtime_history.set_index("时间"), color=["#165DFF", "#ff4b4b", "#7b61ff"], height=320)
                time.sleep(0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    # 模块3：功能说明
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">📌 功能说明</p>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.write("**📡 实时采集**")
            st.caption("模拟智能可穿戴设备，每秒采集心率、血压、血氧核心生命体征数据")
        with col_b:
            st.write("**🤖 AI异常识别**")
            st.caption("基于训练好的深度学习模型，自动识别指标异常波动与趋势变化")
        with col_c:
            st.write("**🚨 分级报警**")
            st.caption("针对不同风险等级，触发对应级别的报警与干预建议，避免漏报误报")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 3. 数据同步中心 --------------------------
elif page == "📊 数据同步中心":
    st.markdown('<p class="main-title">📊 多源健康数据同步中心</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">打通可穿戴设备、体检报告、居家检测全维度数据，打破健康数据孤岛</p>', unsafe_allow_html=True)
    
    # 上排：三个核心同步模块
    col1, col2, col3 = st.columns(3)
    
    # 模块1：可穿戴设备同步
    with col1:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title"><span style="color: #165DFF;">⌚</span> 可穿戴设备同步</p>', unsafe_allow_html=True)
            st.write("**已支持设备品牌**")
            st.caption("✅ 苹果Apple Watch | ✅ 华为Watch\n✅ 小米手环 | ✅ OPPO Watch\n✅ 荣耀手环 | ✅ 华米Amazfit")
            st.divider()

            device_brand = st.selectbox("选择你的设备品牌", ["请选择", "苹果Apple", "华为Huawei", "小米Xiaomi", "OPPO", "荣耀", "其他"])
            if device_brand != "请选择":
                if st.button(f"🔗 授权绑定{device_brand}设备", key="wearable_bind"):
                    with st.spinner(f"正在跳转{device_brand}开放平台授权页面..."):
                        time.sleep(1.5)
                        st.success(f"✅ {device_brand}账号授权成功！")
                        st.info("请上传从设备APP导出的健康时序数据CSV文件，完成数据同步")

            st.divider()
            st.write("**设备健康数据同步**")
            wearable_file = st.file_uploader("上传设备导出的CSV健康数据", type=["csv"], key="wearable_file", label_visibility="collapsed")
            
            if wearable_file is not None:
                with st.spinner("正在解析数据、同步至健康模型..."):
                    time.sleep(2)
                    user_wearable_data = pd.read_csv(wearable_file)
                    st.session_state.health_data = user_wearable_data
                    risk_level, color, reason, score = predict_risk(st.session_state.health_data, st.session_state.user_data)
                    st.session_state.risk_result = (risk_level, color, reason)
                    st.session_state.user_data['health_score'] = score
                    st.success("✅ 数据同步完成！已更新至AI风险模型")

            st.divider()
            st.write("**当前同步状态**")
            st.progress(1.0, text="已完成全量数据同步")
            st.caption(f"已同步{len(st.session_state.health_data)}天健康时序数据")
            st.markdown('</div>', unsafe_allow_html=True)

    # 模块2：体检报告智能解析
    with col2:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title"><span style="color: #7b61ff;">📄</span> 体检报告智能解析</p>', unsafe_allow_html=True)
            st.write("**支持格式**：PDF、JPG、PNG图片")
            st.write("**支持机构**：全国90%以上体检机构、公立医院体检中心")
            st.divider()

            # 统计数据
            col_a, col_b = st.columns(2)
            col_a.metric("累计解析报告", f"{len(st.session_state.physical_reports)}份")
            col_b.metric("提取核心指标", f"{len(st.session_state.physical_reports[-1])}项")
            st.divider()
            st.write("**OCR识别准确率**")
            st.progress(0.98, text="98%")
            st.divider()

            # 上传按钮
            uploaded_file = st.file_uploader("上传新的体检报告", type=["pdf", "png", "jpg"], label_visibility="collapsed")
            
            if uploaded_file is not None:
                with st.spinner("正在执行OCR文字识别→核心指标提取→异常值标注→数据同步至风险模型..."):
                    time.sleep(3)
                    # 生成新的模拟报告
                    new_report = pd.DataFrame({
                        "指标名称": ["收缩压", "舒张压", "总胆固醇", "甘油三酯", "空腹血糖", "心率", "肌酸激酶", "低密度脂蛋白", "同型半胱氨酸"],
                        "检测结果": [
                            f"{np.random.randint(130, 150)}mmHg",
                            f"{np.random.randint(80, 95)}mmHg",
                            f"{round(np.random.uniform(5.1, 6.2), 1)}mmol/L",
                            f"{round(np.random.uniform(1.8, 2.8), 1)}mmol/L",
                            f"{round(np.random.uniform(5.2, 6.0), 1)}mmol/L",
                            f"{np.random.randint(78, 90)}次/分",
                            f"{np.random.randint(160, 220)}U/L",
                            f"{round(np.random.uniform(3.2, 4.1), 1)}mmol/L",
                            f"{np.random.randint(12, 18)}μmol/L"
                        ],
                        "参考范围": [
                            "90-140mmHg", "60-90mmHg", "2.8-5.2mmol/L", "0.45-1.7mmol/L",
                            "3.9-6.1mmol/L", "60-100次/分", "25-200U/L", "0-3.4mmol/L", "0-15μmol/L"
                        ],
                        "异常标识": [
                            "正常" if np.random.randint(0,2) == 0 else "↑",
                            "正常" if np.random.randint(0,2) == 0 else "↑",
                            "↑", "↑",
                            "正常" if np.random.randint(0,2) == 0 else "↑",
                            "正常" if np.random.randint(0,2) == 0 else "↑",
                            "正常" if np.random.randint(0,2) == 0 else "↑",
                            "↑", "↑"
                        ],
                        "报告日期": [datetime.now().strftime("%Y-%m-%d")]*9
                    })
                    st.session_state.physical_reports.append(new_report)
                    st.session_state.current_report_idx = len(st.session_state.physical_reports) - 1
                    
                    # 联动风险模型
                    new_systolic = int(new_report.loc[new_report['指标名称'] == '收缩压', '检测结果'].values[0].replace('mmHg', ''))
                    new_hr = int(new_report.loc[new_report['指标名称'] == '心率', '检测结果'].values[0].replace('次/分', ''))
                    latest_dates = st.session_state.health_data.tail(3).index
                    st.session_state.health_data.loc[latest_dates, '收缩压'] = new_systolic + np.random.randint(-5, 5, 3)
                    st.session_state.health_data.loc[latest_dates, '静息心率'] = new_hr + np.random.randint(-3, 3, 3)
                    
                    risk_level, color, reason, score = predict_risk(st.session_state.health_data, st.session_state.user_data)
                    st.session_state.risk_result = (risk_level, color, reason)
                    st.session_state.user_data['health_score'] = score
                    
                    st.success("✅ 报告解析完成！已提取核心健康指标，同步更新至AI风险模型")
            st.markdown('</div>', unsafe_allow_html=True)

    # 模块3：居家检测数据录入
    with col3:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title"><span style="color: #00c853;">🏠</span> 居家检测数据录入</p>', unsafe_allow_html=True)
            st.write("**支持录入指标**：血压、血糖、心率、尿酸、体重")
            st.write("**数据用途**：补充日常监测数据，优化风险预测精度")
            st.divider()

            col_a, col_b = st.columns(2)
            col_a.metric("今日已录入", "3条")
            col_b.metric("连续录入天数", "7天")
            st.divider()
            st.write("**本月录入完成率**")
            st.progress(0.7, text="70%")
            st.divider()

            new_bp_s = st.number_input("今日收缩压（mmHg）", min_value=80, max_value=200, value=135)
            new_bp_d = st.number_input("今日舒张压（mmHg）", min_value=50, max_value=120, value=88)
            new_hr = st.number_input("今日静息心率（次/分）", min_value=50, max_value=120, value=84)
            if st.button("💾 保存今日数据", key="home"):
                st.success("✅ 数据已保存！已同步更新至风险预测模型")
            st.markdown('</div>', unsafe_allow_html=True)

    # 模块4：体检报告深度分析
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">📋 体检报告深度分析中心</p>', unsafe_allow_html=True)
        
        # 三个核心Tab
        tab1, tab2, tab3 = st.tabs(["📄 最新报告详情", "📊 历史报告对比", "💡 异常指标解读"])
        
        # Tab1：最新报告详情（异常高亮）
        with tab1:
            current_report = st.session_state.physical_reports[st.session_state.current_report_idx]
            st.write(f"**报告日期**：{current_report['报告日期'].iloc[0]}")
            st.dataframe(
                current_report[["指标名称", "检测结果", "参考范围", "异常标识"]].style.apply(highlight_abnormal, axis=1),
                use_container_width=True,
                hide_index=True
            )
        
        # Tab2：历史报告对比
        with tab2:
            if len(st.session_state.physical_reports) >= 2:
                st.write("**选择两份报告进行对比**")
                col_comp1, col_comp2 = st.columns(2)
                report_idx1 = col_comp1.selectbox("选择第一份报告", range(len(st.session_state.physical_reports)), format_func=lambda x: f"报告 {x+1} ({st.session_state.physical_reports[x]['报告日期'].iloc[0]})", index=0)
                report_idx2 = col_comp2.selectbox("选择第二份报告", range(len(st.session_state.physical_reports)), format_func=lambda x: f"报告 {x+1} ({st.session_state.physical_reports[x]['报告日期'].iloc[0]})", index=len(st.session_state.physical_reports)-1)
                
                if report_idx1 != report_idx2:
                    report1 = st.session_state.physical_reports[report_idx1]
                    report2 = st.session_state.physical_reports[report_idx2]
                    
                    # 合并对比
                    compare_df = pd.merge(
                        report1[["指标名称", "检测结果"]],
                        report2[["指标名称", "检测结果", "异常标识"]],
                        on="指标名称",
                        suffixes=(f" ({report1['报告日期'].iloc[0]})", f" ({report2['报告日期'].iloc[0]})")
                    )
                    st.dataframe(
                        compare_df.style.apply(highlight_abnormal, axis=1),
                        use_container_width=True,
                        hide_index=True
                    )
                    st.caption("* 红色加粗为异常指标，可直观看到指标变化趋势")
                else:
                    st.info("请选择两份不同的报告进行对比")
            else:
                st.info("当前只有一份报告，上传新报告后可进行历史对比")
        
        # Tab3：异常指标智能解读
        with tab3:
            current_report = st.session_state.physical_reports[st.session_state.current_report_idx]
            abnormal_items = current_report[current_report["异常标识"].isin(["↑", "↓"])]
            
            if len(abnormal_items) > 0:
                st.warning(f"⚠️ 本次体检共发现 {len(abnormal_items)} 项异常指标，以下是专业解读与建议：")
                st.divider()
                for _, row in abnormal_items.iterrows():
                    item_name = row["指标名称"]
                    abnormal_flag = row["异常标识"]
                    result = row["检测结果"]
                    ref_range = row["参考范围"]
                    
                    # 查找解读建议
                    advice = ABNORMAL_ADVICE.get(item_name, {}).get(abnormal_flag, "建议携带报告前往医院相关科室咨询专业医生。")
                    
                    # 每个异常指标一个独立的小卡片
                    with st.container():
                        st.markdown(f"""
                        <div style="background: rgba(255,75,75,0.05); border: 1px solid rgba(255,75,75,0.2); border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                            <h4 style="color: #ff4b4b; margin-bottom: 0.5rem;">🔴 {item_name} {abnormal_flag}</h4>
                            <p style="margin-bottom: 0.3rem;"><strong>检测结果：</strong>{result}（参考范围：{ref_range}）</p>
                            <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">{advice}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("✅ 本次体检未发现异常指标，继续保持良好的生活习惯！")
        
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 4. 风险预警中心 --------------------------
elif page == "⚠️ 风险预警中心":
    st.markdown('<p class="main-title">⚠️ 隐匿性急重症智能风险预警报告</p>', unsafe_allow_html=True)
    
    risk_level, color, reason = st.session_state.risk_result
    user_data = st.session_state.user_data

    # 模块1：风险评级
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">🎯 最终风险评级</p>', unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: {color}; font-weight: bold; font-size: 3rem;'>{risk_level}</h1>", unsafe_allow_html=True)
            risk_index = 85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15
            st.progress(risk_index/100)
            st.caption(f"风险指数：{risk_index}/100")
            st.divider()
            st.metric("预警时间", datetime.now().strftime("%Y-%m-%d %H:%M"))
            st.metric("覆盖并发症", "5大类28项")
            st.metric("模型置信度", "92.5%")
            st.divider()
            st.write("**风险等级说明**：")
            st.caption("🔴 极高危：需3天内紧急就医")
            st.caption("🟠 中危：需2周内就医复诊")
            st.caption("🟢 低危：常规健康维护即可")
            st.markdown('</div>', unsafe_allow_html=True)

    # 模块2：风险分析
    with col2:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">🔍 风险来源深度分析</p>', unsafe_allow_html=True)
            st.warning(reason)
            st.divider()
            st.write("**核心异常指标明细（近3天）**：")
            st.dataframe(
                st.session_state.health_data.tail(3)[["日期", "静息心率", "夜间心率", "收缩压", "舒张压"]],
                use_container_width=True,
                hide_index=True
            )
            st.divider()
            st.write("**风险权重占比**")
            family_weight = 40 if "有心脑血管" in user_data["family_history"] else 10
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("家族史", f"{family_weight}%")
            col_b.metric("血压异常", "35%")
            col_c.metric("心率异常", "20%")
            col_d.metric("生活习惯", "5%")
            st.bar_chart(
                pd.DataFrame({
                    "风险维度": ["家族史", "血压", "心率", "生活习惯", "既往病史"],
                    "风险值": [family_weight, 80, 75, 60, 30]
                }).set_index("风险维度"),
                color="#ff4b4b",
                height=200
            )
            st.markdown('</div>', unsafe_allow_html=True)

    # 模块3：就医指导
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">🏥 精准就医指导与干预建议</p>', unsafe_allow_html=True)
        if risk_level == "极高危":
            st.error("⚠️ 【极高危紧急响应】请立即启动以下流程：")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**1. 紧急就医建议**")
                st.caption("请于3天内前往三级医院心内科就诊，避免高强度活动、情绪激动，如有胸痛、胸闷立即拨打120")
                st.write("**2. 推荐检查项目**")
                st.caption("必查：24小时动态心电图、冠脉CTA、心肌酶谱、心脏超声、血脂全套")
                st.caption("可选：冠脉造影、运动负荷试验")
            with col_b:
                st.write("**3. 临时干预措施**")
                st.caption("立即停止熬夜、高强度工作，每日早中晚3次监测血压心率，保持情绪平稳，禁止剧烈运动")
                st.write("**4. 随访提醒**")
                st.caption("系统已自动生成7天后的复查提醒，就诊后可上传病历更新风险模型，重新评估风险等级")
        elif risk_level == "中危":
            st.warning("【中危风险响应】请启动以下干预流程：")
            st.write("1. **就医建议**：请于1-2周内前往社区卫生服务中心或医院心内科复诊；")
            st.write("2. **推荐检查项目**：常规心电图、血压监测、血脂、血糖检测；")
            st.write("3. **干预措施**：调整作息，保证7小时睡眠，每日30分钟有氧运动，低盐饮食；")
            st.write("4. **监测要求**：每日上传居家血压心率数据，每周重新评估风险等级。")
        else:
            st.success("【低风险健康维护】")
            st.write("保持当前良好的生活习惯，每月上传1-2次居家检测数据，每季度进行一次全面风险评估，按年度完成常规体检。")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 5. 健康管理中心 --------------------------
elif page == "💊 健康管理中心":
    st.markdown('<p class="main-title">💊 个性化主动健康管理方案</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    # 模块1：随访计划
    with col1:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">📅 个性化随访计划</p>', unsafe_allow_html=True)
            st.progress(0.2, text="本周完成进度：1/5")
            st.divider()
            st.write("✅ **今日待完成**：测量血压心率并上传系统")
            st.write("⏰ **明日提醒**：心内科就诊预约")
            st.write("📅 **7天后**：就诊后复查提醒+风险重评估")
            st.write("📅 **14天后**：第二次风险等级复核")
            st.write("📅 **30天后**：全面健康评估+方案调整")
            st.divider()
            st.write("**随访打卡日历**：")
            col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns(7)
            col_a.write("一\n✅")
            col_b.write("二\n⭕")
            col_c.write("三\n⭕")
            col_d.write("四\n⭕")
            col_e.write("五\n⭕")
            col_f.write("六\n⭕")
            col_g.write("日\n⭕")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 模块2：健康科普
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">📚 今日健康科普</p>', unsafe_allow_html=True)
            st.info("【心源性猝死的3个早期隐匿信号】\n1. 不明原因的持续疲劳乏力，休息后无法缓解；\n2. 夜间静息心率持续升高超过10%，波动幅度大；\n3. 活动后胸闷气短加重，伴随左肩、后背放射性疼痛。")
            st.divider()
            st.write("**权威参考指南**：")
            st.caption("• 《中国心源性猝死防治指南2024》")
            st.caption("• 《中青年高血压管理专家共识》")
            st.markdown('</div>', unsafe_allow_html=True)

    # 模块3：干预方案
    with col2:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">🥗 个体化生活方式干预方案</p>', unsafe_allow_html=True)
            st.divider()
            st.write("**作息调整**")
            st.caption("每日23:00前入睡，保证7.5小时睡眠，禁止熬夜，午间可休息20-30分钟")
            st.write("**运动建议**")
            st.caption("每日进行30分钟中等强度有氧运动（快走、慢跑、游泳、骑行），避免高强度剧烈运动，每周至少5天")
            st.write("**饮食调整**")
            st.caption("每日钠盐摄入不超过5g，减少高脂、高糖、高嘌呤食物，增加新鲜蔬果、优质蛋白、膳食纤维摄入，每日饮水1500-2000ml")
            st.write("**压力管理**")
            st.caption("每日进行10分钟冥想放松训练，减少连续工作时长，每工作1小时休息10分钟，避免长期精神紧张")
            st.write("**烟酒控制**")
            st.caption("禁止吸烟，限制酒精摄入，每周饮酒不超过1次，男性每日酒精摄入不超过25g，女性不超过15g")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 模块4：提醒设置
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">🔔 用药与复查提醒</p>', unsafe_allow_html=True)
            st.divider()
            st.write("**每日提醒**：早8点、晚8点测量血压心率并上传系统")
            st.write("**复查提醒**：2026-XX-XX 心内科就诊，完善24小时动态心电图、冠脉CTA检查")
            st.write("**体检提醒**：2026-XX-XX 年度全面体检，重点关注心血管、血脂、血糖相关指标")
            st.divider()
            if st.button("开启微信提醒"):
                st.success("✅ 微信提醒已开启，将按时推送提醒消息")
            st.markdown('</div>', unsafe_allow_html=True)

    # 模块5：方案说明
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.info("📌 方案说明：本管理方案基于您的风险等级、健康数据、生活习惯，由AI模型自动生成，会根据您每日上传的监测数据动态调整，实现全周期闭环健康管理；所有建议均参考《中国心血管病防治指南》制定，仅供参考，具体诊疗请遵医嘱。")
        st.markdown('</div>', unsafe_allow_html=True)
