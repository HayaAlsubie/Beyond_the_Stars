# Beyond the Stars

**Saudi Tourism Review Analysis with NLP and interactive data visualization**

Beyond the Stars is a team capstone project that explores tourist feedback across Saudi Arabia. It turns a cleaned collection of Google Places reviews into an interactive Streamlit dashboard for comparing sentiment, identifying recurring concerns, and exploring differences across regions, cities, and place types.

> This is an independent educational project. It is not affiliated with or endorsed by the Saudi Tourism Authority, Google, or any venue represented in the data.

## Project snapshot

- **17,095** cleaned tourist reviews
- **5** Saudi regions and **20** cities
- **8** place types, including hotels, restaurants, cafes, parks, museums, and tourist attractions
- Positive/negative sentiment exploration
- Regional and city-level comparison
- Topic exploration for negative English-language reviews using Latent Dirichlet Allocation (LDA)
- Interactive dashboard built with Streamlit

## Questions explored

The project was designed around four practical questions:

1. How do tourist sentiment and ratings vary across Saudi regions and cities?
2. Which types of places receive the most positive or negative feedback?
3. What themes recur in negative English-language reviews?
4. Which cities may deserve closer attention when both rating and negative-review rate are considered?

## Dashboard pages

| Page | Purpose |
|---|---|
| Introduction | Project context, motivation, and data source |
| Data | Filter reviews and inspect rating and sentiment distributions |
| Compare Sentiment | Compare two regions or cities by place type |
| Beyond Words | Explore recurring terms in negative reviews using LDA |
| Tourist Feedback | Review regional, city, and place-type patterns |
| Recommendations | Summarize the team's interpretation of the findings |

## Technology

- Python
- Streamlit
- Pandas and NumPy
- Plotly, Matplotlib, and Seaborn
- scikit-learn
- NLTK

## Repository structure

```text
.
├── introduction.py                  # Streamlit entry point
├── pages/                           # Dashboard pages
├── notebooks/LDA_model_haya.ipynb   # Topic-modeling exploration
├── data/cleaned_reviews.csv         # Cleaned analysis dataset
├── .streamlit/config.toml           # Streamlit theme configuration
└── requirements.txt                 # Python dependencies
```

## Run locally

Python 3.11 is recommended.

```bash
git clone https://github.com/HayaAlsubie/Beyond_the_Stars.git
cd Beyond_the_Stars
python -m venv .venv
```

Activate the environment:

```bash
# macOS or Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install the dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run introduction.py
```

Then open `http://localhost:8501` if Streamlit does not open it automatically.

## Haya Alsubaie's contribution

The Git history documents Haya's work across the final Streamlit application structure, dashboard-page integration, dependency and deployment fixes, and LDA/topic-modeling exploration. The repository also preserves the contributions of the full project team.

## Team

- [Haya Alsubaie](https://github.com/HayaAlsubie)
- [Sarah Alshehri](https://github.com/SarahxHM)
- [Ali Alfaraj](https://github.com/farajay96)
- [Shumoukh Albarraq](https://github.com/xshmbr)
- [Khawlah Aldarwish](https://github.com/khawlah57)

## Data and interpretation notes

- The dashboard presents exploratory results, not an official measure of tourism performance.
- The dataset is imbalanced toward positive reviews, so raw counts should not be interpreted as balanced model performance.
- The topic-modeling page focuses on negative English-language reviews and does not represent every language in the dataset equally.
- The attention score is a project-defined heuristic that combines negative-review rate with average rating; it is not an official benchmark.
- Google Places content remains subject to the [Google Maps Platform Terms and Places API policies](https://developers.google.com/maps/documentation/places/web-service/policies). The included data should not be treated as an independently licensed public dataset.

## License

No open-source license has been assigned. The source code and included data may be viewed for portfolio and educational review, but reuse is not granted automatically.
