#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import gspread
import requests

token = 'AF5y90PW7vmJALond4SEGVBFwmt3Jhj7Ba7oclAeXL4'


# In[2]:


sa = gspread.service_account(filename='geprek-wani-c700b4b8002f.json')


# In[3]:


sheet = sa.open('Wani Spreadsheet')


# In[4]:


database = sheet.worksheet('Database Harga')


# In[5]:


df_harga = pd.DataFrame(database.get_all_records())


# In[6]:


worksheet = sheet.worksheet('Pesanan')


# In[7]:


df = pd.DataFrame(worksheet.get_all_records())


# In[8]:


df.rename(columns={'Request cabe GEPREK': 'Cabe', 'Sambal (+ 2.000)': 'Sambal'}, inplace=True)


# In[9]:


df.head()


# In[10]:


# create a list containing 'Makanan Utama' and 'Nama'
list = ['Makanan Utama', 'Cabe', 'Nama']

# replace the empty string with 1
df[list] = df[list].replace('', 1)

df[list]


# In[11]:


# Custom geprek
df_geprek = df[df['Makanan Utama'].str.contains('Geprek', case=False) & ~df['Makanan Utama'].str.contains('Indomie') & ~df['Makanan Utama'].str.contains('Udang')]
df_geprek


# In[12]:


# Dataframe not-geprek but include 'Indomie' and 'Udang'

df_not_geprek = df[~df['Makanan Utama'].str.contains('geprek', case=False)]

# Dataframe geprek tanpa nasi
df_geprek_tanpa_nasi = df_geprek[df_geprek['Makanan Utama'].str.contains('tanpa nasi')]

# Dataframe geprek dengan nasi
df_geprek_dengan_nasi = df_geprek[~df_geprek['Makanan Utama'].str.contains('tanpa nasi')]

# Dataframe indomie geprek
df_indomie_geprek = df[df['Makanan Utama'].str.contains('Indomie') & df['Makanan Utama'].str.contains('Geprek')]

# Dataframe udang geprek
df_udang_geprek = df[df['Makanan Utama'].str.contains('Udang') & df['Makanan Utama'].str.contains('Geprek')]

# Dataframe camilan
df_camilan = df[['Camilan', 'Nama']]
df_camilan = df_camilan[df_camilan['Camilan'] != '']

# Dataframe minuman
df_minuman = df[['Minuman', 'Nama']]
df_minuman = df_minuman[df_minuman['Minuman'] != '']

# Dataframe sambal
df_sambal = df[['Sambal', 'Nama']]
df_sambal = df_sambal[df_sambal['Sambal'] != '']


# In[13]:


combined_prints = []
combined_prints.append(f"Pesanan Depot Wani: {pd.Timestamp.now()}")
combined_prints.append("=====================================")
combined_prints.extend([f"{sum(df_geprek_dengan_nasi['Cabe'] == i)} Nasi Ayam Geprek Cabe {i} ({', '.join(df_geprek_dengan_nasi[df_geprek_dengan_nasi['Cabe'] == i]['Nama'])})" for i in df_geprek_dengan_nasi['Cabe'].unique()])
combined_prints.extend([f"{sum(df_geprek_tanpa_nasi['Cabe'] == i)} Ayam Geprek tanpa nasi Cabe {i} ({', '.join(df_geprek_tanpa_nasi[df_geprek_tanpa_nasi['Cabe'] == i]['Nama'])})" for i in df_geprek_tanpa_nasi['Cabe'].unique()])
combined_prints.extend([f"{sum(df_not_geprek['Makanan Utama'] == i)} {i} ({', '.join(df_not_geprek[df_not_geprek['Makanan Utama'] == i]['Nama'])})" for i in df_not_geprek['Makanan Utama'].unique()])
combined_prints.extend([f"{sum(df_indomie_geprek['Cabe'] == i)} {df_indomie_geprek[df_indomie_geprek['Cabe'] == i]['Makanan Utama'].iloc[0]} Cabe {i} ({', '.join(df_indomie_geprek[df_indomie_geprek['Cabe'] == i]['Nama'])})" for i in df_indomie_geprek['Cabe'].unique()])
combined_prints.extend([f"{sum(df_udang_geprek['Cabe'] == i)} {df_udang_geprek[df_udang_geprek['Cabe'] == i]['Makanan Utama'].iloc[0]} Cabe {i} ({', '.join(df_udang_geprek[df_udang_geprek['Cabe'] == i]['Nama'])})" for i in df_udang_geprek['Cabe'].unique()])
combined_prints.extend([f"{sum(df_camilan['Camilan'] == i)} {i} ({', '.join(df_camilan[df_camilan['Camilan'] == i]['Nama'])})" for i in df_camilan['Camilan'].unique()])
combined_prints.extend([f"{sum(df_minuman['Minuman'] == i)} {i} ({', '.join(df_minuman[df_minuman['Minuman'] == i]['Nama'])})" for i in df_minuman['Minuman'].unique()])
combined_prints.extend([f"{sum(df_sambal['Sambal'] == i)} {i} ({', '.join(df_sambal[df_sambal['Sambal'] == i]['Nama'])})" for i in df_sambal['Sambal'].unique()])

print('\n'.join(combined_prints))


# In[14]:


# remove all text after '(' in combined_prints
# combined_prints = [i.split('(')[0] for i in combined_prints]

# print('\n'.join(combined_prints))


# In[15]:


payload = {'message' : '\n'.join(combined_prints)}
r = requests.post('https://notify-api.line.me/api/notify'
                , headers={'Authorization' : 'Bearer {}'.format(token)}
                , params = payload)


# In[8]:


# duar
# payload = {'message' : 'Duar'}
# files = {'imageFile': open('duar.jpg', 'rb')}
# r = requests.post('https://notify-api.line.me/api/notify'
#                 , headers={'Authorization' : 'Bearer {}'.format(token)}
#                 , params = payload, files=files)


# In[7]:


# ambatukam
# payload = {'message' : 'Ambatukam @Jason'}
# files = {'imageFile': open('ambatukam.jpg', 'rb')}

# r = requests.post('https://notify-api.line.me/api/notify'
#                 , headers={'Authorization' : 'Bearer {}'.format(token)}
#                 , params = payload, files=files)


# In[ ]:




