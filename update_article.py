import json
import os
from datetime import datetime
from google import genai
from google.genai import types

def generate_daily_article():
    # 讀取藏在 GitHub Secrets 裡的 Gemini 金鑰
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("找不到 GEMINI_API_KEY，請確認 GitHub Secrets 設定是否正確。")
    
    # 初始化新版客戶端
    client = genai.Client(api_key=api_key)
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
        # 使用新版 SDK 呼叫 Gemini (使用 gemini-2.5-flash 模型，並強制要求回傳 JSON)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        # 解析 Gemini 回傳的 JSON 格式
        article_data = json.loads(response.text)
        article_data["date"] = today_str 
        return article_data
        
    except Exception as e:
        print(f"產生文章時發生錯誤: {e}")
        # 如果 API 失敗，提供一篇備用文章
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
    print(f"[{article_data['date']}] 文章已成功由 Gemini 生成並更新！")

if __name__ == "__main__":
    main()
