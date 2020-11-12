# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Gather

# %%
import pandas as pd
import numpy as np
import re

# %%
patients = pd.read_csv('data/patients.csv')
treatments = pd.read_csv('data/treatments.csv')
adverse_reactions = pd.read_csv('data/adverse_reactions.csv')

# %% [markdown]
# ## Assess

# %%
patients.head(2)

# %%
treatments.head(2)

# %%
adverse_reactions.head(2)

# %%
patients.info()

# %%
treatments.info()

# %%
adverse_reactions.info()

# %%
all_columns = pd.Series(list(patients) + list(treatments) + list(adverse_reactions))
all_columns[all_columns.duplicated()]

# %%
list(patients)

# %%
patients[patients['address'].isnull()]

# %%
patients.describe()

# %%
treatments.describe()

# %%
patients.sample(5)

# %%
patients.surname.value_counts()

# %%
patients.address.value_counts()

# %%
patients[patients.address.duplicated()]

# %%
patients.weight.sort_values()

# %%
weight_lbs = patients[patients.surname == 'Zaitseva'].weight * 2.20462
height_in = patients[patients.surname == 'Zaitseva'].height
bmi_check = 703 * weight_lbs / (height_in * height_in)
bmi_check

# %%
patients[patients.surname == 'Zaitseva'].bmi

# %%
sum(treatments.auralin.isnull())

# %%
sum(treatments.novodra.isnull())

# %% [markdown]
# #### Quality
# ##### `patients` table
# - Zip code is a float not a string
# - Zip code has four digits sometimes
# - Tim Neudorf height is 27 in instead of 72 in
# - Full state names sometimes, abbreviations other times
# - Dsvid Gustafsson
# - Missing demographic information (address - contact columns) ***(can't clean)***
# - Erroneous datatypes (assigned sex, state, zip_code, and birthdate columns)
# - Multiple phone number formats
# - Default John Doe data
# - Multiple records for Jakobsen, Gersten, Taylor
# - kgs instead of lbs for Zaitseva weight
#
# ##### `treatments` table
# - Missing HbA1c changes
# - The letter 'u' in starting and ending doses for Auralin and Novodra
# - Lowercase given names and surnames
# - Missing records (280 instead of 350)
# - Erroneous datatypes (auralin and novodra columns)
# - Inaccurate HbA1c changes (leading 4s mistaken as 9s)
# - Nulls represented as dashes (-) in auralin and novodra columns
#
# ##### `adverse_reactions` table
# - Lowercase given names and surnames

# %% [markdown]
# #### Tidiness
# - Contact column in `patients` table should be split into phone number and email
# - Three variables in two columns in `treatments` table (treatment, start dose and end dose)
# - Adverse reaction should be part of the `treatments` table
# - Given name and surname columns in `patients` table duplicated in `treatments` and `adverse_reactions` tables

# %% [markdown]
# ## Clean

# %%
patients_clean = patients.copy()
treatments_clean = treatments.copy()
adverse_reactions_clean = adverse_reactions.copy()

# %%
treatments_cut = pd.read_csv("data/treatments_cut.csv")
treatments_cut.info()

# %% [markdown]
# ### Missing Data

# %% [markdown]
# <font color='red'>Complete the following two "Missing Data" **Define, Code, and Test** sequences after watching the *"Address Missing Data First"* video.</font>

# %% [markdown]
# #### `treatments`: Missing records (280 instead of 350)

# %% [markdown]
# ##### Define
# Add additional records to treatments dataset. Concat treatments_cut into treatments_clean to have 350 records total, not 280.

# %% [markdown]
# ##### Code

# %%
treatments_clean2 = pd.concat([treatments_clean, treatments_cut])
treatments_clean2.head()

# %% [markdown]
# ##### Test

# %%
treatments_clean2.info()

# %%
treatments_clean2.sample(20)

