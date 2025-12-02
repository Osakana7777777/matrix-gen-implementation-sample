# 会話生成フロー図

このドキュメントでは、マルチエージェント会話データ生成システムの処理フローを図解します。

## 1. 全体フロー

```mermaid
flowchart TD
    Start([プログラム開始]) --> LoadGroups[agent_groups_dataから<br/>グループ情報を読み込み]
    LoadGroups --> InitClient[OpenAI Clientを初期化]
    InitClient --> ProcessGroups{各グループを<br/>並列処理}
    
    ProcessGroups --> CreateModulator[Modulatorインスタンスを作成]
    CreateModulator --> CreateAgents[Agentインスタンスを作成<br/>プロフィール、目標、計画を設定]
    CreateAgents --> AddToModulator[エージェントをModulatorに追加]
    
    AddToModulator --> TurnLoop{ターン数<br/>max_turns=2}
    
    TurnLoop -->|各ターン| AgentLoop{各エージェント}
    
    AgentLoop --> GetObservations[Modulatorから<br/>他エージェントの行動を取得<br/>最新3件]
    GetObservations --> CheckReasoning{メッセージインデックス<br/>が奇数?}
    CheckReasoning -->|Yes 奇数| GenerateWithReasoning[LLM呼び出し<br/>reasoning付き]
    CheckReasoning -->|No 偶数| GenerateNoReasoning[LLM呼び出し<br/>reasoningなし]
    
    GenerateWithReasoning --> CollectAction[Modulatorに行動を収集]
    GenerateNoReasoning --> CollectAction
    
    CollectAction --> DetermineRelevance[LLMで関連性判定<br/>どのエージェントに配信するか]
    DetermineRelevance --> AddToHistory[会話履歴に追加<br/>user/assistant交互]
    
    AddToHistory --> NextAgent{次のエージェント?}
    NextAgent -->|あり| AgentLoop
    NextAgent -->|なし| NextTurn{次のターン?}
    
    NextTurn -->|あり| TurnLoop
    NextTurn -->|なし| GroupResult[グループの結果を返す]
    
    GroupResult --> NextGroup{次のグループ?}
    NextGroup -->|あり| ProcessGroups
    NextGroup -->|なし| SaveResults[全グループの結果を<br/>JSONLファイルに保存]
    
    SaveResults --> End([終了])
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style GenerateWithReasoning fill:#fff4e1
    style GenerateNoReasoning fill:#fff4e1
    style DetermineRelevance fill:#e1f0ff
    style SaveResults fill:#f0e1ff
```

## 2. 初期化フェーズ

```mermaid
sequenceDiagram
    participant Main as メインプログラム
    participant Data as agent_groups_data
    participant Client as OpenAI Client
    
    Main->>Data: agent_groupsをインポート
    Main->>Client: get_openai_client()
    Client-->>Main: クライアントインスタンス
```

## 3. グループ処理フェーズ（各グループごと）

```mermaid
sequenceDiagram
    participant Main as メインプログラム
    participant Mod as Modulator
    participant Agent1 as Agent 1
    participant Agent2 as Agent 2
    participant LLM as OpenAI API
    
    Main->>Mod: Modulator作成
    Main->>Agent1: Agent作成(profile, goal, plan)
    Main->>Agent2: Agent作成(profile, goal, plan)
    Main->>Mod: add_agent(Agent1)
    Main->>Mod: add_agent(Agent2)
    
    loop 各ターン (max_turns回)
        loop 各エージェント
            Agent1->>Mod: 他エージェントの観察を取得
            Mod-->>Agent1: 最新3件の行動
            Agent1->>LLM: generate_action() reasoning付き/なし
            LLM-->>Agent1: 生成された行動テキスト
            Agent1->>Mod: collect_action()
            Mod->>LLM: distribute_to_relevant_agents()
            LLM-->>Mod: 関連エージェントリスト
            Agent1->>Main: 会話履歴に追加
        end
    end
    
    Main->>Main: JSONLに保存
```

