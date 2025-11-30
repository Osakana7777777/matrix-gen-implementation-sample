# Modulator実装ガイド

## 概要

MATRIX論文の**Modulator**コンポーネントを実装しました。Modulatorは、エージェントグループ内およびグループ間の効率的なコミュニケーションを可能にします。

## 実装内容

### 新しいファイル

- **`generate_data_with_modulator.py`**: Modulator付きマルチエージェント会話生成

### Modulatorクラスの機能

```python
class Modulator:
    def __init__(self, group_id)
    def add_agent(self, agent)
    async def collect_action(self, agent_id, action)
    async def distribute_to_relevant_agents(client, action, source_agent_id)
    async def evaluate_inter_group_propagation(client, action, other_modulators)
```

#### 主な機能

1. **エージェント管理**: グループ内のエージェントを管理
2. **アクション収集**: エージェントの発言・行動を収集
3. **関連性判定**: LLMを使用して、どのエージェントがそのアクションを受け取るべきか判定
4. **メモリ管理**: グループの構造化されたメモリ（過去のアクション）を維持

### エージェントの拡張

```python
class Agent:
    async def generate_action(self, client, context_messages=None, observations=None)
```

- **observations**: 他のエージェントの発言を観察し、それに基づいて行動

## 生成データ

### エージェントグループ

#### グループ1: health_lifestyle
- **田中みさき** (主婦): 健康的な夕食レシピを探している
- **山田健二** (フィットネストレーナー): 健康的な食事のアドバイスを提供

#### グループ2: tech_learning  
- **佐藤健太** (大学生): Pandasを学びたい
- **中村ユキ** (データサイエンティスト): 初心者をサポート

### 出力形式

```json
{
  "group_id": "health_lifestyle",
  "messages": [
    {"role": "user", "content": "[tanaka_misaki] ..."},
    {"role": "assistant", "content": "[yamada_kenji] ..."},
    ...
  ]
}
```

## 論文との対応

### 実装済み

- ✅ **エージェントグループ**: 類似したプロフィールのエージェントをグループ化
- ✅ **Modulator**: グループごとにModulatorを配置
- ✅ **グループ内通信**: 関連性に基づいてエージェント間でアクションを配信
- ✅ **構造化メモリ**: 過去のアクションを記録

### 簡略化された部分

- **クラスタリング**: 論文ではK-meansクラスタリングを使用。今回は手動でグループ定義
- **グループ間通信**: 論文では複数グループ間でもアクション伝播。今回はグループ内通信のみ
- **スケール**: 論文では1000エージェント、200グループ。今回は2グループ、各2エージェント

## 使い方

```bash
# Modulator付き生成
uv run generate_data_with_modulator.py

# 出力: output_with_modulator.jsonl
```

## 元の実装との違い

| 項目 | generate_data.py | generate_data_with_modulator.py |
|------|------------------|----------------------------------|
| エージェント | 単独（AIアシスタントと会話） | 複数（グループ内で対話） |
| Modulator | なし | あり |
| 関連性判定 | なし | LLMで自動判定 |
| 観察 | なし | 他エージェントの発言を観察 |
| 出力件数 | 3件（独立） | 2件（グループ） |

## 拡張の可能性

1. **グループ間通信**: 複数グループ間でアクションを伝播
2. **自動クラスタリング**: エージェントプロフィールの埋め込みベクトルでK-meansクラスタリング
3. **スケールアップ**: より多くのエージェントとグループ
4. **ターン数増加**: より長い会話シーケンス
5. **DPO用データ**: 好ましい/好ましくない応答のペア生成
