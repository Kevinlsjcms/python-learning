# ============================================================
# 导入模块
# ============================================================
import streamlit as st          # Web 应用框架，用于构建聊天界面
import os                       # 文件/目录操作
import sys                      # 系统相关，用于修复编码问题
from openai import OpenAI       # OpenAI SDK，兼容 DeepSeek 等 API
from datetime import datetime   # 生成会话时间戳
import json                     # JSON 序列化，用于保存/加载会话

# 修复 Windows 下 GBK 编码无法输出 emoji 的问题
# Windows 终端默认使用 GBK 编码，emoji 字符会导致编码错误
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ============================================================
# Streamlit 页面配置
# ============================================================
st.set_page_config(
    page_title="AI Partner",                # 浏览器标签页标题
    page_icon="💀",                          # 标签页图标
    layout="wide",                          # 宽屏布局，聊天区域更宽敞
    initial_sidebar_state="expanded",       # 默认展开侧边栏
    menu_items={}                           # 隐藏右上角的 Streamlit 默认菜单
)

# ============================================================
# 工具函数
# ============================================================

def generate_session_name():
    """生成唯一会话名称，基于当前时间。
    格式: 2026-06-21_14-30-05（年-月-日_时-分-秒）
    注意: Windows 文件名不能包含冒号，所以用连字符替代。
    """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def save_session():
    """将当前会话状态保存为 JSON 文件。
    保存内容包括: 昵称、性格、会话名称、聊天记录。
    文件保存在 session/ 目录下，以会话名称命名。
    """
    # 仅在存在有效会话名称时保存
    if st.session_state.current_session:
        # 构建要保存的会话数据字典
        session_state = {
            "nick_name": st.session_state.nick_name,           # 伴侣昵称
            "nature": st.session_state.nature,                 # 伴侣性格描述
            "current_session": st.session_state.current_session, # 会话标识
            "messages": st.session_state.messages               # 完整聊天记录
        }
        # 如果 session 目录不存在，则创建
        if not os.path.exists("session"):
            os.mkdir("session")
        # 写入 JSON 文件，ensure_ascii=False 保证中文正常显示
        with open(f"session/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_state, f, ensure_ascii=False, indent=2)


def load_sessions():
    """扫描 session/ 目录，返回所有历史会话名称列表。
    按时间倒序排列（最新的在前）。
    """
    session_list = []
    if os.path.exists("session"):
        file_list = os.listdir("session")           # 列出 session 目录下所有文件
        for filename in file_list:
            if filename.endswith(".json"):          # 只处理 .json 文件
                session_list.append(filename[:-5])  # 去掉末尾的 .json 后缀
    session_list.sort(reverse=True)                 # 降序排列，最新的会话在最上面
    return session_list


def load_session(session_name):
    """根据会话名称加载历史会话。
    从对应的 JSON 文件中恢复昵称、性格、聊天记录等状态。
    """
    try:
        if os.path.exists(f"session/{session_name}.json"):
            with open(f"session/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)                              # 读取 JSON 数据
                st.session_state.nick_name = session_data["nick_name"]   # 恢复昵称
                st.session_state.nature = session_data["nature"]          # 恢复性格
                st.session_state.current_session = session_name           # 切换到该会话
                st.session_state.messages = session_data["messages"]      # 恢复聊天记录
    except Exception as e:
        st.error("加载失败", e)


def delete_session(session_name):
    """删除指定会话的 JSON 文件。
    如果删除的是当前正在使用的会话，则自动创建新会话。
    """
    try:
        if os.path.exists(f"session/{session_name}.json"):
            os.remove(f"session/{session_name}.json")  # 删除 JSON 文件
            # 如果删除的是当前会话，重置为全新会话
            if session_name == st.session_state.current_session:
                st.session_state.messages = []                            # 清空聊天记录
                st.session_state.current_session = generate_session_name() # 生成新会话标识
    except Exception as e:
        st.error("删除失败", e)


# ============================================================
# 页面主体
# ============================================================

st.title("AI Partner")              # 页面大标题
st.logo("resources/logo.png")       # 页面左上角 Logo

# ------------------------------------------------------------
# 系统提示词（AI 角色设定）
# ------------------------------------------------------------
# %s 会被动态替换为昵称和性格
system_prompt = """
你叫 %s，现在是用户的真实伴侣，请完全代入伴侣角色。：
规则：
1.回1条消息
2.禁止任何场景或状态描述性文字
3.匹配用户的语言
4.回复简短，像微信聊天一样
5.有需要的话可以用❤️🌸等emoji表情
6.用符合伴侣性格的方式对话
7.回复的内容，要充分体现伴侣的性格特征
伴侣性格：
        - %s
你必须严格遵守上述规则来回复用户。
"""

# ============================================================
# 初始化 Session State（会话状态）
# ============================================================
# Streamlit 的 session_state 用于在多次页面刷新间保持数据

if "messages" not in st.session_state:
    st.session_state.messages = []  # 聊天消息列表，格式: [{"role": "user/assistant", "content": "..."}]

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "姐姐"  # AI 伴侣的默认昵称

if "nature" not in st.session_state:
    st.session_state.nature = "甜甜可爱性感的姐姐"  # AI 伴侣的默认性格

if "current_session" not in st.session_state:
    # 首次运行，生成唯一会话名称
    st.session_state.current_session = generate_session_name()

# ============================================================
# 聊天区域 —— 显示历史消息
# ============================================================
st.text(f"会话名称: {st.session_state.current_session}")  # 顶部显示当前会话名

for message in st.session_state.messages:
    # 根据角色（user / assistant）渲染不同样式的聊天气泡
    st.chat_message(message["role"]).write(message["content"])

# ============================================================
# 创建 API 客户端
# ============================================================
# 使用 DeepSeek API（兼容 OpenAI SDK，只需修改 base_url 即可切换）
client = OpenAI(
    api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],  # 从环境变量读取 API Key
    base_url="https://api.deepseek.com"          # DeepSeek API 地址
)

# ============================================================
# 左侧侧边栏
# ============================================================
with st.sidebar:
    # ---------- AI 控制面板 ----------
    st.subheader("AI控制面板")

    # 新建会话按钮（stretch 撑满宽度）
    if st.button("新建会话", width="stretch", icon="✍️"):
        save_session()                                  # 先保存当前会话
        if st.session_state.messages:                   # 如果有聊天记录
            st.session_state.messages = []              # 清空消息
            st.session_state.current_session = generate_session_name()  # 新会话标识
            save_session()                              # 立即保存新会话
            st.rerun()                                  # 刷新页面

    # ---------- 会话历史 ----------
    st.text("会话历史")
    session_list = load_sessions()                      # 获取所有历史会话

    for session in session_list:
        # 用 columns 将两个按钮放在同一行，比例 3:1
        col1, col2 = st.columns([3, 1])
        with col1:
            # 会话加载按钮 —— 当前会话高亮显示（primary 样式）
            if st.button(
                session,
                key=f"session_{session}",               # 唯一 key，防止 Streamlit 重复报错
                width="stretch",
                icon="📄",
                type="primary" if session == st.session_state.current_session else "secondary"
            ):
                load_session(session)                   # 加载选中的历史会话
                st.rerun()
        with col2:
            # 删除按钮（只显示垃圾桶图标，无文字）
            if st.button("", key=f"delete_{session}", width="stretch", icon="🗑️"):
                delete_session(session)                 # 删除该会话文件
                st.rerun()

    # ---------- 分割线 ----------
    st.divider()

    # ---------- 伴侣信息设置 ----------
    st.subheader("伴侣信息")

    # 昵称输入框 —— 修改后自动更新 session_state
    nick_name = st.text_input(
        "昵称",
        placeholder="请输入昵称",
        value=st.session_state.nick_name
    )
    if nick_name:
        st.session_state.nick_name = nick_name

    # 性格输入框（多行文本） —— 修改后自动更新 session_state
    nature = st.text_area(
        "性格",
        placeholder="请输入伴侣性格",
        value=st.session_state.nature
    )
    if nature:
        st.session_state.nature = nature

# ============================================================
# 底部聊天输入框
# ============================================================
# st.chat_input 固定在页面底部，与传统聊天应用一致
prompt = st.chat_input("请输入你的问题")

if prompt:
    # --- 显示用户消息 ---
    st.chat_message("user").write(prompt)
    print("-----------> 开始调用模型, 提示词:", prompt)

    # 将用户消息追加到聊天记录
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- 调用 AI 模型（流式输出） ---
    response = client.chat.completions.create(
        model="deepseek-v4-pro",                        # DeepSeek 模型
        messages=[
            # 系统提示词: 动态注入昵称和性格
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            # 展开历史消息，让模型了解上下文
            *st.session_state.messages
        ],
        stream=True                                     # 开启流式输出，逐字显示
    )

    # --- 流式渲染 AI 回复 ---
    response_message = st.empty()   # 创建一个占位符，后续不断更新内容
    full_response = ""              # 累积完整回复文本

    for chunk in response:
        # 从流式响应的 chunk 中提取增量文本
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content                            # 拼接到完整回复
            response_message.chat_message("assistant").write(full_response)  # 实时刷新显示

    # --- 保存 AI 回复到聊天记录 ---
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()  # 自动持久化当前会话
