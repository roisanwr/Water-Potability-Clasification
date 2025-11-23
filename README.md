# 💧 Water Potability Classification

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Library](https://img.shields.io/badge/Library-Sklearn%20|%20Pandas%20|%20NumPy-orange)
![Status](https://img.shields.io/badge/Status-Completed-green)

Proyek ini bertujuan untuk membangun model **Machine Learning** yang dapat memprediksi kualitas air (layak minum atau tidak) berdasarkan parameter fisikokimia air. Algoritma yang digunakan adalah **K-Nearest Neighbors (KNN)**.

---

## 📖 Deskripsi Proyek

Akses terhadap air bersih yang aman diminum sangat penting bagi kesehatan. Dalam proyek ini, kita menganalisis dataset kualitas air dan membangun model klasifikasi untuk menentukan potabilitas air (1 = Layak Minum, 0 = Tidak Layak Minum).

### 🎯 Tujuan
* Melakukan Exploratory Data Analysis (EDA) untuk memahami karakteristik data.
* Melakukan preprocessing data untuk menangani *missing values* dan penskalaan fitur.
* Membangun dan mengevaluasi model klasifikasi menggunakan algoritma KNN.

---

## 📂 Tentang Dataset

Dataset yang digunakan memiliki 3276 entri dengan 9 fitur input dan 1 target output.

| Fitur | Deskripsi |
| :--- | :--- |
| **ph** | Tingkat keasaman air (0-14). |
| **Hardness** | Kapasitas air untuk mengendapkan sabun (mg/L). |
| **Solids** | Total padatan terlarut (ppm). |
| **Chloramines** | Jumlah Kloramin (ppm). |
| **Sulfate** | Jumlah Sulfat terlarut (mg/L). |
| **Conductivity** | Konduktivitas listrik air (μS/cm). |
| **Organic_carbon** | Jumlah karbon organik (ppm). |
| **Trihalomethanes** | Jumlah Trihalomethanes (μg/L). |
| **Turbidity** | Tingkat kekeruhan air (NTU). |
| **Potability** | Target (0 = Tidak Layak, 1 = Layak Minum). |

---

## 🛠️ Metodologi & Workflow

Berikut adalah tahapan yang dilakukan dalam notebook:

1.  **Data Loading & Cleaning**:
    * Memuat data dari `water_potability.csv`.
    * Menangani nilai yang hilang (*missing values*) pada kolom `ph`, `Sulfate`, dan `Trihalomethanes` dengan mengisi nilai **median**.

2.  **Exploratory Data Analysis (EDA)**:
    * Melihat distribusi kelas target (Imbalanced data: lebih banyak sampel tidak layak minum).
    * Visualisasi korelasi antar fitur menggunakan Heatmap.
    * Analisis distribusi fitur menggunakan Boxplot.

3.  **Preprocessing**:
    * Membagi data menjadi fitur (X) dan target (y).
    * Melakukan **Feature Scaling** menggunakan `StandardScaler` agar semua fitur memiliki rentang nilai yang sama (sangat penting untuk KNN).
    * Membagi data menjadi **Training Set (70%)** dan **Testing Set (30%)**.

4.  **Modeling**:
    * Melatih model **K-Nearest Neighbors (KNN)**.
    * Melakukan eksperimen dengan nilai `k` (jumlah tetangga) mulai dari 1 hingga 20 untuk mencari performa terbaik.

---

## 📊 Hasil Evaluasi

Berdasarkan eksperimen dengan berbagai nilai `k`, model dievaluasi menggunakan akurasi pada data uji.

* **Akurasi Terbaik (k=15):** ~65%
* **Laporan Klasifikasi (Classification Report):**

```text
              precision    recall  f1-score   support

           0       0.66      0.89      0.76       600
           1       0.62      0.28      0.38       383

    accuracy                           0.65       983
   macro avg       0.64      0.58      0.57       983
weighted avg       0.64      0.65      0.61       983
