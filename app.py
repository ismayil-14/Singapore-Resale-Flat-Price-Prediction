import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import re
from PIL import Image
import warnings
import pickle
warnings.filterwarnings("ignore")

mrt = pd.read_csv("mrt_data.csv")
central = pd.read_csv("central.csv")

def get_median(s):
    start = int(s[0:2])
    end = int(s[-2:])
    return int((start+end)/2)

# Create a Streamlit app
icon = Image.open("icon.jpeg")
st.set_page_config(page_title= "Singapore  Resale Flat Prices Predicting| By Mohamed Ismayil",
                page_icon= icon,
                layout= "wide",
                initial_sidebar_state= "expanded",
                menu_items={'About': """# This dashboard app is created by *Mohamed Ismayil*!"""}
                )

st.write("""
<div style='text-align:center'>
    <h1 style='color:#009999;'>Singapore  Resale Flat Prices Predicting</h1>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Menu", ["Home","PREDICT RESALE PRICE"], 
                        icons=["house","graph-up-arrow","graph-up-arrow"],
                        menu_icon= "menu-button-wide",
                        default_index=0,
                        styles={"nav-link": {"font-size": "25px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                "nav-link-selected": {"background-color": "#FF5A5F"}}
                        )

# HOME PAGE
if selected == "Home":
    st.markdown("## :blue[Domain] : Real Estate")
    st.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, Sciket-Learn, Render")
    st.markdown("## :blue[Overview] : A machine learning-based web application designed to predict the resale prices of flats in Singapore. Utilizing historical data on resale transactions, the application provides potential buyers and sellers with estimated resale values based on factors such as location, flat type, floor area, and lease duration. ")

town_option = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH','BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL', 'CHOA CHU KANG','CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
       'KALLANG', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL', 'QUEENSTOWN','SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES', 'TOA PAYOH','WOODLANDS', 'YISHUN']

flat_type_option = ['1 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', '2 ROOM', 'EXECUTIVE', 'MULTI GENERATION']

flat_model_option = ['Improved', 'New Generation', 'Model A', 'Standard', 'Simplified', 'Model A-Maisonette', 'Apartment', 'Maisonette', 'Terrace',
       '2-Room', 'Improved-Maisonette', 'Multi Generation', 'Premium Apartment', 'Adjoined Flat', 'Premium Maisonette','Model A2', 'Dbss', 
       'Type S1', 'Type S2', 'Premium Apartment Loft','3Gen']

storey_range_option =  ['10 TO 12', '04 TO 06', '07 TO 09', '01 TO 03', '13 TO 15', '19 TO 21', '16 TO 18', '25 TO 27', '22 TO 24', '28 TO 30',
       '31 TO 33', '40 TO 42', '37 TO 39', '34 TO 36', '06 TO 10','01 TO 05', '11 TO 15', '16 TO 20', '21 TO 25', '26 TO 30',
       '36 TO 40', '31 TO 35', '46 TO 48', '43 TO 45', '49 TO 51']

street_name_option = ['ADMIRALTY DR', 'ADMIRALTY LINK', 'AH HOOD RD', 'ALJUNIED AVE', 'ALJUNIED CRES', 'ALJUNIED RD', 'ANCHORVALE CRES', 'ANCHORVALE DR', 'ANCHORVALE LANE',
 'ANCHORVALE LINK', 'ANCHORVALE RD', 'ANCHORVALE ST', 'ANG MO KIO AVE', 'ANG MO KIO ST', 'BAIN ST', 'BALAM RD', 'BANGKIT RD', 'BEACH RD',
 'BEDOK CTRL', 'BEDOK NTH AVE', 'BEDOK NTH RD', 'BEDOK NTH ST', 'BEDOK RESERVOIR CRES', 'BEDOK RESERVOIR RD', 'BEDOK RESERVOIR VIEW',
 'BEDOK STH AVE', 'BEDOK STH RD', 'BENDEMEER RD', 'BEO CRES', 'BISHAN ST', 'BOON KENG RD', 'BOON LAY AVE', 'BOON LAY DR', 'BOON LAY PL',
 'BOON TIONG RD', 'BRIGHT HILL DR', 'BT BATOK CTRL', 'BT BATOK EAST AVE', 'BT BATOK ST', 'BT BATOK WEST AVE', 'BT MERAH CTRL', 'BT MERAH LANE',
 'BT MERAH VIEW', 'BT PANJANG RING RD', 'BT PURMEI RD', 'BUANGKOK CRES', 'BUANGKOK GREEN', 'BUANGKOK LINK', 'BUFFALO RD', "C'WEALTH AVE",
 "C'WEALTH AVE WEST", 'CAMBRIDGE RD', 'CANBERRA CRES', 'CANBERRA LINK', 'CANBERRA RD', 'CANBERRA ST', 'CANBERRA WALK', 'CANTONMENT CL',
 'CANTONMENT RD', 'CASHEW RD', 'CASSIA CRES', 'CHAI CHEE AVE', 'CHAI CHEE DR', 'CHAI CHEE RD', 'CHAI CHEE ST', 'CHANDER RD', 'CHANGI VILLAGE RD',
 'CHIN SWEE RD', 'CHOA CHU KANG AVE', 'CHOA CHU KANG CRES', 'CHOA CHU KANG CTRL', 'CHOA CHU KANG DR', 'CHOA CHU KANG LOOP', 'CHOA CHU KANG NTH',
 'CHOA CHU KANG ST', 'CIRCUIT RD', 'CLARENCE LANE', 'CLEMENTI AVE', 'CLEMENTI ST', 'CLEMENTI WEST ST', 'COMPASSVALE BOW', 'COMPASSVALE CRES',
 'COMPASSVALE DR', 'COMPASSVALE LANE', 'COMPASSVALE LINK', 'COMPASSVALE RD', 'COMPASSVALE ST', 'COMPASSVALE WALK', 'CORPORATION DR', 'CRAWFORD LANE',
 'DAKOTA CRES', 'DAWSON RD', 'DELTA AVE', 'DEPOT RD', 'DORSET RD', 'DOVER CL EAST', 'DOVER CRES', 'DOVER RD', 'EDGEDALE PLAINS', 'EDGEFIELD PLAINS',
 'ELIAS RD', 'EMPRESS RD', 'EUNOS CRES', 'EUNOS RD', 'EVERTON PARK', 'FAJAR RD', 'FARRER PK RD', 'FARRER RD', 'FERNVALE LANE', 'FERNVALE LINK',
 'FERNVALE RD', 'FERNVALE ST', 'FRENCH RD', 'GANGSA RD', 'GEYLANG BAHRU', 'GEYLANG EAST AVE', 'GEYLANG EAST CTRL', 'GEYLANG SERAI', 'GHIM MOH LINK',
 'GHIM MOH RD', 'GLOUCESTER RD', 'HAIG RD', 'HAVELOCK RD', 'HENDERSON CRES', 'HENDERSON RD', 'HO CHING RD', 'HOLLAND AVE', 'HOLLAND CL',
 'HOLLAND DR', 'HOUGANG AVE', 'HOUGANG CTRL', 'HOUGANG ST', 'HOY FATT RD', 'INDUS RD', 'JELAPANG RD', 'JELEBU RD', 'JELLICOE RD', 'JLN BAHAGIA',
 'JLN BATU', 'JLN BERSEH', 'JLN BT HO SWEE', 'JLN BT MERAH', 'JLN DAMAI', 'JLN DUA', 'JLN DUSUN', 'JLN KAYU', 'JLN KLINIK', 'JLN KUKOH',
 "JLN MA'MOR", 'JLN MEMBINA', 'JLN RAJAH', 'JLN RUMAH TINGGI', 'JLN TECK WHYE', 'JLN TENAGA', 'JLN TENTERAM',
 'JLN TIGA', 'JOO CHIAT RD', 'JOO SENG RD', 'JURONG EAST AVE', 'JURONG EAST ST', 'JURONG WEST AVE', 'JURONG WEST CTRL', 'JURONG WEST ST',
 'KALLANG BAHRU', 'KANG CHING RD', 'KEAT HONG CL', 'KEAT HONG LINK', 'KELANTAN RD','KENT RD', 'KG ARANG RD', 'KG KAYU RD', 'KIM CHENG ST',
 'KIM KEAT AVE', 'KIM KEAT LINK', 'KIM PONG RD', 'KIM TIAN PL', 'KIM TIAN RD', "KING GEORGE'S AVE", 'KLANG LANE', 'KRETA AYER RD',
 'LENGKOK BAHRU', 'LENGKONG TIGA', 'LIM LIAK ST', 'LOMPANG RD', 'LOR  GEYLANG', 'LOR  TOA PAYOH', 'LOR A TOA PAYOH','LOR AH SOO',
 'LOR LEW LIAN', 'LOR LIMAU', 'LOWER DELTA RD', 'MACPHERSON LANE', 'MARINE CRES', 'MARINE DR', 'MARINE PARADE CTRL', 'MARINE TER', 'MARSILING CRES',
 'MARSILING DR', 'MARSILING LANE', 'MARSILING RD', 'MARSILING RISE', 'MCNAIR RD', 'MEI LING ST', 'MOH GUAN TER', 'MONTREAL DR', 'MONTREAL LINK',
 'MOULMEIN RD', 'NEW MKT RD', 'NEW UPP CHANGI RD', 'NTH BRIDGE RD', 'OLD AIRPORT RD', 'OWEN RD', 'PANDAN GDNS', 'PASIR RIS DR', 'PASIR RIS ST',
 'PAYA LEBAR WAY', 'PENDING RD', 'PETIR RD', 'PINE CL', 'PIPIT RD', 'POTONG PASIR AVE', 'PUNGGOL CTRL', 'PUNGGOL DR',
 'PUNGGOL EAST', 'PUNGGOL FIELD', 'PUNGGOL FIELD WALK', 'PUNGGOL PL', 'PUNGGOL RD', 'PUNGGOL WALK', 'PUNGGOL WAY', 'QUEEN ST',
 "QUEEN'S CL", "QUEEN'S RD", 'QUEENSWAY', 'RACE COURSE RD', 'REDHILL CL', 'REDHILL LANE', 'REDHILL RD', 'RIVERVALE CRES',
 'RIVERVALE DR', 'RIVERVALE ST', 'RIVERVALE WALK', 'ROWELL RD', 'SAGO LANE', 'SAUJANA RD', 'SEGAR RD', 'SELEGIE RD',
 'SEMBAWANG CL', 'SEMBAWANG CRES', 'SEMBAWANG DR', 'SEMBAWANG VISTA', 'SEMBAWANG WAY', 'SENG POH RD', 'SENGKANG CTRL', 'SENGKANG EAST AVE',
 'SENGKANG EAST RD', 'SENGKANG EAST WAY', 'SENGKANG WEST AVE', 'SENGKANG WEST WAY', 'SENJA LINK', 'SENJA RD', 'SERANGOON AVE',
 'SERANGOON CTRL', 'SERANGOON CTRL DR', 'SERANGOON NTH AVE', 'SHUNFU RD', 'SILAT AVE', 'SIMEI LANE', 'SIMEI RD', 'SIMEI ST', 'SIMS AVE',
 'SIMS DR', 'SIMS PL', 'SIN MING AVE', 'SIN MING RD', 'SMITH ST', 'SPOTTISWOODE PK RD', "ST. GEORGE'S LANE", 'STIRLING RD',
 'STRATHMORE AVE', 'SUMANG LANE', 'SUMANG LINK', 'SUMANG WALK', 'TAH CHING RD', 'TAMAN HO SWEE', 'TAMPINES AVE', 'TAMPINES CTRL',
 'TAMPINES ST', 'TANGLIN HALT RD', 'TAO CHING RD', 'TEBAN GDNS RD', 'TECK WHYE AVE', 'TECK WHYE CRES', 'TECK WHYE LANE',
 'TELOK BLANGAH CRES', 'TELOK BLANGAH DR', 'TELOK BLANGAH HTS', 'TELOK BLANGAH RISE', 'TELOK BLANGAH ST', 'TELOK BLANGAH WAY',
 'TESSENSOHN RD', 'TG PAGAR PLAZA', 'TIONG BAHRU RD', 'TOA PAYOH CTRL', 'TOA PAYOH EAST', 'TOA PAYOH NTH', 'TOH GUAN RD',
 'TOH YI DR', 'TOWNER RD', 'UBI AVE', 'UPP ALJUNIED LANE', 'UPP BOON KENG RD','UPP CROSS ST', 'UPP SERANGOON CRES',
 'UPP SERANGOON RD', 'UPP SERANGOON VIEW', 'VEERASAMY RD', 'WATERLOO ST', 'WELLINGTON CIRCLE',
 'WEST COAST DR', 'WEST COAST RD', 'WHAMPOA DR', 'WHAMPOA RD', 'WHAMPOA STH', 'WHAMPOA WEST',
 'WOODLANDS AVE', 'WOODLANDS CIRCLE','WOODLANDS CRES', 'WOODLANDS DR', 'WOODLANDS RING RD',
 'WOODLANDS RISE', 'WOODLANDS ST', 'YISHUN AVE', 'YISHUN CTRL', 'YISHUN RING RD', 'YISHUN ST',
 'YUAN CHING RD', 'YUNG AN RD', 'YUNG HO RD', 'YUNG KUANG RD', 'YUNG LOH RD', 'YUNG PING RD', 'YUNG SHENG RD', 'ZION RD']


def filter_options(user_input, street_name_option):
    return [option for option in street_name_option if user_input.lower() in option.lower()]



if selected == "PREDICT RESALE PRICE":
    st.header("Predict Resale Price")
    st.markdown("### Enter the details below to predict the Resale price.")

    with st.form("predict_price_form"):
        col1, col2 = st.columns([1, 1])

        with col1:
            town = st.selectbox("Town", town_option)
            flat_type = st.selectbox("Flat Type", flat_type_option)
            storey_range = st.selectbox("Storey Range", storey_range_option)
            flat_model = st.selectbox("Flat Model", flat_model_option)

        with col2:
            floor_sqm = st.text_input("Enter Floor area in sq m (Min: 28.0, Max: 366.7)")
            lease_commence_date = st.text_input("Enter Lease commencing date (Min: 1966, Max: 2020)") 
            user_input = st.text_input('Enter First few characters of street name to filter it')
            filtered_options = filter_options(user_input, street_name_option)
            street_name = st.selectbox('Street Name', filtered_options)
            submit_button = st.form_submit_button(label="Predict Resale Price")

    if submit_button:
        # Validate inputs
        flag = 0 
        pattern = "^(?:\d+|\d*\.\d+)$"
        for i in [floor_sqm, lease_commence_date]:             
            if not re.match(pattern, i):
                flag = 1
                break
        
        if flag == 1:
            st.error(f"You have entered an invalid value: {i}. Please enter a valid number without spaces.")
        else:
            # Load models and scalers
            with open("best_model.pkl", 'rb') as file:
                loaded_model = pickle.load(file)
            with open('scaler.pkl', 'rb') as f:
                scaler_loaded = pickle.load(f)
            with open("flat_type_encoder.pkl", 'rb') as f:
                type_loaded = pickle.load(f)
            with open("flat_model_encoder.pkl", 'rb') as f:
                model_loaded = pickle.load(f)

            street_name = street_name+ " SINGAPORE"
            street= mrt.loc[mrt['street_name'] == street_name, 'nearest_station_distance'].values 
            town = central.loc[central['town'] == town, 'distance_from_central'].values
            # Scale input data
            testing = np.array([[get_median(storey_range),float(floor_sqm),street[0],100 - (2024 - int(lease_commence_date)),town[0],flat_type,flat_model]])
            testing_type = type_loaded.transform(testing[:, [5]]).toarray()
            testing_model = model_loaded.transform(testing[:, [6]]).toarray()
            testing = np.concatenate((testing[:, [0,1,2, 3, 4,]], testing_type, testing_model), axis=1)
            tester = scaler_loaded.transform(testing)
            new_pred = loaded_model.predict(tester)[0]
            st.success(f"Predicted Resale Price: ${(round(np.exp(new_pred),2))}")