# %% [markdown]
# #### `treatments`: Missing HbA1c changes and Inaccurate HbA1c changes (leading 4s mistaken as 9s)
# *Note: the "Inaccurate HbA1c changes (leading 4s mistaken as 9s)" observation, which is an accuracy issue and not a completeness issue, is included in this header because it is also fixed by the cleaning operation that fixes the missing "Missing HbA1c changes" observation. Multiple observations in one **Define, Code, and Test** header occurs multiple times in this notebook.*

# %% [markdown]
# ##### Define
# Inaccurate HbA1c values. Update all hba1c_change values by subtracting hba1c_end from hba1c_start.

# %% [markdown]
# ##### Code

# %%
treatments_clean = treatments_clean2.copy()

# %%
treatments_clean.hba1c_change = treatments_clean.hba1c_start - treatments_clean.hba1c_end
treatments_clean.sample(10)

# %% [markdown]
# ##### Test

# %%
sum(treatments_clean.hba1c_change.isnull())

# %%
treatments_clean.info()

# %% [markdown]
# ### Tidiness

# %% [markdown]
# <font color='red'>Complete the following four "Tidiness" **Define, Code, and Test** sequences after watching the *"Cleaning for Tidiness"* video.</font>

# %% [markdown]
# #### Contact column in `patients` table contains two variables: phone number and email

# %% [markdown]
# ##### Define
# Separate contact data into appropriate columns, email & phone. 
#
# Hint 1: use regular expressions with pandas' [`str.extract` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.extract.html). Here is an amazing [regex tutorial](https://regexone.com/). Hint 2: [various phone number regex patterns](https://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number). Hint 3: [email address regex pattern](http://emailregex.com/), which you might need to modify to distinguish the email from the phone number.*

# %% [markdown]
# ##### Code

# %%
patients_clean.head(2)

# %%
patients_clean['email'] = patients_clean['contact'].str.extract(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,4})')
patients_clean

# %%
pd.isna(patients_clean.contact).value_counts()

# %%
patients_clean.dropna(inplace=True)


# %%
pd.isna(patients_clean.contact).value_counts()


