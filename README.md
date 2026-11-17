# Python 기술 자기평가 증빙용 대시보드

Python으로 광고 데이터와 영상 프레임을 처리하고 결과를 Streamlit으로 시각화한 실행형 데모입니다.

- **글로벌 광고 성과 분석** · Pandas로 가상 광고 CSV를 집계합니다. ROAS, CTR, CPC, CPA, 캠페인 비교 차트 2개, 집계표와 요약을 표시합니다.
- **OpenCV 영상 분석** · OpenCV와 NumPy로 합성 영상의 녹색 이동 객체를 프레임별로 검출합니다. 입력 영상, 검출 박스와 프레임별 통계를 표시합니다.

두 앱 모두 가상 샘플을 사용합니다.

## 로컬 실행

Python 3.12 환경에서 저장소 루트로 이동해 실행할 앱의 명령을 사용합니다.

```bash
python -m pip install -r 01_ad_performance/requirements.txt
python -m streamlit run 01_ad_performance/app.py
```

```bash
python -m pip install -r 02_opencv_demo/requirements.txt
python -m streamlit run 02_opencv_demo/app.py
```
