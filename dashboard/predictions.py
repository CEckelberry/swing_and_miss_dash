import altair as alt
import streamlit as st
import pandas as pd
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from io import StringIO



def predictions():

    add_page_title("Predictions for Solar Production", layout="wide")

    sidebar()
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # # Perform query.
    # iea_data = conn.query(
    #     """
    #     SELECT * FROM "DSS_Datasets_GHG_Solar_iea_data"
    #     """
    # )

    # # Filter data
    # countries = ['Netherlands', 'Belgium', 'Luxembourg']
    # solar_filter = iea_data["Product"] == "Solar"
    # country_filter = iea_data["Country"].isin(countries)
    # iea_data = iea_data[solar_filter & country_filter]

    # # Process data
    # iea_data["Time"] = pd.to_datetime(iea_data["Time"], format="%B %Y")
    # iea_data['Value'] = pd.to_numeric(iea_data['Value'], errors='coerce')
    # data = iea_data.sort_values(by=["Time"], ascending=True)
    # data = data.loc[data['Time'] >= '2017-01-01']

    # # Separate data by country
    
    # NLdata = data[data["Country"] == "Netherlands"]
    # BEdata = data[data["Country"] == "Belgium"]
    # LUXdata = data[data["Country"] == "Luxembourg"]



    # NLdatamin = NLdata.rename(columns={"Time": 'ds', 'Value': 'y'})
    # BEdatamin = BEdata.rename(columns={"Time": 'ds', 'Value': 'y'})
    # LUXdatamin = LUXdata.rename(columns={"Time": 'ds', 'Value': 'y'})

    # BENE = pd.concat([NLdatamin, BEdatamin]).groupby(['ds']).sum().reset_index()
    # BENELUXdatamin = pd.concat([BENE, LUXdatamin]).groupby(['ds']).sum().reset_index()
    # # st.write(BENELUXdatamin.dtypes)
    # BENELUXdatamin = BENELUXdatamin.drop(columns=['Country', 'Balance', 'Product', 'Unit'])


    # # ""
    # # mBENELUX = NeuralProphet()
    # # mBENELUX.fit(BENELUXdatamin)

    # # df_futureBENELUX = mBENELUX.make_future_dataframe(BENELUXdatamin, periods=48)
    # # BENELUXforecast = mBENELUX.predict(df_futureBENELUX)

    # # BENELUXforecast.rename(columns={'yhat1': 'y'}, inplace=True)

    # # BeneluxPred = pd.concat([BENELUXdatamin, BENELUXforecast])

    # # st.subheader("BENELUX Prediction Data")
    # # st.write(BeneluxPred)""

    # # Provided CSV data
    csv_data = """ds,y
    2017-01-01 00:00:00,163.2186
    2017-02-01 00:00:00,179.6164
    2017-03-01 00:00:00,486.5024
    2017-04-01 00:00:00,642.4384
    2017-05-01 00:00:00,742.9395999999999
    2017-06-01 00:00:00,769.6764999999999
    2017-07-01 00:00:00,732.9254
    2017-08-01 00:00:00,705.1677
    2017-09-01 00:00:00,547.0392
    2017-10-01 00:00:00,359.91130000000004
    2017-11-01 00:00:00,185.2433
    2017-12-01 00:00:00,82.53129999999999
    2018-01-01 00:00:00,154.00259999999997
    2018-02-01 00:00:00,516.6856
    2018-03-01 00:00:00,555.1847
    2018-04-01 00:00:00,838.2304
    2018-05-01 00:00:00,1238.8682999999999
    2018-06-01 00:00:00,1092.7826999999997
    2018-07-01 00:00:00,981.1279999999999
    2018-08-01 00:00:00,782.5228
    2018-09-01 00:00:00,636.5418
    2018-10-01 00:00:00,495.4399
    2018-11-01 00:00:00,257.8059
    2018-12-01 00:00:00,153.4244
    2019-01-01 00:00:00,155.222
    2019-02-01 00:00:00,439.7724
    2019-03-01 00:00:00,620.8063
    2019-04-01 00:00:00,1140.8036
    2019-05-01 00:00:00,1291.0143
    2019-06-01 00:00:00,1478.2948
    2019-07-01 00:00:00,1407.4674
    2019-08-01 00:00:00,1291.8518
    2019-09-01 00:00:00,929.3112
    2019-10-01 00:00:00,508.3131
    2019-11-01 00:00:00,290.2519
    2019-12-01 00:00:00,199.5812
    2020-01-01 00:00:00,214.43910000000002
    2020-02-01 00:00:00,390.5302
    2020-03-01 00:00:00,1133.4938
    2020-04-01 00:00:00,1817.4088999999997
    2020-05-01 00:00:00,2228.4934000000003
    2020-06-01 00:00:00,1942.7349
    2020-07-01 00:00:00,1854.9020999999998
    2020-08-01 00:00:00,1739.962
    2020-09-01 00:00:00,1290.4092999999998
    2020-10-01 00:00:00,579.2379
    2020-11-01 00:00:00,396.21479999999997
    2020-12-01 00:00:00,217.5447
    2021-01-01 00:00:00,310.3095
    2021-02-01 00:00:00,725.8607999999999
    2021-03-01 00:00:00,1381.5799
    2021-04-01 00:00:00,2099.9858999999997
    2021-05-01 00:00:00,2313.7679
    2021-06-01 00:00:00,2660.9764000000005
    2021-07-01 00:00:00,2367.9761999999996
    2021-08-01 00:00:00,2031.7354000000003
    2021-09-01 00:00:00,1698.9888
    2021-10-01 00:00:00,956.1077
    2021-11-01 00:00:00,446.04609999999997
    2021-12-01 00:00:00,260.3173
    2022-01-01 00:00:00,405.9771
    2022-02-01 00:00:00,861.2558
    2022-03-01 00:00:00,2190.141
    2022-04-01 00:00:00,2657.7057000000004
    2022-05-01 00:00:00,3411.1589
    2022-06-01 00:00:00,3615.0357000000004
    2022-07-01 00:00:00,3653.3788999999997
    2022-08-01 00:00:00,3402.2019999999998
    2022-09-01 00:00:00,2132.0135
    2022-10-01 00:00:00,1439.8065
    2022-11-01 00:00:00,707.8953
    2022-12-01 00:00:00,398.6848
    2023-01-01 00:00:00,480.0513
    2023-02-01 00:00:00,1040.5212000000001
    2023-03-01 00:00:00,1732.625
    2023-04-01 00:00:00,2916.6533
    2023-05-01 00:00:00,4158.348
    2023-06-01 00:00:00,4838.337
    2023-07-01 00:00:00,3410.27197265625
    2023-08-01 00:00:00,3334.20849609375
    2023-09-01 00:00:00,2717.922119140625
    2023-10-01 00:00:00,2286.7138671875
    2023-11-01 00:00:00,1795.1204833984375
    2023-12-01 00:00:00,1731.6593017578125
    2024-01-01 00:00:00,1797.7125244140625
    2024-02-01 00:00:00,2290.873046875
    2024-03-01 00:00:00,2987.422607421875
    2024-04-01 00:00:00,3541.091796875
    2024-05-01 00:00:00,4227.7939453125
    2024-06-01 00:00:00,4310.12548828125
    2024-07-01 00:00:00,4095.21875
    2024-08-01 00:00:00,3807.3427734375
    2024-09-01 00:00:00,3393.927001953125
    2024-10-01 00:00:00,2759.37841796875
    2024-11-01 00:00:00,2476.727783203125
    2024-12-01 00:00:00,2217.528076171875
    2025-01-01 00:00:00,2492.108154296875
    2025-02-01 00:00:00,2799.236572265625
    2025-03-01 00:00:00,3537.201416015625
    2025-04-01 00:00:00,4155.91552734375
    2025-05-01 00:00:00,4776.724609375
    2025-06-01 00:00:00,4932.947265625
    2025-07-01 00:00:00,4649.3818359375
    2025-08-01 00:00:00,4432.19580078125
    2025-09-01 00:00:00,3951.157470703125
    2025-10-01 00:00:00,3384.359375
    2025-11-01 00:00:00,3032.076416015625
    2025-12-01 00:00:00,2838.093017578125
    2026-01-01 00:00:00,3043.18994140625
    2026-02-01 00:00:00,3412.202880859375
    2026-03-01 00:00:00,4087.024658203125
    2026-04-01 00:00:00,4770.75732421875
    2026-05-01 00:00:00,5325.650390625
    2026-06-01 00:00:00,5555.7490234375
    2026-07-01 00:00:00,5203.591796875
    2026-08-01 00:00:00,5057.0244140625
    2026-09-01 00:00:00,4508.34765625
    2026-10-01 00:00:00,4009.34521484375
    2026-11-01 00:00:00,3587.3994140625
    2026-12-01 00:00:00,3458.677001953125
    2027-01-01 00:00:00,3594.250732421875
    2027-02-01 00:00:00,4025.288330078125
    2027-03-01 00:00:00,4636.91455078125
    2027-04-01 00:00:00,5385.59326171875
    2027-05-01 00:00:00,5874.59423828125
    2027-06-01 00:00:00,6178.5087890625"""

    # Create a DataFrame
    df = pd.read_csv(StringIO(csv_data), parse_dates=['ds'])

    df['ds'] = pd.to_datetime(df['ds'])
    df['ds'] = df['ds'].dt.strftime('%Y-%m')

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['ds'], empty='none')

    line = alt.Chart(df).mark_line(interpolate='linear', color='#3590F3').encode(
        x=alt.X('ds:T', axis=alt.Axis(format="%Y", title='Date',titleFontSize=16, labelFontSize=14)), 
        y=alt.Y('y:Q', axis=alt.Axis(title='Energy Output (GWh)',titleFontSize=16, labelFontSize=14)),
        tooltip=['ds:T', 'y:Q'] 
    ).properties(
        width=700, height=400, title='Solar energy production BeNeLux'
    )

    selectors = alt.Chart(df).mark_point().encode(
        x='ds:T',
        y='y:Q',
        opacity=alt.value(0),  
    ).add_selection(
        nearest  
    )

    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    rules = alt.Chart(df).mark_rule(color='gray').encode(
        x='ds:T',
    ).transform_filter(
        nearest  
    )

    # Combine everything into a layered chart
    chart = alt.layer(
        line, selectors, points, rules
    ).properties(
        width=700, height=400, title='Solar energy production BeNeLux'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)







       
    

predictions()