## 4. 会話履歴の構造

```mermaid
graph LR
    A[Message 0<br/>role: user<br/>agent: tanaka_misaki] --> B[Message 1<br/>role: assistant<br/>agent: yamada_kenji<br/>+reasoning]
    B --> C[Message 2<br/>role: user<br/>agent: suzuki_akira]
    C --> D[Message 3<br/>role: assistant<br/>agent: kobayashi_yui<br/>+reasoning]
    D --> E[...]
    
    style B fill:#fff4e1
    style D fill:#fff4e1
```

**メッセージインデックスとrole/reasoningの対応:**
- 偶数インデックス (0, 2, 4, ...) → `role: "user"` (reasoningなし)
- 奇数インデックス (1, 3, 5, ...) → `role: "assistant"` (reasoning付き)

## 5. Modulatorの役割

```mermaid
flowchart LR
    subgraph Modulator
        Memory[(構造化メモリ<br/>agent_id + action)]
        Agents[エージェントリスト]
    end
    
    Agent1[Agent 1] -->|行動を送信| Memory
    Agent2[Agent 2] -->|行動を送信| Memory
    Agent3[Agent 3] -->|行動を送信| Memory
    
    Memory -->|関連する観察を配信| Agent1
    Memory -->|関連する観察を配信| Agent2
    Memory -->|関連する観察を配信| Agent3
    
    LLM[OpenAI API] -.関連性判定.-> Memory
```

## 6. エージェント行動生成の詳細

```mermaid
flowchart TD
    Start([エージェント行動生成]) --> BuildPrompt[システムプロンプト構築<br/>profile, goal, planを含む]
    BuildPrompt --> CheckObs{観察データあり?}
    CheckObs -->|Yes| AddObs[他エージェントの観察を追加]
    CheckObs -->|No| AddInstruction
    AddObs --> AddInstruction[行動生成指示を追加]
    AddInstruction --> CheckReason{reasoning必要?}
    CheckReason -->|Yes| CallLLMReason[LLM呼び出し<br/>include_reasoning=True]
    CheckReason -->|No| CallLLM[LLM呼び出し<br/>include_reasoning=False]
    CallLLMReason --> Return([生成されたアクションを返す])
    CallLLM --> Return
```

## システムパラメータ

現在のシステム設定：

| パラメータ | 値 | 説明 |
|----------|-----|------|
| グループ数 | 20 | 並列処理される |
| エージェント数/グループ | 2〜4人 | グループによって異なる |
| ターン数 (`max_turns`) | 2 | 各グループでの会話ターン |
| 観察数 | 3 | 各エージェントが参照する最新行動数 |
| reasoning付与 | assistant役のみ | メッセージインデックスが奇数の場合 |
| 出力形式 | JSONL | Hugging Face対応フォーマット |

## データフロー概要

```mermaid
graph TB
    Input[agent_groups_data.py<br/>20グループ x 2-4エージェント] --> Process[generate_data_with_modulator.py]
    Process --> API[OpenAI API]
    API --> Process
    Process --> Output[output_with_modulator.jsonl<br/>会話データセット]
    
    style Input fill:#e1f5e1
    style Output fill:#f0e1ff
    style API fill:#fff4e1
```

## 関連ファイル

- [generate_data_with_modulator.py](file:///Users/shiraishijinsei/Desktop/python_test/matrix-gen/generate_data_with_modulator.py) - メイン処理
- [agent_groups_data.py](file:///Users/shiraishijinsei/Desktop/python_test/matrix-gen/agent_groups_data.py) - エージェントグループ定義
- [utils.py](file:///Users/shiraishijinsei/Desktop/python_test/matrix-gen/utils.py) - ユーティリティ関数
- [output_with_modulator.jsonl](file:///Users/shiraishijinsei/Desktop/python_test/matrix-gen/output_with_modulator.jsonl) - 生成されたデータ
