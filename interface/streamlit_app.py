from pathlib import Path 
import streamlit as st
import base64
import pandas as pd


from agent.assistant import SmartFuelAssistant
from agent.database import (
    get_dashboard_kpis,
    get_transactions_by_city,
    get_failures_by_station,
    get_low_stock,
    get_stations,

    get_maintenance_summary,
    get_maintenance_by_station,
    get_maintenance_by_type,
    get_maintenance_details,

    get_complaints_summary,
    get_complaints_by_station,
    get_complaints_details,
    get_complaints_columns,

    get_transactions_summary,
    get_transactions_by_station,
    get_transactions_by_city,
    get_transactions_details,
    get_transactions_columns,

    get_monthly_sales,
    get_transactions_by_city,
    get_top_stations,
    get_pumps


)

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "logo.png"
with open(LOGO_PATH, "rb") as f:
    base64_logo = base64.b64encode(f.read()).decode()
# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PetroSense",
    page_icon=str(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "assistant" not in st.session_state:
    st.session_state.assistant = SmartFuelAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background-color: #0b0b0f;
        color: #f5f5f5;
    }

    .main {
        background-color: #0b0b0f;
    }

    /* Remove default top padding */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background-color: #09090c;
        border-right: 1px solid #26262d;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #09090c;
    }

    [data-testid="stSidebar"] * {
        color: #f5f5f5;
    }


    /* ========================================================
       SIDEBAR LOGO
       ======================================================== */

    .sidebar-logo {
        text-align: center;
        padding: 10px 5px 25px 5px;
    }

    .sidebar-logo-image {
        width: 170px;
        max-height: 110px;
        object-fit: contain;
        margin-bottom: 10px;
    }

    .sidebar-logo-title {
        font-size: 25px;
        font-weight: 700;
        color: white;
    }

    .sidebar-logo-title span {
        color: #e50914;
    }

    .sidebar-logo-subtitle {
        font-size: 11px;
        color: #888;
        margin-top: 4px;
    }

    /* ========================================================
        NAVIGATION
       ======================================================== */

    .nav-title {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #777;
        margin-bottom: 10px;
    }

    section[data-testid="stSidebar"] button {
        background: transparent;
        border: none;
        border-radius: 10px;
        color: #b8b8be;
        text-align: left;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 5px;
        transition: 0.2s;
    }

    section[data-testid="stSidebar"] button:hover {
        background: #1f1f24;
        color: white;
        border-left: 3px solid #e50914;
    }


    /* ========================================================
       HEADERS
       ======================================================== */

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
    }

    .main-title span {
        color: #e50914;
    }

    .subtitle {
        font-size: 15px;
        color: #777780;
        margin-top: 0;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    .red-line {
        height: 3px;
        width: 55px;
        background-color: #e50914;
        border-radius: 5px;
        margin-top: 12px;
        margin-bottom: 25px;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-card {
        background: linear-gradient(
            145deg,
            #151519,
            #101014
        );

        border: 1px solid #29292f;

        border-left: 4px solid #e50914;

        border-radius: 12px;

        padding: 20px;

        min-height: 125px;

        box-shadow:
            0 5px 20px rgba(0, 0, 0, 0.35);
    }

    .kpi-title {
        font-size: 13px;
        color: #85858d;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 700;
        color: #ffffff;
    }

    .kpi-icon {
        font-size: 22px;
        margin-bottom: 8px;
    }


    /* ========================================================
       SECTION CARDS
       ======================================================== */

    .section-card {
        background-color: #111115;

        border: 1px solid #27272d;

        border-radius: 12px;

        padding: 22px;

        margin-top: 20px;
    }

    .section-title {
        font-size: 38px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
    }

    .section-description {
        font-size: 15px;
        color: #777780;
    }


    /* ========================================================
       CHAT
       ======================================================== */

    [data-testid="stChatMessage"] {
        background-color: #111115;
        border: 1px solid #24242a;
        border-radius: 12px;
        margin-bottom: 10px;
    }

    [data-testid="stChatMessageContent"] {
        color: #eeeeee;
    }


    /* User message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background-color: #15151a;
    }



    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color: #e50914;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #b80710;
        color: #ffffff;
        border: none;
    }


    /* ========================================================
       INFO BOX
       ======================================================== */

    [data-testid="stAlert"] {
        background-color: #151519;
        border: 1px solid #2c2c32;
        color: #d6d6d6;
    }


    /* ========================================================
       TABLE
       ======================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #29292f;
        border-radius: 10px;
    }


    /* ========================================================
       SELECTBOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background-color: #111115;
        border-color: #303038;
        color: white;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {
        background-color: #111115;
        border: 1px solid #29292f;
        border-radius: 10px;
        padding: 15px;
    }


    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #0b0b0f;
    }

    ::-webkit-scrollbar-thumb {
        background: #303038;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #e50914;
    }

    /* Supprimer les icônes User / Assistant */
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }

    /* Supprimer l'espace réservé à l'avatar */
    [data-testid="stChatMessage"] {
        gap: 0 !important;
    }

/* ============================================================
   MESSAGE USER
   ============================================================ */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) {
    background-color: #1f1f1f;
    border-radius: 18px;
    margin-left: auto;
    margin-right: 0;
    margin-bottom: 10px;
    padding: 10px 16px;
    width: fit-content !important;
    max-width: 65% !important;
}


