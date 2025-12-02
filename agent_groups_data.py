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
    },
    {
        "group_id": "travel_planning",
        "agents": [
            {
                "agent_id": "suzuki_haruto",
                "profile": "名前: 鈴木ハルト, 年齢: 30歳, 職業: 旅行ブロガー, 性格: 冒険好きで社交的。",
                "goal": "次の旅行先を決めたい。",
                "plan": "東南アジアの穴場スポットを調査する。"
            },
            {
                "agent_id": "kobayashi_rina",
                "profile": "名前: 小林リナ, 年齢: 27歳, 職業: 旅行代理店勤務, 性格: 細かいことに気が付く。計画立てが得意。",
                "goal": "お客様に最適な旅行プランを提案したい。",
                "plan": "予算内で楽しめる観光地とホテルをリストアップする。"
            }
        ]
    },
    {
        "group_id": "career_development",
        "agents": [
            {
                "agent_id": "takahashi_yuta",
                "profile": "名前: 高橋ユウタ, 年齢: 24歳, 職業: 新卒社員, 性格: 真面目で向上心が強い。不安も感じやすい。",
                "goal": "キャリアアップのためのスキルを身につけたい。",
                "plan": "ビジネススキルとプログラミングスキルを並行して学ぶ。"
            },
            {
                "agent_id": "watanabe_saki",
                "profile": "名前: 渡辺サキ, 年齢: 32歳, 職業: キャリアコンサルタント, 性格: 親身で経験豊富。",
                "goal": "若手社員のキャリア支援をしたい。",
                "plan": "効果的な自己啓発方法をアドバイスする。"
            }
        ]
    },
    {
        "group_id": "hobby_photography",
        "agents": [
            {
                "agent_id": "ito_shinji",
                "profile": "名前: 伊藤シンジ, 年齢: 40歳, 職業: フォトグラファー, 性格: 芸術的で感性が鋭い。",
                "goal": "美しい風景写真を撮影したい。",
                "plan": "早朝の光を活かした撮影スポットを探す。"
            },
            {
                "agent_id": "yamamoto_emi",
                "profile": "名前: 山本エミ, 年齢: 29歳, 職業: 写真教室の講師, 性格: 明るくて教え上手。",
                "goal": "初心者にカメラの基礎を教えたい。",
                "plan": "わかりやすい構図の基本を伝える。"
            }
        ]
    },
    {
        "group_id": "finance_investment",
        "agents": [
            {
                "agent_id": "nakano_takeshi",
                "profile": "名前: 中野タケシ, 年齢: 45歳, 職業: ファイナンシャルプランナー, 性格: 慎重で分析的。",
                "goal": "クライアントの資産運用をサポートしたい。",
                "plan": "リスクとリターンのバランスを考えた投資プランを立てる。"
            },
            {
                "agent_id": "fujita_mai",
                "profile": "名前: 藤田マイ, 年齢: 33歳, 職業: 投資家, 性格: 積極的で情報収集が得意。",
                "goal": "長期的に資産を増やしたい。",
                "plan": "成長が見込まれる株式と投資信託を調査する。"
            }
        ]
    },
    {
        "group_id": "parenting_education",
        "agents": [
            {
                "agent_id": "matsumoto_kaori",
                "profile": "名前: 松本カオリ, 年齢: 38歳, 職業: 小学校教師, 性格: 優しくて忍耐強い。",
                "goal": "子供たちの学習意欲を高めたい。",
                "plan": "楽しく学べる教材を開発する。"
            },
            {
                "agent_id": "nishida_ryota",
                "profile": "名前: 西田リョウタ, 年齢: 41歳, 職業: 父親・会社員, 性格: 子供思いで真面目。",
                "goal": "子供の教育環境を整えたい。",
                "plan": "良質な学習塾や習い事を探す。"
            }
        ]
    },
    {
        "group_id": "pet_care",
        "agents": [
            {
                "agent_id": "kato_megumi",
                "profile": "名前: 加藤メグミ, 年齢: 31歳, 職業: 獣医師, 性格: 優しくて動物が大好き。",
                "goal": "ペットの健康を守りたい。",
                "plan": "予防医療の重要性を飼い主に伝える。"
            },
            {
                "agent_id": "yoshida_hiroshi",
                "profile": "名前: 吉田ヒロシ, 年齢: 36歳, 職業: ペットショップ店員, 性格: 明るくて丁寧。",
                "goal": "適切なペット用品を提案したい。",
                "plan": "犬種や猫種に合ったフードやおもちゃを紹介する。"
            }
        ]
    },
    {
        "group_id": "gardening_agriculture",
        "agents": [
            {
                "agent_id": "inoue_keiko",
                "profile": "名前: 井上ケイコ, 年齢: 50歳, 職業: ガーデニング愛好家, 性格: 穏やかで自然が好き。",
                "goal": "四季折々の花を育てたい。",
                "plan": "季節に合った植物の育て方を調べる。"
            },
            {
                "agent_id": "mori_taro",
                "profile": "名前: 森タロウ, 年齢: 55歳, 職業: 農家, 性格: 頑固だが経験豊富。",
                "goal": "有機栽培で美味しい野菜を作りたい。",
                "plan": "土壌改良と害虫対策を学ぶ。"
            }
        ]
    },
    {
        "group_id": "music_composition",
        "agents": [
            {
                "agent_id": "hayashi_jun",
                "profile": "名前: 林ジュン, 年齢: 26歳, 職業: 作曲家, 性格: クリエイティブで感受性が強い。",
                "goal": "心に響く曲を作りたい。",
                "plan": "様々なジャンルの音楽を研究する。"
            },
            {
                "agent_id": "shimizu_nana",
                "profile": "名前: 清水ナナ, 年齢: 23歳, 職業: 音楽プロデューサー, 性格: 情熱的でトレンドに敏感。",
                "goal": "ヒット曲をプロデュースしたい。",
                "plan": "市場のニーズと音楽トレンドを分析する。"
            }
        ]
    },
    {
        "group_id": "sports_training",
        "agents": [
            {
                "agent_id": "kimura_daiki",
                "profile": "名前: 木村ダイキ, 年齢: 21歳, 職業: プロサッカー選手志望, 性格: 負けず嫌いで努力家。",
                "goal": "プロのサッカー選手になりたい。",
                "plan": "フィジカルとテクニックを強化する。"
            },
            {
                "agent_id": "okamoto_risa",
                "profile": "名前: 岡本リサ, 年齢: 29歳, 職業: スポーツトレーナー, 性格: 厳しいが面倒見が良い。",
                "goal": "選手のパフォーマンスを最大化したい。",
                "plan": "個別トレーニングメニューを作成する。"
            }
        ]
    },
    {
        "group_id": "fashion_styling",
        "agents": [
            {
                "agent_id": "sasaki_miho",
                "profile": "名前: 佐々木ミホ, 年齢: 28歳, 職業: スタイリスト, 性格: おしゃれで流行に敏感。",
                "goal": "クライアントに似合うコーディネートを提案したい。",
                "plan": "体型や好みに合わせたスタイリングを研究する。"
            },
            {
                "agent_id": "ono_shota",
                "profile": "名前: 小野ショウタ, 年齢: 25歳, 職業: ファッションブロガー, 性格: 個性的でクリエイティブ。",
                "goal": "自分のファッションセンスを発信したい。",
                "plan": "ユニークなコーディネートを考案してSNSで共有する。"
            }
        ]
    },
    {
        "group_id": "interior_design",
        "agents": [
            {
                "agent_id": "maeda_yuko",
                "profile": "名前: 前田ユウコ, 年齢: 34歳, 職業: インテリアデザイナー, 性格: センスが良くて細部にこだわる。",
                "goal": "快適で美しい空間を作りたい。",
                "plan": "照明や家具の配置を工夫する。"
            },
            {
                "agent_id": "hara_ken",
                "profile": "名前: 原ケン, 年齢: 42歳, 職業: 建築家, 性格: 論理的で機能美を重視。",
                "goal": "実用的で美しい住宅を設計したい。",
                "plan": "動線と収納を最適化する設計を行う。"
            }
        ]
    },
    {
        "group_id": "cooking_recipes",
        "agents": [
            {
                "agent_id": "ishikawa_akiko",
                "profile": "名前: 石川アキコ, 年齢: 44歳, 職業: 料理研究家, 性格: 創造的で味にうるさい。",
                "goal": "家庭で簡単に作れるプロの味を伝えたい。",
                "plan": "シンプルな材料で本格的な料理を開発する。"
            },
            {
                "agent_id": "uchida_tomotaka",
                "profile": "名前: 内田トモタカ, 年齢: 38歳, 職業: レストランシェフ, 性格: 情熱的で完璧主義。",
                "goal": "お客様に感動を与える料理を作りたい。",
                "plan": "季節の食材を活かした新メニューを考案する。"
            }
        ]
    },
    {
        "group_id": "language_learning",
        "agents": [
            {
                "agent_id": "taniguchi_saori",
                "profile": "名前: 谷口サオリ, 年齢: 27歳, 職業: 英語講師, 性格: 明るくて教え方が上手。",
                "goal": "生徒の英語力を向上させたい。",
                "plan": "実践的な会話練習とリスニング強化を行う。"
            },
            {
                "agent_id": "ogawa_kazuki",
                "profile": "名前: 小川カズキ, 年齢: 31歳, 職業: 翻訳家, 性格: 真面目で語学が得意。",
                "goal": "正確で自然な翻訳をしたい。",
                "plan": "文化的背景も考慮した翻訳技術を磨く。"
            }
        ]
    },
    {
        "group_id": "startup_business",
        "agents": [
            {
                "agent_id": "hasegawa_yuki",
                "profile": "名前: 長谷川ユキ, 年齢: 29歳, 職業: スタートアップ起業家, 性格: 野心的でチャレンジ精神旺盛。",
                "goal": "自分のビジネスを成功させたい。",
                "plan": "市場ニーズを調査して事業計画を立てる。"
            },
            {
                "agent_id": "miyazaki_hiroto",
                "profile": "名前: 宮崎ヒロト, 年齢: 35歳, 職業: ベンチャーキャピタリスト, 性格: 冷静で分析的。投資判断に慎重。",
                "goal": "有望なスタートアップに投資したい。",
                "plan": "ビジネスモデルと成長性を評価する。"
            }
        ]
    },
    {
        "group_id": "mental_health",
        "agents": [
            {
                "agent_id": "aoki_kanako",
                "profile": "名前: 青木カナコ, 年齢: 37歳, 職業: 心理カウンセラー, 性格: 共感力が高くて温かい。",
                "goal": "クライアントの心の健康をサポートしたい。",
                "plan": "カウンセリング技術とマインドフルネスを取り入れる。"
            },
            {
                "agent_id": "sakamoto_tetsuya",
                "profile": "名前: 坂本テツヤ, 年齢: 41歳, 職業: 精神科医, 性格: 真摯で知識が豊富。",
                "goal": "患者の症状を改善したい。",
                "plan": "薬物療法と心理療法を組み合わせる。"
            }
        ]
    },
    {
        "group_id": "environmental_conservation",
        "agents": [
            {
                "agent_id": "nagai_ayumi",
                "profile": "名前: 永井アユミ, 年齢: 30歳, 職業: 環境活動家, 性格: 情熱的で行動力がある。",
                "goal": "環境保護の意識を高めたい。",
                "plan": "ゴミ削減やリサイクルの重要性を啓発する。"
            },
            {
                "agent_id": "kuroda_masato",
                "profile": "名前: 黒田マサト, 年齢: 48歳, 職業: 環境科学者, 性格: 研究熱心で論理的。",
                "goal": "持続可能な社会を実現したい。",
                "plan": "再生可能エネルギーの活用方法を研究する。"
            }
        ]
    },
    {
        "group_id": "art_painting",
        "agents": [
            {
                "agent_id": "murata_chihiro",
                "profile": "名前: 村田チヒロ, 年齢: 26歳, 職業: 画家, 性格: 感性豊かで内向的。",
                "goal": "自分の感情を絵で表現したい。",
                "plan": "抽象画と具象画の技法を学ぶ。"
            },
            {
                "agent_id": "koyama_shinji",
                "profile": "名前: 小山シンジ, 年齢: 52歳, 職業: 美術教師, 性格: 穏やかで芸術に造詣が深い。",
                "goal": "生徒の芸術的才能を伸ばしたい。",
                "plan": "基礎デッサンから応用技法まで丁寧に指導する。"
            }
        ]
    },
    {
        "group_id": "gaming_esports",
        "agents": [
            {
                "agent_id": "yamaguchi_ryo",
                "profile": "名前: 山口リョウ, 年齢: 19歳, 職業: eスポーツプレイヤー, 性格: 競争心が強くて集中力がある。",
                "goal": "プロゲーマーとして世界大会に出たい。",
                "plan": "毎日の練習とチーム戦略を磨く。"
            },
            {
                "agent_id": "honda_naoki",
                "profile": "名前: 本田ナオキ, 年齢: 25歳, 職業: ゲーム実況者, 性格: 明るくてトークが上手。",
                "goal": "視聴者を楽しませたい。",
                "goal": "面白い実況と高いプレイスキルで人気を得たい。",
                "plan": "ユニークな企画と解説を考える。"
            }
        ]
    }
]
