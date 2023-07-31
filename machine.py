
import pandas as pd
import numpy as np

def Machine(data):
# veri setinin okunması
    df = pd.read_csv('datas.csv')

# gereksiz parametrelerin silinmesi
    df.drop('id',inplace=True,axis=1)
    df.drop('com_time',inplace=True,axis=1)
    df.drop('device_id',inplace=True,axis=1)

# toprak neminde bir önceki veriden %10 fazla ise bitkinin sulanmış olduğunu belirten bir parametreli yeni veri seti oluşturuldu
    son_toprak_nemi = df['soil_humidity'].shift(1)
    artis_yuzdesi = (df['soil_humidity'] - son_toprak_nemi) / son_toprak_nemi * 100
    df['sulama'] = np.where(artis_yuzdesi > 50,1 , 0)

    df.to_csv('yeni_dosya_adi.csv', index=False)


    from sklearn.ensemble import RandomForestRegressor
    # Bağımsız değişkenlerin seçilmesi
    X = df.iloc[:, [0,1,3,4]].values
    # Bağımlı değişkenin seçilmesi: Toprak Nemi
    y = df.iloc[:,2].values
    regressor = RandomForestRegressor(n_estimators=100, random_state=100)
    # Modelin eğitilmesi
    regressor.fit(X, y)
    regressor.fit(X, y)
    # Tahmin yapılacak yeni verinin oluşturulması
    yeni_veri = [data]
    print(yeni_veri)
    # Tahmin yapılması
    predict_array = regressor.predict(yeni_veri)
    predict= predict_array[0]

    return predict