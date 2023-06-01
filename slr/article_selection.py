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
    # df1_path = '../data/ieee_xplore_search_results_r2/ieee_xplore_search_result_r2_all_4800.xlsx'
    # df2_path = '../data/ieee_xplore_search_results_r2/ieee_xplore_search_result_r2_all.csv'
    # df2_path = '../data/slr_sheet_ps_R2_v1.xlsx'
    # df2_path = 'D:/Users/Morteza/OneDrive/Online2/_04_2o/o2_university/PhD/project23_articles/a170_similarity_naming_readability/survey/sheets/slr_sheet_ps_R2_v3.xlsx'

    df1_path = 'D:/Users/Morteza/OneDrive/Online2/_04_2o/o2_university/PhD/project23_articles/a170_similarity_naming_readability/survey/submit/Systems and Software/revision3_20230519/slr_papers_R3_v1.xlsx'
    df2_path = 'C:/Users/Morteza/Desktop/SLR_R3/SpringerLink/SpringerLinkMerged_DuplicatedRemoved.csv'

    df1 = pd.read_excel(df1_path, sheet_name='initial-articles')
    df2 = pd.read_csv(df2_path)
    # df2 = pd.read_excel(df2_path, sheet_name='initial-articles')
    #

    is_duplicated = []
    for i, row in df2.iterrows():
        document_title = row['Item Title']
        # print(document_title)
        df_new = df1[df1['Article title'] == document_title]
        if len(df_new) > 0:
            is_duplicated.append(True)
            print(f'Duplicated at row {i}')
        else:
            is_duplicated.append(False)
    df2['Duplicated'] = is_duplicated
    print(f'Number of duplicated rows: {len(is_duplicated)}')
    df2 = df2[df2['Duplicated'] == False]
    # df1.to_excel('../data/ieee_xplore_search_result_r2_all_annotated.xlsx', index=False)
    # df1.to_excel('../data/ieee_xplore_search_results_r2/ieee_xplore_search_result_r2_all_non-duplicated_search2_v3.xlsx',
    #              index=False)

    df2.to_excel('SpringerLinkMerged_DuplicatedRemoved_v2.xlsx', index=False)


def select_by_keywords():
    # df1_path = '../data/ieee_xplore_search_results_r2/ieee_xplore_search_result_r2_all_non-duplicated_v2.xlsx'
    # df1_path = 'C:/Users/Morteza/Desktop/SLR_R3/SpringerLink/SpringerLinkMerged_DuplicatedRemoved_v2.xlsx'
    df1_path = 'C:/Users/Morteza/Desktop/SLR_R3/ACMDL/acm_all_2863_duplicated_removed.xlsx'
    # df1 = pd.read_excel(df1_path, sheet_name='SpringerLinkR3-initial')
    df1 = pd.read_excel(df1_path, sheet_name='initial-articles_r3_noduplicate')
    x = 0
    for index, row in df1.iterrows():
        document_title = row['Article title']
        if ('clone' in document_title or 'Clone' in document_title or
                'Similarity' in document_title or 'similarity' in document_title):
            x += 1
            if str(row['Applied exclusion criteria']) == 'nan':
                print('Selected')
                df1.loc[index, 'Applied exclusion criteria'] = 'Selected'
        else:
            if str(row['Applied exclusion criteria']) == 'nan':
                df1.loc[index, 'Applied exclusion criteria'] = 'EC4'
                print('###', row['Applied exclusion criteria'])
                print(row['ID'], document_title)
    print(x)
    df1.to_excel(df1_path, sheet_name='initial-articles_r3_noduplicate', index=False)


def process_acm_digital_library():
    df1_path = 'C:/Users/Morteza/Desktop/SLR_R3/ACMDL/acm_all_2863.xlsx'
    columns = ['Journal', 'Year', 'Title', 'Booktitle', 'Publisher']
    df1 = pd.read_excel(df1_path, sheet_name='initial-articles_r3_all')

    df2_path = 'D:/Users/Morteza/OneDrive/Online2/_04_2o/o2_university/PhD/project23_articles/a170_similarity_naming_readability/survey/submit/Systems and Software/revision3_20230519/slr_papers_R3_v2.xlsx'
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
    df1.to_excel('C:/Users/Morteza/Desktop/SLR_R3/ACMDL/acm_all_2863_duplicated_removed.xlsx',
                 sheet_name='initial-articles_r3_duplicated_removed')


if __name__ == '__main__':
    # merge_ieee_results_r2()
    # remove_duplicated_papers()
    select_by_keywords()
    # process_acm_digital_library()
