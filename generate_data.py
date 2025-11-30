import json
import asyncio
from utils import get_openai_client, save_to_jsonl, generate_completion

# Define Agent Class
class Agent:
    def __init__(self, profile, goal, plan):
        self.profile = profile
        self.goal = goal
        self.plan = plan
        self.memory = []

    async def generate_action(self, client, context_messages=None):
        """
        Generates an action (message) based on profile, goal, plan, and context.
        """
        system_prompt = f"""
あなたは以下のプロフィールを持つ人物として振る舞ってください。
プロフィール: {self.profile}
人生の目標: {self.goal}
現在の計画: {self.plan}

あなたの目標を達成するために、対話相手（AIアシスタント）に対して発言を行ってください。
自然な日本語で、プロフィールに沿った口調で話してください。
"""
        messages = [{"role": "system", "content": system_prompt}]
        
        if context_messages:
            messages.extend(context_messages)
            
        # Add instruction for the agent to act
        messages.append({
            "role": "user", 
            "content": "これまでの会話の流れを踏まえ、あなたの目標を達成するための次の発言を生成してください。発言内容のみを出力してください。"
        })

        response = await generate_completion(client, messages)
        return response

# Define Scenarios (Profiles, Goals, Plans)
scenarios = [
    {
        "profile": "名前: 佐藤健太, 年齢: 22歳, 職業: 情報系大学生, 性格: 真面目だが少しせっかち。プログラミング初心者。",
        "goal": "Pythonを使ってデータ分析ができるようになりたい。",
        "plan": "まずはPandasライブラリの基本的な使い方をマスターする。"
    },
    {
        "profile": "名前: 田中みさき, 年齢: 35歳, 職業: 主婦, 性格: 料理好きで健康志向。新しいレシピに挑戦するのが好き。",
        "goal": "家族のために健康的で美味しい夕食を作りたい。",
        "plan": "冷蔵庫にある余り野菜（キャベツ、人参）を使った新しいレシピを探す。"
    },
    {
        "profile": "名前: 鈴木一郎, 年齢: 65歳, 職業: 定年退職者, 性格: 穏やかで旅行好き。歴史に興味がある。",
        "goal": "妻と二人で京都へ旅行に行き、歴史的な寺院を巡りたい。",
        "plan": "秋の京都で、あまり混雑していない穴場の寺院を見つける。"
    }
]

async def process_scenario(client, scenario, index):
    print(f"Generating Scenario {index+1}...")
    agent = Agent(scenario["profile"], scenario["goal"], scenario["plan"])
    
    conversation_history = [] 
    agent_context = [] 
    
    # --- Turn 1 ---
    user_msg_1 = await agent.generate_action(client, agent_context)
    if not user_msg_1: return None
    print(f"Scenario {index+1} User: {user_msg_1[:30]}...")
    
    conversation_history.append({"role": "user", "content": user_msg_1})
    agent_context.append({"role": "assistant", "content": user_msg_1})

    assistant_msg_1 = await generate_completion(client, conversation_history)
    if not assistant_msg_1: return None
    print(f"Scenario {index+1} Assistant: {assistant_msg_1[:30]}...")
    
    conversation_history.append({"role": "assistant", "content": assistant_msg_1})
    agent_context.append({"role": "user", "content": assistant_msg_1})

    # --- Turn 2 ---
    user_msg_2 = await agent.generate_action(client, agent_context)
    if not user_msg_2: return None
    print(f"Scenario {index+1} User: {user_msg_2[:30]}...")
    
    conversation_history.append({"role": "user", "content": user_msg_2})
    agent_context.append({"role": "assistant", "content": user_msg_2})

    assistant_msg_2 = await generate_completion(client, conversation_history)
    if not assistant_msg_2: return None
    print(f"Scenario {index+1} Assistant: {assistant_msg_2[:30]}...")
    
    conversation_history.append({"role": "assistant", "content": assistant_msg_2})
    
    return {"messages": conversation_history}

async def run_simulation():
    client = get_openai_client()
    tasks = [process_scenario(client, scenario, i) for i, scenario in enumerate(scenarios)]
    results = await asyncio.gather(*tasks)
    
    generated_data = [r for r in results if r is not None]
    save_to_jsonl(generated_data, "output.jsonl")

if __name__ == "__main__":
    asyncio.run(run_simulation())
