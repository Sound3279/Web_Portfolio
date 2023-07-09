import subprocess
import sys

def update_pip():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install_package(package):
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", package])
    except subprocess.CalledProcessError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

update_pip()
required_packages = ["openai", "gradio"]
for package in required_packages:
    install_package(package)

import openai
import gradio

openai.api_key = "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"

start_sequence = "\nAI: "
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt):
    responce = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        maxtoken=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    return responce.choice[0].text

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    print(input, output, history)
    return history, history

# Gradio의 Blocks 객체를 생성하는 부분
block = gradio.Blocks()


with block:
    # 마크다운 문법을 통해 웹 앱 화면의 텍스트를 설정하는 부분
    gradio.Markdown("""<h1><center>나만의 GPT 챗봇</center></h1>""")
    # Gradio에서 제공하는 ChatBot GUI
    chatbot = gradio.Chatbot()
    # ChatGPT에 입력을 넣는 텍스트 박스를 정의하는 코드
    # placeholder를 통해 텍스트 박스에 사전에 작성한 prompt를 띄움
    message = gradio.Textbox(placeholder=prompt)
    # 데이터가 유지될 수 있도록 하는 State
    state = gradio.State()
    # SEND라고 쓰여 있는 submit 버튼을 만드는 부분
    submit = gradio.Button("SEND")
    # send 버튼이 클릭되었을 때 chatgpt_clone 함수가 호출되며,
    # chatgpt_clone의 매개변수인 input, history에 inputs와 outputs가 들어감
    # state를 input, output에 넣으면 데이터를 유지할 수 있음
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

# debug 모드로 로컬에서 웹을 실행
# 에러 메세지를 확인할 수 있음
block.launch(debug=True)

# 72시간동안 웹을 배포하는 share 옵션
# lock.launch(share=True)