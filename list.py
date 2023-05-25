#!/usr/bin/env python
# coding: utf-8

# In[248]:


import pandas as pd
import gspread
import requests

token = 'AF5y90PW7vmJALond4SEGVBFwmt3Jhj7Ba7oclAeXL4'


# In[249]:


sa = gspread.service_account(filename='geprek-wani-abcd00886732.json')


# In[250]:


sheet = sa.open('Wani Spreadsheet')


# In[251]:


database = sheet.worksheet('Database Harga')


# In[252]:


df_harga = pd.DataFrame(database.get_all_records())


# In[253]:


worksheet = sheet.worksheet('Pesanan')


# In[254]:


df = pd.DataFrame(worksheet.get_all_records())


# In[255]:


df.rename(columns={'Request cabe GEPREK atau cabe TERIYAKI': 'Cabe', 
                   'Sambal Tambahan (Rp 2.000,-)': 'Sambal',
                   'Camilan (Rp 10.000,-)': 'Camilan',
                   }, inplace=True)


# In[256]:


df.head()


# In[257]:


# create a list containing 'Makanan Utama' and 'Nama'
list = ['Makanan Utama', 'Cabe', 'Nama']

# replace the empty string with 1 if Makanan Utama is not empty
df['Cabe'] = df['Cabe'].apply(lambda x: 1 if x == '' else x)

# remove everything after ' ~' in Makanan Utama
df['Makanan Utama'] = df['Makanan Utama'].apply(lambda x: x.split(' ~')[0])
df['Minuman'] = df['Minuman'].apply(lambda x: x.split(' ~')[0])

df[list]


# In[258]:


# Custom geprek
df_geprek = df[df['Makanan Utama'].str.contains('Geprek', case=False) & ~df['Makanan Utama'].str.contains('Indomie') & ~df['Makanan Utama'].str.contains('Udang')]
df_geprek


# In[259]:


# Dataframe not-geprek but include 'Indomie' and 'Udang'

df_not_geprek = df[~df['Makanan Utama'].str.contains('geprek', case=False)]

# drop rows with empty Makanan Utama
df_not_geprek = df_not_geprek[df_not_geprek['Makanan Utama'] != '']

# Dataframe geprek tanpa nasi
df_geprek_tanpa_nasi = df_geprek[df_geprek['Makanan Utama'].str.contains('tanpa Nasi')]

# Dataframe geprek dengan nasi
df_geprek_dengan_nasi = df_geprek[~df_geprek['Makanan Utama'].str.contains('tanpa Nasi')]

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


# In[260]:


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


# In[261]:


# remove all text after '(' in combined_prints
# combined_prints = [i.split('(')[0] for i in combined_prints]

# print('\n'.join(combined_prints))


# In[262]:


# payload = {'message' : '\n'.join(combined_prints)}
# r = requests.post('https://notify-api.line.me/api/notify'
#                 , headers={'Authorization' : 'Bearer {}'.format(token)}
#                 , params = payload)


# In[263]:


# duar
# payload = {'message' : 'Duar'}
# files = {'imageFile': open('duar.jpg', 'rb')}
# r = requests.post('https://notify-api.line.me/api/notify'
#                 , headers={'Authorization' : 'Bearer {}'.format(token)}
#                 , params = payload, files=files)


# In[264]:


# ambatukam
# payload = {'message' : 'Ambatukam @Jason'}
# files = {'imageFile': open('ambatukam.jpg', 'rb')}

# r = requests.post('https://notify-api.line.me/api/notify'
#                 , headers={'Authorization' : 'Bearer {}'.format(token)}
#                 , params = payload, files=files)


# In[ ]:




