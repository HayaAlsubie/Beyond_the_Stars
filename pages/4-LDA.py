import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="Tourism Analysis", layout="wide")
st.title("Beyond the Stars - Insights Dashboard")

st.sidebar.title("Filters")
df = pd.read_csv('/home/engineersh/code/hayaalsubie/Beyond_the_Stars/notebooks/negative_reviews_w_clusters.csv')
lda_model = joblib.load('/home/engineersh/code/hayaalsubie/Beyond_the_Stars/pages/lda_neg_tot.pkl')
kmeans_model = joblib.load('/home/engineersh/code/hayaalsubie/Beyond_the_Stars/pages/kmeans_model.pkl')
vectorizer = joblib.load('/home/engineersh/code/hayaalsubie/Beyond_the_Stars/notebooks/vectorizer.pkl')
feature_names = vectorizer.get_feature_names_out()

st.dataframe(df.head())

regions = df['Region'].unique()
#selected_region = st.sidebar.selectbox('Select Region', sorted(regions))

#filtered_cities = df[df['Region'] == selected_region]['City'].unique()

filtered_cities = df['City'].unique()

selected_city = st.sidebar.selectbox('Select City', sorted(filtered_cities))

#filtered_place_types = df[(df['Region'] == selected_region) & (df['City'] == selected_city)]['Place Type'].unique()
filtered_place_types = df[df['City'] == selected_city]['Place Type'].unique()
selected_place_type = st.sidebar.selectbox('Select Place Type', sorted(filtered_place_types))

#sentiment_option = st.sidebar.radio('Select Sentiment', ['Positive', 'Negative'])

filtered_data = df[
    (df['City'] == selected_city) &
    (df['Place Type'] == selected_place_type)]

#filtered_data['Cluster'] = kmeans_model.predict(vectorizer.transform(filtered_data['Cleaned Review']))

st.dataframe(filtered_data.head())

sentiment_option = 'Negative'

st.subheader(f"{sentiment_option} Comments for {selected_place_type} in {selected_city}")
st.dataframe(filtered_data[['Cleaned Review', 'Sentiment Label', 'Topic']])

st.subheader("Topic Modeling Insights")

st.markdown("""
**What is a topic?**
A topic is a group of words that frequently appear together in reviews.
Each topic represents a common theme such as "cleanliness", "pricing", or "crowding".
""")

topic_numbers = list(range(lda_model.n_components))
selected_topic = st.selectbox('Select Topic to View Keywords', topic_numbers)

top_word_indices = lda_model.components_[selected_topic].argsort()[::-1][:10]
top_words = [(feature_names[i], lda_model.components_[selected_topic][i]) for i in top_word_indices if i < len(feature_names)]

topic_df = pd.DataFrame(top_words, columns=["Word", "Weight"])

st.write(f"Top words for Topic {selected_topic}:")
st.dataframe(topic_df)

fig, ax = plt.subplots()
sns.barplot(data=topic_df, x="Weight", y="Word", palette="pastel", ax=ax)
ax.set_title(f"Top Keywords for Topic {selected_topic}", fontsize=14)
ax.set_xlabel("Weight")
ax.set_ylabel("Word")
st.pyplot(fig)

wordcloud_data = {word: weight for word, weight in top_words}
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Pastel1').generate_from_frequencies(wordcloud_data)

fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis("off")
st.pyplot(fig_wc)

#st.subheader("Cluster Assignment (KMeans)")
#st.dataframe(filtered_data[['Cleaned Review', 'Topic']])
