from src.Agent import get_agent_executor, get_output_response

def run():
    agent_executor = get_agent_executor()

    while True:
        try:
                               "图片地址：https://github.com/heelenzhang/Agent/blob/main/assets/demo_pic_2.jpeg?raw=true\n请输入您的问题：")
            response = agent_executor.run(user_input)
            output_response(response)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    run()