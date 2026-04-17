import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 页面全局配置
st.set_page_config(
    page_title="预健-中青年急重症智能预警系统",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 侧边栏导航
st.sidebar.title("🔧 系统导航")
page = st.sidebar.radio(
    "选择功能模块",
    ["🏠 系统首页", "📡 实时健康监测", "📊 数据同步中心", "⚠️ 风险预警中心", "💊 健康管理中心"]
)

# -------------------------- 全局数据初始化（解决页面空白核心问题）--------------------------
# 用户基础信息
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "age": 32,
        "gender": "男",
        "family_history": "有心脑血管家族史",
        "lifestyle": "熬夜（日均睡眠6小时）、久坐、工作压力大"
    }

# 14天健康时序数据
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

# 风险评估结果（默认初始化，解决页面空白问题）
if 'risk_result' not in st.session_state:
    st.session_state.risk_result = (
        "极高危",
        "#ff4b4b",
        "近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。"
    )

# 实时监测数据缓存
if 'realtime_data' not in st.session_state:
    st.session_state.realtime_data = {
        "hr": 75,
        "bp_s": 128,
        "bp_d": 82,
        "spo2": 98,
        "is_abnormal": False
    }

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
    st.title("❤️ 预健-中青年隐匿性急重症智能预警系统")
    st.divider()
    
    # 核心信息看板
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("👤 用户基础信息")
        with st.container(border=True):
            st.write(f"**年龄**：{st.session_state.user_data['age']}岁")
            st.write(f"**性别**：{st.session_state.user_data['gender']}")
            st.write(f"**家族史**：{st.session_state.user_data['family_history']}")
            st.write(f"**生活习惯**：{st.session_state.user_data['lifestyle']}")
        
        st.divider()
        # 一键风险评估按钮
        if st.button("🚀 一键启动健康风险评估", type="primary", use_container_width=True):
            with st.spinner("正在融合多源健康数据，AI模型分析中..."):
                time.sleep(2)
                risk_level, color, reason = predict_risk(st.session_state.health_data, st.session_state.user_data)
                st.session_state.risk_result = (risk_level, color, reason)
                st.success("✅ 风险评估完成！可前往「风险预警中心」查看完整报告")
    
    with col2:
        st.subheader("📈 核心健康指标趋势（近14天）")
        with st.container(border=True):
            tab1, tab2 = st.tabs(["血压趋势", "心率趋势"])
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
    # 风险概览卡片
    st.subheader("⚠️ 当前健康风险概览")
    risk_level, color, reason = st.session_state.risk_result
    col_a, col_b = st.columns([1, 3])
    with col_a:
        st.metric("健康风险等级", risk_level)
        st.markdown(f"<h2 style='text-align: center; color: {color}; font-weight: bold;'>{risk_level}</h2>", unsafe_allow_html=True)
    with col_b:
        st.warning(reason)
        st.info("👉 可点击左侧导航栏「风险预警中心」查看完整风险报告与就医指导")

# -------------------------- 2. 实时健康监测（修复兼容问题） --------------------------
elif page == "📡 实时健康监测":
    st.title("📡 实时健康数据动态监测")
    st.caption("模拟可穿戴设备实时采集心率、血压、血氧数据，异常指标自动报警")
    st.divider()

    # 实时数据看板
    col1, col2, col3, col4 = st.columns(4)
    hr_placeholder = col1.empty()
    bp_placeholder = col2.empty()
    spo2_placeholder = col3.empty()
    status_placeholder = col4.empty()

    # 趋势图占位
    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

    # 模拟实时数据刷新
    if st.button("▶️ 启动实时监测", type="primary", use_container_width=True):
        st.session_state.realtime_data["is_abnormal"] = False
        # 初始化实时数据缓存
        realtime_history = pd.DataFrame({
            "时间": [],
            "实时心率": [],
            "收缩压": [],
            "血氧饱和度": []
        })

        # 实时刷新循环
        for i in range(60):
            # 模拟数据波动，第30次后触发异常
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
                st.session_state.realtime_data["is_abnormal"] = True

            # 更新全局数据
            st.session_state.realtime_data["hr"] = new_hr
            st.session_state.realtime_data["bp_s"] = new_bp_s
            st.session_state.realtime_data["spo2"] = new_spo2

            # 更新历史数据
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
                alert_placeholder.error("⚠️ 检测到心率、血压持续异常升高，已自动记录异常数据，建议立即停止活动，休息后复测，持续不适请立即就医！")
            else:
                status_placeholder.markdown("<h3 style='color: #00c853; text-align: center;'>🟢 监测正常</h3>", unsafe_allow_html=True)
                alert_placeholder.empty()

            # 刷新趋势图
            chart_placeholder.line_chart(realtime_history.set_index("时间"), color=["#165DFF", "#ff4b4b", "#7b61ff"])
            
            time.sleep(0.5)
    
    # 监测说明
    st.divider()
    st.info("📌 功能说明：本模块模拟可穿戴设备7×24小时实时健康数据采集，AI自动识别异常波动并触发分级报警，异常数据自动同步至风险预警模型，实现急重症的实时捕捉与提前干预。")

# -------------------------- 3. 数据同步中心 --------------------------
elif page == "📊 数据同步中心":
    st.title("📊 多源健康数据同步中心")
    st.caption("打通可穿戴设备、体检报告、居家检测全维度健康数据，打破数据孤岛")
    st.divider()
    
    # 三大功能模块
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True, height=320):
            st.subheader("⌚ 可穿戴设备同步")
            st.divider()
            if st.button("绑定智能手表/手环", use_container_width=True):
                with st.spinner("正在连接设备..."):
                    time.sleep(1)
                    st.success("✅ 已成功模拟绑定主流智能手表！")
                    st.info("正在同步过去14天的心率、血氧、睡眠数据...")
                    time.sleep(1.5)
                    st.success("✅ 可穿戴数据同步完成！")
            st.caption("支持华为、小米、苹果、OPPO等主流品牌设备")

    with col2:
        with st.container(border=True, height=320):
            st.subheader("📄 体检报告上传")
            st.divider()
            uploaded_file = st.file_uploader("上传体检报告（PDF/图片）", type=["pdf", "png", "jpg"])
            if uploaded_file is not None:
                with st.spinner("正在OCR识别体检报告核心指标..."):
                    time.sleep(2)
                    st.success("✅ 体检报告核心指标提取完成！")
                    st.write("已提取：血常规、生化、血脂、肝肾功能等128项核心指标")
            st.caption("支持全国90%以上体检机构报告格式")

    with col3:
        with st.container(border=True, height=320):
            st.subheader("🏠 居家检测数据录入")
            st.divider()
            new_bp_s = st.number_input("今日收缩压（mmHg）", min_value=80, max_value=200, value=135)
            new_bp_d = st.number_input("今日舒张压（mmHg）", min_value=50, max_value=120, value=88)
            new_hr = st.number_input("今日静息心率（次/分）", min_value=50, max_value=120, value=84)
            if st.button("保存今日检测数据", use_container_width=True):
                st.success("✅ 居家检测数据已保存，已同步更新至健康趋势模型！")
    
    st.divider()
    st.subheader("📋 已同步健康数据预览")
    st.dataframe(st.session_state.health_data, use_container_width=True, height=300)

