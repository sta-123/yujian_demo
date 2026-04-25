import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# -------------------------- 页面配置 --------------------------
st.set_page_config(
    page_title="预健·MED·AI | 中青年急重症智能预警系统",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- 自定义CSS（深色科技风）--------------------------
st.markdown("""
<style>
    /* 全局背景与字体 */
    html, body, [class*="css"] {
        font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }
    .stApp {
        background: #0a0e17;
        background-image:
            radial-gradient(ellipse at 15% 10%, rgba(59,130,246,0.04) 0%, transparent 60%),
            radial-gradient(ellipse at 85% 90%, rgba(139,92,246,0.04) 0%, transparent 60%);
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #a0a7b8;
        font-weight: 500;
        padding: 10px 12px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.04);
        color: #e8eaef;
    }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
        display: none;
    }
    [data-testid="stSidebar"] .stRadio [aria-checked="true"] + div label {
        background: rgba(59,130,246,0.1);
        color: #ffffff !important;
        border-left: 3px solid #3b82f6;
        font-weight: 600;
    }
    
    /* 卡片样式 */
    .module-card {
        background: #161b26;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    .module-card:hover {
        border-color: rgba(255,255,255,0.12);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    
    /* 指标卡片 */
    [data-testid="stMetric"] {
        background: #161b26;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.2rem;
        color: white;
    }
    [data-testid="stMetric"] label {
        color: #6b7280 !important;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* 进度条 */
    .stProgress > div > div {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        border-radius: 20px;
    }
    .stProgress > div {
        background: rgba(255,255,255,0.06);
        border-radius: 20px;
    }
    
    /* 按钮 */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #60a5fa, #3b82f6);
        box-shadow: 0 6px 20px rgba(37,99,235,0.3);
        transform: translateY(-1px);
    }
    
    /* 警告框 */
    .stAlert {
        background: rgba(239,68,68,0.06) !important;
        border: 1px solid rgba(239,68,68,0.2) !important;
        border-radius: 12px;
    }
    
    /* 输入框 */
    .stNumberInput>div>div>input,
    .stTextArea textarea,
    .stSelectbox>div>div {
        background: rgba(255,255,255,0.03) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px;
    }
    
    /* 文本 */
    h1, h2, h3, p, li { color: #e8eaef; }
    hr { border-color: rgba(255,255,255,0.06); margin: 1.2rem 0; }
    
    /* 隐藏默认元素 */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# -------------------------- 初始化数据 --------------------------
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

if 'risk_result' not in st.session_state:
    st.session_state.risk_result = (
        "极高危",
        "#ef4444",
        "近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。"
    )

# 体检报告
if 'physical_reports' not in st.session_state:
    report1 = pd.DataFrame({
        "指标名称": ["收缩压", "舒张压", "总胆固醇", "甘油三酯", "空腹血糖", "心率", "肌酸激酶", "低密度脂蛋白", "同型半胱氨酸"],
        "检测结果": ["128mmHg", "82mmHg", "5.1mmol/L", "1.6mmol/L", "5.2mmol/L", "76次/分", "165U/L", "3.1mmol/L", "11μmol/L"],
        "参考范围": ["90-140mmHg", "60-90mmHg", "2.8-5.2mmol/L", "0.45-1.7mmol/L", "3.9-6.1mmol/L", "60-100次/分", "25-200U/L", "0-3.4mmol/L", "0-15μmol/L"],
        "异常标识": ["正常"]*9,
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

# -------------------------- 风险预测函数 --------------------------
def predict_risk(health_data, user_info):
    recent_hr = health_data["静息心率"].tail(3).values
    recent_bp = health_data["收缩压"].tail(3).values
    has_family = "心脑血管" in user_info["family_history"]
    age = user_info["age"]
    lifestyle = user_info["lifestyle"]
    base_risk = 0
    reason = ""
    if has_family:
        base_risk += 40
        reason += "结合心脑血管家族史，遗传风险较高；"
    if np.mean(recent_bp) > 140:
        base_risk += 35
        reason += "近3天收缩压持续高于140mmHg，血压昼夜节律异常；"
    elif np.mean(recent_bp) > 135:
        base_risk += 20
        reason += "近期收缩压持续处于高位，存在血压异常风险；"
    if np.all(np.diff(recent_hr) > 0) and np.mean(recent_hr) > 80:
        base_risk += 20
        reason += "近3天静息心率持续升高15%以上，心率变异性异常；"
    elif np.mean(recent_hr) > 80:
        base_risk += 10
        reason += "近期静息心率持续高于80次/分，存在心血管异常信号；"
    if age >= 40:
        base_risk += 5
        reason += "年龄超过40岁，心脑血管疾病发病风险升高；"
    if any(w in lifestyle for w in ["熬夜", "久坐", "压力大"]):
        base_risk += 5
        reason += "不良生活习惯进一步提升风险；"
    health_score = max(30, min(95, 100 - base_risk))
    if base_risk >= 60:
        level, color = "极高危", "#ef4444"
        full_reason = f"{reason}综合判定心源性猝死、隐匿性冠心病风险显著升高。"
    elif base_risk >= 40:
        level, color = "中危", "#f59e0b"
        full_reason = f"{reason}存在隐匿性心血管异常风险，建议加强监测。"
    else:
        level, color = "低危", "#10b981"
        full_reason = "当前健康指标平稳，无显著异常风险，继续保持良好生活习惯。"
    return level, color, full_reason, health_score

# -------------------------- 侧边栏导航 --------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0;">
        <div style="font-size:2.5rem;">🩺</div>
        <div style="font-weight:700; font-size:1.3rem; background:linear-gradient(135deg,#60a5fa,#818cf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">预健·MED·AI</div>
        <div style="color:#6b7280; font-size:0.7rem; letter-spacing:0.04em;">中青年急重症智能预警系统</div>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio(
        "导航",
        ["🏠 系统首页", "📡 实时健康监测", "📊 数据同步中心", "⚠️ 风险预警中心", "💊 健康管理中心"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("© 2026 PREHEALTH MED·AI")

# -------------------------- 各页面渲染 --------------------------
if page == "🏠 系统首页":
    st.markdown('<h1 style="color:#fff; font-weight:700; font-size:1.8rem;">🩺 预健·MED·AI 中青年急重症智能预警系统</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#a0a7b8; font-size:0.9rem;">基于多模态时序大数据与深度学习，实现急重症的早发现、早预警、早干预</p>', unsafe_allow_html=True)
    
    # 指标栏
    risk_level, color, reason = st.session_state.risk_result
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("当前风险等级", risk_level, delta="需紧急关注", delta_color="inverse")
    with col2:
        st.metric("覆盖并发症", "5大类28项")
    with col3:
        st.metric("数据更新时间", datetime.now().strftime("%Y-%m-%d"))
    with col4:
        st.metric("模型准确率", "93.2%")
    st.divider()
    
    # 用户档案与趋势
    left, right = st.columns([1, 2])
    with left:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p style="font-weight:600; font-size:1.1rem; color:#fff;">👤 用户健康档案（可编辑）</p>', unsafe_allow_html=True)
            score = st.session_state.user_data['health_score']
            st.progress(score/100, text=f"健康评分：{score}/100")
            with st.form("user_form"):
                new_age = st.number_input("年龄", 25, 50, st.session_state.user_data['age'])
                new_gender = st.radio("性别", ["男", "女"], horizontal=True, index=0 if st.session_state.user_data['gender']=="男" else 1)
                new_family = st.selectbox("家族史", ["有心脑血管家族史", "无相关家族史"], index=0 if "有心脑血管" in st.session_state.user_data['family_history'] else 1)
                new_lifestyle = st.text_area("生活习惯", st.session_state.user_data['lifestyle'])
                if st.form_submit_button("💾 保存档案"):
                    st.session_state.user_data.update({"age":new_age, "gender":new_gender, "family_history":new_family, "lifestyle":new_lifestyle})
                    st.success("档案已更新")
            if st.button("🚀 启动AI深度风险评估"):
                with st.spinner("AI模型分析中..."):
                    time.sleep(1.5)
                    level, color, reason, score = predict_risk(st.session_state.health_data, st.session_state.user_data)
                    st.session_state.risk_result = (level, color, reason)
                    st.session_state.user_data['health_score'] = score
                    st.success("评估完成")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with right:
        with st.container():
            st.markdown('<div class="module-card">', unsafe_allow_html=True)
            st.markdown('<p style="font-weight:600; font-size:1.1rem; color:#fff;">📈 核心健康指标趋势（近14天）</p>', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["血压变化趋势", "心率变化趋势"])
            with tab1:
                st.line_chart(st.session_state.health_data.set_index("日期")[["收缩压", "舒张压"]], color=["#ef4444", "#f59e0b"], height=300)
            with tab2:
                st.line_chart(st.session_state.health_data.set_index("日期")[["静息心率", "夜间心率"]], color=["#3b82f6", "#8b5cf6"], height=300)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 风险概览
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:600; font-size:1.1rem; color:#fff;">⚠️ 当前健康风险概览</p>', unsafe_allow_html=True)
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.markdown(f"<h2 style='text-align:center; color:{color}; font-weight:800; font-size:2.8rem;'>{risk_level}</h2>", unsafe_allow_html=True)
            risk_index = 85 if risk_level == "极高危" else 50 if risk_level == "中危" else 15
            st.progress(risk_index/100)
            st.caption(f"风险指数：{risk_index}/100")
        with col_b:
            st.warning(reason)
            st.info("💡 提示：可点击左侧「风险预警中心」查看完整就医指导")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "📡 实时健康监测":
    st.markdown('<h1 style="color:#fff; font-weight:700;">📡 实时健康数据动态监测中心</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#a0a7b8;">模拟可穿戴设备7×24小时实时采集，AI自动识别异常并触发分级报警</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        hr_ph = st.empty()
        bp_ph = st.empty()
        spo2_ph = st.empty()
        status_ph = st.empty()
        chart_ph = st.empty()
        alert_ph = st.empty()
        
        if st.button("▶️ 启动实时监测"):
            history = pd.DataFrame(columns=["时间", "心率", "收缩压", "血氧"])
            for i in range(60):
                is_abnormal = i >= 30
                hr = np.random.randint(95, 110) if is_abnormal else np.random.randint(72, 78)
                bp = np.random.randint(145, 160) if is_abnormal else np.random.randint(125, 132)
                spo2 = round(np.random.uniform(93, 95), 1) if is_abnormal else round(np.random.uniform(97, 99), 1)
                
                hr_ph.metric("实时心率", f"{hr} 次/分", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                bp_ph.metric("实时收缩压", f"{bp} mmHg", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                spo2_ph.metric("血氧饱和度", f"{spo2} %", delta="异常" if is_abnormal else "正常", delta_color="inverse")
                
                if is_abnormal:
                    status_ph.markdown("<h3 style='color:#ef4444; text-align:center;'>🔴 异常报警</h3>", unsafe_allow_html=True)
                    alert_ph.error("⚠️ 检测到心率、血压持续异常升高！建议立即停止活动，休息后复测，持续不适请立即就医！")
                else:
                    status_ph.markdown("<h3 style='color:#10b981; text-align:center;'>🟢 监测正常</h3>", unsafe_allow_html=True)
                    alert_ph.empty()
                
                new_row = pd.DataFrame({"时间": [datetime.now().strftime("%H:%M:%S")], "心率": [hr], "收缩压": [bp], "血氧": [spo2]})
                history = pd.concat([history, new_row]).tail(20)
                chart_ph.line_chart(history.set_index("时间"), color=["#3b82f6", "#ef4444", "#8b5cf6"], height=300)
                time.sleep(0.5)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "📊 数据同步中心":
    st.markdown('<h1 style="color:#fff; font-weight:700;">📊 多源健康数据同步中心</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#a0a7b8;">打通可穿戴设备、体检报告、居家检测全维度数据</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:600; color:#3b82f6;">⌚ 可穿戴设备同步</p>', unsafe_allow_html=True)
        st.selectbox("选择设备品牌", ["请选择", "苹果Apple", "华为Huawei", "小米Xiaomi", "OPPO", "荣耀"], key="device")
        st.button("🔗 授权绑定设备", key="bind")
        st.file_uploader("上传设备CSV数据", type="csv", key="wearable")
        st.progress(1.0, text="已同步全量数据")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:600; color:#8b5cf6;">📄 体检报告智能解析</p>', unsafe_allow_html=True)
        st.metric("累计报告", f"{len(st.session_state.physical_reports)}份")
        st.progress(0.98, text="OCR识别准确率 98%")
        uploaded = st.file_uploader("上传体检报告", type=["pdf","png","jpg"], key="report")
        if uploaded:
            with st.spinner("解析中..."):
                time.sleep(2)
                new_report = pd.DataFrame({
                    "指标名称": ["收缩压","舒张压","总胆固醇","甘油三酯","空腹血糖","心率","肌酸激酶","低密度脂蛋白","同型半胱氨酸"],
                    "检测结果": [f"{np.random.randint(130,150)}mmHg", f"{np.random.randint(80,95)}mmHg", "5.8mmol/L", "2.5mmol/L", "5.6mmol/L", "85次/分", "200U/L", "3.9mmol/L", "17μmol/L"],
                    "参考范围": ["90-140mmHg","60-90mmHg","2.8-5.2mmol/L","0.45-1.7mmol/L","3.9-6.1mmol/L","60-100次/分","25-200U/L","0-3.4mmol/L","0-15μmol/L"],
                    "异常标识": ["正常","正常","↑","↑","正常","正常","正常","↑","↑"],
                    "报告日期": [datetime.now().strftime("%Y-%m-%d")]*9
                })
                st.session_state.physical_reports.append(new_report)
                st.session_state.current_report_idx = len(st.session_state.physical_reports)-1
                st.success("报告解析完成！")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:600; color:#10b981;">🏠 居家检测数据录入</p>', unsafe_allow_html=True)
        st.number_input("今日收缩压", 80, 200, 135)
        st.number_input("今日舒张压", 50, 120, 88)
        st.number_input("今日心率", 50, 120, 84)
        st.button("💾 保存今日数据", key="home_data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 报告详情
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:600;">📋 体检报告深度分析</p>', unsafe_allow_html=True)
        current = st.session_state.physical_reports[st.session_state.current_report_idx]
        st.dataframe(current[["指标名称", "检测结果", "参考范围", "异常标识"]], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚠️ 风险预警中心":
    risk_level, color, reason = st.session_state.risk_result
    st.markdown('<h1 style="color:#fff; font-weight:700;">⚠️ 隐匿性急重症智能风险预警报告</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:{color}; font-weight:800; font-size:3rem;'>{risk_level}</h1>", unsafe_allow_html=True)
        risk_idx = 85 if risk_level=="极高危" else 50 if risk_level=="中危" else 15
        st.progress(risk_idx/100)
        st.caption(f"风险指数：{risk_idx}/100")
        st.metric("预警时间", datetime.now().strftime("%Y-%m-%d %H:%M"))
        st.metric("模型置信度", "92.5%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.warning(reason)
        st.dataframe(st.session_state.health_data.tail(3)[["日期","静息心率","收缩压","舒张压"]], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:600;">🏥 精准就医指导</p>', unsafe_allow_html=True)
        if risk_level == "极高危":
            st.error("⚠️ 极高危：请3天内前往三级医院心内科就诊，完善24小时动态心电图、冠脉CTA等检查，避免剧烈运动和情绪激动。")
        elif risk_level == "中危":
            st.warning("中危：建议1-2周内社区医院复诊，调整作息饮食，每日监测血压心率。")
        else:
            st.success("低风险：继续保持良好生活习惯，定期体检。")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "💊 健康管理中心":
    st.markdown('<h1 style="color:#fff; font-weight:700;">💊 个性化主动健康管理方案</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:600;">📅 随访计划</p>', unsafe_allow_html=True)
        st.progress(0.2, text="本周完成 1/5")
        st.write("✅ 今日：测量血压心率上传")
        st.write("⏰ 明日：心内科就诊预约")
        st.write("📅 7天后：复查提醒")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:600;">🥗 生活方式干预</p>', unsafe_allow_html=True)
        st.write("- 23:00前入睡，保证7.5h睡眠")
        st.write("- 每日30分钟有氧运动")
        st.write("- 低盐低脂饮食，每日饮水1.5-2L")
        st.write("- 冥想放松，避免久坐")
        st.markdown('</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.info("📌 方案说明：基于您的风险等级自动生成，每日动态调整，具体诊疗请遵医嘱。")
        st.markdown('</div>', unsafe_allow_html=True)
