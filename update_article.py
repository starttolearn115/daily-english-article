import json
import os
from datetime import datetime
from groq import Groq

def generate_daily_article():
    # 讀取 GitHub Secrets 裡的 Groq 金鑰
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("找不到 GROQ_API_KEY，請確認 GitHub Secrets 設定是否正確。")
    
    # 初始化 Groq 客戶端
    client = Groq(api_key=api_key)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    prompt = """
    請幫我寫一篇適合台灣高中生閱讀的英文短文（約 150-200 字），難度符合學測英文。
    主題隨機，可以是科技、環保、心理學、歷史等。
    請務必以 JSON 格式回傳，必須嚴格包含以下欄位：
    {
        "title": "文章標題 (英文)",
        "content": "文章內容 (英文，適當分段，段落間用 \\n\\n 隔開)",
        "vocabulary": [
            {"word": "單字", "part_of_speech": "詞性縮寫，例如 v., n., adj.", "meaning": "繁體中文解釋"}
        ]
    }
    請挑選 3-5 個學測級別的核心單字放入 vocabulary 中。
    """

    try:
        # 使用 Meta 開發的 Llama 3 8B 模型，並要求回傳 JSON
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192", 
            response_format={"type": "json_object"},
        )
        
        # 解析 Groq 回傳的 JSON 格式
        article_data = json.loads(chat_completion.choices[0].message.content)
        article_data["date"] = today_str 
        return article_data
        
    except Exception as e:
        print(f"產生文章時發生錯誤: {e}")
        # 備用文章
        return {
            "date": today_str,
            "title": "A Day of Review",
            "content": "Today our AI took a short break to recharge its circuits. It's a great opportunity for you to review the vocabulary words you've learned over the past few days!\n\nConsistency is the key to mastering a new language.",
            "vocabulary": [
                {"word": "opportunity", "part_of_speech": "n.", "meaning": "機會"},
                {"word": "consistency", "part_of_speech": "n.", "meaning": "一致性；堅持"}
            ]
        }

def main():
    article_data = generate_daily_article()
    
    with open('article.json', 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)
    print(f"[{article_data['date']}] 文章已成功由 Groq (Llama 3) 生成並更新！")

if __name__ == "__main__":
    main()
