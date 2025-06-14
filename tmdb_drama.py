import streamlit as st
import requests

# TMDb APIキー
API_KEY = "054399b3517551d518e2aac834aa311a"
API_URL = "https://api.themoviedb.org/3/discover/tv"
IMG_URL = "https://image.tmdb.org/t/p/w500"

# ジャンルと並び順の辞書
genres = {
    "すべて": None,
    "韓国ドラマ": 10759,
    "アニメ": 16,
    "ドキュメンタリー": 99,
    "ファミリー": 10751,
    "ミステリー": 9648,
    "SF & ファンタジー": 10765
}

sort_options = {
    "人気順": "popularity.desc",
    "評価が高い順": "vote_average.desc",
    "レビュー数が多い順": "vote_count.desc",
    "新しい順": "first_air_date.desc",
    "古い順": "first_air_date.asc"
}

st.title("ドラマ キーワード検索")

# キーワード入力欄
query = st.text_input("作品名やキーワードを入力", "")

if query:
    url = f"https://api.themoviedb.org/3/search/tv"
    params = {
        "api_key": API_KEY,
        "language": "ja",
        "query": query
    }
    response = requests.get(url, params=params).json()
    results = response.get("results", [])

    if results:
        st.subheader("検索結果")
        for item in results:
            title = item.get("name", "タイトル不明")
            overview = item.get("overview", "あらすじなし")
            poster_path = item.get("poster_path")

            if poster_path:
                image_url = f"https://image.tmdb.org/t/p/w300{poster_path}"
                st.image(image_url, use_container_width=True)
            st.markdown(f"### {title}")
            with st.expander("あらすじ"):
                st.write(overview)
    else:
        st.warning("該当する作品が見つかりませんでした。")

# サイドバーで選択
st.sidebar.title(" 条件を選ぶ")
genre_name = st.sidebar.selectbox("ジャンル", list(genres.keys()))
sort_label = st.sidebar.selectbox("並び順", list(sort_options.keys()))

# API パラメータ作成
params = {
    "api_key": API_KEY,
    "language": "ja-JP",
    "sort_by": sort_options[sort_label],
    "page": 1
}

if genres[genre_name]:
    params["with_genres"] = genres[genre_name]

# APIリクエスト
response = requests.get(API_URL, params=params)
data = response.json()

# 見出し
st.title("おすすめドラマ/映画検索アプリ")
st.write("ジャンルや並び順を変えて、今見るべきドラマをチェックしよう！")

# 結果表示（2列）
results = data.get("results", [])

for i in range(0, len(results), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(results):
            show = results[i + j]
            title = show.get("name")
            original = show.get("original_name")
            overview = show.get("overview", "")
            poster_path = show.get("poster_path")

            with cols[j]:
                display_title = title if title == original else f"{title}（原題：{original}）"

                title_html = f"""
                <div style="height: 3.5em; overflow: hidden; font-weight: bold; font-size: 1.1rem;">
                  {display_title}
                </div>
                """
                st.markdown(title_html, unsafe_allow_html=True)
                if poster_path:
                    st.image(f"{IMG_URL}{poster_path}", use_container_width=True)
                else:
                    st.write("（ポスター画像なし）")
                with st.expander("あらすじを見る"):
                    st.write(overview[:300] + "..." if len(overview) > 300 else overview)
