from time import strptime
import streamlit as st
import pandas as pd
import datetime as dt
import yfinance as yf
from datetime import datetime


st.write('Práctica Individual n°2 - Alumno Costa Justo')

st.title('Mercado Bursátil')
st.write('<h4><b>Fondo Indexado S&P500</b></h4>', unsafe_allow_html=True)

# Definir fechas

start_date = datetime(2000, 1, 1)
end_date = datetime(2023, 2, 28)
int = '1d'

# OBTENER PREFIJOS DE TODAS LAS EMPRESAS

tickers_sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
Empresas = tickers_sp500['Symbol'].to_list()

# BARRA LATERAL 

st.sidebar.write('**Selecciona los parámetros del reporte**')
start_date = st.sidebar.date_input("Fecha de Inicio", start_date)
end_date = st.sidebar.date_input("Fecha de Cierre", end_date)
int = st.sidebar.selectbox('Intervalos de tiempo', ["1d", "5d", "1wk", "1mo", "3mo"])
empresa = st.sidebar.selectbox('Empresa detallada', Empresas)

#IMPORTACIÓN DE LA TABLA HISTORICA CON YFINANCE

sp500_ticker = yf.Ticker('^GSPC')
historical_prices = sp500_ticker.history(start = start_date , end = end_date, interval = int)

historical_prices = historical_prices.reset_index()
historical_prices['Date'] = pd.to_datetime(historical_prices['Date'])
historical_prices[['Open','High','Low','Close']] = historical_prices[['Open','High','Low','Close']].round(2)




# Valores Principales 

actual_price = historical_prices['Close'].iloc[-1]
yest_price = historical_prices['Close'].iloc[-2]
actual_vol = historical_prices['Volume'].iloc[-1]
yest_vol = historical_prices['Volume'].iloc[-2]

col1, col2, col3 = st.columns(3)
col1.metric("Valor Actual", 'usd ' + str(actual_price), str(round((100*(actual_price - yest_price)/yest_price),2)) + '%' )
col2.metric("Varianza", 'usd ' + str(round(historical_prices['High'].iloc[-1] - historical_prices['Low'].iloc[-1],2)), str(round((100*(historical_prices['High'].iloc[-1] - historical_prices['Low'].iloc[-1])/historical_prices['Low'].iloc[-1]),2)) + '%')
col3.metric("Volumen", str(actual_vol), str(round((100*(actual_vol - yest_vol)/yest_vol),2)) + '%')

#Gráficos

st.write('- Gráfico de los valores de la acción con relación al periodo seleccionado')
st.line_chart(historical_prices['Close'])


st.write('- Gráfico del volumén de transacciones de la acción con relación al periodo seleccionado')
st.line_chart(historical_prices['Volume'])

st.text('Los índices del eje X son todos los intervalos en función del periodo de tiempo seleccionado')

#Punto de críticos históricos

max_historical = historical_prices['High'].max()
min_historical = historical_prices['Low'].min()

vol_max_historical = historical_prices['Volume'].max()
vol_min_historical = historical_prices['Volume'].min()

Date_max = pd.to_datetime(((historical_prices.loc[historical_prices['High'] == max_historical]).iloc[0]['Date']))
Date_min = pd.to_datetime(((historical_prices.loc[historical_prices['Low'] == min_historical]).iloc[0]['Date']))

Date_max_vol = pd.to_datetime(((historical_prices.loc[historical_prices['Volume'] == vol_max_historical]).iloc[0]['Date']))
Date_min_vol = pd.to_datetime(((historical_prices.loc[historical_prices['Volume'] == vol_min_historical]).iloc[0]['Date']))

col1, col2, col3, col4 = st.columns(4)
col1.write('**Máx valor histórico**', unsafe_allow_html=True)
col1.write('usd ' + str(max_historical))
col1.text((Date_max).strftime('%Y-%m-%d'))

col2.write('**Mín valor histórico**', unsafe_allow_html=True)
col2.write('usd ' + str(min_historical))
col2.text((Date_max).strftime('%Y-%m-%d'))

col3.write('**Máx volúmen histórico**', unsafe_allow_html=True)
col3.write(str(vol_max_historical))
col3.text((Date_max_vol).strftime('%Y-%m-%d'))

col4.write('**Mín volúmen histórico**', unsafe_allow_html=True)
col4.write(str(vol_min_historical))
col4.text((Date_min_vol).strftime('%Y-%m-%d'))

# REPORTES DE EMPRESA 
st.write('<h4><b>Reporte de la empresa seleccionada</b></h4>' , unsafe_allow_html=True)

#IMPORTACIÓN DE LA TABLA HISTORICA CON YFINANCE

sp500_ticker = yf.Ticker(empresa)
historical_prices_empresas = sp500_ticker.history(start = start_date , end = end_date, interval = int)

