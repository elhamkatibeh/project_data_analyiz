
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
def export_data (final_datafram):
    # file_path = r'C:\\Users\\Asus\\Desktop\\skill1.xlsx'
    df = final_datafram
    # df.info()
    df["job_offer"] = df["job_offer"].str.replace("برنامه نویس","")
    df["job_offer"] = df["job_offer"].str.replace("توسعه دهنده","")
    df["job_offer"] = df["job_offer"].str.replace("(Python)","")
    df["job_offer"] = df["job_offer"].str.replace("python","Python")
    df["job_offer"] = df["job_offer"].str.strip()
    df["job_name_new"] = df["job_offer"].str.replace(" ","-")
    # df_1 = pd.pivot_table(df, index=df["job_name_new"],aggfunc="sum")
    # df_1.to_excel(r"C:\Users\Asus\Desktop\skill2.xlsx")
    df_1 =pd.DataFrame()
    df_final = pd.DataFrame(columns=["ability_name", "grade", "count_need"])
    list_ability = []
    list_grade = []
    list_count_need = []

    for name_col in df.columns:
        if df[name_col].count() > 5:
            df_1[name_col] = df[name_col]
    for name_col_df_1 in df_1.columns:
        sum_grade = df_1[name_col_df_1].sum()
        count_all_row = df_1[name_col_df_1].count()
        try:
            mean_grade = sum_grade / count_all_row
            if mean_grade <= 10:
                list_grade.append(round(mean_grade))
                list_ability.append(name_col_df_1)
                list_count_need.append(count_all_row)
        except:
            print("it nut true")
    # for i in range(len(list_grade)):

    df_final["ability_name"] = list_ability
    df_final["grade"] = list_grade
    df_final["count_need"] = list_count_need
    df_final["wight"] = df_final["grade"] * df_final["count_need"]
    df_final = df_final.sort_values(by="wight", ascending=False)
    df_final = df_final[df_final["ability_name"] != "Python"]

    fig, axes = plt.subplots(2, 1, figsize=(10, 10) , gridspec_kw={'hspace': 0.9})  # 2 ردیف، 1 ستون

    # نمودار اول: مهارت‌ها با وزن
    axes[0].bar(df_final["ability_name"], df_final["wight"], color='skyblue')
    axes[0].set_xlabel("Ability Name")
    axes[0].set_ylabel("Weight")
    axes[0].set_title("Weight by Ability")
    axes[0].tick_params(axis='x', rotation=45)

    # نمودار دوم: job_name_new با تعداد بیشتر از threshold
    threshold = 1

    job_counts = df["job_name_new"].value_counts()
    job_counts_filtered = job_counts[job_counts > threshold]

    axes[1].bar(job_counts_filtered.index, job_counts_filtered.values, color='orange')
    axes[1].set_xlabel("Job Name")
    axes[1].set_ylabel("Count")
    axes[1].set_title(f"THE BEST JOB  {threshold}")
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()  # جلوگیری از تداخل نوشته‌ها
    plt.show()
