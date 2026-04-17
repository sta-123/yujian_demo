import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 页面配置
st.set_page_config(page_title="预健-中青年急重症智能预警系统", page_icon="❤️", layout="wide")

# 侧边栏导航
st.sidebar.title("🔧 系统导航")
page = st.sidebar.radio("选择功能模块", ["🏠 系统首页", "📊 数据同步", "⚠️ 风险预警", "💊 健康管理"])

# 模拟用户数据
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "name": "用户",
        "age": 32,
        "gender": "男",
        "family_history": "有心脑血管家族史",
        "lifestyle": "熬夜（日均睡眠6小时）、久坐、工作压力大"
    }

if 'health_data' not in st.session_state:
    # 模拟过去2周的可穿戴数据
    dates = [datetime.now() - timedelta(days=i) for i in range(14, 0, -1)]
    st.session_state.health_data = pd.DataFrame({
        "日期": dates,
        "静息心率": np.random.randint(65, 85, 14),
        "夜间心率": np.random.randint(58, 78, 14),
        "收缩压": np.random.randint(115, 145, 14),
        "舒张压": np.random.randint(75, 95, 14),
        "血氧饱和度": np.random.uniform(94, 99, 14).round(1)
    })
    # 模拟最近3天的异常数据
    st.session_state.health_data.loc[11:, "静息心率"] = [82, 84, 86]
    st.session_state.health_data.loc[11:, "夜间心率"] = [75, 77, 79]
    st.session_state.health_data.loc[11:, "收缩压"] = [138, 142, 145]

# 模拟风险预测模型
def predict_risk(health_data, user_info):
    # 简单的模拟逻辑：最近3天静息心率持续升高+血压高+家族史=高风险
    recent_hr = health_data["静息心率"].tail(3).values
    recent_bp = health_data["收缩压"].tail(3).values
    has_family_history = "心脑血管" in user_info["family_history"]
    
    if (np.all(np.diff(recent_hr) > 0) and np.mean(recent_bp) > 140) or has_family_history:
        return "极高危", "红色", "近3天静息心率持续升高12%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死风险显著升高。"
    elif np.mean(recent_hr) > 80 or np.mean(recent_bp) > 135:
        return "中危", "橙色", "近期静息心率与血压处于高位，建议加强监测。"
    else:
        return "低危", "绿色", "当前健康指标平稳，继续保持良好生活习惯。"

# 页面1：系统首页
if page == "🏠 系统首页":
    st.title("❤️ 预健-中青年隐匿性急重症智能预警系统")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("👤 用户基本信息")
        st.write(f"**年龄**：{st.session_state.user_data['age']}岁")
        st.write(f"**性别**：{st.session_state.user_data['gender']}")
        st.write(f"**家族史**：{st.session_state.user_data['family_history']}")
        st.write(f"**生活习惯**：{st.session_state.user_data['lifestyle']}")
    
    with col2:
        st.subheader("📈 核心健康指标趋势")
        st.line_chart(st.session_state.health_data.set_index("日期")[["静息心率", "收缩压"]])
    
    st.markdown("---")
    # 模拟一键风险评估
    if st.button("🚀 一键启动健康风险评估", type="primary", use_container_width=True):
        with st.spinner("正在分析多源健康数据，请稍候..."):
            import time
            time.sleep(2)
            risk_level, color, reason = predict_risk(st.session_state.health_data, st.session_state.user_data)
            st.session_state.risk_result = (risk_level, color, reason)
            st.success("风险评估完成！请前往「风险预警」模块查看详情。")

# 页面2：数据同步
elif page == "📊 数据同步":
    st.title("📊 多源健康数据同步中心")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("⌚ 可穿戴设备同步")
        if st.button("绑定智能手表/手环", use_container_width=True):
            st.success("已成功模拟绑定主流智能手表！")
            st.info("正在同步过去14天的心率、血氧、睡眠数据...")
            time.sleep(1.5)
            st.success("✅ 可穿戴数据同步完成！")
    
    with col2:
        st.subheader("📄 体检报告上传")
        uploaded_file = st.file_uploader("上传年度/季度体检报告（PDF/图片）", type=["pdf", "png", "jpg"])
        if uploaded_file is not None:
            with st.spinner("正在OCR识别体检报告核心指标..."):
                time.sleep(2)
                st.success("✅ 体检报告核心指标提取完成！")
                st.write("已提取：血常规、生化、血脂、肝肾功能等128项核心指标")
    
    with col3:
        st.subheader("🏠 居家检测数据录入")
        st.number_input("今日收缩压（mmHg）", min_value=80, max_value=200, value=135)
        st.number_input("今日舒张压（mmHg）", min_value=50, max_value=120, value=88)
        st.number_input("今日静息心率（次/分）", min_value=50, max_value=120, value=84)
        if st.button("保存今日检测数据", use_container_width=True):
            st.success("✅ 居家检测数据已保存！")
    
    st.markdown("---")
    st.subheader("📋 已同步健康数据预览")
    st.dataframe(st.session_state.health_data, use_container_width=True)

# 页面3：风险预警
elif page == "⚠️ 风险预警中心":
    st.title("⚠️ 隐匿性急重症智能风险预警")
    st.markdown("---")
    
    if 'risk_result' not in st.session_state:
        st.warning("请先前往「系统首页」启动健康风险评估，或上传最新健康数据！")
    else:
        risk_level, color, reason = st.session_state.risk_result
        
        # 展示风险等级
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("当前健康风险等级", risk_level, delta_color="inverse")
            st.markdown(f"<h3 style='text-align: center; color: {color};'>{risk_level}</h3>", unsafe_allow_html=True)
        
        with col2:
            st.subheader("🔍 风险来源分析（可解释AI）")
            st.warning(reason)
            st.write("**核心异常指标**：")
            st.dataframe(st.session_state.health_data.tail(3)[["日期", "静息心率", "夜间心率", "收缩压"]], use_container_width=True)
        
        st.markdown("---")
        st.subheader("🏥 精准就医指导建议")
        st.error("⚠️ 【极高危响应】请立即启动以下流程：")
        st.info("1. **紧急就医建议**：请于3天内前往三级医院心内科就诊；")
        st.info("2. **推荐检查项目**：24小时动态心电图、冠脉CTA、心肌酶谱、心脏超声；")
        st.info("3. **临时干预措施**：立即停止熬夜、高强度工作，保持情绪平稳，每日监测血压心率；")
        st.info("4. **随访提醒**：已自动为您生成7天后的复查提醒。")

# 页面4：健康管理
elif page == "💊 主动健康管理中心":
    st.title("💊 个性化主动健康管理方案")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📅 个性化随访计划")
        st.write("✅ 今日任务：测量血压心率并上传")
        st.write("⏰ 明日提醒：心内科就诊预约")
        st.write("📅 7天后：复查提醒")
        st.write("📅 30天后：全面健康评估")
    
    with col2:
        st.subheader("🥗 生活方式干预方案")
        st.write("**作息调整**：每日23:00前入睡，保证7.5小时睡眠；")
        st.write("**运动建议**：每日进行30分钟中等强度有氧运动（如快走）；")
        st.write("**饮食调整**：减少钠盐摄入，每日不超过5g，增加新鲜蔬果摄入；")
        st.write("**压力管理**：每日进行10分钟冥想放松训练。")
    
    st.markdown("---")
    st.subheader("📚 专属健康科普")
    st.info("【今日科普】心源性猝死的3个早期隐匿信号：① 不明原因的疲劳乏力；② 夜间静息心率持续升高；③ 活动后胸闷气短加重。")