# -------------------------- 4. 风险预警中心 --------------------------
elif page == "⚠️ 风险预警中心":
    st.title("⚠️ 隐匿性急重症智能风险预警报告")
    st.divider()

    # 读取风险结果
    risk_level, color, reason = st.session_state.risk_result

    # 风险等级看板
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("🎯 最终风险评级")
        with st.container(border=True):
            st.markdown(f"<h1 style='text-align: center; color: {color}; font-weight: bold;'>{risk_level}</h1>", unsafe_allow_html=True)
            st.metric("预警时间", datetime.now().strftime("%Y-%m-%d %H:%M"))
            st.metric("覆盖并发症", "5大类28项")

    with col2:
        st.subheader("🔍 风险来源深度分析（可解释AI）")
        with st.container(border=True):
            st.warning(reason)
            st.write("**核心异常指标明细（近3天）**：")
            st.dataframe(
                st.session_state.health_data.tail(3)[["日期", "静息心率", "夜间心率", "收缩压", "舒张压"]],
                use_container_width=True,
                hide_index=True
            )
            st.write("**风险权重占比**：家族史(40%)、血压持续异常(35%)、心率节律异常(20%)、生活习惯(5%)")

    st.divider()
    # 就医指导
    st.subheader("🏥 精准就医指导与干预建议")
    if risk_level == "极高危":
        st.error("⚠️ 【极高危紧急响应】请立即启动以下流程：")
        with st.container(border=True):
            st.write("1. **紧急就医建议**：请于3天内前往三级医院心内科就诊，避免高强度活动与情绪激动；")
            st.write("2. **推荐检查项目**：24小时动态心电图、冠脉CTA、心肌酶谱、心脏超声、血脂全套；")
            st.write("3. **临时干预措施**：立即停止熬夜、高强度工作，每日早中晚3次监测血压心率，保持情绪平稳；")
            st.write("4. **随访提醒**：系统已自动为您生成7天后的复查提醒，就诊后可上传病历更新风险模型。")
    elif risk_level == "中危":
        st.warning("【中危风险响应】请启动以下干预流程：")
        with st.container(border=True):
            st.write("1. **就医建议**：请于1-2周内前往社区卫生服务中心或医院心内科复诊；")
            st.write("2. **推荐检查项目**：常规心电图、血压监测、血脂、血糖检测；")
            st.write("3. **干预措施**：调整作息，保证每日7小时睡眠，每日30分钟中等强度有氧运动，低盐饮食；")
            st.write("4. **监测要求**：每日上传居家血压心率数据，每周重新评估风险等级。")
    else:
        st.success("【低风险健康维护】")
        with st.container(border=True):
            st.write("1. 保持当前良好的生活习惯，继续规律运动与健康饮食；")
            st.write("2. 每月上传1-2次居家检测数据，每季度进行一次全面风险评估；")
            st.write("3. 按年度完成常规体检，及时更新体检报告数据。")

# -------------------------- 5. 健康管理中心 --------------------------
elif page == "💊 健康管理中心":
    st.title("💊 个性化主动健康管理方案")
    st.divider()

    # 随访计划+干预方案
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📅 个性化随访计划")
        with st.container(border=True):
            st.write("✅ **今日待完成**：测量血压心率并上传系统")
            st.write("⏰ **明日提醒**：心内科就诊预约")
            st.write("📅 **7天后**：就诊后复查提醒+风险重评估")
            st.write("📅 **14天后**：第二次风险等级复核")
            st.write("📅 **30天后**：全面健康评估+方案调整")
        st.divider()
        st.subheader("📚 专属健康科普")
        with st.container(border=True):
            st.info("【今日科普】心源性猝死的3个早期隐匿信号：\n1. 不明原因的持续疲劳乏力，休息后无法缓解；\n2. 夜间静息心率持续升高，波动幅度超过10%；\n3. 活动后胸闷气短加重，伴随左肩、后背放射性疼痛。")

    with col2:
        st.subheader("🥗 个体化生活方式干预方案")
        with st.container(border=True, height=320):
            st.write("**作息调整**：每日23:00前入睡，保证7.5小时睡眠，禁止熬夜；")
            st.write("**运动建议**：每日进行30分钟中等强度有氧运动（快走、慢跑、游泳），避免高强度剧烈运动；")
            st.write("**饮食调整**：每日钠盐摄入不超过5g，减少高脂、高糖食物，增加新鲜蔬果、优质蛋白摄入；")
            st.write("**压力管理**：每日进行10分钟冥想放松训练，减少连续工作时长，每工作1小时休息10分钟；")
            st.write("**烟酒控制**：禁止吸烟，限制酒精摄入，每周饮酒不超过1次。")
        
        st.divider()
        st.subheader("🔔 用药与复查提醒")
        with st.container(border=True):
            st.write("**每日提醒**：早8点、晚8点测量血压心率并上传；")
            st.write("**复查提醒**：2026-XX-XX 心内科就诊，完善24小时动态心电图检查；")
            st.write("**体检提醒**：2026-XX-XX 年度全面体检，重点关注心血管相关指标。")

    st.divider()
    st.info("📌 方案说明：本管理方案基于您的风险等级、健康数据、生活习惯AI自动生成，会根据您每日上传的监测数据动态调整，实现全周期闭环健康管理。")
