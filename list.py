#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import gspread


# In[3]:


sa = gspread.service_account(filename='geprek-wani-c700b4b8002f.json')


# In[4]:


sheet = sa.open('Wani Spreadsheet')


# In[5]:


worksheet = sheet.worksheet('Pesanan')


# In[33]:


df = pd.DataFrame(worksheet.get_all_records())


# In[34]:


df.rename(columns={'Request cabe makanan utama': 'Cabe'}, inplace=True)


# In[35]:


df.head()


# In[36]:


# create a list containing 'Makanan Utama' and 'Nama'
list = ['Makanan Utama', 'Cabe', 'Nama']

# replace the empty string with 1
df[list] = df[list].replace('', 1)

df[list]


# In[37]:


# Custom geprek
df_geprek = df[df['Makanan Utama'].str.contains('Geprek')]
df_geprek


# In[38]:


# Dataframe non-geprek
df_not_geprek = df[~df['Makanan Utama'].str.contains('Geprek')]

# Dataframe geprek tanpa nasi
df_geprek_tanpa_nasi = df_geprek[df_geprek['Makanan Utama'].str.contains('tanpa nasi')]

# Dataframe geprek dengan nasi
df_geprek_dengan_nasi = df_geprek[~df_geprek['Makanan Utama'].str.contains('tanpa nasi')]

# Dataframe camilan
df_camilan = df[['Camilan', 'Nama']]
df_camilan = df_camilan[df_camilan['Camilan'] != '']

# Dataframe minuman
df_minuman = df[['Minuman', 'Nama']]
df_minuman = df_minuman[df_minuman['Minuman'] != '']

# Dataframe sambal
df_sambal = df[['Sambal', 'Nama']]
df_sambal = df_sambal[df_sambal['Sambal'] != '']


# In[41]:


combined_prints = []
combined_prints.append(f"Pesanan Depot Wani: {pd.Timestamp.now()}")
combined_prints.append("=====================================")
combined_prints.extend([f"{sum(df_geprek_dengan_nasi['Cabe'] == i)} Nasi Ayam Geprek Cabe {i} ({', '.join(df_geprek_dengan_nasi[df_geprek_dengan_nasi['Cabe'] == i]['Nama'])})" for i in df_geprek_dengan_nasi['Cabe'].unique()])
combined_prints.extend([f"{sum(df_geprek_tanpa_nasi['Cabe'] == i)} Ayam Geprek tanpa nasi Cabe {i} ({', '.join(df_geprek_tanpa_nasi[df_geprek_tanpa_nasi['Cabe'] == i]['Nama'])})" for i in df_geprek_tanpa_nasi['Cabe'].unique()])
combined_prints.extend([f"{sum(df_not_geprek['Makanan Utama'] == i)} {i} ({', '.join(df_not_geprek[df_not_geprek['Makanan Utama'] == i]['Nama'])})" for i in df_not_geprek['Makanan Utama'].unique()])
combined_prints.extend([f"{sum(df_camilan['Camilan'] == i)} {i} ({', '.join(df_camilan[df_camilan['Camilan'] == i]['Nama'])})" for i in df_camilan['Camilan'].unique()])
combined_prints.extend([f"{sum(df_minuman['Minuman'] == i)} {i} ({', '.join(df_minuman[df_minuman['Minuman'] == i]['Nama'])})" for i in df_minuman['Minuman'].unique()])
combined_prints.extend([f"{sum(df_sambal['Sambal'] == i)} {i} ({', '.join(df_sambal[df_sambal['Sambal'] == i]['Nama'])})" for i in df_sambal['Sambal'].unique()])

print('\n'.join(combined_prints))


# In[ ]:




