# Python 学习笔记

## 2025.06.15 — AI API 调用 + Streamlit 入门

### 📚 今日学习内容

#### 1. DeepSeek API 调用
- 使用 OpenAI SDK 调用 DeepSeek 模型
- API Key 配置：环境变量 vs 硬编码（不要硬编码！）
- 基础对话：`client.chat.completions.create()`
- 多轮对话：维护 `messages` 列表实现上下文记忆

相关文件：[deepseektest.py](./deepseektest.py)、[streamlit_chat.py](./streamlit_chat.py)

#### 2. Streamlit 入门
- 页面配置：`set_page_config(title, layout, icon)`
- 文本显示：`title`, `header`, `subheader`, `write`
- 交互组件：`text_input`, `button`, `chat_input`, `chat_message`
- 数据展示：`table`, `image`
- 状态持久化：`st.session_state`
- 融合 DeepSeek 做成聊天界面

相关文件：[streamlit_basic.py](./streamlit_basic.py)、[streamlit_chat.py](./streamlit_chat.py)

#### 3. 其他
- Apifox 安装配置（D 盘）
- Postman vs Apifox 工具选择
- HTTP / 网络基础知识扫盲（配合课程 92-96 节）

### 🛠 环境
- Python 3.13
- openai SDK
- streamlit
- Windows 10 / PowerShell

### 📝 笔记
- [6.15 笔记](./6.15-notes.md)（含 Typora 截图，本地查看）
