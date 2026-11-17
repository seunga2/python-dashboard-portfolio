from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title='글로벌 광고 성과 분석', page_icon='📊', layout='wide')
st.title('📊 글로벌 광고 성과 분석 대시보드')
st.caption('Python · Pandas · Streamlit | 포트폴리오 데모 (기본 데이터는 가상 데이터)')

SAMPLE_CSV = Path(__file__).with_name('sample_data.csv')

uploaded = st.file_uploader('내 CSV로 분석하기 (선택)', type=['csv'])
if uploaded:
    try:
        df = pd.read_csv(uploaded)
        required = {'date','channel','impressions','clicks','spend','orders','revenue'}
        if not required.issubset(df.columns):
            st.error('필수 열: ' + ', '.join(sorted(required)))
            st.stop()
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        for c in ['impressions','clicks','spend','orders','revenue']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        df = df.dropna(subset=['date'])
    except Exception as exc:
        st.error(f'CSV를 읽을 수 없습니다: {exc}')
        st.stop()
else:
    df = pd.read_csv(SAMPLE_CSV, parse_dates=['date'])
    st.info('현재 가상 샘플 데이터를 표시 중입니다. 실제 프로젝트 원본 성과가 아닙니다.')

# Preserve support for earlier CSVs that only include a channel column.
if 'campaign' not in df:
    df['campaign'] = df['channel']
else:
    df['campaign'] = df['campaign'].fillna(df['channel'])

selected = st.multiselect('광고 채널', sorted(df.channel.dropna().unique()), default=sorted(df.channel.dropna().unique()))
view = df[df.channel.isin(selected)]
if view.empty:
    st.warning('표시할 채널을 선택하세요.')
    st.stop()

spend, revenue, clicks, impressions, orders = [view[c].sum() for c in ['spend','revenue','clicks','impressions','orders']]
roas = revenue/spend if spend else 0
ctr = clicks/impressions*100 if impressions else 0
cpc = spend/clicks if clicks else 0
cpa = spend/orders if orders else 0
cols=st.columns(4)
for col, lab, val in zip(cols,['ROAS','CTR','CPC','CPA'],[f'{roas:.2f}x',f'{ctr:.2f}%',f'₩{cpc:,.0f}',f'₩{cpa:,.0f}']):
    col.metric(lab,val)

agg = view.groupby('campaign')[['impressions', 'clicks', 'spend', 'orders', 'revenue']].sum()
agg['ROAS'] = (agg.revenue / agg.spend.where(agg.spend > 0)).round(2)
agg['CTR (%)'] = (agg.clicks / agg.impressions.where(agg.impressions > 0) * 100).round(2)

st.subheader('캠페인별 매출 및 광고비 (원)')
st.bar_chart(agg[['revenue', 'spend']], stack=False)
st.subheader('캠페인별 ROAS (배)')
st.bar_chart(agg['ROAS'].fillna(0).sort_values(ascending=False))
st.subheader('캠페인별 집계')
st.dataframe(agg.sort_values('ROAS', ascending=False), width='stretch')

ranked = agg['ROAS'].dropna()
if not ranked.empty:
    best = ranked.idxmax()
    st.success(f'선택한 채널에서 {best} 캠페인의 ROAS가 {ranked[best]:.2f}배로 가장 높습니다.')
else:
    st.info('광고비가 있는 캠페인의 ROAS를 비교할 수 있습니다.')

with st.expander('데이터 컬럼 형식'):
    st.code('date,channel,impressions,clicks,spend,orders,revenue')
    st.caption('campaign 열을 생략하면 채널 이름으로 집계합니다.')
    st.download_button('샘플 CSV 받기', SAMPLE_CSV.read_bytes(), SAMPLE_CSV.name, 'text/csv')
