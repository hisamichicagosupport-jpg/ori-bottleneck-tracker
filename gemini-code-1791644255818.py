import datetime
import os
import pandas as pd
import streamlit as st

# CSVファイルの保存先
DATA_FILE = "ori_research_bottlenecks.csv"

st.set_page_config(
    page_title="ORI Research - Physical AI Bottleneck Tracker", layout="centered"
)

st.title("🤖 ORI Research: 現場の物理ボトルネック・データベース")
st.markdown(
    """
北米・FAロボティクス現場における「ハードウェアの限界・ペイン」を収集し、
日米の技術協業（コンソーシアム）の種をまくためのプロトタイプ入力フォームです。
"""
)

# 1. データの読み込み
if os.path.exists(DATA_FILE):
  df_existing = pd.read_csv(DATA_FILE)
else:
  df_existing = pd.DataFrame(
      columns=[
          "Timestamp",
          "Company/Observer",
          "Machine Category",
          "Target Part",
          "Problem/Pain Point",
          "Desired Tech/Solution",
      ]
  )

# 2. 入力フォームの作成
with st.form(key="bottleneck_form"):
  st.subheader("📝 ボトルネック情報の入力")

  company = st.text_input(
      "企業名・ヒアリング元 (任意)",
      placeholder="例: ABC Automation (Chicago)",
  )

  col1, col2 = st.columns(2)
  with col1:
    machine_category = st.selectbox(
        "機械カテゴリ",
        [
            "多関節ロボット (Articulated Robot)",
            "SCARA・パラレルロボット",
            "AGV / AMR (搬送ロボット)",
            "工作機械・加工機",
            "包装・コンベアライン",
            "その他",
        ],
    )
  with col2:
    target_part = st.selectbox(
        "対象の部位・コンポーネント",
        [
            "サーボモータ・アクチュエーター",
            "高精度減速機 (Gearbox)",
            "軸受・ベアリング (Bearing)",
            "エンドエフェクター・グリッパー",
            "センサー・制御基板まわり",
            "フレーム・機構全体（熱膨張・共振等）",
        ],
    )

  problem = st.text_area(
      "発生している問題点・物理的ペイン (自由記述)",
      placeholder=(
          "例: 高速連続稼働時に熱膨張が起き、〇ミクロン単位の位置ズレ（サーマルドリフト）が発生する。"
      ),
  )

  desired_tech = st.text_area(
      "求めている技術・解決策 (自由記述)",
      placeholder=(
          "例: 耐熱性に優れた高精度な放熱機構、またはゼロ膨張に近い素材のカスタム部品。"
      ),
  )

  submit_button = st.form_submit_button(label="データを登録する")

  if submit_button:
    if problem.strip() == "":
      st.error("「発生している問題点」は必須項目です。")
    else:
      new_data = pd.DataFrame(
          [{
              "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "Company/Observer": company if company else "匿名 / 現地ヒアリング",
              "Machine Category": machine_category,
              "Target Part": target_part,
              "Problem/Pain Point": problem,
              "Desired Tech/Solution": desired_tech,
          }]
      )

      # データの結合と保存
      df_updated = pd.concat([df_existing, new_data], ignore_index=True)
      df_updated.to_csv(DATA_FILE, index=False)
      st.success(
          "✨ データを正常に登録しました！ご協力ありがとうございます。"
      )
      df_existing = df_updated

# 3. 蓄積されたデータの確認セクション（簡易ダッシュボード）
st.markdown("---")
st.subheader("📊 収集済みボトルネック一覧（リアルタイム蓄積）")

if not df_existing.empty:
  st.metric(
      label="総エントリ数", value=f"{len(df_existing)} 件のペインを蓄積"
  )
  st.dataframe(df_existing, use_container_width=True)

  # CSVダウンロードボタン
  csv = df_existing.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 蓄積データをCSVでダウンロード",
      data=csv,
      file_name="ori_research_bottlenecks.csv",
      mime="text/csv",
  )
else:
  st.info(
      "まだデータが登録されていません。上のフォームから最初のデータを追加してみましょう。"
  )