import json
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class MusashinoAssistant_SAR:
    def __init__(self):
        # Setup OpenAI Client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Load the local vector database once
        self.vectors = np.load('vector_db/jp_vectors_SAR.npy')
        with open('vector_db/jp_metadata_SAR.json', 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)

    def get_answer(self, user_query):
        # 1. RETRIEVAL
        query_vector = np.array(self.client.embeddings.create(
            input=user_query,
            model="text-embedding-3-large"
        ).data[0].embedding)

        # Semantic similarity
        scores = np.dot(self.vectors, query_vector)
        top_indices = np.argsort(scores)[::-1][:2]

        # 2. AUGMENTATION
        reference_text = ""
        for idx in top_indices:
            item = self.metadata[idx]
            reference_text += f"\n【資料のURL】: {item['url']}\n"
            reference_text += f"【要約】: {item['summary']}\n"
            reference_text += f"【内容】: {item['chunk_text']}\n"
            reference_text += "---------------------------\n"

        # 3. GENERATION
        system_prompt = """あなたは武蔵野大学の事務局アシスタントです。
            以下の【参考資料】の情報のみを使用してユーザーの質問に回答してください。

            ルール:
            1. 回答はユーザーの質問と同じ言語で行ってください。（日本語または英語）
            2. 回答は簡潔かつ丁寧にしてください。
            3. 回答の最後に引用した資料のURLを記載してください。
            4. 資料に答えがない場合は「該当する情報が見つかりませんでした」と回答してください。
            """

        user_prompt = f"【参考資料】:\n{reference_text}\n\nユーザーの質問: {user_query}"

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
            

        )
        return response.choices[0].message.content