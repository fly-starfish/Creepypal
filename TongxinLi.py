import openai
import re
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# 下载 NLTK 的词性标注器所需的模型
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# 设置 OpenAI API 密钥
openai.api_key = ''


def extract_keywords(response, max_keywords=10):
    """
    Extract keywords by filtering based on word type (nouns and verbs) and character length.
    Focuses on more meaningful words without using a stop words list.
    """
    # 使用 NLTK 将回答进行词性标注
    words = word_tokenize(response)
    tagged_words = pos_tag(words)

    # 仅提取名词 (NN) 和动词 (VB) 的词，并且长度大于4个字符
    keywords = [word for word, pos in tagged_words if (pos.startswith('NN') or pos.startswith('VB')) and len(word) > 4]

    # 限制关键词数量
    keywords = keywords[:max_keywords]

    # 返回最终的关键词列表
    return keywords


def format_as_steps(response):
    """
    Format the response into steps (1, 2, 3, 4) using basic split by sentence.
    Cleans up repeated or unnecessary step numbers.
    """
    # 将回答按句号分割，并且为每个句子添加编号
    sentences = re.split(r'\.\s*', response)  # 使用正则表达式匹配句子结束
    formatted_response = ""
    step_counter = 1
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and not sentence.isdigit():  # 忽略空行或仅有数字的行
            formatted_response += f"{step_counter}. {sentence}.\n"
            step_counter += 1
    return formatted_response


def ask_minecraft_chatbot(conversation_history, prompt):
    """
    Send a request to GPT-3.5-turbo to generate a response based on the conversation history.
    Let GPT model decide whether the question is related to Minecraft.
    """
    try:
        # Add the user's question to the conversation history
        conversation_history.append({"role": "user", "content": prompt})

        # 调试信息：输出对话历史
        print(f"Debug: Current conversation history: {conversation_history}")

        # 发送请求到 GPT-3.5-turbo 模型
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        # 获取 GPT 的回答
        bot_response = response.choices[0].message['content'].strip()

        # 将模型的回答添加到对话历史
        conversation_history.append({"role": "assistant", "content": bot_response})

        # 处理并提取关键词
        keywords = extract_keywords(bot_response)

        # 按步骤格式化回答
        formatted_response = format_as_steps(bot_response)

        # 返回格式化的回答和关键词
        return formatted_response, keywords

    except openai.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}", []
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", []


# 示例使用
if __name__ == "__main__":

    # 初始化对话历史，包含系统提示
    conversation_history = [
        {"role": "system",
         "content": "You are a Minecraft expert. Answer questions in clear steps (1, 2, 3, 4). Answer only questions related to Minecraft. If a question is not related to Minecraft, politely decline to answer by saying 'I can only answer questions related to Minecraft.'"}
    ]

    print(
        "Welcome to the Minecraft Expert Chatbot! Feel free to ask any Minecraft-related questions (type 'exit' to end the chat).")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chat session ended!")
            break

        answer, keywords = ask_minecraft_chatbot(conversation_history, user_input)
        print(f"Chatbot:\n{answer}")
        print(f"Keywords: {', '.join(keywords)}")
