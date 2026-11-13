import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="残り物には福がある？",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 残り物には福がある？")
st.write("最初に引く人と最後に引く人。当たりやすいのはどちら？")

st.divider()

st.subheader("実験条件")

participants = st.number_input(
    "参加人数（くじの本数）",
    min_value=2,
    max_value=1000,
    value=10,
    step=1
)

winners = st.number_input(
    "当たり本数",
    min_value=1,
    max_value=int(participants),
    value=1,
    step=1
)

trials = st.select_slider(
    "試行回数",
    options=[1000, 10000, 50000, 100000, 500000, 1000000],
    value=100000,
    format_func=lambda x: f"{x:,}回"
)

theory = winners / participants * 100

st.info(
    f"理論上の当選確率：{theory:.3f}%"
)

if st.button("実験開始", type="primary"):

    first_wins = 0
    last_wins = 0

    progress = st.progress(0)
    status = st.empty()

    interval = max(1, trials // 100)

    for i in range(trials):

        # 最初の人の当選判定
        first = random.random() < winners / participants

        # 最後の人の当選判定
        remaining_winners = winners - int(first)
        remaining_people = participants - 1

        last = random.random() < (
            remaining_winners / remaining_people
        )

        if first:
            first_wins += 1

        if last:
            last_wins += 1

        if (i + 1) % interval == 0 or i + 1 == trials:
            progress.progress((i + 1) / trials)
            status.write(
                f"実験中：{i + 1:,} / {trials:,}"
            )

    first_rate = first_wins / trials * 100
    last_rate = last_wins / trials * 100

    st.success("実験完了！")

    st.divider()
    st.subheader("実験結果")

    col1, col2 = st.columns(2)

    col1.metric(
        "最初の人",
        f"{first_rate:.3f}%",
        f"{first_wins:,}回当選"
    )

    col2.metric(
        "最後の人",
        f"{last_rate:.3f}%",
        f"{last_wins:,}回当選"
    )

    st.metric(
        "理論上の当選確率",
        f"{theory:.3f}%"
    )

    st.metric(
        "実測値の差",
        f"{abs(first_rate - last_rate):.3f}ポイント"
    )

    st.divider()
    st.subheader("当選確率の比較")

    df = pd.DataFrame({
        "対象": ["最初", "最後", "理論値"],
        "当選確率（%）": [
            first_rate,
            last_rate,
            theory
        ]
    })

    st.bar_chart(
        df,
        x="対象",
        y="当選確率（%）"
    )

    st.subheader("考察")

    st.write(
        f"{participants:,}人中、当たりは{winners:,}本。"
    )

    st.write(
        f"理論上の当選確率は{theory:.3f}%です。"
    )

    st.write(
        "最初と最後の当選確率は理論上同じです。"
        "実測値との差は試行回数による偶然の変動です。"
    )
