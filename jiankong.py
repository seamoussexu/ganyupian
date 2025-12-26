import streamlit as st
import akshare as ak
import pandas as pd
import time

# 1. 网页标题和配置
st.set_page_config(page_title="基差监控", page_icon="📈")
st.title("📈 股指期货实时基差")

# 自动刷新按钮
if st.button('🔄 点击手动刷新'):
    st.rerun()

# 显示加载状态
status_text = st.empty()
status_text.text("⏳ 正在连接交易所数据...")

try:
    # 2. 获取数据 (复用刚才成功的逻辑)
    spot_df = ak.stock_zh_index_spot_em()
    
    # 定义目标
    targets = [
        {"name": "上证50", "spot_code": "000016", "future_code": "IH0", "label": "IH (主力)"},
        {"name": "沪深300", "spot_code": "000300", "future_code": "IF0", "label": "IF (主力)"},
        {"name": "中证500", "spot_code": "000905", "future_code": "IC0", "label": "IC (主力)"},
        {"name": "中证1000", "spot_code": "000852", "future_code": "IM0", "label": "IM (主力)"},
    ]
    
    results = []
    
    for t in targets:
        # A. 现货
        spot_row = spot_df[spot_df['代码'] == t['spot_code']]
        spot_price = float(spot_row['最新价'].values[0]) if not spot_row.empty else 0.0
        
        # B. 期货 (使用稳定的分钟接口)
        # 注意：这里我们只取最新一分钟的收盘价作为参考
        kline_df = ak.futures_zh_minute_sina(symbol=t['future_code'], period="1")
        futures_price = float(kline_df.iloc[-1]['close'])
        
        # C. 计算
        basis = spot_price - futures_price
        basis_rate = (basis / spot_price) * 100 # 贴水率%
        
        results.append({
            "品种": t['label'],
            "现货价格": f"{spot_price:.2f}",
            "期货价格": f"{futures_price:.2f}",
            "基差": f"{basis:.2f}",
            "贴水率": f"{basis_rate:.2f}%"
        })

    # 3. 转换为表格并展示
    df_show = pd.DataFrame(results)
    
    # 移除加载提示
    status_text.empty()
    
    # 使用 Streamlit 原生表格展示
    st.dataframe(df_show, use_container_width=True)
    
    # 显示最后更新时间
    st.caption(f"最后更新: {time.strftime('%H:%M:%S')}")

except Exception as e:
    st.error(f"数据获取失败: {e}")