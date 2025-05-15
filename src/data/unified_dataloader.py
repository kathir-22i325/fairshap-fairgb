import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import copy
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import re



def load_dataset(dataset_name):
    """
    Load the specified dataset
    Parameters:
    dataset_name (str): Dataset name ('german_credit' or 'uci')
    Returns:
    orginal_data (pd.DataFrame): Original dataset
    processed_data (pd.DataFrame): Processed dataset
    """
    if dataset_name == 'german_credit':
        original_data, processed_data = german_credit()
    elif dataset_name == 'adult':
        original_data, processed_data = adult()
    elif dataset_name == 'census_income_kdd':
        original_data, processed_data = census_income_kdd()
    elif dataset_name == 'default_credit':
        original_data, processed_data = default_credit()
    elif dataset_name == 'compas':
        original_data, processed_data = compas()
    elif dataset_name == 'compas4race':
        original_data, processed_data = compas4race()
    else:
        raise ValueError(
            f"Unknown dataset: {dataset_name}. If you want to use the German Credit Dataset, please input 'german_credit'. If you want to use the UCI Dataset, please input 'uci'. If you want to use the bank_marketing Dataset, please input 'bank_marketing'."
        )
    return original_data, processed_data


def german_credit():
    '''Load the German Credit dataset and preprocess it.'''
    # Load data
    data = pd.read_csv('dataset/german_credit/german_credit.csv')
    original_data = data.copy()

    # Print number of missing values per column
    missing_values = data.isnull().sum()
    print(missing_values)

    # Handle missing values
    saving_imputer = SimpleImputer(strategy='most_frequent')
    checking_imputer = SimpleImputer(strategy='most_frequent')
    data['Saving accounts'] = saving_imputer.fit_transform(data[['Saving accounts']]).ravel()
    data['Checking account'] = checking_imputer.fit_transform(data[['Checking account']]).ravel()

    # 1. Standardize continuous variables
    scaler = StandardScaler()
    data[['Age', 'Credit amount', 'Duration']] = scaler.fit_transform(data[['Age', 'Credit amount', 'Duration']])

    # 2. Encode gender variable
    data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})

    # 3. One-hot encode categorical variables
    categorical_columns = ['Job', 'Housing', 'Saving accounts', 'Checking account', 'Purpose']
    data = pd.get_dummies(data, columns=categorical_columns, drop_first=False)

    # Convert boolean one-hot encoded columns to integers
    for column in data.select_dtypes(include=['bool']).columns:
        data[column] = data[column].astype(int)

    # 4. Map target variable
    data['Risk'] = data['Risk'].map({'good': 0, 'bad': 1})

    # Move Risk column to last position
    risk_column = data.pop('Risk')
    data['Risk'] = risk_column

    # Rename Sex column to sex
    data.rename(columns={'Sex': 'sex'}, inplace=True)

    return original_data, data


