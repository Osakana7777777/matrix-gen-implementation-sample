import json
import asyncio
import random
from utils import get_openai_client, save_to_jsonl, generate_completion
from agent_groups_data import agent_groups

# Define Agent Class
class Agent:
    def __init__(self, agent_id, profile, goal, plan):
        self.agent_id = agent_id
        self.profile = profile
        self.goal = goal
        self.plan = plan
        self.memory = []

    async def generate_action(self, client, context_messages=None, observations=None, include_reasoning=False):
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

        response = await generate_completion(client, messages, include_reasoning=include_reasoning)
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


async def select_relevant_agent(client, modulator, agents, previous_speaker):
    """
    前の発言に対してrelevantなエージェントからランダムに1人選択
    
    Args:
        client: OpenAI client
        modulator: Modulatorインスタンス
        agents: エージェントのリスト
        previous_speaker: 前の発言者（Agentオブジェクト）
    
    Returns:
        選択されたAgentオブジェクト、またはNone
    """
    if not modulator.structured_memory:
        return None
    
    # 最後の発言を取得
    latest_action = modulator.structured_memory[-1]["action"]
    source_agent_id = modulator.structured_memory[-1]["agent_id"]
    
    # 前の発言に対してrelevantなエージェントのIDを取得
    relevant_agent_ids = await modulator.distribute_to_relevant_agents(
        client, latest_action, source_agent_id
    )
    
    if not relevant_agent_ids:
        return None
    
    print(f"  -> Relevant agents: {relevant_agent_ids}")
    
    # relevantなエージェントの中からランダムに選択
    relevant_agents = [a for a in agents if a.agent_id in relevant_agent_ids]
    return random.choice(relevant_agents) if relevant_agents else None



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
    message_index = 0  # Track message index for reasoning control
    
    # Run multi-turn interaction
    # max_turns represents the number of conversation rounds (each round = user + assistant message)
    previous_speaker = None
    
    for turn in range(max_turns):
        print(f"\n--- Turn {turn + 1} ---")
        
        # Select user agent
        if turn == 0:
            # First turn: select random user agent
            user_agent = random.choice(agents)
        else:
            # Subsequent turns: select from agents relevant to the previous message
            relevant_agent = await select_relevant_agent(
                client, modulator, agents, previous_speaker
            )
            user_agent = relevant_agent if relevant_agent else random.choice(
                [a for a in agents if a != previous_speaker]
            )
        
        # Generate user message
        observations = [
            entry["action"] for entry in modulator.structured_memory
            if entry["agent_id"] != user_agent.agent_id
        ][-3:]  # Last 3 observations
        
        user_action = await user_agent.generate_action(
            client,
            observations=observations if observations else None,
            include_reasoning=False  # User messages don't need reasoning
        )
        
        if user_action:
            print(f"{user_agent.agent_id} (user): {user_action[:50]}...")
            await modulator.collect_action(user_agent.agent_id, user_action)
            
            conversation_history.append({
                "role": "user",
                "content": user_action,
                "agent_id": user_agent.agent_id
            })
            
            previous_speaker = user_agent
        
        # Select assistant agent based on relevance to user's message
        relevant_assistant = await select_relevant_agent(
            client, modulator, agents, user_agent
        )
        assistant_agent = relevant_assistant if relevant_assistant else random.choice(
            [a for a in agents if a != user_agent]
        )
        
        # Generate assistant message
        observations = [
            entry["action"] for entry in modulator.structured_memory
            if entry["agent_id"] != assistant_agent.agent_id
        ][-3:]  # Last 3 observations
        
        assistant_action = await assistant_agent.generate_action(
            client,
            observations=observations if observations else None,
            include_reasoning=True  # Assistant messages include reasoning
        )
        
        if assistant_action:
            print(f"{assistant_agent.agent_id} (assistant): {assistant_action[:50]}...")
            await modulator.collect_action(assistant_agent.agent_id, assistant_action)
            
            conversation_history.append({
                "role": "assistant",
                "content": assistant_action,
                "agent_id": assistant_agent.agent_id
            })
            
            previous_speaker = assistant_agent
    
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
