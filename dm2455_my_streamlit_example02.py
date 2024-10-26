import streamlit as st
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

# openai api key
# openai_api_key = st.secrets["openai_api_key"]
openai_api_key = st.sidebar.text_input("請輸入openai api key")

# 確認prompt
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("請先設定openai_api_key")
        st.stop()
    
    # llm = OpenAI(temperature= 0.7, openai_api_key = openai_api_key, streaming = True)
    # 設置OpenAI模型為 gpt-4o-mini
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=openai_api_key, streaming=True)
    tools = load_tools(["ddg-search"])
    
    # 建立agent
    agent = initialize_agent(tools, llm, agent =AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True, verbose = True)
    
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        #透過回呼方式展示Agent的思考過程
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks = [st_callback])
        
        st.write(response)
        