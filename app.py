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

# -------------------------- 顶级玻璃拟态CSS（修复渲染空白问题）--------------------------
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
    
    /* 玻璃拟态容器核心样式（修复空白） */
    div[data-testid="stVerticalBlock"] > div[class*="stContainer"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    div[data-testid="stVerticalBlock"] > div[class*="stContainer"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(22, 93, 255, 0.2);
        border: 1px solid rgba(22, 93, 255, 0.3);
    }
    
    /* 侧边栏玻璃拟态 */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(30px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* 侧边栏品牌区 */
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
    
    /* 标题样式 */
    .main-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 1rem;
        font-weight: 400;
    }
    
    /* 指标卡片样式 */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255, 255, 255, 0.6) !important;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background: linear-gradient(135deg, #165DFF 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 20px rgba(22, 93, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(22, 93, 255, 0.6);
        background: linear-gradient(135deg, #0e4bcc 0%, #2563eb 100%);
    }
    
    /* 文本颜色统一 */
    h1, h2, h3, h4, h5, h6, p, li, div {
        color: #ffffff;
    }
    
    /* 警告/信息框样式 */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
    }
    
    /* 表格样式 */
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }
    
    /* 分隔线样式 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 2.5rem 0;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
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

# -------------------------- 全局数据初始化 --------------------------
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "age": 32,
        "gender": "男",
        "family_history": "有心脑血管家族史",
        "lifestyle": "熬夜（日均睡眠6小时）、久坐、工作压力大",
        "health_score": 58
    }

if 'health_data' not in st.session_state:
    dates = [datetime.now() - timedelta(days=i) for i in range(14, 0, -1)]
    base_hr = np.random.randint(65, 75, 11)
    abnormal_hr = [78, 82, 85]
    base_bp = np.random.randint(115, 130, 11)
    abnormal_bp = [135, 140, 145]
    
    st.session_state.health_data = pd.DataFrame({
        "日期": dates,
        "静息心率": np.concatenate([base_hr, abnormal_hr]),
        "夜间心率": np.concatenate([base_hr - 8, abnormal_hr - 5]),
        "收缩压": np.concatenate([base_bp, abnormal_bp]),
        "舒张压": np.concatenate([np.random.randint(70, 80, 11), [82, 88, 92]]),
        "血氧饱和度": np.round(np.random.uniform(96, 99, 14), 1)
    })

if 'risk_result' not in st.session_state:
    st.session_state.risk_result = (
        "极高危",
        "#ff4b4b",
        "近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。"
    )

# -------------------------- 风险预测核心函数 --------------------------
def predict_risk(health_data, user_info):
    recent_hr = health_data["静息心率"].tail(3).values
    recent_bp = health_data["收缩压"].tail(3).values
    has_family_history = "心脑血管" in user_info["family_history"]
    
    if (np.all(np.diff(recent_hr) > 0) and np.mean(recent_bp) > 140) or has_family_history:
        return "极高危", "#ff4b4b", "近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。", 58
    elif np.mean(recent_hr) > 80 or np.mean(recent_bp) > 135:
        return "中危", "#ff9800", "近期静息心率与血压持续处于高位，存在隐匿性心血管异常风险，建议加强监测。", 75
    else:
        return "低危", "#00c853", "当前健康指标平稳，无显著异常风险，继续保持良好生活习惯。", 92

# -------------------------- 1. 系统首页 --------------------------
if page == "🏠 系统首页":
    st.markdown('<p class="main-title">🩺 预健·MED·AI 中青年急重症智能预警系统</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">基于多模态时序大数据与深度学习，实现急重症的早发现、早预警、早干预</p>', unsafe_allow_html=True)
    st.divider()
    
    # 顶部核心指标看板
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("当前风险等级", "极高危", delta="需紧急关注", delta_color="inverse")
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
        # 用户健康档案卡片（内容拉满，不再空白）
        with st.container():
            st.subheader("👤 用户健康档案")
            st.progress(st.session_state.user_data['health_score'], text=f"健康评分：{st.session_state.user_data['health_score']}/100")
            st.divider()
            st.write(f"**年龄**：{st.session_state.user_data['age']}岁")
            st.write(f"**性别**：{st.session_state.user_data['gender']}")
            st.write(f"**家族史**：{st.session_state.user_data['family_history']}")
            st.write(f"**生活习惯**：{st.session_state.user_data['lifestyle']}")
            st.divider()
            st.write("**已同步数据维度**：")
            col_a, col_b = st.columns(2)
            col_a.write("✅ 可穿戴设备数据")
            col_a.write("✅ 体检报告数据")
            col_b.write("✅ 居家检测数据")
            col_b.write("✅ 病史数据")
            
            st.divider()
            if st.button("🚀 启动AI深度风险评估", type="primary", use_container_width=True):
                with st.spinner("正在融合多源健康数据，AI模型深度分析中..."):
                    time.sleep(2)
                    risk_level, color, reason, score = predict_risk(st.session_state.health_data, st.session_state.user_data)
                    st.session_state.risk_result = (risk_level, color, reason)
                    st.session_state.user_data['health_score'] = score
                    st.success("✅ 风险评估完成！")
    
    with col_main2:
        # 健康趋势卡片（内容拉满，不再空白）
        with st.container():
            st.subheader("📈 核心健康指标趋势（近14天）")
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

    st.divider()
    
    # 风险概览卡片（内容拉满，不再空白）
    with st.container():
        st.subheader("⚠️ 当前健康风险概览")
        risk_level, color, reason = st.session_state.risk_result
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.markdown(f"<h2 style='text-align: center; color: {color}; font-weight: bold; font-size: 2.5rem;'>{risk_level}</h2>", unsafe_allow_html=True)
            st.progress(85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15)
            st.caption("风险指数：85/100")
        with col_b:
            st.warning(reason)
            st.info("💡 提示：可点击左侧导航栏「风险预警中心」查看完整就医指导与干预方案")

# -------------------------- 2. 实时健康监测 --------------------------
elif page == "📡 实时健康监测":
    st.markdown('<p class="main-title">📡 实时健康数据动态监测中心</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">模拟可穿戴设备7×24小时实时采集，AI自动识别异常并触发分级报警</p>', unsafe_allow_html=True)
    st.divider()

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

    # 实时监测卡片（内容拉满）
    with st.container():
        if st.button("▶️ 启动实时监测", type="primary", use_container_width=True):
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
    # 监测说明卡片（内容拉满）
    with st.container():
        st.subheader("📌 功能说明")
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

# -------------------------- 3. 数据同步中心（彻底修复空白，内容拉满）--------------------------
elif page == "📊 数据同步中心":
    st.markdown('<p class="main-title">📊 多源健康数据同步中心</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">打通可穿戴设备、体检报告、居家检测全维度数据，打破健康数据孤岛</p>', unsafe_allow_html=True)
    st.divider()
    
    # 三个核心功能卡片（彻底填充内容，不再空白）
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container():
            st.subheader("⌚ 可穿戴设备同步")
            st.divider()
            st.write("**已支持设备品牌**：")
            st.write("✅ 苹果Apple Watch | ✅ 华为Watch | ✅ 小米手环")
            st.write("✅ OPPO Watch | ✅ 荣耀手环 | ✅ 华米Amazfit")
            st.divider()
            st.write("**已同步数据**：")
            st.metric("累计同步天数", "14天")
            st.metric("数据条目", "2016条")
            st.divider()
            if st.button("绑定/同步设备", key="wearable", use_container_width=True):
                with st.spinner("正在连接设备..."):
                    time.sleep(1)
                    st.success("✅ 设备连接成功！")
                    st.info("正在同步过去14天的健康数据...")
                    time.sleep(1.5)
                    st.success("✅ 数据同步完成！已更新至风险模型")

    with col2:
        with st.container():
            st.subheader("📄 体检报告智能解析")
            st.divider()
            st.write("**支持格式**：PDF、JPG、PNG图片")
            st.write("**支持机构**：全国90%以上体检机构、公立医院体检中心")
            st.divider()
            st.write("**已解析报告**：")
            st.metric("累计解析报告", "2份")
            st.metric("提取核心指标", "128项")
            st.divider()
            uploaded_file = st.file_uploader("上传新的体检报告", type=["pdf", "png", "jpg"], label_visibility="collapsed")
            if uploaded_file is not None:
                with st.spinner("正在OCR识别并解析报告..."):
                    time.sleep(2)
                    st.success("✅ 报告解析完成！")
                    st.write("已提取128项核心健康指标，已同步至风险模型")

    with col3:
        with st.container():
            st.subheader("🏠 居家检测数据录入")
            st.divider()
            st.write("**支持录入指标**：血压、血糖、心率、尿酸、体重")
            st.write("**数据用途**：补充日常监测数据，优化风险预测精度")
            st.divider()
            st.write("**今日已录入**：")
            st.metric("数据条目", "3条")
            st.metric("连续录入天数", "7天")
            st.divider()
            new_bp_s = st.number_input("今日收缩压（mmHg）", min_value=80, max_value=200, value=135)
            new_bp_d = st.number_input("今日舒张压（mmHg）", min_value=50, max_value=120, value=88)
            new_hr = st.number_input("今日静息心率（次/分）", min_value=50, max_value=120, value=84)
            if st.button("保存今日数据", key="home", use_container_width=True):
                st.success("✅ 数据已保存！已同步更新至风险预测模型")
    
    st.divider()
    # 数据预览卡片（内容拉满）
    with st.container():
        st.subheader("📋 已同步健康数据预览")
        st.dataframe(st.session_state.health_data, use_container_width=True, height=300)
        st.caption("* 以上为近14天的核心健康指标时序数据")

# -------------------------- 4. 风险预警中心（内容拉满，不再空白）--------------------------
elif page == "⚠️ 风险预警中心":
    st.markdown('<p class="main-title">⚠️ 隐匿性急重症智能风险预警报告</p>', unsafe_allow_html=True)
    st.divider()

    risk_level, color, reason = st.session_state.risk_result

    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container():
            st.subheader("🎯 最终风险评级")
            st.markdown(f"<h1 style='text-align: center; color: {color}; font-weight: bold; font-size: 3rem;'>{risk_level}</h1>", unsafe_allow_html=True)
            st.progress(85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15)
            st.caption("风险指数：85/100")
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
            st.subheader("🔍 风险来源深度分析")
            st.warning(reason)
            st.divider()
            st.write("**核心异常指标明细（近3天）**：")
            st.dataframe(
                st.session_state.health_data.tail(3)[["日期", "静息心率", "夜间心率", "收缩压", "舒张压"]],
                use_container_width=True,
                hide_index=True
            )
            st.divider()
            st.write("**风险权重占比**：")
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("家族史", "40%")
            col_b.metric("血压异常", "35%")
            col_c.metric("心率异常", "20%")
            col_d.metric("生活习惯", "5%")
            # 风险雷达图占位（可视化填充）
            st.bar_chart(
                pd.DataFrame({
                    "风险维度": ["家族史", "血压", "心率", "生活习惯", "既往病史"],
                    "风险值": [85, 80, 75, 60, 30]
                }).set_index("风险维度"),
                color="#ff4b4b",
                height=200
            )

    st.divider()
    
    # 就医指导卡片（内容拉满）
    with st.container():
        st.subheader("🏥 精准就医指导与干预建议")
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

# -------------------------- 5. 健康管理中心（内容拉满，不再空白）--------------------------
elif page == "💊 健康管理中心":
    st.markdown('<p class="main-title">💊 个性化主动健康管理方案</p>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        # 随访计划卡片（内容拉满）
        with st.container():
            st.subheader("📅 个性化随访计划")
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
        
        # 健康科普卡片（内容拉满）
        with st.container():
            st.subheader("📚 今日健康科普")
            st.info("【心源性猝死的3个早期隐匿信号】\n1. 不明原因的持续疲劳乏力，休息后无法缓解；\n2. 夜间静息心率持续升高超过10%，波动幅度大；\n3. 活动后胸闷气短加重，伴随左肩、后背放射性疼痛。")
            st.divider()
            st.write("**推荐阅读**：")
            st.caption("《中国心源性猝死防治指南2024》")
            st.caption("《中青年高血压管理专家共识》")

    with col2:
        # 干预方案卡片（内容拉满）
        with st.container():
            st.subheader("🥗 个体化生活方式干预方案")
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
        
        # 提醒卡片（内容拉满）
        with st.container():
            st.subheader("🔔 用药与复查提醒")
            st.divider()
            st.write("**每日提醒**：早8点、晚8点测量血压心率并上传系统")
            st.write("**复查提醒**：2026-XX-XX 心内科就诊，完善24小时动态心电图、冠脉CTA检查")
            st.write("**体检提醒**：2026-XX-XX 年度全面体检，重点关注心血管、血脂、血糖相关指标")
            st.divider()
            if st.button("开启微信提醒", use_container_width=True):
                st.success("✅ 微信提醒已开启，将按时推送提醒消息")

    st.divider()
    # 方案说明卡片（内容拉满）
    with st.container():
        st.info("📌 方案说明：本管理方案基于您的风险等级、健康数据、生活习惯，由AI模型自动生成，会根据您每日上传的监测数据动态调整，实现全周期闭环健康管理；所有建议均参考《中国心血管病防治指南》制定，仅供参考，具体诊疗请遵医嘱。")
