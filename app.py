import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة الاحترافية والحديثة
st.set_page_config(
    page_title="ICU Riyadh | Performance Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# كود الواجهة العصري بلمسات "Glassmorphism" و "Neon" (HTML/CSS/JS)
dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-base: #0a0e17;
            --glass-base: rgba(30, 41, 59, 0.6);
            --glass-accent: rgba(56, 189, 248, 0.1);
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
            --neon-cyan: #38bdf8;
            --neon-rose: #fb7185;
            --font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            font-family: var(--font-family);
            background-color: var(--bg-base);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            overflow-x: hidden;
            display: flex;
            justify-content: center;
        }

        .dashboard-wrapper {
            width: 100%;
            max-width: 1300px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* رأس الصفحة العصري */
        .modern-header {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            background: var(--glass-base);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .title-group h1 { margin: 0; font-size: 1.6rem; color: var(--neon-cyan); text-shadow: 0 0 10px rgba(56, 189, 248, 0.4); }
        .title-group p { margin: 5px 0 0 0; color: var(--text-dim); font-size: 0.9rem; }
        
        .q-badge-modern {
            background: var(--neon-cyan);
            color: #0a0e17;
            padding: 10px 30px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 1.3rem;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
            transition: all 0.3s;
        }

        /* شبكة الكروت "Glassmorphism" الـ 8 */
        .modern-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            width: 100%;
            margin-bottom: 30px;
        }

        .modern-card {
            background: var(--glass-base);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.03);
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            position: relative;
            overflow: hidden;
        }

        .modern-card:hover { 
            transform: translateY(-8px); 
            border-color: rgba(56, 189, 248, 0.3); 
            background: var(--glass-accent);
            box-shadow: 0 10px 30px rgba(56, 189, 248, 0.1);
        }

        .stat-circle-modern {
            width: 110px;
            height: 110px;
            border-radius: 50%;
            border: 5px solid rgba(255, 255, 255, 0.05);
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            font-weight
