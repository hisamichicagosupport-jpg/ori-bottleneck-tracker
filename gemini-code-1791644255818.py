import datetime
import os
import pandas as pd
import streamlit as st

# CSVファイルの保存先
DATA_FILE = "ori_research_bottlenecks.csv"

st.set_page_config(
    page_title="ORI Research - Physical AI Bottleneck Tracker", layout="centered"
)

st.title("🤖 ORI Research: Field Bottleneck Tracker")
st.markdown(
    """
Capturing hardware limits and mechanical pain points in North American FA & robotics 
to bridge Japanese precision manufacturers with US industrial integrators.
"""
)

# 1. データの読み込み
if os.path.exists(DATA_FILE):
  df_existing = pd.read_csv(DATA_FILE)
else:
  df_existing = pd.DataFrame(
      columns=[
          "Timestamp",
          "Company / Observer",
          "Machine Category",
          "Target Component",
          "Problem / Pain Point",
          "Desired Technology / Solution",
      ]
  )

# 2. 入力フォームの作成（英語化）
with st.form(key="bottleneck_form"):
  st.subheader("📝 Log a Physical Bottleneck")

  company = st.text_input(
      "Company Name / Contact (Optional)",
      placeholder="e.g., ABC Automation (Chicago)",
  )

  col1, col2 = st.columns(2)
  with col1:
    machine_category = st.selectbox(
        "Machine Category",
        [
            "Articulated Robot",
            "SCARA / Parallel Robot",
            "AGV / AMR (Mobile Robot)",
            "CNC / Machine Tool",
            "Packaging & Conveyor Line",
            "Other",
        ],
    )
  with col2:
    target_part = st.selectbox(
        "Target Component / Part",
        [
            "Servo Motor & Actuator",
            "High-Precision Gearbox",
            "Bearing & Bushing",
            "End Effector & Gripper",
            "Sensor & Control Board",
            "Mechanical Frame (Thermal/Vibration)",
        ],
    )

  problem = st.text_area(
      "Observed Problem / Physical Pain Point",
      placeholder=(
          "e.g., Thermal drift causes micron-level positional deviation during"
          " high-speed continuous operation."
      ),
  )

  desired_tech = st.text_area(
      "Desired Technology / Solution",
      placeholder=(
          "e.g., Heat-resistant high-precision cooling structure, or"
          " near-zero expansion custom components."
      ),
  )

  submit_button = st.form_submit_button(label="Submit Bottleneck Data")

  if submit_button:
    if problem.strip() == "":
      st.error("Please fill in the 'Observed Problem' field.")
    else:
      new_data = pd.DataFrame(
          [{
              "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "Company / Observer": (
                  company if company else "Anonymous / Field Interview"
              ),
              "Machine Category": machine_category,
              "Target Component": target_part,
              "Problem / Pain Point": problem,
              "Desired Technology / Solution": desired_tech,
          }]
      )

      # データの結合と保存
      df_updated = pd.concat([df_existing, new_data], ignore_index=True)
      df_updated.to_csv(DATA_FILE, index=False)
      st.success(
          "✨ Data successfully registered! Thank you for your contribution."
      )
      df_existing = df_updated

# 3. 蓄積されたデータの確認セクション
st.markdown("---")
st.subheader("📊 Collected Bottlenecks (Live Database)")

if not df_existing.empty:
  st.metric(label="Total Entries", value=f"{len(df_existing)} pain points logged")
  st.dataframe(df_existing, use_container_width=True)

  # CSVダウンロードボタン
  csv = df_existing.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Download Data as CSV",
      data=csv,
      file_name="ori_research_bottlenecks.csv",
      mime="text/csv",
  )
else:
  st.info("No data logged yet. Use the form above to add the first entry.")
