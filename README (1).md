
# TravelTide Customer Segmentation & Rewards Program

## Project Description
This project analyzes user behavior on the TravelTide travel booking platform to develop a customer segmentation framework and a personalized rewards (perks) program. Using session-level, trip-level, and user-level data, we apply feature engineering, dimensionality reduction, and clustering techniques to identify meaningful customer segments and recommend targeted perks that improve conversion, retention, and customer lifetime value.

---

## Project Summary
TravelTide is exploring the launch of a rewards program to increase customer engagement and loyalty. To support this initiative, we:

- Cleaned and integrated data from users, sessions, flights, and hotels  
- Engineered behavioral, monetary, and preference-based features  
- Applied PCA to reduce dimensionality while retaining 95% of variance  
- Used K-Means clustering to segment users into five distinct groups  
- Profiled clusters and mapped each to an appropriate perk strategy  

### Key Insights
- Users differ significantly in booking frequency, spending level, and hotel vs. flight preference  
- Preference indices (hotel_hunter_index, flight_fanatic_index, bundle_index) improve interpretability  
- Five meaningful customer segments were identified  

### Deliverables
- Executive Summary  
- Detailed Analysis Report  
- Clustered user dataset (CSV)  
- Jupyter/Colab notebooks  

---

## Installation Instructions

```bash
git clone https://github.com/yourusername/TravelTide.git
cd TravelTide
pip install -r requirements.txt
```

---

## Dependencies
- Python 3.9+  
- pandas  
- numpy  
- scikit-learn  
- matplotlib  
- seaborn  
- jupyter  

---

## Usage Instructions
Run notebooks in order:

1. Data Processing  
2. Feature Engineering  
3. PCA  
4. KMeans  
5. Cluster Profiling  

Final output file:

```
data/processed/users_with_clusters.csv
```

---

## Example Usage

```python
import pandas as pd
df = pd.read_csv("data/processed/users_with_clusters.csv")
df.head()

df["cluster"].value_counts()
df.groupby("cluster")["total_spend"].mean()
```

---

## Directory Structure

```
TravelTide/
├── data/
│   ├── raw/
│   ├── processed/
├── ipynb/
│   ├── 01_data_processing.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_pca.ipynb
│   ├── 04_kmeans.ipynb
│   ├── 05_cluster_profiling.ipynb
├── reports/
│   ├── executive_summary.docx
│   ├── detailed_report.docx
├── src/
├── requirements.txt
└── README.md
```

---

## Results & Perk Mapping

| Cluster Type | Recommended Perk |
|-------------|-----------------|
| Business Travelers | Free Checked Bag |
| Hotel-Centric Leisure | Room Upgrade |
| Bundle Seekers | Bundle Discount |
| Price Sensitive | Coupon |
| At-Risk Users | Re-engagement Offer |

---

## Future Improvements
- Dynamic segmentation  
- Lifetime value modeling  
- Real A/B testing  
- Alternative clustering algorithms  

---

## Author
Your Name
