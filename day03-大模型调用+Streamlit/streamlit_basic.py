import streamlit as st
st.set_page_config(
    page_title="streamlit学习",
    page_icon="1",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)
st.title("大标题")
st.header("一级标题")
st.subheader("二级标题")

st.write("aaaaa")
st.write("bbbbb")
st.write("ccccc")

st.image("./resources/image1.png")
st.image("./resources/image2.png")

#st.audio()

#st.video()

#st.logo()

test_table = {
    "表头":["1","2","3"],
    "表头2":["4","5","6"],
    "表头3":["7","8","9"],
}
st.table(test_table)

name = st.text_input("请输入")
st.write(f"输入内容是{name}")

if st.button("点我"):
    st.success(f"按钮被点击了！你输入的是：{name}")
    st.balloons()

 
