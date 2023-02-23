"""
Scripts used to apply parts of exclusion criteria automatically,

"""
import os
import pandas as pd


def merge_ieee_results_r2(path='../data/ieee_xplore_search_result_r2'):
    files = os.listdir(path)
    files = [os.path.join(path, f) for f in files if os.path.isfile(path + '/' + f)]  # Filtering only the files.
    print(*files, sep="\n")
    df = pd.DataFrame()
    for f in files:
        df1 = pd.read_csv(f)
        df = pd.concat([df, df1], ignore_index=True)
    df.to_csv('../data/ieee_xplore_search_result_r2_all.csv')


def remove_duplicated_papers():
    df1_path = '../data/ieee_xplore_search_result_r2_all.csv'
    df2_path = '../data/slr_sheet_ps_R2_v1.xlsx'
    df1 = pd.read_csv(df1_path)
    df2 = pd.read_excel(df2_path, sheet_name='initial-articles')
    #

    is_duplicated = []
    for i, row in df1.iterrows():
        document_title = row['Document Title']
        # print(document_title)
        df_new = df2[df2['Article title'] == document_title]
        if len(df_new) > 0:
            is_duplicated.append(True)
            print(f'Duplicated at row {i}')
        else:
            is_duplicated.append(False)
    df1['Duplicated'] = is_duplicated
    df1 = df1[df1['Duplicated'] == False]
    # df1.to_excel('../data/ieee_xplore_search_result_r2_all_annotated.xlsx', index=False)
    df1.to_excel('../data/ieee_xplore_search_result_r2_all_non-duplicated.xlsx', index=False)


if __name__ == '__main__':
    # merge_ieee_results_r2()
    remove_duplicated_papers()