def adult():
    
    '''Load the UCI dataset and preprocess it.'''

    # column names
    column_names = [
        "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
        "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        "hours-per-week", "native-country", "income"
    ]

    # import dataset from adult.data
    original_data = pd.read_csv('dataset/uci_dataset/adult.data', header=None, names=column_names, skipinitialspace=True)
    df = original_data.copy()
    df = df.dropna()

    # 0 represents <=50K, 1 represents >50K
    df['income'] = df['income'].map({'<=50K': 0, '>50K': 1})
    # 0 represents Female, 1 represents Male
    label_encoder_sex = LabelEncoder()
    df['sex'] = label_encoder_sex.fit_transform(df['sex'])

    # numerical and categorical features
    numeric_features = ['age', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
    categorical_features = ['workclass', 'education', 'marital-status', 'occupation', 'relationship','race','native-country']

    # numeric_features --- Scaler
    scaler = StandardScaler()
    df_numeric = scaler.fit_transform(df[numeric_features])
    df_numeric = pd.DataFrame(df_numeric, columns=numeric_features)  # , index=X_labeled.index  means keep the same index

    # categorical_features --- OneHot encoder
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    df_categorical = encoder.fit_transform(df[categorical_features])
    # get feature names after one-hot encoding
    encoded_feature_names = encoder.get_feature_names_out(categorical_features)
    df_categorical = pd.DataFrame(df_categorical, columns=encoded_feature_names)

    # sensitive features 
    sex_column = df['sex']
    # race_column = df['race']

    # target feature
    target = df['income']

    # df_processed = pd.concat((df_numeric, sex_column, race_column, df_categorical, target), axis=1)

    df_processed = pd.concat((df_numeric, sex_column, df_categorical, target), axis=1)
    # print(f'X_processed shape: {df_processed.shape}')
    return original_data, df_processed

def census_income_kdd():
    '''Load the Bank marketing dataset and preprocess it.'''

    colum_names = ["age","workclass","industry_code","occupation_code","education","wage_per_hour","enrolled_in_edu_inst_last_wk",
    "marital_status","major_industry_code","major_occupation_code","race","hispanic_origin","sex","member_of_a_labour_union","reason_for_unemployment",
    "employment_status","capital_gains","capital_losses","dividend_from_stocks","tax_filler_status","region_of_previous_residence","state_of_previous_residence",
    "detailed_household_and_family_stat","detailed_household_summary_in_household","instance_weight","migration_code_change_in_msa","migration_code_change_in_reg",
    "migration_code_move_within_reg","live_in_this_house_1_year_ag","migration_prev_res_in_sunbelt","num_persons_worked_for_employer","family_members_under_18","country_of_birth_father",
    "country_of_birth_mother","country_of_birth_self","citizenship","own_business_or_self_employed","fill_inc_questionnaire_for_veteran's_admin","veterans_benefits","weeks_worked_in_year","year","class"]
    categorical_features = [
    "workclass","industry_code","occupation_code","education","enrolled_in_edu_inst_last_wk",
    "marital_status","major_industry_code","major_occupation_code","hispanic_origin","member_of_a_labour_union","reason_for_unemployment",
    "employment_status","tax_filler_status","region_of_previous_residence","state_of_previous_residence",
    "detailed_household_and_family_stat","detailed_household_summary_in_household","migration_code_change_in_msa","migration_code_change_in_reg",
    "migration_code_move_within_reg","live_in_this_house_1_year_ag","migration_prev_res_in_sunbelt","family_members_under_18","country_of_birth_father",
    "country_of_birth_mother","country_of_birth_self","citizenship","own_business_or_self_employed","fill_inc_questionnaire_for_veteran's_admin","veterans_benefits","year"
    ]
    numeric_features = [
    "age","wage_per_hour","capital_gains","capital_losses","dividend_from_stocks",
    "instance_weight","num_persons_worked_for_employer","weeks_worked_in_year"]

    # feature_to_keep = [ "workclass","industry_code","occupation_code","education","enrolled_in_edu_inst_last_wk",
    # "marital_status","major_industry_code","major_occupation_code","hispanic_origin","member_of_a_labour_union","reason_for_unemployment",
    # "employment_status","tax_filler_status","region_of_previous_residence","state_of_previous_residence",
    # "detailed_household_and_family_stat","detailed_household_summary_in_household","instance_weight","migration_code_change_in_msa","migration_code_change_in_reg",
    # "migration_code_move_within_reg","live_in_this_house_1_year_ag","migration_prev_res_in_sunbelt","family_members_under_18","country_of_birth_father",
    # "country_of_birth_mother","country_of_birth_self","citizenship","own_business_or_self_employed","fill_inc_questionnaire_for_veteran's_admin","veterans_benefits","year"]

    df1 = pd.read_csv('dataset/census_income_kdd/raw/census-income.data',header=None,names=colum_names)
    df2 = pd.read_csv('dataset/census_income_kdd/raw/census-income.test',header=None,names=colum_names)
    data = pd.concat([df1, df2], ignore_index=True)
    original_data = data.copy()
    
    
    data = data.dropna()
    # # targets; 1 , otherwise 0
    target = (data["class"] == " - 50000.").astype(int)
    data = data.drop_duplicates(keep="first", inplace=False)

    # print number of missing values per column
    missing_values = data.isnull().sum()
    print(missing_values)

    # numeric_features --- Scaler
    scaler = StandardScaler()
    df_numeric = scaler.fit_transform(data[numeric_features])
    df_numeric = pd.DataFrame(df_numeric, columns=numeric_features)  # , index=X_labeled.index  means keep the same index

    # categorical_features --- OneHot encoder
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    df_categorical = encoder.fit_transform(data[categorical_features])
    # get feature names after one-hot encoding
    encoded_feature_names = encoder.get_feature_names_out(categorical_features)
    df_categorical = pd.DataFrame(df_categorical, columns=encoded_feature_names)

    s = data['sex']
    s = (s == " Male").astype(int).to_frame()

    data = pd.concat((df_numeric, s , df_categorical, target), axis=1)
    
    original_data.columns = [re.sub(r"[\[\]<]", "", col) for col in original_data.columns]
    data.columns = [re.sub(r"[\[\]<]", "", col) for col in data.columns]

    data = data.dropna()
    return original_data, data

def default_credit():
    file_path = 'dataset/default_of_credit_card_clients/default of credit card clients.xls'
    original_data = pd.read_excel(file_path, skiprows=1)
    
    '''Process the data
    1. Drop the ID column
    2. rename the column 'SEX' to 'sex'(lowercase)
    3. change the mapping relationship from (male:1, female:2) to (female:0, male:1)
    4. One-hot encoding for the categorical features
    5. Standardization for the numerical features
    '''
    processed_data = original_data.copy()
    # 1. Drop the ID column
    processed_data.drop('ID', axis=1, inplace=True)
    # 2. rename the column
    processed_data = processed_data.rename(columns={'SEX': 'sex'})
    processed_data = processed_data.rename(columns={'default payment next month': 'default_payment_next_month'})
    # 3. change the mapping relationship
    processed_data.loc[processed_data['sex'] == 2, 'sex'] = 0
    # 4. One-hot encoding for the categorical features
    categorical_features = ['EDUCATION', 'MARRIAGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
    processed_data = pd.get_dummies(processed_data, columns=categorical_features)
    processed_data = processed_data.astype(int)
    # 5. Standardization for the numerical features
    numerical_features = ['LIMIT_BAL', 'AGE', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']
    scaler = StandardScaler()
    processed_data[numerical_features] = scaler.fit_transform(processed_data[numerical_features])
    # 6. Move the target column to the last column
    target_column = processed_data.pop('default_payment_next_month')
    processed_data['default_payment_next_month'] = target_column
    return original_data, processed_data

def compas():
    '''Load the COMPAS dataset and preprocess it.
    
    1. Load the COMPAS dataset
    2. choose existing_columns and drop the rest
    3. set the mapping relationship female:0, male:1
    4. One-hot encoding for the categorical features
    5. Standardization for the numerical features
    '''
    # 1. Load the COMPAS dataset
    file_path = 'dataset/compas/compas-scores-two-years.csv'
    original_data = pd.read_csv(file_path,sep=",",header=0)
    # 2. choose existing_columns and drop the rest
    processed_data = original_data.copy()
    existing_columns = ['sex','age', 'race', 'juv_fel_count','juv_misd_count','juv_other_count','priors_count','c_charge_degree','score_text','type_of_assessment','two_year_recid']
    processed_data = processed_data[existing_columns]
    # 3. set the mapping relationship
    processed_data['sex'] = processed_data['sex'].map({'Male':1,'Female':0})
    # 4. One-hot encoding for the categorical features
    categorical_features = ['race', 'c_charge_degree', 'type_of_assessment','score_text']
    processed_data = pd.get_dummies(processed_data, columns=categorical_features)
    processed_data = processed_data.astype(int)
    # 5. Standardization for the numerical features
    numerical_features = ['age', 'juv_fel_count','juv_misd_count', 'juv_other_count', 'priors_count']
    scaler = StandardScaler()
    processed_data[numerical_features] = scaler.fit_transform(processed_data[numerical_features])
    # 6. Move the target column to the last column
    target_column = processed_data.pop('two_year_recid')
    processed_data['two_year_recid'] = target_column
    return original_data, processed_data

def compas4race():
    '''Load the COMPAS dataset and preprocess it (sensitive feature = race,  only reserve race_African-American and race_Caucasian).
    
    1. Load the COMPAS dataset
    2. choose existing_columns and drop the rest, and only reserve rows with 'African-American' and 'Caucasian'
    3. set the mapping relationship {'Female':0, 'Male':1} and {'Caucasian':0, 'African-American':1}
    4. One-hot encoding for the categorical features
    5. Standardization for the numerical features
    '''
    # 1. Load the COMPAS dataset
    file_path = 'dataset/compas/compas-scores-two-years.csv'
    original_data = pd.read_csv(file_path,sep=",",header=0)
    # 2. choose existing_columns and drop the rest
    processed_data = original_data.copy()
    existing_columns = ['sex','age', 'race', 'juv_fel_count','juv_misd_count','juv_other_count','priors_count','c_charge_degree','score_text','type_of_assessment','two_year_recid']
    processed_data = processed_data[existing_columns]
    processed_data = processed_data[processed_data['race'].isin(['African-American', 'Caucasian'])]
    processed_data = processed_data.reset_index(drop=True)
    # 3. set the mapping relationship
    processed_data['sex'] = processed_data['sex'].map({'Male':1,'Female':0})
    processed_data['race'] = processed_data['race'].map({'Caucasian':0, 'African-American':1})
    # 4. One-hot encoding for the categorical features
    categorical_features = ['c_charge_degree', 'type_of_assessment','score_text']
    processed_data = pd.get_dummies(processed_data, columns=categorical_features)
    processed_data = processed_data.astype(int)
    # 5. Standardization for the numerical features
    numerical_features = ['age', 'juv_fel_count','juv_misd_count', 'juv_other_count', 'priors_count']
    scaler = StandardScaler()
    processed_data[numerical_features] = scaler.fit_transform(processed_data[numerical_features])
    # 6. Move the target column to the last column
    target_column = processed_data.pop('two_year_recid')
    processed_data['two_year_recid'] = target_column
    return original_data, processed_data

def recruit():
    '''Utrecht Fairness Recruitment dataset- https://www.kaggle.com/datasets/ictinstitute/utrecht-fairness-recruitment-dataset?resource=download&select=recruitmentdataset-2022-1.3.csv'''
    file_path = 'dataset/recruit/recruitmentdataset-2022-1.3.csv'
    original_data = pd.read_csv(file_path)
    processed_data = original_data.copy()
    processed_data = processed_data.dropna()
    # 1. Drop the ID column
    processed_data.drop('Id', axis=1, inplace=True)
    # 2. rename 'gender' feature to 'sex'
    processed_data['sex'] = processed_data['gender'].map({'male':1, 'female':0})
    processed_data.drop('gender', axis=1, inplace=True)
    # 处理布尔特征
    for col in ['ind-debateclub', 'ind-programming_exp', 'ind-international_exp', 'ind-entrepeneur_exp', 'ind-exact_study']:
        # 确保值为布尔类型
        processed_data[col] = processed_data[col].astype(bool)
        # 映射布尔值
        processed_data[col] = processed_data[col].map({True:1, False:0})

    # 处理目标列 'decision'
    processed_data['decision'] = processed_data['decision'].map({True:1, False:0})
    numerical_features = ['age', 'ind-university_grade', 'ind-languages']
    scaler = StandardScaler()
    processed_data[numerical_features] = scaler.fit_transform(processed_data[numerical_features])   
    # 对分类特征进行独热编码
    categorical_features = ['nationality', 'sport', 'ind-degree', 'company']
    processed_data = pd.get_dummies(processed_data, columns=categorical_features)

    # 获取独热编码生成的列名
    one_hot_columns = [col for col in processed_data.columns if col not in original_data.columns]
    processed_data = processed_data.dropna()
    # 将独热编码列转换为整数类型
    processed_data[one_hot_columns] = processed_data[one_hot_columns].astype(int)

    target_column = processed_data.pop('decision')
    processed_data['decision'] = target_column
    return original_data, processed_data



if __name__ == '__main__':
    a, b =german_credit()
    print(a)
    print(b)

    # c, d = uci()
    # print(c)
    # print(d)