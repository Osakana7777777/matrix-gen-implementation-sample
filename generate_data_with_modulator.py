import json
import asyncio
from utils import get_openai_client, save_to_jsonl, generate_completion

# Define Agent Class
class Agent:
    def __init__(self, agent_id, profile, goal, plan):
        self.agent_id = agent_id
        self.profile = profile
        self.goal = goal
        self.plan = plan
        self.memory = []

    async def generate_action(self, client, context_messages=None, observations=None):
        """
        Generates an action (message) based on profile, goal, plan, context, and observations.
        """
        system_prompt = f"""
あなたは以下のプロフィールを持つ人物として振る舞ってください。
プロフィール: {self.profile}
人生の目標: {self.goal}
現在の計画: {self.plan}

あなたの目標を達成するために発言を行ってください。
自然な日本語で、プロフィールに沿った口調で話してください。
"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add observations from other agents if any
        if observations:
            obs_text = "\n".join([f"- {obs}" for obs in observations])
            messages.append({
                "role": "user",
                "content": f"以下は他の人の発言や行動です:\n{obs_text}\n\nこれを参考にしてください。"
            })
        
        if context_messages:
            messages.extend(context_messages)
            
        # Add instruction for the agent to act
        messages.append({
            "role": "user", 
            "content": "これまでの会話や観察を踏まえ、あなたの目標を達成するための次の発言を生成してください。発言内容のみを出力してください。"
        })

        response = await generate_completion(client, messages)
        return response


# Define Modulator Class
class Modulator:
    def __init__(self, group_id):
        self.group_id = group_id
        self.structured_memory = []  # Past agent actions in this group
        self.agents = []
    
    def add_agent(self, agent):
        """Add an agent to this group"""
        self.agents.append(agent)
    
    async def collect_action(self, agent_id, action):
        """Collect an action from an agent"""
        self.structured_memory.append({
            "agent_id": agent_id,
            "action": action
        })
    
    async def distribute_to_relevant_agents(self, client, action, source_agent_id):
        """
        Determine which agents should receive this action based on relevance.
        For simplicity, we check semantic similarity using LLM.
        """
        relevant_agents = []
        
        for agent in self.agents:
            if agent.agent_id == source_agent_id:
                continue  # Don't send to the source agent
            
            # Use LLM to determine relevance
            relevance_prompt = f"""
以下のプロフィールを持つ人物にとって、この発言は関連性がありますか？

プロフィール: {agent.profile}
目標: {agent.goal}

発言: {action}

関連性がある場合は「はい」、ない場合は「いいえ」とだけ答えてください。
"""
            
            relevance_check = await generate_completion(
                client, 
                [{"role": "user", "content": relevance_prompt}]
            )
            
            if relevance_check and "はい" in relevance_check:
                relevant_agents.append(agent.agent_id)
        
        return relevant_agents
    
    async def evaluate_inter_group_propagation(self, client, action, other_modulators):
        """
        Evaluate whether to propagate this action to other groups.
        For simplicity, we skip inter-group communication in this implementation.
        """
        # In full MATRIX implementation, this would check relevance to other groups
        pass


# Define Scenarios with agent groups
agent_groups = [
    {
        "group_id": "health_lifestyle",
        "agents": [
            {
                "agent_id": "tanaka_misaki",
                "profile": "名前: 田中みさき, 年齢: 35歳, 職業: 主婦, 性格: 料理好きで健康志向。新しいレシピに挑戦するのが好き。",
                "goal": "家族のために健康的で美味しい夕食を作りたい。",
                "plan": "冷蔵庫にある余り野菜（キャベツ、人参）を使った新しいレシピを探す。"
            },
            {
                "agent_id": "yamada_kenji",
                "profile": "名前: 山田健二, 年齢: 28歳, 職業: フィットネストレーナー, 性格: 健康志向で明るい。栄養学にも詳しい。",
                "goal": "クライアントに健康的な食事のアドバイスをしたい。",
                "plan": "簡単に作れる高タンパク低カロリーのレシピを集める。"
            }
        ]
    },
    {
        "group_id": "tech_learning",
        "agents": [
            {
                "agent_id": "sato_kenta",
                "profile": "名前: 佐藤健太, 年齢: 22歳, 職業: 情報系大学生, 性格: 真面目だが少しせっかち。プログラミング初心者。",
                "goal": "Pythonを使ってデータ分析ができるようになりたい。",
                "plan": "まずはPandasライブラリの基本的な使い方をマスターする。"
            },
            {
                "agent_id": "nakamura_yuki",
                "profile": "名前: 中村ユキ, 年齢: 26歳, 職業: データサイエンティスト, 性格: 親切で教えることが好き。",
                "goal": "データ分析の知識を広めたい。初心者を支援したい。",
                "plan": "わかりやすいPandasチュートリアルを作成する。"
            }
        ]
    }
]


async def process_group_scenario(client, group_config, max_turns=2):
    """
    Process a multi-agent scenario within a group using Modulator.
    """
    group_id = group_config["group_id"]
    print(f"\n=== Processing Group: {group_id} ===")
    
    # Create Modulator for this group
    modulator = Modulator(group_id)
    
    # Create agents and add to modulator
    agents = []
    for agent_config in group_config["agents"]:
        agent = Agent(
            agent_config["agent_id"],
            agent_config["profile"],
            agent_config["goal"],
            agent_config["plan"]
        )
        agents.append(agent)
        modulator.add_agent(agent)
    
    # Conversation history (for generating final dataset)
    conversation_history = []
    
    # Run multi-turn interaction
    for turn in range(max_turns):
        print(f"\n--- Turn {turn + 1} ---")
        
        # Each agent generates an action
        for agent in agents:
            # Get observations from modulator's memory (excluding own actions)
            observations = [
                entry["action"] for entry in modulator.structured_memory
                if entry["agent_id"] != agent.agent_id
            ][-3:]  # Last 3 observations
            
            # Generate action
            action = await agent.generate_action(
                client,
                observations=observations if observations else None
            )
            
            if not action:
                continue
            
            print(f"{agent.agent_id}: {action[:50]}...")
            
            # Collect action in modulator
            await modulator.collect_action(agent.agent_id, action)
            
            # Add to conversation history
            conversation_history.append({
                "role": "user" if len(conversation_history) % 2 == 0 else "assistant",
                "content": f"[{agent.agent_id}] {action}"
            })
            
            # Determine which agents should receive this action
            relevant_agents = await modulator.distribute_to_relevant_agents(
                client, action, agent.agent_id
            )
            print(f"  -> Relevant to: {relevant_agents}")
    
    return {
        "group_id": group_id,
        "messages": conversation_history
    }


async def run_modulator_simulation():
    """
    Run simulation with Modulator-based multi-agent groups.
    """
    client = get_openai_client()
    
    # Process each group
    tasks = [
        process_group_scenario(client, group_config, max_turns=2)
        for group_config in agent_groups
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Save to JSONL
    save_to_jsonl(results, "output_with_modulator.jsonl")
    print("\n✅ Data saved to output_with_modulator.jsonl")


if __name__ == "__main__":
    asyncio.run(run_modulator_simulation())