# %%
def extract_phone(row):
    ph_re = re.compile(r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?')
    found = ph_re.search(row)
    if found:
        return found.group()
    else:
        return ''


# %%
extract_phone(patients_clean.contact[1])

# %%
patients_clean['phone'] = patients_clean.apply(lambda row: extract_phone(row['contact']), axis=1)
patients_clean


# %% [markdown]
# ### Fix email column where contacts contained phone numbers BEFORE the email address. Since email can start with numbers, it is theoritcally possible to have a phone number in front of letters in an email address.

# %%
def remove_phone_from_email(email,phone):
    if phone in email:
        return re.sub(phone, '', email)
    else:
        return email


# %%
patients_clean2 = patients_clean.iloc[0:5,:].copy()
patients_clean2

# %%
patients_clean2['email']

# %%
patients_clean2['email'] = patients_clean2.apply(lambda row: remove_phone_from_email(row['email'],row['phone']),axis=1)
patients_clean2

# %%
patients_clean['email'] = patients_clean.apply(lambda row: remove_phone_from_email(row['email'],row['phone']),axis=1)

# %%
patients_clean.drop(columns='contact',inplace=True)

# %% [markdown]
# ##### Test

# %%
patients_clean.sample(20)

# %% [markdown]
# #### Three variables in two columns in `treatments` table (treatment, start dose and end dose)

# %%
treatments_clean.head(5)

# %%
treat = treatments_clean.copy()

# %% [markdown]
# ##### Define
# Separate auralin & novodra columns into 3. Treatment, start dose, & end dose.

# %% [markdown]
# ##### Code

# %%
val = treat.iloc[0,2]
val2 = val.split()
val2


# %%
def split_dose(aur_dose,nov_dose):
    if aur_dose != '-':
        val = aur_dose.split()
        start_dose = val[0]
        start_dose = re.sub('u','',start_dose)
        end_dose = val[2]
        end_dose = re.sub('u','',end_dose)
        treatment = 'auralin'
    elif nov_dose != '-':
        val = nov_dose.split()
        start_dose = val[0]
        start_dose = re.sub('u','',start_dose)
        end_dose = val[2]
        end_dose = re.sub('u','',end_dose)
        treatment = 'novodra'
    
    return pd.Series([treatment,int(start_dose),int(end_dose)])


# %%
treat[['treatment','start_dose','end_dose']] = treat.apply(lambda row: split_dose(row.auralin,row.novodra), axis=1)
treat.sample(5)

# %%

# %% [markdown]
# ##### Test

# %%
treat.sample(20)

# %% [markdown]
# #### Adverse reaction should be part of the `treatments` table

# %% [markdown]
# ##### Define
# Consolidate files/dataframes table, adverse_reactions. Add data to treatments dataframe. 

# %% [markdown]
# ##### Code

# %%
adverse_reactions.sample(5)

# %%
adverse_reactions.info()

# %%
treat.info()

# %%
treat_adver = pd.concat([treat,adverse_reactions], join='outer')
treat_adver

# %%
treatment_adverse = pd.merge(adverse_reactions,treat, on='surname', how='outer')
treatment_adverse

# %%
treatment_adverse.query("surname == 'day'")

# %%
dups = treatment_adverse[treatment_adverse['surname'].duplicated()]

# %%
dups

# %%

# %%

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### Given name and surname columns in `patients` table duplicated in `treatments` and `adverse_reactions` tables  and Lowercase given names and surnames

# %% [markdown]
# ##### Define
# *Your definition here. Hint: [tutorial](https://chrisalbon.com/python/pandas_join_merge_dataframe.html) for one function used in the solution and [tutorial](http://erikrood.com/Python_References/dropping_rows_cols_pandas.html) for another function used in the solution.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# ### Quality

# %% [markdown]
# <font color='red'>Complete the remaining "Quality" **Define, Code, and Test** sequences after watching the *"Cleaning for Quality"* video.</font>

# %% [markdown]
# #### Zip code is a float not a string and Zip code has four digits sometimes

# %% [markdown]
# ##### Define
# *Your definition here. Hint: see the "Data Cleaning Process" page.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### Tim Neudorf height is 27 in instead of 72 in

# %% [markdown]
# ##### Define
# *Your definition here.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### Full state names sometimes, abbreviations other times

# %% [markdown]
# ##### Define
# *Your definition here. Hint: [tutorial](https://chrisalbon.com/python/pandas_apply_operations_to_dataframes.html) for method used in solution.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### Dsvid Gustafsson

# %% [markdown]
# ##### Define
# *Your definition here.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### Erroneous datatypes (assigned sex, state, zip_code, and birthdate columns) and Erroneous datatypes (auralin and novodra columns) and The letter 'u' in starting and ending doses for Auralin and Novodra

# %% [markdown]
# ##### Define
# *Your definition here. Hint: [documentation page](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.astype.html) for one method used in solution, [documentation page](http://pandas.pydata.org/pandas-docs/version/0.20/generated/pandas.to_datetime.html) for one function used in the solution, and [documentation page](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.strip.html) for another method used in the solution.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### Multiple phone number formats

# %% [markdown]
# ##### Define
# *Your definition here. Hint: helpful [Stack Overflow answer](https://stackoverflow.com/a/123681).*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### Default John Doe data

# %% [markdown]
# ##### Define
# *Your definition here. Recall that it is assumed that the data that this John Doe data displaced is not recoverable.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### Multiple records for Jakobsen, Gersten, Taylor

# %% [markdown]
# ##### Define
# *Your definition here.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here

# %% [markdown]
# #### kgs instead of lbs for Zaitseva weight

# %% [markdown]
# ##### Define
# *Your definition here.*

# %% [markdown]
# ##### Code

# %%
# Your cleaning code here

# %% [markdown]
# ##### Test

# %%
# Your testing code here
