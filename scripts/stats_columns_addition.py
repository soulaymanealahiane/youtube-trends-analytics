import pandas as pd
import numpy as np

# === CONFIGURATION ===
# Update this path to point to your ALREADY reduced file (the one without descriptions)
INPUT_PATH = r"C:\Users\pc\OneDrive - Al Akhawayn University in Ifrane\Desktop\BAI_midterm_project\data\python_csv's\deleted_columns_data_1048576_rows.csv"
OUTPUT_PATH = r"C:\Users\pc\OneDrive - Al Akhawayn University in Ifrane\Desktop\BAI_midterm_project\data\python_csv's\final_tableau_dataset.csv"

def process_data(input_file, output_file):
    print("Loading data...")
    # Load the data
    df = pd.read_csv(input_file)
    
    initial_rows = len(df)
    print(f"Original Row Count: {initial_rows}")

    # 1. HANDLING MISSING DATA
    # We drop rows only if the critical metrics are missing. 
    # If a view count is missing, the row is useless for analytics.
    df.dropna(subset=['view_count', 'like_count', 'comment_count'], inplace=True)
    print(f"Rows after dropping null metrics: {len(df)}")

    # 2. NORMALIZATION / STANDARDIZATION
    # Creating "Rates" to compare big channels vs small channels fairly.
    
    # Avoid division by zero by replacing 0 views with 1 (negligible impact on 1M rows)
    df['view_count'] = df['view_count'].replace(0, 1)

    print("Calculating Engagement Rates...")
    # Engagement Rate = (Likes + Comments) / Views
    df['engagement_rate'] = (df['like_count'] + df['comment_count']) / df['view_count']
    
    # Like Ratio = Likes / Views
    df['like_ratio'] = df['like_count'] / df['view_count']
    
    # Comment Ratio = Comments / Views
    df['comment_ratio'] = df['comment_count'] / df['view_count']

    # 3. OUTLIER DETECTION (The IQR Method)
    # We will flag outliers in 'view_count' so you can filter them in Tableau
    # rather than deleting them (since viral videos are important).
    
    print("Identifying Outliers...")
    Q1 = df['view_count'].quantile(0.25)
    Q3 = df['view_count'].quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds (1.5 * IQR is standard)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Create a flag column. 
    # True = Statistical Outlier (Likely a mega-viral video)
    # False = Normal distribution
    df['is_view_outlier'] = np.where((df['view_count'] < lower_bound) | (df['view_count'] > upper_bound), True, False)

    # 4. FINAL CLEANUP
    # Rounding decimals to 4 places to save file size/memory
    df['engagement_rate'] = df['engagement_rate'].round(4)
    df['like_ratio'] = df['like_ratio'].round(4)
    df['comment_ratio'] = df['comment_ratio'].round(4)

    print(f"Saving final dataset to: {output_file}")
    df.to_csv(output_file, index=False)
    print("Done! Import this new file into Tableau.")

if __name__ == "__main__":
    try:
        process_data(INPUT_PATH, OUTPUT_PATH)
    except FileNotFoundError:
        print("Error: Could not find the input file. Please check the INPUT_PATH path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