/* ============================================================
   MESSAGE ASSISTANT
   ============================================================ */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarAssistant"]
) {
    background-color: #151515;
    border-left: 3px solid #e30613;
    border-radius: 12px;
    margin-right: 15%;
    margin-bottom: 10px;
    padding: 12px 16px;
}


/* ========================================================
   page CHAT INPUT
   ======================================================== */

/* Conteneur principal du chat input */
[data-testid="stChatInput"] {
    background: transparent !important;
    border: none !important;
    border-radius: 28px !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Tous les conteneurs autour */
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div {
    background: transparent !important;
    border: none !important;
    border-radius: 28px !important;
    box-shadow: none !important;
}

/* Le vrai champ */
[data-testid="stChatInput"] textarea {
    background: #1e1e23 !important;
    border: 1px solid #3a3a42 !important;
    border-radius: 28px !important;
    color: white !important;
    padding: 12px 18px !important;
}

/* Focus */
[data-testid="stChatInput"]:focus-within textarea {
    border-radius: 28px !important;
    border-color: #55555f !important;
    box-shadow: none !important;
}

/* ========================================================
   CONTENEUR FIXE EN BAS DE STREAMLIT
   ======================================================== */

[data-testid="stBottom"] {
    background: transparent !important;
    border: none !important;
    border-radius: 28px !important;
    box-shadow: none !important;
}

/* Éventuel pseudo-élément de fond */
[data-testid="stBottom"]::before,
[data-testid="stBottom"]::after {
    background: transparent !important;
    box-shadow: none !important;
}

/* Conteneurs à l'intérieur de stBottom */
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div {
    background: transparent !important;
    border: none !important;
    border-radius: 28px !important;
    box-shadow: none !important;
}
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        f"""
        <div class="sidebar-logo">
            <img src="data:image/png;base64,{base64_logo}"class="sidebar-logo-image">
            <div class="sidebar-logo-title">Petro<span>Sense</span></div>
            <div class="sidebar-logo-subtitle">PetroSolutions AI Assistant</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()


    if st.button("Dashboard", use_container_width=True):
        st.session_state["page"] = "Dashboard"

    if st.button("Assistant", use_container_width=True):
        st.session_state["page"] = "Assistant"

    if st.button("Stations", use_container_width=True):
        st.session_state["page"] = "Stations"

    if st.button("Maintenance", use_container_width=True):
        st.session_state["page"] = "Maintenance"

    if st.button("Réclamations", use_container_width=True):
        st.session_state["page"] = "Réclamations"

    if st.button("Transactions", use_container_width=True):
        st.session_state["page"] = "Transactions"

    page = st.session_state.get("page", "Dashboard")

    st.divider()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#66666f;
            font-size:11px;
        ">
            Smart Fuel Station Assistant<br>
            PetroSolutions
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        """
        <div class="main-title">
            Welcome to <span>PetroSense</span>
        </div>

        <div class="subtitle">
            Vue globale du réseau de stations-service
        </div>

        <div class="red-line"></div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # KPI
    # ========================================================

    kpis = get_dashboard_kpis()

    col1, col2, col3, col4 = st.columns(4)


    # --------------------------------------------------------
    # STATIONS
    # --------------------------------------------------------

    with col1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon"></div>
                <div class="kpi-title">Stations</div>
                <div class="kpi-value">{kpis["stations"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # TRANSACTIONS
    # --------------------------------------------------------

    with col2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon"></div>
                <div class="kpi-title">Transactions</div>
                <div class="kpi-value">
                    {kpis["transactions"]:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # LITRES
    # --------------------------------------------------------

    with col3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon"></div>
                <div class="kpi-title">Litres vendus</div>
                <div class="kpi-value">
                    {kpis["liters"]:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # CHIFFRE D'AFFAIRES
    # --------------------------------------------------------

    with col4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon"></div>
                <div class="kpi-title">Chiffre d'affaires</div>
                <div class="kpi-value">{kpis["revenue"]:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # LIGNE 1 : ÉVOLUTION + VILLES
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # ÉVOLUTION DU CHIFFRE D'AFFAIRES
    # ========================================================

    with col1:

        st.markdown(
            f""" <div class="section-card"> 
            <div class="section-title"><h3>Évolution du chiffre d'affaires</h3></div>
            <div class="section-description">Chiffre d'affaires mensuel du réseau</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        monthly_sales = get_monthly_sales()

        if monthly_sales is not None and len(monthly_sales) > 0:

            import pandas as pd

            df_sales = pd.DataFrame(
                monthly_sales,
                columns=[
                    "Mois",
                    "Chiffre d'affaires"
                ]
            )

            # S'assurer que les valeurs sont numériques
            df_sales["Chiffre d'affaires"] = pd.to_numeric(
                df_sales["Chiffre d'affaires"],
                errors="coerce"
            )

            # Supprimer les lignes invalides
            df_sales = df_sales.dropna(
                subset=["Chiffre d'affaires"]
            )

            # Index temporel
            df_sales["Mois"] = pd.to_datetime(
                df_sales["Mois"],
                errors="coerce"
            )

            df_sales = df_sales.dropna(
                subset=["Mois"]
            )

            df_sales = df_sales.sort_values("Mois")

            df_sales = df_sales.set_index("Mois")

            if not df_sales.empty:
                import plotly.express as px
                fig = px.line(
        df_sales,
        x=df_sales.index,
        y="Chiffre d'affaires",
        markers=True
    )

                fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

                fig.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title=None,
        yaxis_title="Chiffre d'affaires (MAD)",
        hovermode="x unified",
        showlegend=False
    )

                st.plotly_chart(
        fig,
        use_container_width=True
    )


            else:

                st.info(
                    "Aucune donnée valide de chiffre d'affaires."
                )

        
    # ========================================================
    # TRANSACTIONS PAR VILLE
    # ========================================================

    with col2:

        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title"><h3>Activité par ville</h3></div>
                <div class="section-description">Nombre de transactions par ville</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        city_data = get_transactions_by_city()

        if city_data:

            import pandas as pd

            df_city = pd.DataFrame(
                city_data,
                columns=[
                    "Ville",
                    "Transactions"
                ]
            )

            df_city = df_city.set_index("Ville")

            st.bar_chart(
                df_city,
                use_container_width=True
            )

        else:

            st.info(
                "Aucune donnée de transaction disponible."
            )


    st.markdown("<br>", unsafe_allow_html=True)


    
    # ========================================================
    # TOP STATIONS
    # ========================================================

    st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title"><h3>Stations les plus performantes</h3></div>
                <div class="section-description">Classement selon le nombre de transactions</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    top_stations = get_top_stations()

    if top_stations:

            import pandas as pd

            df_top = pd.DataFrame(
                top_stations,
                columns=[
                    "Station",
                    "Ville",
                    "Transactions",
                    "revenue",
                    "liters"
                ]
            )

            df_top = df_top.head(5)

            st.dataframe(
                df_top,
                use_container_width=True,
                hide_index=True
            )

    else:

            st.info(
                "Aucune donnée de station disponible."
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================
    # STATISTIQUES OPÉRATIONNELLES
    # ========================================================

    
    st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title"><h3>Statistiques opérationnelles</h3></div>
                <div class="section-description">Indicateurs clés du réseau</div>
            </div>
            """,
        unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # STATIONS ACTIVES
        # ----------------------------------------------------

    transaction_summary = get_transactions_summary()

    total_transactions, active_stations = transaction_summary


        # ----------------------------------------------------
        # MAINTENANCE
        # ----------------------------------------------------

    maintenance_summary = get_maintenance_summary()

    total_failures, affected_stations = maintenance_summary


        # ----------------------------------------------------
        # RÉCLAMATIONS
        # ----------------------------------------------------

    complaints_summary = get_complaints_summary()

    total_complaints, complaint_stations = complaints_summary


        # ----------------------------------------------------
        # STATISTIQUES
        # ----------------------------------------------------

    stat1, stat2 = st.columns(2)

    with stat1:

            st.metric(
                "Ticket moyen",
                f'{kpis["ticket_moyen"]:,.2f} MAD'
            )

            st.metric(
                "Stations actives",
                f"{active_stations}"
            )

    with stat2:

            st.metric(
                "Pannes",
                f"{total_failures}"
            )

            st.metric(
                "Réclamations",
                f"{total_complaints}"
            )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # LIGNE 3 : ALERTES
    # ========================================================

    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title"><h3>⚠️ Alertes du réseau</h3></div>
            <div class="section-description">Stations nécessitant une attention particulière</div>
        </div>
        """,
        unsafe_allow_html=True
    )


    failures = get_failures_by_station()

    low_stock = get_low_stock()


    # ========================================================
    # ALERTES : DEUX COLONNES
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # PANNES
    # ========================================================

    with col1:

        st.markdown("###  Pannes")

        if failures:

            # Afficher les 5 stations ayant le plus de pannes

            for station, count in failures[:5]:

                st.warning(
                    f"**{station}** — {count} panne(s)"
                )

        else:

            st.success(
                "✅ Aucune panne détectée."
            )


    # ========================================================
    # STOCK FAIBLE
    # ========================================================

    with col2:

        st.markdown("###  Stock faible")

        if low_stock:

            # Afficher les 5 stocks les plus faibles

            for station, fuel, quantity, threshold in low_stock[:5]:

                st.error(
                    f"**{station}** — {fuel} : "
                    f"{quantity:,.0f} ≤ {threshold:,.0f}"
                )

        else:

            st.success(
                "✅ Aucun stock critique."
            )
# ============================================================
# ASSISTANT
# ============================================================

elif page == "Assistant":

    st.markdown(
        """
        <div class="main-title">
            <span>PetroSense</span> Assistant
        </div>

        <div class="subtitle">
            Posez vos questions sur le réseau PetroSolutions
        </div>

        <div class="red-line"></div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"], avatar=None):

            if message["type"] == "text":

                st.markdown(message["content"])

            elif message["type"] == "chart":

                for figure in message["figures"]:

                    st.pyplot(figure)


    # ========================================================
    # INPUT
    # ========================================================

    question = st.chat_input(
        "Posez votre question à PetroSense..."
    )


    if question:

        # ----------------------------------------------------
        # USER
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "type": "text",
                "content": question
            }
        )

        with st.chat_message("user", avatar=None):

            st.markdown(question)


        # ----------------------------------------------------
        # ASSISTANT
        # ----------------------------------------------------

        with st.chat_message("assistant", avatar=None):

            with st.spinner(
                "PetroSense analyse votre question..."
            ):

                try:

                    answer = (
                        st.session_state
                        .assistant
                        .ask(question)
                    )

                except Exception as e:

                    answer = {
                        "type": "text",
                        "content": (
                            "Une erreur est survenue :\n\n"
                            f"`{e}`"
                        )
                    }


            # =================================================
            # GRAPHIQUE
            # =================================================

            if (
                isinstance(answer, dict)
                and answer.get("type") == "chart"
            ):

                for figure in answer["figures"]:

                    st.pyplot(figure)


            # =================================================
            # TEXTE
            # =================================================

            else:

                st.markdown(
                    answer["content"]
                    if isinstance(answer, dict)
                    else answer
                )


        # ----------------------------------------------------
        # SAVE ASSISTANT RESPONSE
        # ----------------------------------------------------

        if (
            isinstance(answer, dict)
            and answer.get("type") == "chart"
        ):

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "type": "chart",
                    "figures": answer["figures"],
                    "content": "Voici le graphique demandé."
                }
            )

        else:

            content = (
                answer["content"]
                if isinstance(answer, dict)
                else answer
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "type": "text",
                    "content": content
                }
            )
# ============================================================
# STATIONS
# ============================================================

elif page == "Stations":

    import pandas as pd

    stations = get_stations()

    df_stations = pd.DataFrame(
        stations,
        columns=[
            "ID",
            "Station",
            "Ville",
            "Carburant",
            "Stock maximum",
            "Stock actuel",
            "Seuil de réapprovisionnement"
        ]
    )

    # ========================================================
    # TITRE
    # ========================================================

    st.markdown(
        """
        <div class="main-title">
            Réseau de stations
        </div>

        <div class="subtitle">
            Stations, carburants et niveaux de stock
        </div>

        <div class="red-line"></div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # FILTRES
    # ========================================================

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:

        search = st.text_input(
            "🔎 Rechercher une station",
            placeholder="Nom de la station..."
        )

    with col2:

        cities = ["Toutes les villes"] + sorted(
            df_stations["Ville"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_city = st.selectbox(
            "📍 Ville",
            cities
        )

    with col3:

        fuels = ["Tous les carburants"] + sorted(
            df_stations["Carburant"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_fuel = st.selectbox(
            "Carburant",
            fuels
        )

    # ========================================================
    # FILTRAGE
    # ========================================================

    filtered_df = df_stations.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df["Station"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if selected_city != "Toutes les villes":

        filtered_df = filtered_df[
            filtered_df["Ville"] == selected_city
        ]

    if selected_fuel != "Tous les carburants":

        filtered_df = filtered_df[
            filtered_df["Carburant"] == selected_fuel
        ]

    # ========================================================
    # NIVEAU DE STOCK
    # ========================================================

    filtered_df["Stock (%)"] = (
        filtered_df["Stock actuel"]
        / filtered_df["Stock maximum"]
        * 100
    ).round(1)

    # ========================================================
    # INFORMATIONS
    # ========================================================

    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title"><h3>Stations et stocks</h3></div>
            <div class="section-description">
                {filtered_df["Station"].nunique()} station(s)
                — {len(filtered_df)} réservoir(s) affiché(s)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # TABLEAU
    # ========================================================

    if not filtered_df.empty:

        display_df = filtered_df[
            [
                "Station",
                "Ville",
                "Carburant",
                "Stock actuel",
                "Stock maximum",
                "Stock (%)",
                "Seuil de réapprovisionnement"
            ]
        ].copy()

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Aucune station ne correspond aux critères."
        )


    # ========================================================
    # POMPES
    # ========================================================

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title"><h3>Pompes</h3></div>
            <div class="section-description">
                État et caractéristiques des pompes du réseau
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    pumps = get_pumps()

    if pumps:

        df_pumps = pd.DataFrame(
            pumps,
            columns=[
                "ID",
                "Station",
                "Carburant",
                "Date d'installation",
                "Âge",
                "Statut",
                "Utilisations",
                "Fin de réparation"
            ]
        )

        # ----------------------------------------------------
        # TABLEAU DES POMPES
        # ----------------------------------------------------

        st.dataframe(
            df_pumps,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Aucune pompe enregistrée dans le réseau."
        )

# ============================================================
# MAINTENANCE
# ============================================================

elif page == "Maintenance":

    st.markdown(
        """
        <div class="main-title">Maintenance du réseau</div>
        <div class="subtitle">Suivi des pannes et des interventions de maintenance</div>
        <div class="red-line"></div>
        """,
        unsafe_allow_html=True
    )


    # ============================================================
    # SUMMARY
    # ============================================================

    total_failures, affected_stations = get_maintenance_summary()

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            " Total des pannes",
            total_failures
        )


    with col2:

        st.metric(
            " Stations concernées",
            affected_stations
        )


    st.divider()


    # ============================================================
    # GRAPHS
    # ============================================================

    col1, col2 = st.columns(2)


    # ------------------------------------------------------------
    # PANNES PAR STATION
    # ------------------------------------------------------------

    with col1:

        st.markdown("###  Pannes par station")

        data = get_maintenance_by_station()

        if data:

            import pandas as pd

            df = pd.DataFrame(
                data,
                columns=[
                    "Station",
                    "Ville",
                    "Pannes"
                ]
            )

            st.bar_chart(
                df.set_index("Station")["Pannes"]
            )

        else:

            st.info("Aucune donnée de maintenance.")


    # ------------------------------------------------------------
    # TYPES DE PANNES
    # ------------------------------------------------------------

    with col2:

        st.markdown("###  Types de pannes")

        data = get_maintenance_by_type()

        if data:

            import pandas as pd

            df = pd.DataFrame(
                data,
                columns=[
                    "Type de panne",
                    "Occurrences"
                ]
            )

            st.bar_chart(
                df.set_index("Type de panne")["Occurrences"]
            )

        else:

            st.info("Aucun type de panne enregistré.")


    # ============================================================
    # DETAILS
    # ============================================================

    st.markdown("###  Historique de maintenance")

    data = get_maintenance_details()

    if data:

        import pandas as pd

        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Station",
                "Ville",
                "Type de panne"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Aucune intervention de maintenance enregistrée.")

    st.markdown("### Rapports de maintenance")

    REPORTS_DIR = BASE_DIR / "simulator" / "LLM" / "documents"/ "maintenance"

    reports = sorted(REPORTS_DIR.glob("*"))

    if reports:

        report_names = [
            report.name
            for report in reports
            if report.is_file() and report.name!=".gitkeep"
        ]

        selected_report = st.selectbox(
            "Sélectionner un rapport",
            report_names
        )

        report_path = REPORTS_DIR / selected_report

        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        st.text_area(
            "Contenu du rapport",
            content,
            height=400
        )

    else:

        st.info("Aucun rapport de maintenance disponible.")

# ============================================================
# RÉCLAMATIONS
# ============================================================

elif page == "Réclamations":

    st.markdown(
        """
        <div class="main-title">Réclamations clients</div>
        <div class="subtitle">Suivi des réclamations et de la qualité de service</div>
        <div class="red-line"></div>
        """,
        unsafe_allow_html=True
    )


    # ============================================================
    # RÉSUMÉ
    # ============================================================

    total_complaints, affected_stations = get_complaints_summary()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            " Total des réclamations",
            total_complaints
        )

    with col2:

        st.metric(
            " Stations concernées",
            affected_stations
        )


    st.divider()


    # ============================================================
    # RÉCLAMATIONS PAR STATION
    # ============================================================

    st.markdown("### Réclamations par station")

    data = get_complaints_by_station()

    if data:

        import pandas as pd

        df_complaints = pd.DataFrame(
            data,
            columns=[
                "Station",
                "Ville",
                "Réclamations"
            ]
        )

        st.bar_chart(
            df_complaints.set_index("Station")["Réclamations"]
        )

    else:

        st.info("Aucune réclamation enregistrée.")


    # ============================================================
    # HISTORIQUE
    # ============================================================

    st.markdown("###  Historique des réclamations")

    data = get_complaints_details()
    columns = get_complaints_columns()

    if data:

        import pandas as pd

        df = pd.DataFrame(
            data,
            columns=columns
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Aucune réclamation enregistrée.")


    st.markdown("### Réclamations des clients")
    
    REPORTS_DIR = BASE_DIR / "simulator" / "LLM" / "documents"/ "complaints"

    reports = sorted(REPORTS_DIR.glob("*"))

    if reports:

        report_names = [
            report.name
            for report in reports
            if report.is_file() and report.name!=".gitkeep"
        ]

        selected_report = st.selectbox(
            "Sélectionner une réclamation",
            report_names
        )

        report_path = REPORTS_DIR / selected_report

        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        st.text_area(
            "Contenu du reclamation",
            content,
            height=400
        )

    else:

        st.info("Aucune réclamation disponible.")

# ============================================================
# TRANSACTIONS
# ============================================================

elif page == "Transactions":

    # ============================================================
    # TRANSACTIONS
    # ============================================================

    st.markdown(
        """
        <div class="main-title">Transactions</div>
        <div class="subtitle">Analyse de l'activité transactionnelle du réseau</div>
        <div class="red-line"></div>
        """,
        unsafe_allow_html=True
    )


    # ============================================================
    # RÉSUMÉ
    # ============================================================

    total_transactions, active_stations = get_transactions_summary()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total des transactions",
            f"{total_transactions:,}"
        )

    with col2:

        st.metric(
            "Stations actives",
            active_stations
        )


    st.divider()


    # ============================================================
    # ANALYSE
    # ============================================================

    col1, col2 = st.columns(2)


    # ------------------------------------------------------------
    # TRANSACTIONS PAR VILLE
    # ------------------------------------------------------------

    with col1:

        st.markdown("### Transactions par ville")

        data = get_transactions_by_city()

        if data:

            import pandas as pd

            df_city = pd.DataFrame(
                data,
                columns=[
                    "Ville",
                    "Transactions"
                ]
            )

            st.bar_chart(
                df_city.set_index("Ville")["Transactions"]
            )

        else:

            st.info("Aucune transaction enregistrée.")


    # ------------------------------------------------------------
    # TRANSACTIONS PAR STATION
    # ------------------------------------------------------------

    with col2:

        st.markdown("### Transactions par station")

        data = get_transactions_by_station()

        if data:

            import pandas as pd

            df_station = pd.DataFrame(
                data,
                columns=[
                    "Station",
                    "Ville",
                    "Transactions"
                ]
            )

            st.bar_chart(
                df_station.set_index("Station")["Transactions"]
            )

        else:

            st.info("Aucune transaction enregistrée.")


    # ============================================================
    # HISTORIQUE
    # ============================================================

    st.markdown("### Historique des transactions")

    data = get_transactions_details()
    columns = get_transactions_columns()

    if data:

        import pandas as pd

        df_transactions = pd.DataFrame(
            data,
            columns=columns
        )

        st.dataframe(
            df_transactions,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Aucune transaction enregistrée.")
