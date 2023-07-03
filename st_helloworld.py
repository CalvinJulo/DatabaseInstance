# coding=utf-8

import streamlit as st

from PIL import Image, ImageDraw, ImageEnhance, ImageColor, ImageFilter, ImageOps, ImageFont
from io import BytesIO
st.set_page_config(page_title="图形处理 App", page_icon="🧊", layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'Report a bug': "https://www.extremelycoolapp.com/bug",
                       'About': "# This is a header. This is an *extremely* cool app!"})
st.write('## Welcome to Image World  😁😭😊❤️'+'\n'+'***')

sessionState_List = ['img']
for i in sessionState_List:
    if i not in st.session_state:
        st.session_state[i] = ''

col0_0, col0_1, col0_2 = st.columns([2, 1, 1])
with col0_0:
    with st.form('Please Input Image'):
        img_url = st.text_input('Input image Url', '')
        img_local = st.file_uploader('upload image local')
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.session_state.img = img_url
            st.write(img_url)
            st.session_state.img = Image.open(img_local)
    img_original = st.session_state.img
    img = img_original.copy()
with col0_1:
    st.image(img_original)
with col0_2:
    st.write('Filename:', img_original.filename)
    st.write('Size:', img_original.size)
    st.write('Width:', img_original.width)
    st.write('Height:', img_original.height)
    st.write('Palette:', img_original.palette)
    st.write('Mode:', img_original.mode)
    st.write('Format:', img_original.format)
    # st.write('Info:',img.info)
st.write('***')
col1_0, col1_1, col1_2, col1_3, col1_4, col1_5, col1_6 = st.columns(7)
with col1_0:
    c0 = st.checkbox('Resize')
    if c0:
        st.write('***')
        with st.container():
            restrict = st.checkbox('Restrict')
            width, height = img_original.size[0], img_original.size[1]
            if restrict:
                width = st.number_input('Width (px)', value=width)
                height = int(width * img_original.size[1] / img_original.size[0])
                height = st.number_input('Height (px)', value=height)
            else:
                width = st.number_input('Width (px)', value=width)
                height = st.number_input('Height (px)', value=height)
            img = img.resize((int(width), int(height)))
        with st.container():
            transpose = st.checkbox('Transpose R/L')
            if transpose:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            rotate_slider = st.slider(label="Rotate_silder", min_value=0, max_value=360, value=0)
            rotate = st.number_input('Rotate_number', min_value=0, max_value=360, value=rotate_slider)
            img = img.rotate(rotate)

with col1_1:
    c1 = st.checkbox('Crop')
    if c1:
        st.write('***')
        left_right = st.slider(label="Left_Right", min_value=0, max_value=img.size[0], value=(0, img.size[0]))
        upper_lower = st.slider(label="Upper_Lower", min_value=0, max_value=img.size[1], value=(0, img.size[1]))
        box = st.text_input('Box', value=f'{left_right[0]},{upper_lower[0]},{left_right[1]},{upper_lower[1]}')
        img = img.crop([int(i) for i in box.split(',')])
with col1_2:
    c2 = st.checkbox('Enhance')
    if c2:
        st.write('***')
        Color = st.slider(label="Color", min_value=-100, max_value=100, value=1)
        img = ImageEnhance.Color(img).enhance(Color)  # 颜色增强
        Contrast = st.slider(label="Contrast", min_value=-100, max_value=100, value=1)
        img = ImageEnhance.Contrast(img).enhance(Contrast)  # 对比度增强
        Brightness = st.slider(label="Brightness", min_value=-100, max_value=100, value=1)
        img = ImageEnhance.Brightness(img).enhance(Brightness)  # 亮度增强
        Sharpness = st.slider(label="Sharpness", min_value=-100, max_value=100, value=1)
        img = ImageEnhance.Sharpness(img).enhance(Sharpness)  # 图像锐化
        st.write("img.convert('L')")
with col1_3:
    c3 = st.checkbox('Filter')
    if c3:
        st.write('***')
        BoxBlur = st.slider(label="BoxBlur", min_value=-100, max_value=100, value=0)
        img = img.filter(ImageFilter.BoxBlur(BoxBlur))  # 模糊图像
        GaussianBlur = st.slider(label="GaussianBlur", min_value=-100, max_value=100, value=0)
        img = img.filter(ImageFilter.GaussianBlur(GaussianBlur))  # 高斯模糊
        CONTOUR = st.slider(label="CONTOUR", min_value=-100, max_value=100, value=0)
        img = img.filter(ImageFilter.CONTOUR)  # 轮廓滤波
        MedianFilter = st.slider(label="MedianFilter", min_value=-100, max_value=100, value=1)
        img = img.filter(ImageFilter.MedianFilter(MedianFilter))  # 中值滤波
with col1_4:
    c4 = st.checkbox('Draw')
    if c4:
        st.write('***')
        st.write('**Paste Image**')
        bg_color = st.color_picker(label='bg_color', value='#000000')
        text_color = st.color_picker('text_color', value='#FFFFFF')
        Paste_width = st.slider(label="Paste_width", min_value=0, max_value=img.size[0], value=int(img.size[0]/10))
        Paste_height = st.slider(label="Paste_height", min_value=0, max_value=img.size[1], value=int(img.size[1]/10))
        img_fig = Image.new('RGB', [Paste_width, Paste_height], bg_color)  # (255, 255, 255)
        img_draw = ImageDraw.Draw(img_fig)
        text = st.text_input('Input text', 'This is text')
        img_draw.text(xy=(10, 2), text=text, fill=text_color)
        # st.image(img_fig)
        paste = st.checkbox('Paste')
        if paste:
            pos_left = st.slider(label="Pos_left", min_value=0, max_value=img.size[0], value=int(img.size[0] / 10))
            pos_top = st.slider(label="Pos_top", min_value=0, max_value=img.size[1],
                                value=int(img.size[1] / 10))
            img.paste(img_fig, [pos_left, pos_top])

with col1_6:
    c6 = st.checkbox('CV')
    if c6:
        st.write('***')
        s1 = st.slider(label="像素的邻域直径", min_value=0, max_value=255, value=10)
        s2 = st.slider(label="颜色空间的标准方差，一般尽可能大", min_value=10, max_value=255, value=250)
        s3 = st.slider(label="坐标空间的标准方差(像素单位)，一般尽可能小", min_value=0, max_value=255, value=250)
        s4 = st.slider(label="图像平滑参数", min_value=0, max_value=200, value=60)
        s5 = st.slider(label="颜色平衡度，数值越大，同颜色的区域就会越大", min_value=0.00, max_value=1.00, value=0.05)
        s6 = st.slider(label="铅笔画亮度参数，值越大，图像越亮", min_value=0.00, max_value=0.10, value=0.05)
with col1_4:
    st.empty()
with col1_5:
    st.empty()
st.write('***')
col2_0, col2_1, col2_2, col2_3 = st.columns(4)
with col2_0:
    st.image(img)
with col2_1:
    st.write('Filename:', 'New')
    st.write('Size:', img.size)
    st.write('Mode:', img.mode)
    st.write('Format:', img.format)
    bytesIO=BytesIO()
    img.save(bytesIO, format='PNG')
    st.download_button('Save', data=bytesIO.getvalue(), file_name='test.png')
with col2_2:
    st.image(img_fig)
