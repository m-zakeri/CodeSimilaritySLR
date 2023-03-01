"""
Scripts used to apply parts of exclusion criteria automatically,

"""
import os

import numpy as np
import pandas as pd


def merge_ieee_results_r2(path='../data/ieee_xplore_search_result_r2/raw/'):
    files = os.listdir(path)
    files = [os.path.join(path, f) for f in files if os.path.isfile(path + '/' + f)]  # Filtering only the files.
    print(*files, sep="\n")
    df = pd.DataFrame()
    for f in files:
        df1 = pd.read_csv(f)
        df = pd.concat([df, df1], ignore_index=True)
    df.to_csv('../data/ieee_xplore_search_results_r2/ieee_xplore_search_result_r2_all.csv')


def remove_duplicated_papers():
    df1_path = '../data/ieee_xplore_search_results_r2/ieee_xplore_search_result_r2_all.csv'
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
    df1.to_excel('../data/ieee_xplore_search_results_r2/ieee_xplore_search_result_r2_all_non-duplicated.xlsx',
                 index=False)


def select_by_keywords():
    df1_path = '../data/ieee_xplore_search_results_r2/ieee_xplore_search_result_r2_all_non-duplicated_v2.xlsx'
    df1 = pd.read_excel(df1_path, sheet_name='IEEE_R2_initial-articles')
    x = 0
    for index, row in df1.iterrows():
        document_title = row['Article title']
        if 'clone' in document_title or 'Clone' in document_title:
            x += 1
            if str(row['Applied exclusion criteria']) == 'nan':
                print('***')
                df1.loc[index, 'Applied exclusion criteria'] = ['Selected']
        else:
            if str(row['Applied exclusion criteria']) == 'nan':
                df1.loc[index, 'Applied exclusion criteria'] = ['EC4']
                print('###', row['Applied exclusion criteria'])
                print(row['ID'], document_title)
    print(x)
    df1.to_excel(df1_path, sheet_name='IEEE_R2_initial-articles', index=False)


def process_acm_digital_library():
    df1_path = '../data/acm_digital_library_results_r2/raw/acm_digital_library_r2_v2.xlsx'
    columns = ['Journal', 'Year', 'Title', 'Booktitle', 'Publisher']
    df1 = pd.read_excel(df1_path, sheet_name='initial-articles_r2_all')

    df2_path = '../data/slr_sheet_ps_R2_v1.xlsx'
    df2 = pd.read_excel(df2_path, sheet_name='initial-articles')

    is_duplicated = []
    for i, row in df1.iterrows():
        document_title = row['Article title']
        # print(document_title)
        df_new = df2[df2['Article title'] == document_title]
        if len(df_new) > 0:
            is_duplicated.append(True)
            print(f'Duplicated at row {i}')
        else:
            is_duplicated.append(False)
    df1['Duplicated'] = is_duplicated
    df1 = df1[df1['Duplicated'] == False]

    print(df1)
    df1.to_excel('../data/acm_digital_library_results_r2/acm_digital_library_r2_v3.xlsx',
                 sheet_name='initial-articles_r2_new')


if __name__ == '__main__':
    # merge_ieee_results_r2()
    # remove_duplicated_papers()
    # select_by_keywords()
    process_acm_digital_library()
