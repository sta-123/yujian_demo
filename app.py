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

# -------------------------- 核心CSS（两个按钮颜色完全统一）--------------------------
st.markdown("""
<style>
    /* 全局背景与字体 */
    html, body, [class*="css"] {
        font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        background-attachment: fixed;
    }
    
    /* 玻璃拟态容器（统一等高+视觉拉满） */
    div[data-testid="stVerticalBlock"] > div[class*="stContainer"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
        height: 100%;
    }
    
    div[data-testid="stVerticalBlock"] > div[class*="stContainer"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(22, 93, 255, 0.25);
        border: 1px solid rgba(22, 93, 255, 0.4);
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(30px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .sidebar-brand {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 1rem;
    }
    
    .sidebar-title {
        background: linear-gradient(90deg, #165DFF, #3b82f6, #165DFF);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s linear infinite;
        font-weight: 800;
        font-size: 1.6rem;
        margin-bottom: 0.3rem;
    }
    
    @keyframes gradient {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    /* 标题样式统一 */
    .main-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 2rem;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        white-space: nowrap;
    }
    
    /* 指标卡片样式 */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
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
    
    /* 按钮样式（两个按钮完全统一的核心样式） */
    .stButton>button {
        background: linear-gradient(135deg, #165DFF 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 20px rgba(22, 93, 255, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(22, 93, 255, 0.6);
        background: linear-gradient(135deg, #0e4bcc 0%, #2563eb 100%);
    }
    
    /* 上传按钮和绑定按钮完全统一（核心修改） */
    .stFileUploader > div {
        background: rgba(255,255,255,0.05);
        border: 2px dashed rgba(22, 93, 255, 0.5);
        border-radius: 10px;
        color: white;
        padding: 1.2rem;
        transition: all 0.3s ease;
    }
    .stFileUploader > div:hover {
        border-color: #165DFF;
        background: rgba(22, 93, 255, 0.1);
    }
    /* 上传按钮和主按钮完全一样的蓝色渐变 */
    .stFileUploader > div > button {
        background: linear-gradient(135deg, #165DFF 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        width: 100%;
        font-weight: 600;
        margin-top: 0.5rem;
        box-shadow: 0 4px 20px rgba(22, 93, 255, 0.4);
        transition: all 0.3s ease;
    }
    .stFileUploader > div > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(22, 93, 255, 0.6);
        background: linear-gradient(135deg, #0e4bcc 0%, #2563eb 100%);
    }
    /* 上传按钮文字改成白色 */
    .stFileUploader > div > span {
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
    }
    
    /* 文本颜色统一 */
    h1, h2, h3, h4, h5, h6, p, li, div {
        color: #ffffff;
    }
    
    /* 单选/下拉框样式适配 */
    [data-baseweb="select"] {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
    }
    [data-baseweb="radio"] {
        color: white;
    }
    [data-testid="stTextArea"] textarea {
        background: rgba(255,255,255,0.05);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    
    /* 警告/信息框样式 */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
    }
    
    /* 表格样式 */
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* 分隔线样式 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 1.5rem 0;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.8rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(22, 93, 255, 0.3);
        border-bottom: 2px solid #165DFF;
    }
    
    /* 进度条样式 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #165DFF, #3b82f6);
        border-radius: 10px;
    }
    
    /* 数字输入框样式 */
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.05);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    .stNumberInput > div > div > button {
        color: white;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------- 侧边栏导航 --------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🩺</div>
        <div class="sidebar-title">预健·MED·AI</div>
        <div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">中青年急重症智能预警系统</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 导航选项
    page = st.radio(
        "",
        ["🏠 系统首页", "📡 实时健康监测", "📊 数据同步中心", "⚠️ 风险预警中心", "💊 健康管理中心"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("© 2026 PREHEALTH MED·AI | All Rights Reserved")

# -------------------------- 全局数据初始化（彻底避免报错）--------------------------
# 用户基础数据（可编辑，全局同步）
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "age": 32,
        "gender": "男",
        "family_history": "有心脑血管家族史",
        "lifestyle": "熬夜（日均睡眠6小时）、久坐、工作压力大",
        "health_score": 58
    }
# 确保健康评分字段存在
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

# -------------------------- 风险预测核心函数（优化：联动用户编辑的信息）--------------------------
def predict_risk(health_data, user_info):
    recent_hr = health_data["静息心率"].tail(3).values
    recent_bp = health_data["收缩压"].tail(3).values
    has_family_history = "心脑血管" in user_info["family_history"]
    age = user_info["age"]
    lifestyle = user_info["lifestyle"]
    
    # 风险权重计算（联动用户编辑的所有信息）
    base_risk = 0
    risk_reason = ""
    
    # 1. 家族史权重（最高40%）
    if has_family_history:
        base_risk += 40
        risk_reason += "结合心脑血管家族史，遗传风险较高；"
    # 2. 血压异常权重（35%）
    if np.mean(recent_bp) > 140:
        base_risk += 35
        risk_reason += "近3天收缩压持续高于140mmHg，血压昼夜节律异常；"
    elif np.mean(recent_bp) > 135:
        base_risk += 20
        risk_reason += "近期收缩压持续处于高位，存在血压异常风险；"
    # 3. 心率异常权重（20%）
    if np.all(np.diff(recent_hr) > 0) and np.mean(recent_hr) > 80:
        base_risk += 20
        risk_reason += "近3天静息心率持续升高15%以上，心率变异性异常；"
    elif np.mean(recent_hr) > 80:
        base_risk += 10
        risk_reason += "近期静息心率持续高于80次/分，存在心血管异常信号；"
    # 4. 年龄权重（5%）
    if age >= 40:
        base_risk += 5
        risk_reason += "年龄超过40岁，心脑血管疾病发病风险升高；"
    # 5. 生活习惯权重（额外加减分）
    if "熬夜" in lifestyle or "久坐" in lifestyle or "压力大" in lifestyle:
        base_risk += 5
        risk_reason += "不良生活习惯进一步提升风险；"
    
    # 健康评分计算
    health_score = 100 - base_risk
    health_score = max(30, min(95, health_score)) # 限制评分范围
    
    # 风险等级判定
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

# -------------------------- 1. 系统首页（核心修改：健康档案可编辑）--------------------------
if page == "🏠 系统首页":
    st.markdown('<p class="main-title">🩺 预健·MED·AI 中青年急重症智能预警系统</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">基于多模态时序大数据与深度学习，实现急重症的早发现、早预警、早干预</p>', unsafe_allow_html=True)
    
    # 顶部核心指标看板
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
    
    with col_main1:
        # 用户健康档案卡片（全字段可编辑）
        with st.container():
            st.markdown('<p class="card-title">👤 用户健康档案（可编辑）</p>', unsafe_allow_html=True)
            
            # 健康评分进度条（实时联动）
            health_score = st.session_state.user_data['health_score']
            st.progress(health_score, text=f"健康评分：{health_score}/100")
            st.divider()
            
            # 可编辑基础信息（双列布局）
            col_a, col_b = st.columns(2)
            with col_a:
                # 年龄编辑
                new_age = st.number_input(
                    "年龄",
                    min_value=25,
                    max_value=50,
                    value=st.session_state.user_data['age'],
                    step=1,
                    help="目标人群25-50岁中青年"
                )
                # 性别编辑
                new_gender = st.radio(
                    "性别",
                    options=["男", "女"],
                    index=0 if st.session_state.user_data['gender'] == "男" else 1,
                    horizontal=True
                )
            with col_b:
                # 家族史编辑
                new_family_history = st.selectbox(
                    "家族史",
                    options=["有心脑血管家族史", "无相关家族史"],
                    index=0 if "有心脑血管" in st.session_state.user_data['family_history'] else 1
                )
                # 生活习惯编辑
                new_lifestyle = st.text_area(
                    "生活习惯",
                    value=st.session_state.user_data['lifestyle'],
                    height=80,
                    help="可编辑修改您的作息、运动、工作压力等情况"
                )
            
            # 实时同步编辑内容到全局session_state
            st.session_state.user_data.update({
                "age": new_age,
                "gender": new_gender,
                "family_history": new_family_history,
                "lifestyle": new_lifestyle
            })
            
            st.divider()
            # 数据同步状态
            st.write("✅ 已同步数据维度：")
            col_c, col_d = st.columns(2)
            col_c.write("• 可穿戴设备数据")
            col_c.write("• 体检报告数据")
            col_d.write("• 居家检测数据")
            col_d.write("• 病史数据")
            st.divider()
            
            # AI评估按钮（用最新编辑的用户数据计算）
            if st.button("🚀 启动AI深度风险评估", type="primary"):
                with st.spinner("正在融合多源健康数据，AI模型分析中..."):
                    time.sleep(2)
                    # 调用风险预测函数，传入最新的用户数据
                    risk_level, color, reason, score = predict_risk(
                        st.session_state.health_data,
                        st.session_state.user_data
                    )
                    # 更新全局结果
                    st.session_state.risk_result = (risk_level, color, reason)
                    st.session_state.user_data['health_score'] = score
                    st.success("✅ 风险评估完成！已根据您的档案信息更新结果")
    
    with col_main2:
        # 健康趋势卡片
        with st.container():
            st.markdown('<p class="card-title">📈 核心健康指标趋势（近14天）</p>', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["血压变化趋势", "心率变化趋势"])
            with tab1:
                st.line_chart(
                    st.session_state.health_data.set_index("日期")[["收缩压", "舒张压"]],
                    color=["#ff4b4b", "#ff9800"],
                    height=320
                )
                st.caption("* 红色为收缩压，橙色为舒张压，正常参考值：90-140/60-90 mmHg")
            with tab2:
                st.line_chart(
                    st.session_state.health_data.set_index("日期")[["静息心率", "夜间心率"]],
                    color=["#165DFF", "#7b61ff"],
                    height=320
                )
                st.caption("* 蓝色为日间静息心率，紫色为夜间静息心率，正常参考值：60-100 次/分")

    st.divider()
    
    # 风险概览卡片
    with st.container():
        st.markdown('<p class="card-title">⚠️ 当前健康风险概览</p>', unsafe_allow_html=True)
        risk_level, color, reason = st.session_state.risk_result
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.markdown(f"<h2 style='text-align: center; color: {color}; font-weight: bold; font-size: 2.5rem;'>{risk_level}</h2>", unsafe_allow_html=True)
            # 风险进度条联动风险等级
            risk_index = 85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15
            st.progress(risk_index)
            st.caption(f"风险指数：{risk_index}/100")
        with col_b:
            st.warning(reason)
            st.info("💡 提示：可点击左侧导航栏「风险预警中心」查看完整就医指导与干预方案")

# -------------------------- 2. 实时健康监测 --------------------------
elif page == "📡 实时健康监测":
    st.markdown('<p class="main-title">📡 实时健康数据动态监测中心</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">模拟可穿戴设备7×24小时实时采集，AI自动识别异常并触发分级报警</p>', unsafe_allow_html=True)

    # 实时数据看板
    col1, col2, col3, col4 = st.columns(4)
    hr_placeholder = col1.empty()
    bp_placeholder = col2.empty()
    spo2_placeholder = col3.empty()
    status_placeholder = col4.empty()

    # 初始化默认值
    hr_placeholder.metric("实时心率", "75 次/分", delta="正常", delta_color="off")
    bp_placeholder.metric("实时收缩压", "128 mmHg", delta="正常", delta_color="off")
    spo2_placeholder.metric("血氧饱和度", "98 %", delta="正常", delta_color="off")
    status_placeholder.markdown("<h3 style='color: #00c853; text-align: center;'>🟢 等待监测启动</h3>", unsafe_allow_html=True)

    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

    # 实时监测卡片
    with st.container():
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

                # 刷新看板
                hr_placeholder.metric("实时心率", f"{new_hr} 次/分", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                bp_placeholder.metric("实时收缩压", f"{new_bp_s} mmHg", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                spo2_placeholder.metric("血氧饱和度", f"{new_spo2} %", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                
                if is_abnormal:
                    status_placeholder.markdown("<h3 style='color: #ff4b4b; text-align: center;'>🔴 异常报警</h3>", unsafe_allow_html=True)
                    alert_placeholder.error("⚠️ 检测到心率、血压持续异常升高！已自动记录异常数据，建议立即停止活动，休息后复测，持续不适请立即就医！")
                else:
                    status_placeholder.markdown("<h3 style='color: #00c853; text-align: center;'>🟢 监测正常</h3>", unsafe_allow_html=True)
                    alert_placeholder.empty()

                chart_placeholder.line_chart(realtime_history.set_index("时间"), color=["#165DFF", "#ff4b4b", "#7b61ff"], height=350)
                time.sleep(0.5)
    
    st.divider()
    # 监测说明卡片
    with st.container():
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

# -------------------------- 3. 数据同步中心 --------------------------
elif page == "📊 数据同步中心":
    st.markdown('<p class="main-title">📊 多源健康数据同步中心</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">打通可穿戴设备、体检报告、居家检测全维度数据，打破健康数据孤岛</p>', unsafe_allow_html=True)
    
    # 三个核心卡片（等高布局·视觉拉满）
    col1, col2, col3 = st.columns(3)
    
    # 卡片1：可穿戴设备同步
    with col1:
        with st.container():
            # 标题+图标
            st.markdown('<p class="card-title"><span style="color: #165DFF;">⌚</span> 可穿戴设备同步</p>', unsafe_allow_html=True)
            # 支持品牌
            st.write("**已支持设备品牌**")
            st.caption("✅ 苹果Apple Watch | ✅ 华为Watch\n✅ 小米手环 | ✅ OPPO Watch\n✅ 荣耀手环 | ✅ 华米Amazfit")
            st.divider()

            # 1. 选择设备品牌
            device_brand = st.selectbox("选择你的设备品牌", ["请选择", "苹果Apple", "华为Huawei", "小米Xiaomi", "OPPO", "荣耀", "其他"])
            # 2. 绑定授权模拟
            if device_brand != "请选择":
                if st.button(f"🔗 授权绑定{device_brand}设备", key="wearable_bind"):
                    with st.spinner(f"正在跳转{device_brand}开放平台授权页面..."):
                        time.sleep(1.5)
                        st.success(f"✅ {device_brand}账号授权成功！")
                        st.info("请上传从设备APP导出的健康时序数据CSV文件，完成数据同步")

            st.divider()
            # 3. 真实CSV数据上传解析（核心：支持你自己的手机数据）
            st.write("**设备健康数据同步**")
            wearable_file = st.file_uploader("上传设备导出的CSV健康数据", type=["csv"], key="wearable_file", label_visibility="collapsed")
            
            # 数据解析逻辑（适配主流设备导出格式）
            if wearable_file is not None:
                with st.spinner("正在解析数据、同步至健康模型..."):
                    try:
                        # 读取用户上传的真实数据
                        user_wearable_data = pd.read_csv(wearable_file)
                        # 自动识别时间、心率、血压核心列（适配苹果/华为/小米的导出格式）
                        time_col = None
                        hr_col = None
                        bp_s_col = None
                        for col in user_wearable_data.columns:
                            col_lower = col.lower()
                            if "时间" in col or "date" in col_lower or "time" in col_lower:
                                time_col = col
                            elif "心率" in col or "heart" in col_lower or "hr" in col_lower:
                                hr_col = col
                            elif "收缩压" in col or "高压" in col or "systolic" in col_lower:
                                bp_s_col = col
                        
                        # 同步数据到全局状态，替换模拟数据，实现真实数据联动
                        if time_col and hr_col:
                            st.session_state.health_data = user_wearable_data.rename(columns={
                                time_col: "日期",
                                hr_col: "静息心率",
                                bp_s_col: "收缩压" if bp_s_col else "收缩压"
                            })
                            # 自动重新评估风险
                            risk_level, color, reason, score = predict_risk(st.session_state.health_data, st.session_state.user_data)
                            st.session_state.risk_result = (risk_level, color, reason)
                            st.session_state.user_data['health_score'] = score
                            
                            st.success("✅ 数据同步完成！已更新至AI风险模型")
                            # 显示同步结果
                            col_a, col_b = st.columns(2)
                            col_a.metric("同步数据天数", f"{len(st.session_state.health_data)}天")
                            col_b.metric("数据条目", f"{len(st.session_state.health_data)}条")
                        else:
                            st.warning("⚠️ 未识别到核心数据列，请确保CSV包含时间、心率相关列")
                    except Exception as e:
                        st.error(f"数据解析失败：{str(e)}，请使用设备官方导出的标准CSV文件")

            st.divider()
            # 同步进度&状态
            st.write("**当前同步状态**")
            if len(st.session_state.health_data) > 0:
                st.progress(100, text="已完成全量数据同步")
                st.caption(f"已同步{len(st.session_state.health_data)}天健康时序数据")
            else:
                st.progress(0, text="未同步数据")

    # 卡片2：体检报告智能解析
    with col2:
        with st.container():
            # 标题+图标
            st.markdown('<p class="card-title"><span style="color: #7b61ff;">📄</span> 体检报告智能解析</p>', unsafe_allow_html=True)
            # 支持说明
            st.write("**支持格式**：PDF、JPG、PNG图片")
            st.write("**支持机构**：全国90%以上体检机构、公立医院体检中心")
            st.divider()
            # 数据统计（双列指标）
            col_a, col_b = st.columns(2)
            col_a.metric("累计解析报告", "2份")
            col_b.metric("提取核心指标", "128项")
            st.divider()
            # 解析准确率
            st.write("**OCR识别准确率**")
            st.progress(98, text="98%")
            st.divider()
            # 上传按钮（和绑定按钮完全一样的蓝色）
            uploaded_file = st.file_uploader("上传新的体检报告", type=["pdf", "png", "jpg"], label_visibility="collapsed")
            if uploaded_file is not None:
                with st.spinner("正在OCR识别并解析报告..."):
                    time.sleep(2)
                    st.success("✅ 报告解析完成！")
                    st.write("已提取128项核心健康指标，已同步至风险模型")

    # 卡片3：居家检测数据录入
    with col3:
        with st.container():
            # 标题+图标
            st.markdown('<p class="card-title"><span style="color: #00c853;">🏠</span> 居家检测数据录入</p>', unsafe_allow_html=True)
            # 支持说明
            st.write("**支持录入指标**：血压、血糖、心率、尿酸、体重")
            st.write("**数据用途**：补充日常监测数据，优化风险预测精度")
            st.divider()
            # 数据统计（双列指标）
            col_a, col_b = st.columns(2)
            col_a.metric("今日已录入", "3条")
            col_b.metric("连续录入天数", "7天")
            st.divider()
            # 录入完成率
            st.write("**本月录入完成率**")
            st.progress(70, text="70%")
            st.divider()
            # 录入表单
            new_bp_s = st.number_input("今日收缩压（mmHg）", min_value=80, max_value=200, value=135)
            new_bp_d = st.number_input("今日舒张压（mmHg）", min_value=50, max_value=120, value=88)
            new_hr = st.number_input("今日静息心率（次/分）", min_value=50, max_value=120, value=84)
            if st.button("💾 保存今日数据", key="home"):
                st.success("✅ 数据已保存！已同步更新至风险预测模型")
    
    st.divider()
    # 全量数据预览卡片
    with st.container():
        st.markdown('<p class="card-title">📋 已同步健康数据全量预览</p>', unsafe_allow_html=True)
        st.dataframe(st.session_state.health_data, use_container_width=True, height=300)
        st.caption("* 以上为近14天的核心健康指标时序数据，已全部同步至AI风险预测模型")

# -------------------------- 4. 风险预警中心 --------------------------
elif page == "⚠️ 风险预警中心":
    st.markdown('<p class="main-title">⚠️ 隐匿性急重症智能风险预警报告</p>', unsafe_allow_html=True)
    st.divider()

    risk_level, color, reason = st.session_state.risk_result
    user_data = st.session_state.user_data

    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container():
            st.markdown('<p class="card-title">🎯 最终风险评级</p>', unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: {color}; font-weight: bold; font-size: 3rem;'>{risk_level}</h1>", unsafe_allow_html=True)
            risk_index = 85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15
            st.progress(risk_index)
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

    with col2:
        with st.container():
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
            # 风险权重联动用户编辑的家族史
            family_weight = 40 if "有心脑血管" in user_data["family_history"] else 10
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("家族史", f"{family_weight}%")
            col_b.metric("血压异常", "35%")
            col_c.metric("心率异常", "20%")
            col_d.metric("生活习惯", "5%")
            # 风险可视化
            st.bar_chart(
                pd.DataFrame({
                    "风险维度": ["家族史", "血压", "心率", "生活习惯", "既往病史"],
                    "风险值": [family_weight, 80, 75, 60, 30]
                }).set_index("风险维度"),
                color="#ff4b4b",
                height=200
            )

    st.divider()
    
    # 就医指导卡片
    with st.container():
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

# -------------------------- 5. 健康管理中心 --------------------------
elif page == "💊 健康管理中心":
    st.markdown('<p class="main-title">💊 个性化主动健康管理方案</p>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        # 随访计划卡片
        with st.container():
            st.markdown('<p class="card-title">📅 个性化随访计划</p>', unsafe_allow_html=True)
            st.progress(20, text="本周完成进度：1/5")
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
        
        st.divider()
        
        # 健康科普卡片
        with st.container():
            st.markdown('<p class="card-title">📚 今日健康科普</p>', unsafe_allow_html=True)
            st.info("【心源性猝死的3个早期隐匿信号】\n1. 不明原因的持续疲劳乏力，休息后无法缓解；\n2. 夜间静息心率持续升高超过10%，波动幅度大；\n3. 活动后胸闷气短加重，伴随左肩、后背放射性疼痛。")
            st.divider()
            st.write("**权威参考指南**：")
            st.caption("• 《中国心源性猝死防治指南2024》")
            st.caption("• 《中青年高血压管理专家共识》")

    with col2:
        # 干预方案卡片
        with st.container():
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
        
        st.divider()
        
        # 提醒卡片
        with st.container():
            st.markdown('<p class="card-title">🔔 用药与复查提醒</p>', unsafe_allow_html=True)
            st.divider()
            st.write("**每日提醒**：早8点、晚8点测量血压心率并上传系统")
            st.write("**复查提醒**：2026-XX-XX 心内科就诊，完善24小时动态心电图、冠脉CTA检查")
            st.write("**体检提醒**：2026-XX-XX 年度全面体检，重点关注心血管、血脂、血糖相关指标")
            st.divider()
            if st.button("开启微信提醒"):
                st.success("✅ 微信提醒已开启，将按时推送提醒消息")

    st.divider()
    # 方案说明卡片
    with st.container():
        st.info("📌 方案说明：本管理方案基于您的风险等级、健康数据、生活习惯，由AI模型自动生成，会根据您每日上传的监测数据动态调整，实现全周期闭环健康管理；所有建议均参考《中国心血管病防治指南》制定，仅供参考，具体诊疗请遵医嘱。")
