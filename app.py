import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# -------------------------- 页面全局配置（核心优化）--------------------------
st.set_page_config(
    page_title="预健·中青年急重症智能预警系统",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "预健·中青年隐匿性急重症智能预警系统"
    }
)

# 自定义CSS样式（注入高级感）
st.markdown("""
<style>
    /* 全局字体与背景 */
    html, body, [class*="css"] {
        font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }
    
    /* 侧边栏样式优化 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        padding-top: 2rem;
    }
    [data-testid="stSidebar"] h1 {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    [data-testid="stSidebar"] p {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* 主内容区容器优化 */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    /* 标题样式优化 */
    h1 {
        color: #0f172a;
        font-weight: 700;
    }
    h2 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    h3 {
        color: #334155;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* 按钮样式优化 */
    .stButton>button {
        background: linear-gradient(90deg, #165DFF 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(22, 93, 255, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0e4bcc 0%, #2563eb 100%);
        box-shadow: 0 6px 15px rgba(22, 93, 255, 0.4);
    }
    
    /* 指标卡片样式 */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #165DFF;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    /* 分隔线优化 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------- 侧边栏导航（全新设计）--------------------------
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>❤️ 预健</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>中青年急重症智能预警系统</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # 导航选项（带图标，更直观）
    page = st.radio(
        "功能导航",
        ["🏠 系统首页", "📡 实时健康监测", "📊 数据同步中心", "⚠️ 风险预警中心", "💊 健康管理中心"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("© 2026 预健智能 · 守护生命健康")

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
    st.title("❤️ 预健·中青年隐匿性急重症智能预警系统")
    st.caption("基于多模态时序大数据与AI技术，实现急重症的早发现、早预警、早干预")
    st.divider()
    
    # 顶部核心指标看板
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("当前风险等级", "极高危", delta="需关注", delta_color="inverse")
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
        with st.container(border=True):
            st.subheader("👤 用户健康档案")
            st.write(f"**年龄**：{st.session_state.user_data['age']}岁")
            st.write(f"**性别**：{st.session_state.user_data['gender']}")
            st.write(f"**家族史**：{st.session_state.user_data['family_history']}")
            st.write(f"**生活习惯**：{st.session_state.user_data['lifestyle']}")
            
            st.divider()
            if st.button("🚀 启动AI风险评估", type="primary", use_container_width=True):
                with st.spinner("正在融合多源健康数据，AI深度分析中..."):
                    time.sleep(2)
                    risk_level, color, reason = predict_risk(st.session_state.health_data, st.session_state.user_data)
                    st.session_state.risk_result = (risk_level, color, reason)
                    st.success("✅ 风险评估完成！")
    
    with col_main2:
        with st.container(border=True):
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

    st.divider()
    
    # 风险概览
    with st.container(border=True):
        st.subheader("⚠️ 当前健康风险概览")
        risk_level, color, reason = st.session_state.risk_result
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.markdown(f"<h2 style='text-align: center; color: {color}; font-weight: bold;'>{risk_level}</h2>", unsafe_allow_html=True)
            st.progress(85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15)
        with col_b:
            st.warning(reason)
            st.info("💡 提示：可点击左侧导航栏「风险预警中心」查看完整就医指导")

# -------------------------- 2. 实时健康监测 --------------------------
elif page == "📡 实时健康监测":
    st.title("📡 实时健康数据动态监测中心")
    st.caption("模拟可穿戴设备7×24小时实时采集，AI自动识别异常并触发分级报警")
    st.divider()

    # 实时数据看板
    col1, col2, col3, col4 = st.columns(4)
    hr_placeholder = col1.empty()
    bp_placeholder = col2.empty()
    spo2_placeholder = col3.empty()
    status_placeholder = col4.empty()

    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

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
    
    st.divider()
    with st.container(border=True):
        st.subheader("📌 功能说明")
        st.write("本模块模拟智能手表/手环等可穿戴设备的实时数据采集，AI算法自动识别指标的异常波动与趋势变化，一旦发现高危信号立即触发分级报警，实现急重症的实时捕捉。")

# -------------------------- 3. 数据同步中心 --------------------------
elif page == "📊 数据同步中心":
    st.title("📊 多源健康数据同步中心")
    st.caption("打通可穿戴设备、体检报告、居家检测全维度数据，打破健康数据孤岛")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True, height=350):
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

    with col2:
        with st.container(border=True, height=350):
            st.subheader("📄 体检报告智能解析")
            st.divider()
            uploaded_file = st.file_uploader("上传体检报告（PDF/图片）", type=["pdf", "png", "jpg"], label_visibility="collapsed")
            if uploaded_file is not None:
                with st.spinner("正在OCR识别并解析报告..."):
                    time.sleep(2)
                    st.success("✅ 报告解析完成！")
                    st.write("已提取128项核心健康指标")
            st.caption("支持全国90%以上体检机构格式")

    with col3:
        with st.container(border=True, height=350):
            st.subheader("🏠 居家检测数据录入")
            st.divider()
            new_bp_s = st.number_input("今日收缩压（mmHg）", min_value=80, max_value=200, value=135)
            new_bp_d = st.number_input("今日舒张压（mmHg）", min_value=50, max_value=120, value=88)
            new_hr = st.number_input("今日静息心率（次/分）", min_value=50, max_value=120, value=84)
            if st.button("保存今日数据", key="home", use_container_width=True):
                st.success("✅ 数据已保存并同步至风险模型！")
    
    st.divider()
    with st.container(border=True):
        st.subheader("📋 已同步健康数据预览")
        st.dataframe(st.session_state.health_data, use_container_width=True, height=300)

# -------------------------- 4. 风险预警中心 --------------------------
elif page == "⚠️ 风险预警中心":
    st.title("⚠️ 隐匿性急重症智能风险预警报告")
    st.divider()

    risk_level, color, reason = st.session_state.risk_result

    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container(border=True):
            st.subheader("🎯 最终风险评级")
            st.markdown(f"<h1 style='text-align: center; color: {color}; font-weight: bold;'>{risk_level}</h1>", unsafe_allow_html=True)
            st.divider()
            st.metric("预警时间", datetime.now().strftime("%Y-%m-%d %H:%M"))
            st.metric("覆盖并发症", "5大类28项")
            st.metric("模型置信度", "92.5%")

    with col2:
        with st.container(border=True):
            st.subheader("🔍 风险来源深度分析")
            st.warning(reason)
            st.write("**核心异常指标明细（近3天）**：")
            st.dataframe(
                st.session_state.health_data.tail(3)[["日期", "静息心率", "夜间心率", "收缩压", "舒张压"]],
                use_container_width=True,
                hide_index=True
            )
            st.write("**风险权重占比**：家族史(40%)、血压异常(35%)、心率异常(20%)、生活习惯(5%)")

    st.divider()
    
    with st.container(border=True):
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

# -------------------------- 5. 健康管理中心 --------------------------
elif page == "💊 健康管理中心":
    st.title("💊 个性化主动健康管理方案")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("📅 个性化随访计划")
            st.write("✅ **今日待完成**：测量血压心率并上传")
            st.write("⏰ **明日提醒**：心内科就诊预约")
            st.write("📅 **7天后**：复查提醒+风险重评估")
            st.write("📅 **14天后**：第二次风险复核")
            st.write("📅 **30天后**：全面健康评估")
        
        st.divider()
        
        with st.container(border=True):
            st.subheader("📚 今日健康科普")
            st.info("【心源性猝死的3个早期隐匿信号】\n1. 不明原因的持续疲劳乏力；\n2. 夜间静息心率持续升高超过10%；\n3. 活动后胸闷气短加重，伴随左肩放射性疼痛。")

    with col2:
        with st.container(border=True, height=320):
            st.subheader("🥗 个体化生活方式干预方案")
            st.write("**作息调整**：每日23:00前入睡，保证7.5小时睡眠；")
            st.write("**运动建议**：每日30分钟中等强度有氧运动（快走、慢跑）；")
            st.write("**饮食调整**：每日钠盐摄入不超过5g，增加新鲜蔬果摄入；")
            st.write("**压力管理**：每日进行10分钟冥想放松训练；")
            st.write("**烟酒控制**：禁止吸烟，限制酒精摄入。")
        
        st.divider()
        
        with st.container(border=True):
            st.subheader("🔔 用药与复查提醒")
            st.write("**每日提醒**：早8点、晚8点测量血压心率；")
            st.write("**复查提醒**：2026-XX-XX 心内科就诊，完善动态心电图；")
            st.write("**体检提醒**：2026-XX-XX 年度全面体检。")

    st.divider()
    st.info("📌 方案说明：本方案基于您的风险等级AI自动生成，会根据每日监测数据动态调整，实现全周期闭环健康管理。")
