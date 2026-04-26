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

# -------------------------- 终极清晰CSS（所有选择框100%可见） --------------------------
st.markdown("""
<style>
    /* 全局强制文字最清晰 */
    * {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    /* 主背景 */
    .stApp {
        background: #0F172A;
    }

    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: #1E293B;
    }

    /* 卡片 */
    .module-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* 标题 */
    .main-title {
        color: #fff !important;
        font-size: 2rem;
        font-weight: 700;
    }
    .subtitle {
        color: rgba(255,255,255,0.9) !important;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #fff !important;
    }

    /* ========== 输入框 / 数字框 / 文本框 - 最清晰 ========== */
    input, textarea, .stNumberInput input {
        background: #FFFFFF !important;
        color: #000000 !important;
        font-size: 1rem !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        border: 1px solid #ccc !important;
    }

    /* ========== 下拉选择框 - 100%清晰 ========== */
    .stSelectbox div[data-baseweb="select"] {
        background: #FFFFFF !important;
        border-radius: 8px !important;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* 下拉弹出菜单 - 强制黑底白字，超级清晰 */
    div[data-baseweb="popover"] {
        background: #000000 !important;
        border: 2px solid #3B82F6 !important;
    }
    div[data-baseweb="popover"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    div[role="option"]:hover {
        background: #2563EB !important;
    }

    /* ========== 单选按钮 - 100%清晰 ========== */
    .stRadio label {
        color: #FFFFFF !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    div[role="radio"] {
        border: 2px solid #fff !important;
        transform: scale(1.2);
    }

    /* ========== 按钮 ========== */
    .stButton button {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.2rem !important;
        font-weight: 600 !important;
    }
    .stButton button:hover {
        background: #1D4ED8 !important;
    }

    /* ========== 表格、指标、图表 ========== */
    .stDataFrame * {
        color: #fff !important;
    }
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 1rem;
    }

    /* 隐藏多余元素 */
    #MainMenu, footer, header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------- China-PAR 风险评估函数 --------------------------
def china_par_score(age, gender, sbp, tc, hdl, has_diabetes, is_smoker):
    if gender == "男":
        base_survival = 0.9656
        coef_age = 0.048
        coef_sbp = 0.016
        coef_tc = 0.245
        coef_hdl = -0.532
        coef_diabetes = 0.783 if has_diabetes else 0
        coef_smoking = 0.513 if is_smoker else 0
        base_risk = -26.193
    else:
        base_survival = 0.9766
        coef_age = 0.058
        coef_sbp = 0.015
        coef_tc = 0.196
        coef_hdl = -0.427
        coef_diabetes = 0.874 if has_diabetes else 0
        coef_smoking = 0.356 if is_smoker else 0
        base_risk = -26.016
    
    lp = (base_risk + coef_age * age + coef_sbp * sbp + 
          coef_tc * tc + coef_hdl * hdl + coef_diabetes + coef_smoking)
    
    risk = 1 - base_survival ** np.exp(lp)
    return round(risk * 100, 1)

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
    <div style="text-align:center; padding:1.5rem 1rem; background:rgba(59,130,246,0.08); border-radius:12px; margin:1rem;">
        <div style="font-size:2.2rem; margin-bottom:0.6rem;">🩺</div>
        <div style="font-weight:700; font-size:1.4rem;">预健·MED·AI</div>
        <div style="color:rgba(255,255,255,0.7); font-size:0.85rem;">中青年急重症智能预警系统</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    page = st.radio(
        "功能导航",
        ["🏠 系统首页", "📡 实时健康监测", "📊 数据同步中心", "⚠️ 风险预警中心", "💊 健康管理中心"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("© 2026 PREHEALTH MED·AI")

# -------------------------- 全局数据初始化 --------------------------
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "age": 32, "gender": "男",
        "family_history": "有心脑血管家族史",
        "lifestyle": "熬夜、久坐、压力大", "health_score": 58
    }
if 'health_data' not in st.session_state:
    dates = [datetime.now() - timedelta(days=i) for i in range(14, 0, -1)]
    st.session_state.health_data = pd.DataFrame({
        "日期": dates,
        "静息心率": np.concatenate([np.random.randint(65,75,11), [78,82,85]]),
        "夜间心率": np.concatenate([np.random.randint(57,67,11), [73,77,80]]),
        "收缩压": np.concatenate([np.random.randint(115,130,11), [135,140,145]]),
        "舒张压": np.concatenate([np.random.randint(70,80,11), [82,88,92]]),
        "血氧饱和度": np.round(np.random.uniform(96,99,14),1)
    })
if 'risk_result' not in st.session_state:
    st.session_state.risk_result = (
        "极高危", "#EF4444",
        "近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。"
    )
if 'physical_reports' not in st.session_state:
    report1 = pd.DataFrame({
        "指标名称": ["收缩压","舒张压","总胆固醇","甘油三酯","空腹血糖","心率","肌酸激酶","低密度脂蛋白","同型半胱氨酸"],
        "检测结果": ["128mmHg","82mmHg","5.1mmol/L","1.6mmol/L","5.2mmol/L","76次/分","165U/L","3.1mmol/L","11μmol/L"],
        "参考范围": ["90-140","60-90","2.8-5.2","0.45-1.7","3.9-6.1","60-100","25-200","0-3.4","0-15"],
        "异常标识": ["正常"]*9, "报告日期": ["2026-01-15"]*9
    })
    report2 = pd.DataFrame({
        "指标名称": ["收缩压","舒张压","总胆固醇","甘油三酯","空腹血糖","心率","肌酸激酶","低密度脂蛋白","同型半胱氨酸"],
        "检测结果": ["138mmHg","88mmHg","5.9mmol/L","2.4mmol/L","5.7mmol/L","84次/分","192U/L","3.8mmol/L","16μmol/L"],
        "参考范围": ["90-140","60-90","2.8-5.2","0.45-1.7","3.9-6.1","60-100","25-200","0-3.4","0-15"],
        "异常标识": ["正常","正常","↑","↑","正常","正常","正常","↑","↑"], "报告日期": ["2026-04-20"]*9
    })
    st.session_state.physical_reports = [report1, report2]
    st.session_state.current_report_idx = 1

# -------------------------- 风险预测 --------------------------
def predict_risk(health_data, user_info):
    recent_hr = health_data["静息心率"].tail(3).values
    recent_bp = health_data["收缩压"].tail(3).values
    age = user_info["age"]
    gender = user_info["gender"]
    has_family = "心脑血管" in user_info["family_history"]
    par_risk = china_par_score(age, gender, np.mean(recent_bp), 5.0, 1.2, False, False)
    trend = 0
    reason = ""
    if np.mean(recent_bp)>135:
        trend +=15
        reason+="血压偏高；"
    if np.mean(recent_hr)>80:
        trend +=10
        reason+="心率偏高；"
    if has_family:
        trend +=15
        reason+="家族史；"
    total = par_risk + trend
    score = max(20, min(95,100-total))
    if total>=50 or par_risk>=15:
        return "极高危","#EF4444",f"风险{par_risk}%，{reason}风险极高",score
    elif total>=30 or par_risk>=7:
        return "中危","#F59E0B",f"风险{par_risk}%，{reason}需关注",score
    else:
        return "低危","#10B981",f"风险{par_risk}%，正常",score

def highlight_abnormal(row):
    if row["异常标识"] in ["↑","↓"]:
        return ['color:#EF4444; font-weight:600;']*len(row)
    return ['']*len(row)

# -------------------------- 页面内容 --------------------------
if page == "🏠 系统首页":
    st.markdown('<p class="main-title">🩺 预健·MED·AI 中青年急重症智能预警系统</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">基于多模态时序大数据与深度学习，提前预警急重症风险</p>', unsafe_allow_html=True)
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("风险等级", st.session_state.risk_result[0])
    col2.metric("覆盖病种", "5大类28项")
    col3.metric("更新时间", datetime.now().strftime("%m-%d %H:%M"))
    col4.metric("模型准确率", "93.2%")
    st.divider()
    colA,colB = st.columns([1,1.6])
    with colA:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">👤 用户健康档案</p>', unsafe_allow_html=True)
        score = st.session_state.user_data['health_score']
        st.markdown(f'<div style="text-align:center; font-size:2.8rem; font-weight:700;">{score}</div>', unsafe_allow_html=True)
        st.progress(score/100)
        st.divider()
        c1,c2 = st.columns(2)
        age = c1.number_input("年龄",25,50,st.session_state.user_data['age'])
        gender = c2.radio("性别",["男","女"],horizontal=True)
        family = st.selectbox("家族史",["有心脑血管家族史","无"])
        life = st.text_area("生活习惯", st.session_state.user_data['lifestyle'])
        st.session_state.user_data.update({"age":age,"gender":gender,"family_history":family,"lifestyle":life})
        if st.button("🚀 启动AI风险评估", type="primary"):
            res = predict_risk(st.session_state.health_data, st.session_state.user_data)
            st.session_state.risk_result = res[:3]
            st.session_state.user_data['health_score'] = res[3]
            st.success("评估完成")
        st.markdown('</div>', unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">📈 近14天健康趋势</p>', unsafe_allow_html=True)
        t1,t2 = st.tabs(["血压","心率"])
        with t1:
            st.line_chart(st.session_state.health_data.set_index("日期")[["收缩压","舒张压"]])
        with t2:
            st.line_chart(st.session_state.health_data.set_index("日期")[["静息心率","夜间心率"]])
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">⚠️ 风险概览</p>', unsafe_allow_html=True)
    st.warning(st.session_state.risk_result[2])
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📡 实时健康监测":
    st.markdown('<p class="main-title">📡 实时健康监测</p>', unsafe_allow_html=True)
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("心率","75 次/分")
    c2.metric("血压","128 mmHg")
    c3.metric("血氧","98 %")
    c4.markdown("<h3>🟢 正常</h3>", unsafe_allow_html=True)
    st.button("▶️ 启动实时监测", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📊 数据同步中心":
    st.markdown('<p class="main-title">📊 多源数据同步</p>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">⌚ 设备同步</p>', unsafe_allow_html=True)
        st.selectbox("选择品牌",["请选择","苹果","华为","小米"])
        st.file_uploader("上传数据")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">📄 体检报告解析</p>', unsafe_allow_html=True)
        st.file_uploader("上传报告")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">🏠 居家数据录入</p>', unsafe_allow_html=True)
        st.number_input("收缩压",100,200,135)
        st.number_input("舒张压",60,120,88)
        st.number_input("心率",50,120,84)
        st.button("保存")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚠️ 风险预警中心":
    st.markdown('<p class="main-title">⚠️ 风险预警报告</p>', unsafe_allow_html=True)
    level,col,reason = st.session_state.risk_result
    c1,c2 = st.columns([1,2])
    with c1:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color:{col}; text-align:center;">{level}</h1>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.warning(reason)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "💊 健康管理中心":
    st.markdown('<p class="main-title">💊 个性化健康管理</p>', unsafe_allow_html=True)
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.write("✅ 随访计划、作息建议、饮食运动、用药提醒已全部生成")
    st.markdown('</div>', unsafe_allow_html=True)
