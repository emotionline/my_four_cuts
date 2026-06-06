import streamlit as st
from PIL import Image, ImageOps
import io

# 1. 웹페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="나만의 인생네컷 제작소", layout="centered")

st.title("📸 온라인 인생네컷 제작소")
st.write("사진 4장을 업로드하면 인생네컷 스타일로 합쳐줍니다!")

# 2. 파일 업로드 컴포넌트
uploaded_files = st.file_uploader(
    "사진 4장을 선택해주세요 (JPG, PNG, WEBP 지원)", 
    type=['png', 'jpg', 'jpeg', 'webp'], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"현재 선택된 사진: {len(uploaded_files)}장")
    
    # 정확히 4장일 때만 작동
    if len(uploaded_files) == 4:
        if st.button("✨ 인생네컷 생성하기", use_container_width=True):
            try:
                # 디자인 상수 정의 (4:3 비율 프레임)
                img_w, img_h = 400, 300  
                margin = 20
                logo_space = 80
                
                frame_w = img_w + (margin * 2)
                frame_h = (img_h * 4) + (margin * 5) + logo_space
                
                # 흰색 배경 프레임 생성
                frame = Image.new("RGB", (frame_w, frame_h), color="white")
                
                # 이미지 크롭 및 순서대로 합성
                for i, uploaded_file in enumerate(uploaded_files):
                    img = Image.open(uploaded_file)
                    img = ImageOps.exif_transpose(img)  # 스마트폰 사진 회전 방지
                    img = ImageOps.fit(img, (img_w, img_h), Image.Resampling.LANCZOS)
                    
                    y_offset = margin + i * (img_h + margin)
                    frame.paste(img, (margin, y_offset))
                
                # 웹 화면에 결과물 미리보기 출력
                st.success("인생네컷이 완성되었습니다! 아래에서 다운로드하세요.")
                st.image(frame, caption="완성된 이미지 미리보기", use_container_width=True)
                
                # 다운로드 버튼 생성을 위한 메모리 버퍼 변환
                img_buffer = io.BytesIO()
                frame.save(img_buffer, format="PNG")
                img_bytes = img_buffer.getvalue()
                
                # 웹 다운로드 버튼
                st.download_button(
                    label="💾 인생네컷 이미지 다운로드",
                    data=img_bytes,
                    file_name="life_four_cuts.png",
                    mime="image/png",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"이미지 처리 중 오류가 발생했습니다: {e}")
                
    elif len(uploaded_files) > 4:
        st.error("사진이 4장을 초과했습니다. 정확히 4장만 선택해주세요!")