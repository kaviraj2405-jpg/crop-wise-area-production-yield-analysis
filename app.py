import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crop Analysis Dashboard", page_icon="🌾", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("crop-wise-area-production-yield.csv")

df=load_data()

st.title("🌾 Crop Wise Area, Production and Yield Analysis Dashboard")

st.sidebar.header("🔍 Filters")
state=st.sidebar.selectbox("State",["All"]+sorted(df["state_name"].dropna().unique().tolist()))
season=st.sidebar.selectbox("Season",["All"]+sorted(df["season"].dropna().unique().tolist()))
crop=st.sidebar.selectbox("Crop",["All"]+sorted(df["crop_name"].dropna().unique().tolist()))

filtered_df=df.copy()
if state!="All":
    filtered_df=filtered_df[filtered_df["state_name"]==state]
if season!="All":
    filtered_df=filtered_df[filtered_df["season"]==season]
if crop!="All":
    filtered_df=filtered_df[filtered_df["crop_name"]==crop]

c1,c2,c3,c4,c5,c6=st.columns(6)
c1.metric("📄 Records",f"{len(filtered_df):,}")
c2.metric("🏛 States",filtered_df["state_name"].nunique())
c3.metric("🏘 Districts",filtered_df["district_name"].nunique())
c4.metric("🌾 Crops",filtered_df["crop_name"].nunique())
c5.metric("📈 Avg Production",f"{filtered_df['production'].mean():,.0f}")
c6.metric("🌱 Avg Yield",f"{filtered_df['yield'].mean():.2f}")

with st.expander("📄 View Dataset"):
    st.dataframe(filtered_df,use_container_width=True)

l,r=st.columns(2)
with l:
    st.subheader("📊 Top 10 States by Production")
    s=filtered_df.groupby("state_name",as_index=False)["production"].sum().sort_values("production",ascending=False).head(10)
    st.plotly_chart(px.bar(s,x="state_name",y="production",color="production",text_auto=".2s"),use_container_width=True)
with r:
    st.subheader("🌾 Top 10 Crops by Production")
    c=filtered_df.groupby("crop_name",as_index=False)["production"].sum().sort_values("production",ascending=False).head(10)
    st.plotly_chart(px.bar(c,x="crop_name",y="production",color="production",text_auto=".2s"),use_container_width=True)

l,r=st.columns(2)
with l:
    st.subheader("🌱 Average Yield by Season")
    y=filtered_df.groupby("season",as_index=False)["yield"].mean()
    st.plotly_chart(px.bar(y,x="season",y="yield",color="yield",text_auto=".2f"),use_container_width=True)
with r:
    st.subheader("🌾 Crop Type Distribution")
    ct=filtered_df["crop_type"].value_counts().reset_index()
    ct.columns=["Crop Type","Count"]
    st.plotly_chart(px.pie(ct,names="Crop Type",values="Count",hole=.45),use_container_width=True)

sample=filtered_df.sample(min(10000,len(filtered_df)),random_state=42)
l,r=st.columns(2)
with l:
    st.subheader("📉 Area vs Production")
    st.plotly_chart(px.scatter(sample,x="area",y="production",color="season",opacity=.6),use_container_width=True)
with r:
    st.subheader("📉 Area vs Yield")
    st.plotly_chart(px.scatter(sample,x="area",y="yield",color="season",opacity=.6),use_container_width=True)

st.subheader("🔥 Correlation Heatmap")
corr=filtered_df[["area","production","yield"]].corr()
st.plotly_chart(px.imshow(corr,text_auto=True,color_continuous_scale="Viridis"),use_container_width=True)

csv=filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download Filtered Dataset",csv,"Filtered_Crop_Data.csv","text/csv")
