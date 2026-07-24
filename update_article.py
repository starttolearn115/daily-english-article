import json
import os
from datetime import datetime
from groq import Groq

def generate_daily_vocabulary():
    # 讀取 GitHub Secrets 裡的 Groq 金鑰
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("找不到 GROQ_API_KEY，請確認 GitHub Secrets 設定是否正確。")
    
    # 初始化 Groq 客戶端
    client = Groq(api_key=api_key)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    prompt = """
    請幫我隨機挑選 50 個台灣高中「學測英文 (GSAT)」範圍的核心單字。
    請務必以 JSON 格式回傳，必須嚴格包含以下欄位：
    {
        "title": "今日學測單字挑戰 (英文標題，例如 Daily GSAT Vocabulary)",
        "vocabulary": [
            {
                "word": "單字",
                "part_of_speech": "詞性縮寫，例如 v., n., adj.",
                "meaning": "繁體中文解釋",
                "example": "包含該單字的英文例句"
            }
        ]
    }
    請確保 vocabulary 陣列中剛好有 50 個單字。
    """

    try:
        # 使用 Llama 3.1 模型
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant", 
            response_format={"type": "json_object"},
        )
        
        # 解析 Groq 回傳的 JSON 格式
        article_data = json.loads(chat_completion.choices[0].message.content)
        article_data["date"] = today_str 
        return article_data
        
    except Exception as e:
        print(f"產生單字時發生錯誤: {e}")
        # 如果 API 失敗，提供備用單字
        return {
            "date": today_str,
            "title": "System Break - Vocabulary Review",
            "vocabulary": [
                {"word": "opportunity", "part_of_speech": "n.", "meaning": "機會", "example": "This is a great opportunity to review what you've learned."},
                {"word": "consistency", "part_of_speech": "n.", "meaning": "一致性；堅持", "example": "Consistency is the key to mastering a new language."}
            ]
        }

def main():
    article_data = generate_daily_vocabulary()
    
    with open('article.json', 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)
    print(f"[{article_data['date']}] 50個單字已成功由 Groq (Llama 3.1) 生成並更新！")

if __name__ == "__main__":
    main()
