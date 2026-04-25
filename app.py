<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>预健·MED·AI | 中青年急重症智能预警系统</title>
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: #161b26;
            --bg-card-hover: #1c2333;
            --bg-sidebar: #0d1117;
            --border-subtle: rgba(255, 255, 255, 0.06);
            --border-medium: rgba(255, 255, 255, 0.10);
            --border-accent: rgba(22, 93, 255, 0.35);
            --text-primary: #e8eaef;
            --text-secondary: #a0a7b8;
            --text-muted: #6b7280;
            --accent-blue: #3b82f6;
            --accent-blue-glow: rgba(59, 130, 246, 0.25);
            --accent-red: #ef4444;
            --accent-red-glow: rgba(239, 68, 68, 0.3);
            --accent-orange: #f59e0b;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
            --accent-teal: #14b8a6;
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 20px;
            --radius-xl: 24px;
            --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.4), 0 1px 2px rgba(0, 0, 0, 0.3);
            --shadow-card-hover: 0 8px 32px rgba(0, 0, 0, 0.5), 0 2px 8px rgba(0, 0, 0, 0.4);
            --shadow-glow-blue: 0 0 40px rgba(59, 130, 246, 0.12), 0 0 80px rgba(59, 130, 246, 0.05);
            --shadow-glow-red: 0 0 40px rgba(239, 68, 68, 0.15), 0 0 80px rgba(239, 68, 68, 0.06);
            --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-smooth: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            --font-sans: 'Inter', 'PingFang SC', 'Microsoft YaHei', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: var(--font-sans);
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
            background-image:
                radial-gradient(ellipse at 15% 10%, rgba(59, 130, 246, 0.04) 0%, transparent 60%),
                radial-gradient(ellipse at 85% 90%, rgba(139, 92, 246, 0.04) 0%, transparent 60%),
                radial-gradient(ellipse at 50% 50%, rgba(20, 184, 166, 0.02) 0%, transparent 70%);
        }

        /* ========== 布局容器 ========== */
        .app-container {
            display: flex;
            min-height: 100vh;
        }

        /* ========== 侧边栏 ========== */
        .sidebar {
            width: 260px;
            min-width: 260px;
            background: var(--bg-sidebar);
            border-right: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            position: sticky;
            top: 0;
            height: 100vh;
            z-index: 100;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        .sidebar-brand {
            padding: 28px 20px 20px;
            text-align: center;
            border-bottom: 1px solid var(--border-subtle);
        }
        .sidebar-brand .logo-icon {
            font-size: 2.6rem;
            margin-bottom: 8px;
            display: block;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%,
            100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-6px);
            }
        }
        .sidebar-brand .brand-name {
            font-size: 1.25rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60a5fa, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.01em;
        }
        .sidebar-brand .brand-subtitle {
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-top: 2px;
            letter-spacing: 0.04em;
            font-weight: 500;
        }

        .sidebar-nav {
            flex: 1;
            padding: 16px 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            overflow-y: auto;
        }
        .sidebar-nav .nav-section-label {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            padding: 12px 10px 6px;
            font-weight: 600;
        }
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 11px 14px;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all var(--transition-smooth);
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.9rem;
            position: relative;
            text-decoration: none;
            border: 1px solid transparent;
        }
        .nav-item:hover {
            background: rgba(255, 255, 255, 0.04);
            color: var(--text-primary);
            border-color: var(--border-medium);
        }
        .nav-item.active {
            background: rgba(59, 130, 246, 0.1);
            color: #ffffff;
            border-color: rgba(59, 130, 246, 0.3);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.08);
            font-weight: 600;
        }
        .nav-item.active::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 3px;
            height: 24px;
            border-radius: 0 3px 3px 0;
            background: var(--accent-blue);
        }
        .nav-item .nav-icon {
            font-size: 1.2rem;
            width: 24px;
            text-align: center;
            flex-shrink: 0;
        }
        .nav-item .nav-badge {
            margin-left: auto;
            background: var(--accent-red);
            color: #fff;
            font-size: 0.65rem;
            padding: 3px 8px;
            border-radius: 20px;
            font-weight: 700;
            letter-spacing: 0.03em;
            animation: pulse-badge 2s ease-in-out infinite;
        }
        @keyframes pulse-badge {
            0%,
            100% {
                box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5);
            }
            50% {
                box-shadow: 0 0 0 8px rgba(239, 68, 68, 0);
            }
        }

        .sidebar-footer {
            padding: 16px 20px;
            border-top: 1px solid var(--border-subtle);
            font-size: 0.7rem;
            color: var(--text-muted);
            text-align: center;
            letter-spacing: 0.03em;
        }

        /* ========== 主内容区 ========== */
        .main-content {
            flex: 1;
            padding: 28px 32px 40px;
            overflow-y: auto;
            max-height: 100vh;
        }
        .main-content::-webkit-scrollbar {
            width: 5px;
        }
        .main-content::-webkit-scrollbar-track {
            background: transparent;
        }
        .main-content::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 20px;
        }

        /* ========== 页面标题 ========== */
        .page-header {
            margin-bottom: 28px;
        }
        .page-title {
            font-size: 1.7rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }
        .page-subtitle {
            font-size: 0.88rem;
            color: var(--text-secondary);
            font-weight: 400;
        }

        /* ========== 顶部指标栏 ========== */
        .metrics-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .metric-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 20px 24px;
            transition: all var(--transition-smooth);
            position: relative;
            overflow: hidden;
        }
        .metric-card::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.02) 0%, transparent 70%);
            pointer-events: none;
        }
        .metric-card:hover {
            border-color: var(--border-medium);
            box-shadow: var(--shadow-card-hover);
            transform: translateY(-2px);
        }
        .metric-card.danger {
            border-color: rgba(239, 68, 68, 0.25);
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.06) 0%, var(--bg-card) 100%);
        }
        .metric-card .metric-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .metric-card .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #ffffff;
        }
        .metric-card .metric-delta {
            font-size: 0.78rem;
            margin-top: 4px;
            font-weight: 500;
        }
        .metric-card .metric-delta.warning {
            color: var(--accent-red);
        }
        .metric-card .metric-delta.normal {
            color: var(--accent-green);
        }

        /* ========== 通用卡片 ========== */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin-bottom: 20px;
            transition: all var(--transition-smooth);
            position: relative;
        }
        .card:hover {
            border-color: var(--border-medium);
        }
        .card.glow-blue {
            box-shadow: var(--shadow-glow-blue);
        }
        .card.glow-red {
            box-shadow: var(--shadow-glow-red);
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: #ffffff;
            letter-spacing: -0.01em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card-title .icon {
            font-size: 1.3rem;
        }
        .card-badge {
            font-size: 0.7rem;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: 600;
            letter-spacing: 0.03em;
        }
        .card-badge.danger {
            background: rgba(239, 68, 68, 0.15);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.25);
        }
        .card-badge.success {
            background: rgba(16, 185, 129, 0.12);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }
        .card-badge.info {
            background: rgba(59, 130, 246, 0.12);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        /* ========== 网格布局 ========== */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        .grid-1-2 {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
        }
        .grid-1-3 {
            display: grid;
            grid-template-columns: 1fr 3fr;
            gap: 20px;
        }

        /* ========== 进度条 ========== */
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 20px;
            overflow: hidden;
            position: relative;
        }
        .progress-bar .fill {
            height: 100%;
            border-radius: 20px;
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        .progress-bar .fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg,
                    transparent 0%,
                    rgba(255, 255, 255, 0.25) 50%,
                    transparent 100%);
            animation: shimmer 2s ease-in-out infinite;
        }
        @keyframes shimmer {
            0% {
                transform: translateX(-100%);
            }
            100% {
                transform: translateX(100%);
            }
        }
        .progress-bar .fill.danger {
            background: linear-gradient(135deg, #ef4444, #f87171);
        }
        .progress-bar .fill.warning {
            background: linear-gradient(135deg, #f59e0b, #fbbf24);
        }
        .progress-bar .fill.success {
            background: linear-gradient(135deg, #10b981, #34d399);
        }
        .progress-bar .fill.info {
            background: linear-gradient(135deg, #3b82f6, #60a5fa);
        }
        .progress-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
            margin-bottom: 6px;
            color: var(--text-secondary);
        }
        .progress-label .value {
            font-weight: 700;
            color: #ffffff;
        }

        /* ========== 按钮 ========== */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 12px 22px;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 0.88rem;
            cursor: pointer;
            transition: all var(--transition-smooth);
            border: none;
            font-family: var(--font-sans);
            letter-spacing: -0.01em;
            text-decoration: none;
            white-space: nowrap;
        }
        .btn-primary {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: #ffffff;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
            width: 100%;
        }
        .btn-primary:hover {
            box-shadow: 0 6px 24px rgba(37, 99, 235, 0.45);
            transform: translateY(-1px);
            background: linear-gradient(135deg, #60a5fa, #3b82f6);
        }
        .btn-outline {
            background: transparent;
            border: 1px solid var(--border-medium);
            color: var(--text-primary);
            width: 100%;
        }
        .btn-outline:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(255, 255, 255, 0.2);
        }
        .btn-sm {
            padding: 8px 16px;
            font-size: 0.78rem;
            border-radius: var(--radius-sm);
        }
        .btn-danger {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: #fff;
            box-shadow: 0 4px 16px rgba(220, 38, 38, 0.3);
        }
        .btn-success {
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff;
            box-shadow: 0 4px 16px rgba(5, 150, 105, 0.3);
        }

        /* ========== 输入框 ========== */
        .input-group {
            margin-bottom: 14px;
        }
        .input-group label {
            display: block;
            font-size: 0.78rem;
            color: var(--text-secondary);
            margin-bottom: 5px;
            font-weight: 500;
        }
        .input-field {
            width: 100%;
            padding: 11px 14px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-medium);
            border-radius: var(--radius-sm);
            color: #ffffff;
            font-size: 0.88rem;
            font-family: var(--font-sans);
            transition: all var(--transition-fast);
            outline: none;
        }
        .input-field:focus {
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            background: rgba(255, 255, 255, 0.05);
        }
        .input-field::placeholder {
            color: var(--text-muted);
        }
        textarea.input-field {
            resize: vertical;
            min-height: 70px;
        }
        select.input-field {
            appearance: none;
            cursor: pointer;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'%3E%3C/path%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 14px center;
            padding-right: 36px;
        }

        /* ========== 表格 ========== */
        .table-wrapper {
            overflow-x: auto;
            border-radius: var(--radius-md);
            border: 1px solid var(--border-subtle);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }
        table th {
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            font-size: 0.7rem;
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-subtle);
        }
        table td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-primary);
        }
        table tbody tr {
            transition: all var(--transition-fast);
        }
        table tbody tr:hover {
            background: rgba(255, 255, 255, 0.02);
        }
        table tbody tr:last-child td {
            border-bottom: none;
        }
        .cell-abnormal {
            color: #fca5a5 !important;
            font-weight: 700;
            background: rgba(239, 68, 68, 0.06);
            border-radius: 4px;
            padding: 4px 8px;
            display: inline-block;
        }
        .cell-normal {
            color: #6ee7b7 !important;
        }

        /* ========== 风险展示 ========== */
        .risk-display {
            text-align: center;
            padding: 20px 0;
        }
        .risk-level-badge {
            display: inline-block;
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            padding: 16px 36px;
            border-radius: var(--radius-xl);
            animation: riskPulse 3s ease-in-out infinite;
        }
        .risk-level-badge.critical {
            background: rgba(239, 68, 68, 0.12);
            color: #fca5a5;
            border: 2px solid rgba(239, 68, 68, 0.4);
            box-shadow: 0 0 40px rgba(239, 68, 68, 0.2), 0 0 80px rgba(239, 68, 68, 0.08);
        }
        .risk-level-badge.medium {
            background: rgba(245, 158, 11, 0.1);
            color: #fcd34d;
            border: 2px solid rgba(245, 158, 11, 0.35);
            box-shadow: 0 0 30px rgba(245, 158, 11, 0.15);
        }
        .risk-level-badge.low {
            background: rgba(16, 185, 129, 0.1);
            color: #6ee7b7;
            border: 2px solid rgba(16, 185, 129, 0.3);
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.1);
        }
        @keyframes riskPulse {
            0%,
            100% {
                box-shadow: 0 0 40px rgba(239, 68, 68, 0.2), 0 0 80px rgba(239, 68, 68, 0.05);
            }
            50% {
                box-shadow: 0 0 55px rgba(239, 68, 68, 0.35), 0 0 100px rgba(239, 68, 68, 0.12);
            }
        }

        /* ========== 告警框 ========== */
        .alert {
            padding: 16px 20px;
            border-radius: var(--radius-md);
            margin-bottom: 16px;
            font-weight: 500;
            font-size: 0.88rem;
            line-height: 1.6;
            border: 1px solid;
        }
        .alert-danger {
            background: rgba(239, 68, 68, 0.08);
            border-color: rgba(239, 68, 68, 0.25);
            color: #fca5a5;
        }
        .alert-warning {
            background: rgba(245, 158, 11, 0.06);
            border-color: rgba(245, 158, 11, 0.2);
            color: #fcd34d;
        }
        .alert-info {
            background: rgba(59, 130, 246, 0.06);
            border-color: rgba(59, 130, 246, 0.2);
            color: #93c5fd;
        }
        .alert-success {
            background: rgba(16, 185, 129, 0.06);
            border-color: rgba(16, 185, 129, 0.2);
            color: #6ee7b7;
        }

        /* ========== 标签页 ========== */
        .tabs {
            display: flex;
            gap: 6px;
            margin-bottom: 18px;
            flex-wrap: wrap;
        }
        .tab {
            padding: 9px 18px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.82rem;
            font-weight: 500;
            transition: all var(--transition-smooth);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid transparent;
            color: var(--text-secondary);
            white-space: nowrap;
        }
        .tab:hover {
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-primary);
        }
        .tab.active {
            background: rgba(59, 130, 246, 0.15);
            color: #ffffff;
            border-color: rgba(59, 130, 246, 0.3);
            font-weight: 600;
        }

        /* ========== 分隔线 ========== */
        .divider {
            border: none;
            height: 1px;
            background: var(--border-subtle);
            margin: 18px 0;
        }
        .divider-dashed {
            border: none;
            height: 1px;
            background: repeating-linear-gradient(90deg,
                    rgba(255, 255, 255, 0.08) 0px,
                    rgba(255, 255, 255, 0.08) 4px,
                    transparent 4px,
                    transparent 8px);
            margin: 18px 0;
        }

        /* ========== 小标签 ========== */
        .tag {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.03em;
        }
        .tag-red {
            background: rgba(239, 68, 68, 0.15);
            color: #fca5a5;
        }
        .tag-green {
            background: rgba(16, 185, 129, 0.12);
            color: #6ee7b7;
        }
        .tag-blue {
            background: rgba(59, 130, 246, 0.12);
            color: #93c5fd;
        }
        .tag-purple {
            background: rgba(139, 92, 246, 0.12);
            color: #c4b5fd;
        }

        /* ========== 图表占位 ========== */
        .chart-placeholder {
            width: 100%;
            height: 280px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: var(--radius-md);
            border: 1px dashed var(--border-medium);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            position: relative;
            overflow: hidden;
        }
        .chart-placeholder .chart-line {
            position: absolute;
            bottom: 30%;
            left: 5%;
            width: 90%;
            height: 2px;
            background: linear-gradient(90deg,
                    transparent,
                    rgba(59, 130, 246, 0.5) 20%,
                    rgba(239, 68, 68, 0.6) 60%,
                    rgba(239, 68, 68, 0.8) 90%,
                    transparent);
            border-radius: 2px;
        }
        .chart-placeholder .chart-dot {
            position: absolute;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #ef4444;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.6);
        }

        /* ========== 响应式 ========== */
        @media (max-width: 1200px) {
            .metrics-row {
                grid-template-columns: repeat(2, 1fr);
            }
            .grid-3 {
                grid-template-columns: 1fr;
            }
            .grid-1-2,
            .grid-1-3 {
                grid-template-columns: 1fr;
            }
            .grid-2 {
                grid-template-columns: 1fr;
            }
            .sidebar {
                width: 220px;
                min-width: 220px;
            }
            .main-content {
                padding: 20px;
            }
        }
        @media (max-width: 768px) {
            .app-container {
                flex-direction: column;
            }
            .sidebar {
                width: 100%;
                min-width: 100%;
                height: auto;
                position: relative;
                flex-direction: row;
                overflow-x: auto;
                padding: 10px;
            }
            .sidebar-nav {
                flex-direction: row;
                gap: 8px;
                flex-wrap: nowrap;
            }
            .sidebar-brand {
                display: none;
            }
            .main-content {
                padding: 16px;
            }
            .metrics-row {
                grid-template-columns: 1fr 1fr;
            }
            .page-title {
                font-size: 1.3rem;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- ==================== 侧边栏 ==================== -->
        <aside class="sidebar">
            <div class="sidebar-brand">
                <span class="logo-icon">🩺</span>
                <div class="brand-name">预健·MED·AI</div>
                <div class="brand-subtitle">中青年急重症智能预警系统</div>
            </div>
            <nav class="sidebar-nav">
                <div class="nav-section-label">主菜单</div>
                <a href="#home" class="nav-item active" onclick="switchPage('home', this)">
                    <span class="nav-icon">🏠</span> 系统首页
                </a>
                <a href="#monitor" class="nav-item" onclick="switchPage('monitor', this)">
                    <span class="nav-icon">📡</span> 实时健康监测
                </a>
                <a href="#sync" class="nav-item" onclick="switchPage('sync', this)">
                    <span class="nav-icon">📊</span> 数据同步中心
                </a>
                <a href="#risk" class="nav-item" onclick="switchPage('risk', this)">
                    <span class="nav-icon">⚠️</span> 风险预警中心
                    <span class="nav-badge">极高危</span>
                </a>
                <a href="#health" class="nav-item" onclick="switchPage('health', this)">
                    <span class="nav-icon">💊</span> 健康管理中心
                </a>
            </nav>
            <div class="sidebar-footer">
                © 2026 PREHEALTH MED·AI<br>All Rights Reserved
            </div>
        </aside>

        <!-- ==================== 主内容区 ==================== -->
        <main class="main-content" id="mainContent">
            <!-- 页面内容由JS动态渲染 -->
        </main>
    </div>

    <script>
        // ==================== 全局状态 ====================
        const state = {
            currentPage: 'home',
            userData: {
                age: 32,
                gender: '男',
                familyHistory: '有心脑血管家族史',
                lifestyle: '熬夜（日均睡眠6小时）、久坐、工作压力大',
                healthScore: 58
            },
            riskResult: {
                level: '极高危',
                color: '#ef4444',
                cssClass: 'critical',
                reason: '近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。',
                index: 85
            },
            // 模拟14天健康数据
            healthData: generateHealthData(),
            physicalReports: generatePhysicalReports(),
            currentReportIdx: 1
        };

        function generateHealthData() {
            const data = [];
            const now = new Date();
            for (let i = 13; i >= 0; i--) {
                const date = new Date(now);
                date.setDate(date.getDate() - i);
                const isRecent = i < 3;
                data.push({
                    date: date.toISOString().split('T')[0],
                    hrResting: isRecent ? Math.floor(Math.random() * 8) + 78 : Math.floor(Math
                        .random() * 10) + 65,
                    hrNight: isRecent ? Math.floor(Math.random() * 6) + 72 : Math.floor(Math.random() *
                        8) + 58,
                    bpSystolic: isRecent ? Math.floor(Math.random() * 10) + 138 : Math.floor(Math.random() *
                        15) + 115,
                    bpDiastolic: isRecent ? Math.floor(Math.random() * 8) + 84 : Math.floor(Math.random() *
                        10) + 72,
                    spo2: (Math.random() * 2.5 + 96.5).toFixed(1)
                });
            }
            return data;
        }

        function generatePhysicalReports() {
            const indicators = ['收缩压', '舒张压', '总胆固醇', '甘油三酯', '空腹血糖', '心率', '肌酸激酶', '低密度脂蛋白', '同型半胱氨酸'];
            const report1 = {
                date: '2026-01-15',
                items: indicators.map(name => ({
                    name,
                    result: getNormalResult(name),
                    refRange: getRefRange(name),
                    flag: '正常'
                }))
            };
            const report2 = {
                date: '2026-04-20',
                items: indicators.map(name => ({
                    name,
                    result: getAbnormalResult(name),
                    refRange: getRefRange(name),
                    flag: getFlag(name)
                }))
            };
            return [report1, report2];
        }

        function getNormalResult(name) {
            const map = {
                '收缩压': '128mmHg',
                '舒张压': '82mmHg',
                '总胆固醇': '5.1mmol/L',
                '甘油三酯': '1.6mmol/L',
                '空腹血糖': '5.2mmol/L',
                '心率': '76次/分',
                '肌酸激酶': '165U/L',
                '低密度脂蛋白': '3.1mmol/L',
                '同型半胱氨酸': '11μmol/L'
            };
            return map[name] || '-';
        }

        function getAbnormalResult(name) {
            const map = {
                '收缩压': '138mmHg',
                '舒张压': '88mmHg',
                '总胆固醇': '5.9mmol/L',
                '甘油三酯': '2.4mmol/L',
                '空腹血糖': '5.7mmol/L',
                '心率': '84次/分',
                '肌酸激酶': '192U/L',
                '低密度脂蛋白': '3.8mmol/L',
                '同型半胱氨酸': '16μmol/L'
            };
            return map[name] || '-';
        }

        function getRefRange(name) {
            const map = {
                '收缩压': '90-140mmHg',
                '舒张压': '60-90mmHg',
                '总胆固醇': '2.8-5.2mmol/L',
                '甘油三酯': '0.45-1.7mmol/L',
                '空腹血糖': '3.9-6.1mmol/L',
                '心率': '60-100次/分',
                '肌酸激酶': '25-200U/L',
                '低密度脂蛋白': '0-3.4mmol/L',
                '同型半胱氨酸': '0-15μmol/L'
            };
            return map[name] || '-';
        }

        function getFlag(name) {
            const abnormal = ['总胆固醇', '甘油三酯', '低密度脂蛋白', '同型半胱氨酸'];
            return abnormal.includes(name) ? '↑' : '正常';
        }

        // ==================== 页面切换 ====================
        function switchPage(pageName, navEl) {
            state.currentPage = pageName;
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            if (navEl) navEl.classList.add('active');
            renderPage();
            document.getElementById('mainContent').scrollTop = 0;
        }

        // ==================== 渲染引擎 ====================
        function renderPage() {
            const container = document.getElementById('mainContent');
            switch (state.currentPage) {
                case 'home':
                    container.innerHTML = renderHomePage();
                    break;
                case 'monitor':
                    container.innerHTML = renderMonitorPage();
                    break;
                case 'sync':
                    container.innerHTML = renderSyncPage();
                    break;
                case 'risk':
                    container.innerHTML = renderRiskPage();
                    break;
                case 'health':
                    container.innerHTML = renderHealthPage();
                    break;
                default:
                    container.innerHTML = renderHomePage();
            }
            attachEventListeners();
        }

        function attachEventListeners() {
            // 风险预测按钮
            const predictBtn = document.getElementById('btnPredictRisk');
            if (predictBtn) {
                predictBtn.addEventListener('click', () => {
                    const btn = predictBtn;
                    btn.textContent = '⏳ AI分析中...';
                    btn.disabled = true;
                    btn.style.opacity = '0.7';
                    setTimeout(() => {
                        state.riskResult = {
                            level: '极高危',
                            color: '#ef4444',
                            cssClass: 'critical',
                            reason: '近3天静息心率持续升高15%，合并血压昼夜节律异常，结合心脑血管家族史，心源性猝死、隐匿性冠心病风险显著升高。',
                            index: 85
                        };
                        state.userData.healthScore = Math.max(30, 100 - state.riskResult
                            .index);
                        renderPage();
                        document.getElementById('mainContent').scrollTop = 0;
                    }, 2000);
                });
            }

            // 实时监测按钮
            const monitorBtn = document.getElementById('btnStartMonitor');
            if (monitorBtn) {
                monitorBtn.addEventListener('click', () => {
                    startRealtimeMonitoring();
                });
            }

            // 体检报告上传
            const uploadInput = document.getElementById('uploadReport');
            if (uploadInput) {
                uploadInput.addEventListener('change', (e) => {
                    if (e.target.files.length > 0) {
                        simulateReportUpload();
                    }
                });
            }

            // Tab切换
            document.querySelectorAll('.tab').forEach(tab => {
                tab.addEventListener('click', function() {
                    const tabGroup = this.parentElement;
                    tabGroup.querySelectorAll('.tab').forEach(t => t.classList.remove(
                        'active'));
                    this.classList.add('active');
                    const tabName = this.dataset.tab;
                    showTabContent(tabName);
                });
            });
        }

        function showTabContent(tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            const target = document.getElementById('tab-' + tabName);
            if (target) target.style.display = 'block';
        }

        function startRealtimeMonitoring() {
            const statusEl = document.getElementById('monitorStatus');
            const hrEl = document.getElementById('realtimeHR');
            const bpEl = document.getElementById('realtimeBP');
            const spo2El = document.getElementById('realtimeSpO2');
            const alertEl = document.getElementById('monitorAlert');

            if (!statusEl) return;

            let count = 0;
            const maxCount = 30;
            statusEl.innerHTML =
                '<span style="color:#10b981;">🟢 监测运行中...</span>';

            const interval = setInterval(() => {
                count++;
                const isAbnormal = count > 18;
                const hr = isAbnormal ? Math.floor(Math.random() * 15) + 95 : Math.floor(Math.random() *
                    6) + 72;
                const bp = isAbnormal ? Math.floor(Math.random() * 15) + 145 : Math.floor(Math.random() *
                    8) + 125;
                const spo2 = isAbnormal ? (Math.random() * 2 + 93).toFixed(1) : (Math.random() * 2 + 97)
                    .toFixed(1);

                if (hrEl) hrEl.textContent = hr + ' 次/分';
                if (bpEl) bpEl.textContent = bp + ' mmHg';
                if (spo2El) spo2El.textContent = spo2 + ' %';

                if (isAbnormal && alertEl) {
                    statusEl.innerHTML = '<span style="color:#ef4444;">🔴 异常报警</span>';
                    alertEl.style.display = 'block';
                    alertEl.innerHTML =
                        '<div class="alert alert-danger">⚠️ 检测到心率、血压持续异常升高！已自动记录异常数据，建议立即停止活动，休息后复测，持续不适请立即就医！</div>';
                }

                if (count >= maxCount) {
                    clearInterval(interval);
                    statusEl.innerHTML = '<span style="color:#10b981;">✅ 监测完成</span>';
                }
            }, 600);
        }

        function simulateReportUpload() {
            const statusEl = document.getElementById('uploadStatus');
            if (statusEl) {
                statusEl.innerHTML =
                    '<div class="alert alert-info">⏳ 正在执行OCR文字识别→核心指标提取→异常值标注→数据同步至风险模型...</div>';
                setTimeout(() => {
                    statusEl.innerHTML =
                        '<div class="alert alert-success">✅ 报告解析完成！已提取核心健康指标，同步更新至AI风险模型</div>';
                    // 添加新报告
                    const newReport = {
                        date: new Date().toISOString().split('T')[0],
                        items: state.physicalReports[1].items.map(item => ({ ...item }))
                    };
                    state.physicalReports.push(newReport);
                    state.currentReportIdx = state.physicalReports.length - 1;
                    renderPage();
                }, 2500);
            }
        }

        // ==================== 页面渲染函数 ====================

        function renderHomePage() {
            const risk = state.riskResult;
            const user = state.userData;
            const recentData = state.healthData.slice(-3);
            const bpData = state.healthData;
            const hrData = state.healthData;

            return `
            <div class="page-header">
              <h1 class="page-title">🩺 预健·MED·AI 中青年急重症智能预警系统</h1>
              <p class="page-subtitle">基于多模态时序大数据与深度学习，实现急重症的早发现、早预警、早干预</p>
            </div>

            <!-- 顶部指标栏 -->
            <div class="metrics-row">
              <div class="metric-card danger">
                <div class="metric-label">当前风险等级</div>
                <div class="metric-value" style="color:${risk.color};">${risk.level}</div>
                <div class="metric-delta warning">⚠ 需紧急关注</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">覆盖并发症</div>
                <div class="metric-value">5大类28项</div>
                <div class="metric-delta normal">全面覆盖</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">数据更新时间</div>
                <div class="metric-value" style="font-size:1.2rem;">2026-04-25</div>
                <div class="metric-delta normal">实时同步</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">模型准确率</div>
                <div class="metric-value">93.2%</div>
                <div class="metric-delta normal">高精度</div>
              </div>
            </div>

            <!-- 主体两栏 -->
            <div class="grid-1-2">
              <!-- 左栏：用户档案 -->
              <div>
                <div class="card glow-blue">
                  <div class="card-header">
                    <span class="card-title"><span class="icon">👤</span> 用户健康档案</span>
                    <span class="card-badge info">可编辑</span>
                  </div>
                  <div class="progress-label">
                    <span>健康评分</span>
                    <span class="value">${user.healthScore}/100</span>
                  </div>
                  <div class="progress-bar">
                    <div class="fill ${user.healthScore < 60 ? 'danger' : user.healthScore < 75 ? 'warning' : 'success'}" style="width:${user.healthScore}%;"></div>
                  </div>
                  <hr class="divider-dashed">
                  <div class="input-group">
                    <label>年龄</label>
                    <input type="number" class="input-field" value="${user.age}" min="25" max="50" id="inputAge">
                  </div>
                  <div class="input-group">
                    <label>性别</label>
                    <select class="input-field" id="inputGender">
                      <option value="男" ${user.gender==='男'?'selected':''}>男</option>
                      <option value="女" ${user.gender==='女'?'selected':''}>女</option>
                    </select>
                  </div>
                  <div class="input-group">
                    <label>家族史</label>
                    <select class="input-field" id="inputFamilyHistory">
                      <option value="有心脑血管家族史" ${user.familyHistory==='有心脑血管家族史'?'selected':''}>有心脑血管家族史</option>
                      <option value="无相关家族史" ${user.familyHistory==='无相关家族史'?'selected':''}>无相关家族史</option>
                    </select>
                  </div>
                  <div class="input-group">
                    <label>生活习惯</label>
                    <textarea class="input-field" id="inputLifestyle">${user.lifestyle}</textarea>
                  </div>
                  <hr class="divider-dashed">
                  <p style="font-size:0.78rem;color:var(--text-muted);margin-bottom:8px;">✅ 已同步数据维度：血压 · 心率 · 睡眠 · 运动 · 饮食 · 情绪</p>
                  <button class="btn btn-primary" id="btnPredictRisk">🚀 启动AI深度风险评估</button>
                </div>
              </div>

              <!-- 右栏：健康趋势 -->
              <div>
                <div class="card">
                  <div class="card-header">
                    <span class="card-title"><span class="icon">📈</span> 核心健康指标趋势（近14天）</span>
                  </div>
                  <div class="tabs">
                    <span class="tab active" data-tab="bp">血压变化趋势</span>
                    <span class="tab" data-tab="hr">心率变化趋势</span>
                  </div>
                  <div class="tab-content" id="tab-bp" style="display:block;">
                    <div class="chart-placeholder">
                      <div class="chart-line" style="bottom:45%; background: linear-gradient(90deg, transparent, rgba(239,68,68,0.4) 15%, rgba(239,68,68,0.7) 50%, rgba(239,68,68,0.9) 85%, transparent);"></div>
                      <div class="chart-line" style="bottom:25%; background: linear-gradient(90deg, transparent, rgba(245,158,11,0.4) 15%, rgba(245,158,11,0.7) 50%, rgba(245,158,11,0.9) 85%, transparent);"></div>
                      <div class="chart-dot" style="bottom:48%; right:12%;"></div>
                      <span style="position:relative;z-index:1;">📊 收缩压（红）& 舒张压（橙）趋势图</span>
                    </div>
                    <p style="font-size:0.7rem;color:var(--text-muted);margin-top:6px;">* 正常参考值：90-140 / 60-90 mmHg</p>
                  </div>
                  <div class="tab-content" id="tab-hr" style="display:none;">
                    <div class="chart-placeholder">
                      <div class="chart-line" style="bottom:40%; background: linear-gradient(90deg, transparent, rgba(59,130,246,0.4) 15%, rgba(59,130,246,0.7) 50%, rgba(239,68,68,0.8) 85%, transparent);"></div>
                      <div class="chart-line" style="bottom:20%; background: linear-gradient(90deg, transparent, rgba(139,92,246,0.3) 20%, rgba(139,92,246,0.6) 60%, rgba(139,92,246,0.8) 85%, transparent);"></div>
                      <div class="chart-dot" style="bottom:43%; right:10%; background:#ef4444;"></div>
                      <span style="position:relative;z-index:1;">📊 日间静息心率（蓝）& 夜间心率（紫）趋势图</span>
                    </div>
                    <p style="font-size:0.7rem;color:var(--text-muted);margin-top:6px;">* 正常参考值：60-100 次/分</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 风险概览 -->
            <div class="card glow-red">
              <div class="card-header">
                <span class="card-title"><span class="icon">⚠️</span> 当前健康风险概览</span>
                <span class="card-badge danger">需关注</span>
              </div>
              <div class="grid-1-3">
                <div class="risk-display">
                  <div class="risk-level-badge ${risk.cssClass}">${risk.level}</div>
                  <div class="progress-label" style="margin-top:12px;justify-content:center;">
                    <span>风险指数：</span>
                    <span class="value">${risk.index}/100</span>
                  </div>
                  <div class="progress-bar" style="margin-top:6px;">
                    <div class="fill danger" style="width:${risk.index}%;"></div>
                  </div>
                </div>
                <div>
                  <div class="alert alert-danger">${risk.reason}</div>
                  <div class="alert alert-info">💡 提示：可点击左侧导航栏「风险预警中心」查看完整就医指导与干预方案</div>
                </div>
              </div>
            </div>
          `;
        }

        function renderMonitorPage() {
            return `
            <div class="page-header">
              <h1 class="page-title">📡 实时健康数据动态监测中心</h1>
              <p class="page-subtitle">模拟可穿戴设备7×24小时实时采集，AI自动识别异常并触发分级报警</p>
            </div>

            <div class="card glow-blue">
              <div class="card-header">
                <span class="card-title"><span class="icon">📡</span> 实时数据看板</span>
                <span id="monitorStatus" style="font-weight:600;">🟢 等待监测启动</span>
              </div>
              <div class="metrics-row" style="margin-bottom:12px;">
                <div class="metric-card">
                  <div class="metric-label">实时心率</div>
                  <div class="metric-value" id="realtimeHR">-- 次/分</div>
                  <div class="metric-delta normal">等待数据</div>
                </div>
                <div class="metric-card">
                  <div class="metric-label">实时收缩压</div>
                  <div class="metric-value" id="realtimeBP">-- mmHg</div>
                  <div class="metric-delta normal">等待数据</div>
                </div>
                <div class="metric-card">
                  <div class="metric-label">血氧饱和度</div>
                  <div class="metric-value" id="realtimeSpO2">-- %</div>
                  <div class="metric-delta normal">等待数据</div>
                </div>
                <div class="metric-card">
                  <div class="metric-label">监测状态</div>
                  <div class="metric-value" style="font-size:1rem;" id="monitorState">未启动</div>
                </div>
              </div>
              <div id="monitorAlert" style="display:none;"></div>
              <div class="chart-placeholder" style="height:200px;">
                <span>📊 实时数据波形图（启动监测后显示）</span>
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="card-title"><span class="icon">🎛️</span> 监测控制</span>
              </div>
              <button class="btn btn-primary" id="btnStartMonitor" style="width:auto;padding:14px 36px;">▶️ 启动实时监测</button>
              <p style="font-size:0.75rem;color:var(--text-muted);margin-top:8px;">* 模拟60秒监测过程，前30秒正常，后30秒模拟异常报警</p>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="card-title"><span class="icon">📌</span> 功能说明</span>
              </div>
              <div class="grid-3">
                <div style="text-align:center;padding:16px;">
                  <span style="font-size:2rem;">📡</span>
                  <p style="font-weight:600;margin:8px 0;">实时采集</p>
                  <p style="font-size:0.78rem;color:var(--text-secondary);">模拟智能可穿戴设备，每秒采集心率、血压、血氧核心生命体征数据</p>
                </div>
                <div style="text-align:center;padding:16px;">
                  <span style="font-size:2rem;">🤖</span>
                  <p style="font-weight:600;margin:8px 0;">AI异常识别</p>
                  <p style="font-size:0.78rem;color:var(--text-secondary);">基于训练好的深度学习模型，自动识别指标异常波动与趋势变化</p>
                </div>
                <div style="text-align:center;padding:16px;">
                  <span style="font-size:2rem;">🚨</span>
                  <p style="font-weight:600;margin:8px 0;">分级报警</p>
                  <p style="font-size:0.78rem;color:var(--text-secondary);">针对不同风险等级，触发对应级别的报警与干预建议，避免漏报误报</p>
                </div>
              </div>
            </div>
          `;
        }

        function renderSyncPage() {
            const latestReport = state.physicalReports[state.currentReportIdx];
            const abnormalCount = latestReport.items.filter(i => i.flag !== '正常').length;

            return `
            <div class="page-header">
              <h1 class="page-title">📊 多源健康数据同步中心</h1>
              <p class="page-subtitle">打通可穿戴设备、体检报告、居家检测全维度数据，打破健康数据孤岛</p>
            </div>

            <div class="grid-3">
              <!-- 可穿戴设备 -->
              <div class="card">
                <div class="card-header">
                  <span class="card-title"><span class="icon" style="color:#3b82f6;">⌚</span> 可穿戴设备同步</span>
                </div>
                <p style="font-size:0.78rem;color:var(--text-secondary);margin-bottom:10px;">✅ Apple Watch · 华为Watch · 小米手环 · OPPO Watch · 荣耀手环 · 华米Amazfit</p>
                <select class="input-field" style="margin-bottom:10px;">
                  <option>请选择设备品牌</option>
                  <option>苹果Apple</option>
                  <option>华为Huawei</option>
                  <option>小米Xiaomi</option>
                  <option>OPPO</option>
                  <option>荣耀</option>
                  <option>其他</option>
                </select>
                <button class="btn btn-outline btn-sm" style="margin-bottom:8px;">🔗 授权绑定设备</button>
                <hr class="divider-dashed">
                <p style="font-size:0.75rem;color:var(--text-muted);">当前同步状态</p>
                <div class="progress-bar"><div class="fill info" style="width:100%;"></div></div>
                <p style="font-size:0.7rem;color:var(--text-muted);margin-top:4px;">已同步 ${state.healthData.length} 天健康时序数据</p>
              </div>

              <!-- 体检报告 -->
              <div class="card">
                <div class="card-header">
                  <span class="card-title"><span class="icon" style="color:#8b5cf6;">📄</span> 体检报告智能解析</span>
                </div>
                <div style="display:flex;gap:20px;margin-bottom:10px;">
                  <div><strong style="font-size:1.3rem;">${state.physicalReports.length}</strong><br><span style="font-size:0.7rem;color:var(--text-muted);">累计解析报告</span></div>
                  <div><strong style="font-size:1.3rem;">${latestReport.items.length}</strong><br><span style="font-size:0.7rem;color:var(--text-muted);">提取核心指标</span></div>
                </div>
                <p style="font-size:0.75rem;color:var(--text-muted);">OCR识别准确率</p>
                <div class="progress-bar"><div class="fill success" style="width:98%;"></div></div>
                <p style="font-size:0.7rem;color:var(--text-muted);margin-top:4px;">98%</p>
                <hr class="divider-dashed">
                <label class="btn btn-outline btn-sm" style="cursor:pointer;display:inline-block;text-align:center;">
                  📤 上传新的体检报告
                  <input type="file" id="uploadReport" accept=".pdf,.png,.jpg" style="display:none;">
                </label>
                <div id="uploadStatus"></div>
              </div>

              <!-- 居家检测 -->
              <div class="card">
                <div class="card-header">
                  <span class="card-title"><span class="icon" style="color:#10b981;">🏠</span> 居家检测数据录入</span>
                </div>
                <p style="font-size:0.78rem;color:var(--text-secondary);">支持录入：血压、血糖、心率、尿酸、体重</p>
                <div style="display:flex;gap:20px;margin-bottom:10px;">
                  <div><strong style="font-size:1.3rem;">3条</strong><br><span style="font-size:0.7rem;color:var(--text-muted);">今日已录入</span></div>
                  <div><strong style="font-size:1.3rem;">7天</strong><br><span style="font-size:0.7rem;color:var(--text-muted);">连续录入</span></div>
                </div>
                <p style="font-size:0.75rem;color:var(--text-muted);">本月录入完成率</p>
                <div class="progress-bar"><div class="fill warning" style="width:70%;"></div></div>
                <p style="font-size:0.7rem;color:var(--text-muted);margin-top:4px;">70%</p>
                <hr class="divider-dashed">
                <div class="input-group"><label>今日收缩压（mmHg）</label><input type="number" class="input-field" value="135"></div>
                <div class="input-group"><label>今日舒张压（mmHg）</label><input type="number" class="input-field" value="88"></div>
                <div class="input-group"><label>今日静息心率（次/分）</label><input type="number" class="input-field" value="84"></div>
                <button class="btn btn-success btn-sm">💾 保存今日数据</button>
              </div>
            </div>

            <!-- 报告分析 -->
            <div class="card">
              <div class="card-header">
                <span class="card-title"><span class="icon">📋</span> 体检报告深度分析中心</span>
                <span class="card-badge ${abnormalCount > 0 ? 'danger' : 'success'}">${abnormalCount > 0 ? abnormalCount+'项异常' : '全部正常'}</span>
              </div>
              <div class="tabs">
                <span class="tab active" data-tab="latest">📄 最新报告详情</span>
                <span class="tab" data-tab="compare">📊 历史报告对比</span>
                <span class="tab" data-tab="advice">💡 异常指标解读</span>
              </div>
              <div class="tab-content" id="tab-latest" style="display:block;">
                <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:10px;">报告日期：<strong>${latestReport.date}</strong></p>
                <div class="table-wrapper">
                  <table>
                    <thead><tr><th>指标名称</th><th>检测结果</th><th>参考范围</th><th>异常标识</th></tr></thead>
                    <tbody>
                      ${latestReport.items.map(item => `
                        <tr>
                          <td>${item.name}</td>
                          <td>${item.result}</td>
                          <td style="color:var(--text-muted);">${item.refRange}</td>
                          <td><span class="${item.flag !== '正常' ? 'cell-abnormal' : 'cell-normal'}">${item.flag}</span></td>
                        </tr>
                      `).join('')}
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="tab-content" id="tab-compare" style="display:none;">
                <p style="color:var(--text-muted);">选择两份报告进行对比（功能演示中）</p>
                <div style="display:flex;gap:20px;">
                  <select class="input-field" style="flex:1;">
                    ${state.physicalReports.map((r,i) => `<option value="${i}" ${i===0?'selected':''}>报告 ${i+1} (${r.date})</option>`).join('')}
                  </select>
                  <select class="input-field" style="flex:1;">
                    ${state.physicalReports.map((r,i) => `<option value="${i}" ${i===state.physicalReports.length-1?'selected':''}>报告 ${i+1} (${r.date})</option>`).join('')}
                  </select>
                </div>
              </div>
              <div class="tab-content" id="tab-advice" style="display:none;">
                ${abnormalCount > 0 ? `
                  <div class="alert alert-warning">⚠️ 本次体检共发现 ${abnormalCount} 项异常指标，以下是专业解读与建议：</div>
                  ${latestReport.items.filter(i=>i.flag!=='正常').map(item => `
                    <div style="background:rgba(239,68,68,0.04);border:1px solid rgba(239,68,68,0.15);border-radius:10px;padding:14px;margin-bottom:8px;">
                      <strong style="color:#fca5a5;">🔴 ${item.name} ${item.flag}</strong>
                      <p style="font-size:0.82rem;margin:4px 0;">检测结果：${item.result}（参考范围：${item.refRange}）</p>
                      <p style="font-size:0.8rem;color:var(--text-secondary);">${getAdviceText(item.name, item.flag)}</p>
                    </div>
                  `).join('')}
                ` : '<div class="alert alert-success">✅ 本次体检未发现异常指标，继续保持良好的生活习惯！</div>'}
              </div>
            </div>
          `;
        }

        function getAdviceText(name, flag) {
            const advices = {
                '总胆固醇': { '↑': '建议严格控制高脂食物（动物内脏、肥肉），增加深海鱼、新鲜蔬果摄入，每日运动30分钟，3个月后复查血脂。' },
                '甘油三酯': { '↑': '建议严格控制甜食、酒精和精制碳水，增加膳食纤维摄入，每周至少150分钟中等强度运动。' },
                '低密度脂蛋白': { '↑': '这是心脑血管疾病的高危因素！建议立即启动低脂饮食，增加运动，必要时就医心内科启动药物干预。' },
                '同型半胱氨酸': { '↑': '这是心脑血管疾病的独立危险因素！建议补充叶酸、维生素B6/B12，增加新鲜蔬果摄入，定期复查。' },
                '收缩压': { '↑': '建议减少钠盐摄入（每日<5g），避免熬夜和情绪激动，每日监测血压2-3次，如持续高于140mmHg请及时就医心内科。' },
                '舒张压': { '↑': '建议加强有氧运动（每日30分钟快走），减少高脂饮食，规律作息，2周后复查血压。' },
                '心率': { '↑': '建议避免浓茶、咖啡，减少熬夜和精神紧张，每日进行冥想放松，如持续高于100次/分请就医。' },
                '空腹血糖': { '↑': '建议控制精制糖和主食摄入，增加全谷物和蔬菜，规律监测血糖，必要时就医内分泌科。' },
                '肌酸激酶': { '↑': '建议近期避免剧烈运动，休息1周后复查，如伴随胸痛、胸闷请立即就医。' }
            };
            return advices[name]?.[flag] || '建议携带报告前往医院相关科室咨询专业医生。';
        }

        function renderRiskPage() {
            const risk = state.riskResult;
            const user = state.userData;
            const recentData = state.healthData.slice(-3);

            return `
            <div class="page-header">
              <h1 class="page-title">⚠️ 隐匿性急重症智能风险预警报告</h1>
            </div>

            <div class="grid-1-3">
              <div class="card glow-red">
                <div class="card-header">
                  <span class="card-title"><span class="icon">🎯</span> 最终风险评级</span>
                </div>
                <div class="risk-display">
                  <div class="risk-level-badge ${risk.cssClass}">${risk.level}</div>
                  <div class="progress-label" style="margin-top:12px;justify-content:center;">
                    <span>风险指数：</span>
                    <span class="value">${risk.index}/100</span>
                  </div>
                  <div class="progress-bar" style="margin-top:6px;">
                    <div class="fill danger" style="width:${risk.index}%;"></div>
                  </div>
                </div>
                <hr class="divider-dashed">
                <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.8;">
                  <p>📅 预警时间：2026-04-25</p>
                  <p>📋 覆盖并发症：5大类28项</p>
                  <p>🎯 模型置信度：92.5%</p>
                </div>
                <hr class="divider-dashed">
                <p style="font-size:0.72rem;color:var(--text-muted);">🔴 极高危：需3天内紧急就医<br>🟠 中危：需2周内就医复诊<br>🟢 低危：常规健康维护即可</p>
              </div>

              <div class="card">
                <div class="card-header">
                  <span class="card-title"><span class="icon">🔍</span> 风险来源深度分析</span>
                </div>
                <div class="alert alert-danger">${risk.reason}</div>
                <p style="font-weight:600;margin-bottom:8px;">核心异常指标明细（近3天）：</p>
                <div class="table-wrapper">
                  <table>
                    <thead><tr><th>日期</th><th>静息心率</th><th>夜间心率</th><th>收缩压</th><th>舒张压</th></tr></thead>
                    <tbody>
                      ${recentData.map(d => `
                        <tr>
                          <td>${d.date}</td>
                          <td>${d.hrResting} 次/分</td>
                          <td>${d.hrNight} 次/分</td>
                          <td style="color:#fca5a5;font-weight:600;">${d.bpSystolic} mmHg</td>
                          <td>${d.bpDiastolic} mmHg</td>
                        </tr>
                      `).join('')}
                    </tbody>
                  </table>
                </div>
                <hr class="divider-dashed">
                <p style="font-weight:600;margin-bottom:8px;">风险权重占比</p>
                <div style="display:flex;gap:16px;flex-wrap:wrap;">
                  <span class="tag tag-red">家族史 40%</span>
                  <span class="tag tag-red">血压异常 35%</span>
                  <span class="tag tag-red">心率异常 20%</span>
                  <span class="tag tag-purple">生活习惯 5%</span>
                </div>
              </div>
            </div>

            <div class="card glow-red">
              <div class="card-header">
                <span class="card-title"><span class="icon">🏥</span> 精准就医指导与干预建议</span>
              </div>
              <div class="alert alert-danger" style="font-size:0.9rem;">
                ⚠️ 【极高危紧急响应】请立即启动以下流程：
              </div>
              <div class="grid-2">
                <div>
                  <p style="font-weight:700;">1. 紧急就医建议</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">请于<strong style="color:#fca5a5;">3天内</strong>前往三级医院心内科就诊，避免高强度活动、情绪激动，如有胸痛、胸闷立即拨打120</p>
                  <p style="font-weight:700;margin-top:12px;">2. 推荐检查项目</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">必查：24小时动态心电图、冠脉CTA、心肌酶谱、心脏超声、血脂全套<br>可选：冠脉造影、运动负荷试验</p>
                </div>
                <div>
                  <p style="font-weight:700;">3. 临时干预措施</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">立即停止熬夜、高强度工作，每日早中晚3次监测血压心率，保持情绪平稳，禁止剧烈运动</p>
                  <p style="font-weight:700;margin-top:12px;">4. 随访提醒</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">系统已自动生成7天后的复查提醒，就诊后可上传病历更新风险模型，重新评估风险等级</p>
                </div>
              </div>
            </div>
          `;
        }

        function renderHealthPage() {
            return `
            <div class="page-header">
              <h1 class="page-title">💊 个性化主动健康管理方案</h1>
            </div>

            <div class="grid-2">
              <div>
                <div class="card">
                  <div class="card-header">
                    <span class="card-title"><span class="icon">📅</span> 个性化随访计划</span>
                  </div>
                  <div class="progress-label">
                    <span>本周完成进度</span>
                    <span class="value">1/5</span>
                  </div>
                  <div class="progress-bar"><div class="fill info" style="width:20%;"></div></div>
                  <hr class="divider-dashed">
                  <p style="font-size:0.82rem;">✅ <strong>今日待完成：</strong>测量血压心率并上传系统</p>
                  <p style="font-size:0.82rem;">⏰ <strong>明日提醒：</strong>心内科就诊预约</p>
                  <p style="font-size:0.82rem;">📅 <strong>7天后：</strong>就诊后复查提醒+风险重评估</p>
                  <p style="font-size:0.82rem;">📅 <strong>14天后：</strong>第二次风险等级复核</p>
                  <p style="font-size:0.82rem;">📅 <strong>30天后：</strong>全面健康评估+方案调整</p>
                  <hr class="divider-dashed">
                  <p style="font-weight:600;">随访打卡日历：</p>
                  <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <span style="background:rgba(16,185,129,0.15);color:#6ee7b7;padding:8px 12px;border-radius:8px;font-size:0.78rem;">一 ✅</span>
                    <span style="background:rgba(255,255,255,0.03);padding:8px 12px;border-radius:8px;font-size:0.78rem;">二 ⭕</span>
                    <span style="background:rgba(255,255,255,0.03);padding:8px 12px;border-radius:8px;font-size:0.78rem;">三 ⭕</span>
                    <span style="background:rgba(255,255,255,0.03);padding:8px 12px;border-radius:8px;font-size:0.78rem;">四 ⭕</span>
                    <span style="background:rgba(255,255,255,0.03);padding:8px 12px;border-radius:8px;font-size:0.78rem;">五 ⭕</span>
                    <span style="background:rgba(255,255,255,0.03);padding:8px 12px;border-radius:8px;font-size:0.78rem;">六 ⭕</span>
                    <span style="background:rgba(255,255,255,0.03);padding:8px 12px;border-radius:8px;font-size:0.78rem;">日 ⭕</span>
                  </div>
                </div>

                <div class="card">
                  <div class="card-header">
                    <span class="card-title"><span class="icon">📚</span> 今日健康科普</span>
                  </div>
                  <div class="alert alert-info">
                    <strong>【心源性猝死的3个早期隐匿信号】</strong><br>
                    1. 不明原因的持续疲劳乏力，休息后无法缓解；<br>
                    2. 夜间静息心率持续升高超过10%，波动幅度大；<br>
                    3. 活动后胸闷气短加重，伴随左肩、后背放射性疼痛。
                  </div>
                  <p style="font-size:0.75rem;color:var(--text-muted);">权威参考：</p>
                  <p style="font-size:0.72rem;color:var(--text-muted);">• 《中国心源性猝死防治指南2024》<br>• 《中青年高血压管理专家共识》</p>
                </div>
              </div>

              <div>
                <div class="card">
                  <div class="card-header">
                    <span class="card-title"><span class="icon">🥗</span> 个体化生活方式干预方案</span>
                  </div>
                  <p style="font-weight:700;">🛌 作息调整</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">每日23:00前入睡，保证7.5小时睡眠，禁止熬夜，午间可休息20-30分钟</p>
                  <p style="font-weight:700;margin-top:10px;">🏃 运动建议</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">每日进行30分钟中等强度有氧运动（快走、慢跑、游泳、骑行），避免高强度剧烈运动，每周至少5天</p>
                  <p style="font-weight:700;margin-top:10px;">🍎 饮食调整</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">每日钠盐摄入不超过5g，减少高脂、高糖、高嘌呤食物，增加新鲜蔬果、优质蛋白、膳食纤维摄入，每日饮水1500-2000ml</p>
                  <p style="font-weight:700;margin-top:10px;">🧘 压力管理</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">每日进行10分钟冥想放松训练，减少连续工作时长，每工作1小时休息10分钟，避免长期精神紧张</p>
                  <p style="font-weight:700;margin-top:10px;">🚭 烟酒控制</p>
                  <p style="font-size:0.82rem;color:var(--text-secondary);">禁止吸烟，限制酒精摄入，每周饮酒不超过1次，男性每日酒精摄入不超过25g，女性不超过15g</p>
                </div>

                <div class="card">
                  <div class="card-header">
                    <span class="card-title"><span class="icon">🔔</span> 用药与复查提醒</span>
                  </div>
                  <p style="font-size:0.82rem;">📌 <strong>每日提醒：</strong>早8点、晚8点测量血压心率并上传系统</p>
                  <p style="font-size:0.82rem;">📌 <strong>复查提醒：</strong>心内科就诊，完善24小时动态心电图、冠脉CTA检查</p>
                  <p style="font-size:0.82rem;">📌 <strong>体检提醒：</strong>年度全面体检，重点关注心血管、血脂、血糖相关指标</p>
                  <hr class="divider-dashed">
                  <button class="btn btn-primary btn-sm" style="width:auto;">🔔 开启微信提醒</button>
                </div>
              </div>
            </div>

            <div class="alert alert-info" style="margin-top:16px;">
              📌 <strong>方案说明：</strong>本管理方案基于您的风险等级、健康数据、生活习惯，由AI模型自动生成，会根据您每日上传的监测数据动态调整，实现全周期闭环健康管理；所有建议均参考《中国心血管病防治指南》制定，仅供参考，具体诊疗请遵医嘱。
            </div>
          `;
        }

        // ==================== 初始化 ====================
        document.addEventListener('DOMContentLoaded', () => {
            renderPage();
        });

        // 监听hash变化
        window.addEventListener('hashchange', () => {
            const hash = window.location.hash.replace('#', '');
            const pageMap = {
                'home': 'home',
                'monitor': 'monitor',
                'sync': 'sync',
                'risk': 'risk',
                'health': 'health'
            };
            const page = pageMap[hash] || 'home';
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(el => el.classList.remove('active'));
            const targetNav = document.querySelector(`.nav-item[href="#${hash}"]`);
            if (targetNav) targetNav.classList.add('active');
            state.currentPage = page;
            renderPage();
            document.getElementById('mainContent').scrollTop = 0;
        });

        // 初始化hash
        if (!window.location.hash) {
            window.location.hash = 'home';
        } else {
            window.dispatchEvent(new HashChangeEvent('hashchange'));
        }
    </script>
</body>
</html>
