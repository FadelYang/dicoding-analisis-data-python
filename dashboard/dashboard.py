import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

# create helper function
def create_yearly_monthly_count_df(df):
    return df.groupby(["year", "month"])["count"].sum().unstack()

def create_season_df(df):
    return df.groupby(["year", "season"])["count"].sum().reset_index()

def create_weather_df(df):
    return df.groupby(["weather_situation"])["count"].sum()

# create dataframe
main_df = pd.read_csv("data_csv/Bike-sharing-dataset/day.csv")

def cleaning_data(df):
    # merubah beberapa nama kolom agar mudah dibaca
    column_rename_mapping = {
        "dteday": "dateday",
        "yr": "year",
        "mnth": "month",
        "weathersit": "weather_situation",
        "temp": "temperature",
        "atemp": "feeling_temperature",
        "hum": "humidity",
        "cnt": "count"  
    }

    df.rename(columns=column_rename_mapping, inplace=True)
    df.head()

    df["dateday"] = pd.to_datetime(df["dateday"])
    df["dateday"].info()

    # merubah value data categorical dengan value sebenarnya (tidak diwakili angka) agar lebih mudah dibaca
    # kolom season
    df["season"] = df["season"].astype("category")
    df["season"] = df["season"].cat.rename_categories({
        1: "springer",
        2: "summer",
        3: "fall",
        4: "winter"
    })

    # kolom year
    df["year"] = df["year"].astype("category")
    df["year"] = df["year"].cat.rename_categories({
        0: "2011",
        1: "2012"
    })

    # kolom month
    df["month"] = df["month"].astype("category")
    df["month"] = df["month"].cat.rename_categories({
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Des"
    })

    # kolom weather_situation
    df["weather_situation"] = df["weather_situation"].astype("category")
    df["weather_situation"] = df["weather_situation"].cat.rename_categories({
        1: "Clear/Partly cloudy",
        2: "Mist/Cloudy",
        3: "Light rain/snow",
        4: "Heavy rain/snow",
    })

    # kolom weekday
    df["weekday"] = df["weekday"].astype("category")
    df["weekday"] = df["weekday"].cat.rename_categories({
        0: "Sun",
        1: "Mon",
        2: "Thu",
        3: "Wed",
        4: "Tue",
        5: "Fri",
        6: "Sat",
    })

    # kolom holiday
    df["holiday"] = df["holiday"].astype("category")
    df["holiday"] = df["holiday"].cat.rename_categories({
        0: "No",
        1: "Yes",
    })

    # kolom Working
    df["workingday"] = df["workingday"].astype("category")
    df["workingday"] = df["workingday"].cat.rename_categories({
        0: "No",
        1: "Yes",
    })

cleaning_data(main_df)

by_yearly_monthly_counts_df = create_yearly_monthly_count_df(main_df)
by_season_df = create_season_df(main_df)
by_weather_df = create_weather_df(main_df)

# visualization
st.header('Bike Bike Sharing Dashboard :sparkles:')
st.subheader('Tren penggunaan bike sharing tahun 2011 - 2012')

col1, col2 = st.columns(2)

with col1:
    total_transaction = main_df["count"].sum()
    st.metric("Total Transaction", value="{:,}".format(total_transaction))
 
with col2:
    total_registered_user = main_df["registered"].sum() 
    st.metric("Total Register User", value="{:,}".format(total_registered_user))

# create first visualization chart
st.subheader("Tren Pengguna Selama Satu Tahun (2011 dan 2012)")

fig, ax = plt.subplots(figsize=(10, 6))

for year in by_yearly_monthly_counts_df.index:
    ax.plot(
        by_yearly_monthly_counts_df.columns,
        by_yearly_monthly_counts_df.loc[year],
        label=str(year),
        marker='o'
    )

ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Pengguna')
ax.set_title('Tren Pengguna Selama Satu Tahun (2011 dan 2012)')
ax.grid(True)
ax.set_xticks(range(0, 12))
ax.legend()

st.pyplot(fig)

# create second visualization
st.subheader("Tren Pengguna Selama Satu Tahun Berdasarkan Musim")

by_season_df = main_df.groupby(["year", "season"])["count"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(x="season", y="count", hue="year", data=by_season_df)

ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Pengguna')
ax.set_title('Tren Pengguna Selama Satu Tahun Berdasarkan Musim')
ax.legend()

st.pyplot(fig)

# create third visualization
st.subheader("Tren Pengguna Selama Satu Berdasarkan Cuaca")
by_weather_df = main_df.groupby(["weather_situation"])["count"].sum()

fig, ax = plt.subplots(figsize=(8, 8))

ax.pie(
    by_weather_df.values,
    labels=by_weather_df.index,
    autopct='%1.1f%%',
    startangle=120
)

ax.axis('equal')

ax.set_title('Tren Penguna Berdasarkan Cuaca')

st.pyplot(fig)


