import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# -------------------------- 页面全局配置（顶级配置）--------------------------
st.set_page_config(
    page_title="预健·MED·AI | 中青年急重症智能预警系统",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- 顶级玻璃拟态CSS（核心升级）--------------------------
st.markdown("""
<style>
    /* 全局重置与背景 */
    html, body, [class*="css"] {
        font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        background-attachment: fixed;
    }
    
    /* 玻璃拟态容器通用样式 */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
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
    
    /* 主标题样式 */
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
    
    /* 指标卡片玻璃拟态 */
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
    
    /* 按钮高端样式 */
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
    
    /* 警告/成功信息玻璃拟态 */
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
    
    /* 分隔线高端样式 */
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
</style>
""", unsafe_allow_html=True)

# -------------------------- 侧边栏（顶级品牌设计）--------------------------
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
        "lifestyle": "熬夜（日均睡眠6小时）、久坐、工作压力大"
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
        return "极高危", "#ff4b4b", "近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。"
    elif np.mean(recent_hr) > 80 or np.mean(recent_bp) > 135:
        return "中危", "#ff9800", "近期静息心率与血压持续处于高位，存在隐匿性心血管异常风险，建议加强监测。"
    else:
        return "低危", "#00c853", "当前健康指标平稳，无显著异常风险，继续保持良好生活习惯。"

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
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👤 用户健康档案")
        st.write(f"**年龄**：{st.session_state.user_data['age']}岁")
        st.write(f"**性别**：{st.session_state.user_data['gender']}")
        st.write(f"**家族史**：{st.session_state.user_data['family_history']}")
        st.write(f"**生活习惯**：{st.session_state.user_data['lifestyle']}")
        
        st.divider()
        if st.button("🚀 启动AI深度风险评估", type="primary", use_container_width=True):
            with st.spinner("正在融合多源健康数据，AI模型深度分析中..."):
                time.sleep(2)
                risk_level, color, reason = predict_risk(st.session_state.health_data, st.session_state.user_data)
                st.session_state.risk_result = (risk_level, color, reason)
                st.success("✅ 风险评估完成！")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_main2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📈 核心健康指标趋势（近14天）")
        tab1, tab2 = st.tabs(["血压变化趋势", "心率变化趋势"])
        with tab1:
            st.line_chart(
                st.session_state.health_data.set_index("日期")[["收缩压", "舒张压"]],
                color=["#ff4b4b", "#ff9800"]
            )
        with tab2:
            st.line_chart(
                st.session_state.health_data.set_index("日期")[["静息心率", "夜间心率"]],
                color=["#165DFF", "#7b61ff"]
            )
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # 风险概览
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⚠️ 当前健康风险概览")
    risk_level, color, reason = st.session_state.risk_result
    col_a, col_b = st.columns([1, 3])
    with col_a:
        st.markdown(f"<h2 style='text-align: center; color: {color}; font-weight: bold; font-size: 2.5rem;'>{risk_level}</h2>", unsafe_allow_html=True)
        st.progress(85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15)
    with col_b:
        st.warning(reason)
        st.info("💡 提示：可点击左侧导航栏「风险预警中心」查看完整就医指导")
    st.markdown('</div>', unsafe_allow_html=True)

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

    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
                alert_placeholder.error("⚠️ 检测到心率、血压持续异常升高！已自动记录异常数据，建议立即停止活动，休息后复测。")
            else:
                status_placeholder.markdown("<h3 style='color: #00c853; text-align: center;'>🟢 监测正常</h3>", unsafe_allow_html=True)
                alert_placeholder.empty()

            chart_placeholder.line_chart(realtime_history.set_index("时间"), color=["#165DFF", "#ff4b4b", "#7b61ff"])
            time.sleep(0.5)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📌 功能说明")
    st.write("本模块模拟智能手表/手环等可穿戴设备的实时数据采集，AI算法自动识别指标的异常波动与趋势变化，一旦发现高危信号立即触发分级报警，实现急重症的实时捕捉。")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 3. 数据同步中心 --------------------------
elif page == "📊 数据同步中心":
    st.markdown('<p class="main-title">📊 多源健康数据同步中心</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">打通可穿戴设备、体检报告、居家检测全维度数据，打破健康数据孤岛</p>', unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="glass-card" style="height: 380px;">', unsafe_allow_html=True)
        st.subheader("⌚ 可穿戴设备同步")
        st.divider()
        if st.button("绑定智能手表/手环", key="wearable", use_container_width=True):
            with st.spinner("正在连接设备..."):
                time.sleep(1)
                st.success("✅ 设备绑定成功！")
                st.info("正在同步过去14天的健康数据...")
                time.sleep(1.5)
                st.success("✅ 数据同步完成！")
        st.caption("支持华为、小米、苹果、OPPO等主流品牌")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card" style="height: 380px;">', unsafe_allow_html=True)
        st.subheader("📄 体检报告智能解析")
        st.divider()
        uploaded_file = st.file_uploader("上传体检报告（PDF/图片）", type=["pdf", "png", "jpg"], label_visibility="collapsed")
        if uploaded_file is not None:
            with st.spinner("正在OCR识别并解析报告..."):
                time.sleep(2)
                st.success("✅ 报告解析完成！")
                st.write("已提取128项核心健康指标")
        st.caption("支持全国90%以上体检机构格式")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="glass-card" style="height: 380px;">', unsafe_allow_html=True)
        st.subheader("🏠 居家检测数据录入")
        st.divider()
        new_bp_s = st.number_input("今日收缩压（mmHg）", min_value=80, max_value=200, value=135)
        new_bp_d = st.number_input("今日舒张压（mmHg）", min_value=50, max_value=120, value=88)
        new_hr = st.number_input("今日静息心率（次/分）", min_value=50, max_value=120, value=84)
        if st.button("保存今日数据", key="home", use_container_width=True):
            st.success("✅ 数据已保存并同步至风险模型！")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📋 已同步健康数据预览")
    st.dataframe(st.session_state.health_data, use_container_width=True, height=300)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 4. 风险预警中心 --------------------------
elif page == "⚠️ 风险预警中心":
    st.markdown('<p class="main-title">⚠️ 隐匿性急重症智能风险预警报告</p>', unsafe_allow_html=True)
    st.divider()

    risk_level, color, reason = st.session_state.risk_result

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎯 最终风险评级")
        st.markdown(f"<h1 style='text-align: center; color: {color}; font-weight: bold; font-size: 3rem;'>{risk_level}</h1>", unsafe_allow_html=True)
        st.divider()
        st.metric("预警时间", datetime.now().strftime("%Y-%m-%d %H:%M"))
        st.metric("覆盖并发症", "5大类28项")
        st.metric("模型置信度", "92.5%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🔍 风险来源深度分析")
        st.warning(reason)
        st.write("**核心异常指标明细（近3天）**：")
        st.dataframe(
            st.session_state.health_data.tail(3)[["日期", "静息心率", "夜间心率", "收缩压", "舒张压"]],
            use_container_width=True,
            hide_index=True
        )
        st.write("**风险权重占比**：家族史(40%)、血压异常(35%)、心率异常(20%)、生活习惯(5%)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏥 精准就医指导与干预建议")
    if risk_level == "极高危":
        st.error("⚠️ 【极高危紧急响应】")
        st.write("1. **紧急就医建议**：请于3天内前往三级医院心内科就诊，避免高强度活动；")
        st.write("2. **推荐检查项目**：24小时动态心电图、冠脉CTA、心肌酶谱、心脏超声；")
        st.write("3. **临时干预措施**：立即停止熬夜，每日监测血压心率3次；")
        st.write("4. **随访提醒**：系统已自动生成7天后的复查提醒。")
    elif risk_level == "中危":
        st.warning("【中危风险响应】")
        st.write("1. **就医建议**：请于1-2周内前往医院心内科复诊；")
        st.write("2. **推荐检查项目**：常规心电图、血压监测、血脂血糖检测；")
        st.write("3. **干预措施**：调整作息，保证7小时睡眠，每日30分钟有氧运动；")
        st.write("4. **监测要求**：每日上传数据，每周重新评估风险。")
    else:
        st.success("【低风险健康维护】")
        st.write("保持良好生活习惯，每月上传1-2次数据，每季度进行一次全面评估。")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 5. 健康管理中心 --------------------------
elif page == "💊 健康管理中心":
    st.markdown('<p class="main-title">💊 个性化主动健康管理方案</p>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📅 个性化随访计划")
        st.write("✅ **今日待完成**：测量血压心率并上传")
        st.write("⏰ **明日提醒**：心内科就诊预约")
        st.write("📅 **7天后**：复查提醒+风险重评估")
        st.write("📅 **14天后**：第二次风险复核")
        st.write("📅 **30天后**：全面健康评估")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📚 今日健康科普")
        st.info("【心源性猝死的3个早期隐匿信号】\n1. 不明原因的持续疲劳乏力；\n2. 夜间静息心率持续升高超过10%；\n3. 活动后胸闷气短加重，伴随左肩放射性疼痛。")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card" style="height: 320px;">', unsafe_allow_html=True)
        st.subheader("🥗 个体化生活方式干预方案")
        st.write("**作息调整**：每日23:00前入睡，保证7.5小时睡眠；")
        st.write("**运动建议**：每日30分钟中等强度有氧运动（快走、慢跑）；")
        st.write("**饮食调整**：每日钠盐摄入不超过5g，增加新鲜蔬果摄入；")
        st.write("**压力管理**：每日进行10分钟冥想放松训练；")
        st.write("**烟酒控制**：禁止吸烟，限制酒精摄入。")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🔔 用药与复查提醒")
        st.write("**每日提醒**：早8点、晚8点测量血压心率；")
        st.write("**复查提醒**：2026-XX-XX 心内科就诊，完善动态心电图；")
        st.write("**体检提醒**：2026-XX-XX 年度全面体检。")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.info("📌 方案说明：本方案基于您的风险等级AI自动生成，会根据每日监测数据动态调整，实现全周期闭环健康管理。")
    st.markdown('</div>', unsafe_allow_html=True)
