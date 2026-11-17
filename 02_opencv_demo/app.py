from pathlib import Path
import cv2
import numpy as np
import streamlit as st

st.set_page_config(page_title='OpenCV 영상 처리 데모', page_icon='🎥', layout='wide')
st.title('🎥 OpenCV 영상 처리 데모')
st.caption('Python · OpenCV · NumPy')

st.subheader('사전 처리된 검출·추적 시연')
st.caption('제작자가 만든 시연 영상입니다. 검출 박스, 추적 ID, 대기 구역과 집계가 영상에 표시됩니다.')
st.video(Path(__file__).with_name('detection_demo.mp4').read_bytes())

@st.cache_data(show_spinner=False)
def analyze_video():
    path = Path(__file__).with_name('sample_video.mp4')
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError('샘플 영상을 열 수 없습니다.')
    frames = []
    counts = []
    while True:
        ok, frame=cap.read()
        if not ok: break
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,np.array([35,90,70]),np.array([85,255,255]))
        contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        n=0
        for cnt in contours:
            if cv2.contourArea(cnt)<100: continue
            x,y,w,h=cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,200,255),2)
            cv2.putText(frame,'Object',(x,max(16,y-6)),cv2.FONT_HERSHEY_SIMPLEX,.45,(255,255,255),1)
            n+=1
        cv2.line(frame,(160,0),(160,240),(240,150,80),2)
        cv2.putText(frame,f'Objects: {n}',(8,22),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2)
        frames.append(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        counts.append(n)
    cap.release()
    if not frames:
        raise RuntimeError('샘플 영상에 읽을 수 있는 프레임이 없습니다.')
    return frames, counts

with st.expander('OpenCV 처리 과정 보기', expanded=False):
    st.caption('OpenCV가 가상 영상의 녹색 객체를 프레임별로 검출합니다.')
    try:
        frames, counts=analyze_video()
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    source, result = st.columns(2)
    with source:
        st.subheader('입력 영상')
        st.video(Path(__file__).with_name('sample_video.mp4').read_bytes())
    with result:
        st.subheader('분석 결과')
        idx = st.slider('프레임 이동', 0, len(frames) - 1, 0) if len(frames) > 1 else 0
        st.image(frames[idx], caption=f'{idx + 1}번째 프레임 · 검출 객체 {counts[idx]}개')

    st.subheader('검출 통계')
    total, detected, peak = st.columns(3)
    total.metric('분석 프레임', len(frames))
    detected.metric('객체가 검출된 프레임', sum(count > 0 for count in counts))
    peak.metric('한 프레임의 최대 검출 객체', max(counts))
    st.line_chart({'검출 객체 수': counts}, x_label='프레임 인덱스')
    st.caption('OpenCV가 각 프레임을 HSV로 변환한 뒤 녹색 영역의 외곽선을 찾아 박스로 표시합니다.')