historical_prices_empresas = historical_prices_empresas.reset_index()
historical_prices_empresas['Date'] = pd.to_datetime(historical_prices_empresas['Date'])
historical_prices_empresas[['Open','High','Low','Close']] = historical_prices_empresas[['Open','High','Low','Close']].round(2)

# Valores Principales de la empresa selecionada

actual_price_emp = historical_prices_empresas['Close'].iloc[-1]
yest_price_emp = historical_prices_empresas['Close'].iloc[-2]
actual_vol_emp = historical_prices_empresas['Volume'].iloc[-1]
yest_vol_emp = historical_prices_empresas['Volume'].iloc[-2]

col1, col2, col3 = st.columns(3)
col1.metric("Valor Actual", 'usd ' + str(actual_price_emp), str(round((100*(actual_price_emp - yest_price_emp)/yest_price_emp),2)) + '%' )
col2.metric("Varianza", 'usd ' + str(round(historical_prices_empresas['High'].iloc[-1] - historical_prices_empresas['Low'].iloc[-1],2)), str(round((100*(historical_prices['High'].iloc[-1] - historical_prices['Low'].iloc[-1])/historical_prices['Low'].iloc[-1]),2)) + '%')
col3.metric("Volumen", str(actual_vol_emp), str(round((100*(actual_vol_emp - yest_vol_emp)/yest_vol_emp),2)) + '%')

# Gráfico de la empresa seleccionada 

st.write('- Gráfico de los valores de la acción con relación al periodo seleccionado')
st.line_chart(historical_prices_empresas['Close'])

#Punto de críticos históricos de la empresa seleccionada

max_historical_emp = historical_prices_empresas['High'].max()
min_historical_emp = historical_prices_empresas['Low'].min()

vol_max_historical_emp = historical_prices_empresas['Volume'].max()
vol_min_historical_emp = historical_prices_empresas['Volume'].min()

Date_max_emp = pd.to_datetime(((historical_prices_empresas.loc[historical_prices_empresas['High'] == max_historical_emp]).iloc[0]['Date']))
Date_min_emp = pd.to_datetime(((historical_prices_empresas.loc[historical_prices_empresas['Low'] == min_historical_emp]).iloc[0]['Date']))

Date_max_vol_emp = pd.to_datetime(((historical_prices_empresas.loc[historical_prices_empresas['Volume'] == vol_max_historical_emp]).iloc[0]['Date']))
Date_min_vol_emp = pd.to_datetime(((historical_prices_empresas.loc[historical_prices_empresas['Volume'] == vol_min_historical_emp]).iloc[0]['Date']))

col1, col2, col3, col4 = st.columns(4)
col1.write('**Máx valor histórico**', unsafe_allow_html=True)
col1.write('usd ' + str(max_historical_emp))
col1.text((Date_max_emp).strftime('%Y-%m-%d'))

col2.write('**Mín valor histórico**', unsafe_allow_html=True)
col2.write('usd ' + str(min_historical_emp))
col2.text((Date_max_emp).strftime('%Y-%m-%d'))

col3.write('**Máx volúmen histórico**', unsafe_allow_html=True)
col3.write(str(vol_max_historical_emp))
col3.text((Date_max_vol_emp).strftime('%Y-%m-%d'))

col4.write('**Mín volúmen histórico**', unsafe_allow_html=True)
col4.write(str(vol_min_historical_emp))
col4.text((Date_min_vol_emp).strftime('%Y-%m-%d'))

# Indices de Inversión 

Rendimiento = historical_prices_empresas['Close'].pct_change()
Volatilidad = Rendimiento.std()

Rendimiento_sp500 = historical_prices['Close'].pct_change()
Volatilidad_sp500 = Rendimiento_sp500.std()

risk_free_rate = 0.02 #tasa libre de riesgo del 2%
sharpe_ratio = (Rendimiento.mean() - risk_free_rate) / Volatilidad
sharpe_ratio_sp500 = (Rendimiento_sp500.mean() - risk_free_rate) / Volatilidad_sp500


st.write('<h5><b>KPIS IMPORTANTES</b></h5>', unsafe_allow_html=True)
st.write(' - Rendimiento = ' + str(round(Rendimiento.mean(),5)) + ' |SP500 = '+ str(round(Rendimiento_sp500.mean(),5)), unsafe_allow_html=True)
st.write(' - Volatilidad = ' + str(round(Volatilidad,5)) + ' |SP500 = '+ str(round(Volatilidad_sp500.mean(),5)), unsafe_allow_html=True)
st.write(' - Sharpe Ratio = ' + str(round(sharpe_ratio,5)) + ' |SP500 = '+ str(round(sharpe_ratio_sp500.mean(),5)))



