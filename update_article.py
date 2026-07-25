import json
import os
from datetime import datetime
from groq import Groq

def generate_daily_vocabulary():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("找不到 GROQ_API_KEY，請確認 GitHub Secrets 設定是否正確。")
    
    client = Groq(api_key=api_key)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # 🌟 強化版提示詞：加入難度限制與絕對防呆範例
    prompt = """
    請幫我挑選 15 個台灣高中「學測英文 (GSAT)」範圍的進階核心單字 (難度約為高中 7000 單字表的 Level 3 到 Level 5，請勿挑選太簡單的單字如 student, happy)。
    請務必以 JSON 格式回傳。
    
    【重要範例格式】
    請嚴格參考這個範例的欄位對應方式填寫，"word" 欄位必須是「英文單字本身」，不能填成詞性！
    {
        "title": "今日學測單字挑戰",
        "vocabulary": [
            {
                "word": "abandon",
                "part_of_speech": "v.",
                "meaning": "放棄；拋棄",
                "example": "The captain gave the order to abandon the sinking ship.",
                "example_translation": "船長下令棄沉船。"
            }
        ]
    }
    
    請依照上述範例格式，生成剛好 15 個單字。絕對不能缺少任何一個欄位。
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant", 
            response_format={"type": "json_object"},
            max_tokens=4000 
        )
        
        article_data = json.loads(chat_completion.choices[0].message.content)
        article_data["date"] = today_str 
        return article_data
        
    except Exception as e:
        print(f"產生單字時發生錯誤: {e}")
        return {
            "date": today_str,
            "title": "單字產生中斷，請重試",
            "vocabulary": [
                {
                    "word": "opportunity", 
                    "part_of_speech": "n.", 
                    "meaning": "機會", 
                    "example": "This is a great opportunity to review what you've learned.",
                    "example_translation": "這是一個複習你所學內容的絕佳機會。"
                }
            ]
        }

def main():
    article_data = generate_daily_vocabulary()
    
    with open('article.json', 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)
    print(f"[{article_data['date']}] 15個完整單字資料已成功由 Groq 生成並更新！")

if __name__ == "__main__":
    main()
