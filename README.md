# MATRIX マルチエージェント合成データ生成

論文 [Synthesizing Post-Training Data for LLMs through Multi-Agent Simulation](https://arxiv.org/abs/2410.14251)に基づいて、マルチターンの日本語合成会話データを生成するPythonプロジェクトです。

## 概要

このプロジェクトでは、複数のAIエージェントがそれぞれのプロフィール、目標、計画に基づいて対話を行い、Hugging Face形式の学習データ（JSONL）を生成します。論文のMATRIXメソッドから**Modulator**コンポーネントを実装し、エージェントグループ内での効率的なコミュニケーションを実現しています。

### 主な特徴

- 🤖 **マルチエージェントシミュレーション**: 各エージェントが独自のプロフィール、目標、計画を持って行動
- 🔄 **Modulatorコンポーネント**: エージェントグループ内でのアクション収集・配信を管理
- 🎯 **関連性ベースの通信**: LLMを使用して、どのエージェントが他のエージェントの発言を受け取るべきか自動判定
- ⚡ **非同期処理**: OpenAI APIを非同期で呼び出し、効率的にデータ生成
- 🔁 **リトライ機能**: レート制限エラーに対する指数バックオフでのリトライ機構
- 💾 **JSONL出力**: Hugging Face対応のJSONL形式で出力

## ファイル構成

```
matrix-gen/
├── generate_data_with_modulator.py  # Modulator付きマルチエージェント会話生成（メイン）
├── generate_data.py                 # シンプルなエージェント会話生成
├── utils.py                         # OpenAI API呼び出しとユーティリティ関数
├── .env.example                     # 環境変数の設定例
├── MODULATOR_README.md              # Modulator実装の詳細ドキュメント
└── output_with_modulator.jsonl      # 生成された会話データ
```

## セットアップ

### 必要要件

- Python 3.12
- uv (Pythonパッケージマネージャー)
- OpenAI API キー

### インストール

1. リポジトリをクローン

2. 仮想環境の作成とパッケージインストール:
```bash
uv venv
uv pip install -r requirements.txt
```

3. 環境変数の設定:
```bash
cp .env.example .env
```

`.env` ファイルを編集して、以下の値を設定してください:
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://your-custom-url/v1
OPENAI_MODEL_NAME=your-model-name
INCLUDE_REASONING=false
```

## 使い方

### Modulator付きマルチエージェント会話生成（推奨）

```bash
uv run generate_data_with_modulator.py
```

**出力**: `output_with_modulator.jsonl`

このスクリプトでは、2つのエージェントグループが会話を行います:

#### グループ1: health_lifestyle
- **田中みさき** (35歳・主婦): 冷蔵庫の余り野菜を使った健康的な夕食レシピを探している
- **山田健二** (28歳・フィットネストレーナー): 高タンパク低カロリーのレシピを提案

#### グループ2: tech_learning  
- **佐藤健太** (22歳・大学生): Pythonでデータ分析を学びたい
- **中村ユキ** (26歳・データサイエンティスト): 初心者向けのPandasチュートリアルを提供

### シンプルなエージェント会話生成

```bash
uv run generate_data.py
```

**出力**: `output_with_modulator.jsonl`

## 出力形式

生成されるJSONLファイルの各行は以下の形式です:

```json
{
  "group_id": "health_lifestyle",
  "messages": [
    {
      "role": "user",
      "content": "こんにちは！今日の夕食に...",
      "agent_id": "tanaka_misaki"
    },
    {
      "role": "assistant",
      "content": "それは素晴らしいですね！...",
      "agent_id": "yamada_kenji"
    }
  ]
}
```

## 実装の詳細

### Modulatorクラス

```python
class Modulator:
    def __init__(self, group_id)
    def add_agent(self, agent)
    async def collect_action(self, agent_id, action)
    async def distribute_to_relevant_agents(client, action, source_agent_id)
```

**機能**:
- エージェントグループの管理
- エージェントの発言（アクション）を収集
- LLMで関連性を判定し、適切なエージェントにアクションを配信
- 構造化メモリで過去のアクションを記録

### Agentクラス

```python
class Agent:
    def __init__(self, agent_id, profile, goal, plan)
    async def generate_action(self, client, context_messages, observations)
```

**機能**:
- プロフィール、目標、計画に基づいた発言生成
- 他のエージェントの発言（observations）を観察して応答

## 論文との対応

### 実装済み機能

- ✅ エージェントグループ化
- ✅ Modulator（グループ内通信管理）
- ✅ 関連性ベースのアクション配信
- ✅ 構造化メモリ

### 簡略化した部分

- **クラスタリング**: 論文ではK-meansを使用、今回は手動でグループ定義
- **グループ間通信**: 今回はグループ内通信のみ実装
- **スケール**: 論文は1000エージェント×200グループ、今回は2グループ×各2エージェント

詳細は [`MODULATOR_README.md`](MODULATOR_README.md) を参照してください。

## カスタマイズ

### エージェントの追加

`generate_data_with_modulator.py` の `agent_groups` 配列を編集して、新しいエージェントやグループを追加できます:

```python
agent_groups = [
    {
        "group_id": "your_group_id",
        "agents": [
            {
                "agent_id": "agent_name",
                "profile": "エージェントのプロフィール",
                "goal": "エージェントの目標",
                "plan": "エージェントの計画"
            },
            # 他のエージェント...
        ]
    }
]
```

### ターン数の変更

`process_group_scenario` 関数の `max_turns` パラメータを変更:

```python
results = await asyncio.gather(*[
    process_group_scenario(client, group_config, max_turns=5)  # 5ターンに変更
    for group_config in agent_groups
])
```

## トラブルシューティング

### API レート制限エラー

`utils.py` の `generate_completion` 関数は、自動的にリトライ（指数バックオフ）を実行します。環境変数 `OPENAI_MODEL_NAME` でより高いレート制限のモデルを指定することもできます。

### Reasoning機能

一部のモデル（o1系など）でreasoningを含める場合、`.env` で以下を設定:

```env
INCLUDE_REASONING=true
```



## 参考文献

- [Synthesizing Post-Training Data for LLMs through Multi-Agent Simulation](https://arxiv.org/abs/2410.14251) (arXiv:2410.14251v2)
