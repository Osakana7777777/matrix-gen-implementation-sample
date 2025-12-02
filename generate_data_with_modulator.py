import json
import asyncio
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
            # Only include reasoning for even-indexed messages (assistant messages)
            # message_index: 0=user, 1=assistant, 2=user, 3=assistant, etc.
            should_include_reasoning = (message_index % 2 == 1)  # 1, 3, 5, ...
            
            action = await agent.generate_action(
                client,
                observations=observations if observations else None,
                include_reasoning=should_include_reasoning
            )
            
            if not action:
                continue
            
            print(f"{agent.agent_id}: {action[:50]}...")
            
            # Collect action in modulator
            await modulator.collect_action(agent.agent_id, action)
            
            # Add to conversation history with agent_id as separate key
            # Determine role based on message index
            role = "user" if message_index % 2 == 0 else "assistant"
            
            conversation_history.append({
                "role": role,
                "content": action,
                "agent_id": agent.agent_id
            })
            
            message_index += 1
            
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
