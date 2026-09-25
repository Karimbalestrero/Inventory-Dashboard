import streamlit as st
import pandas as pd
from datetime import datetime
import html
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# ============================================================
# SEITENKONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Inventur Fortschrittskontrolle",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st_autorefresh(
    interval=10_000,
    limit=None,
    key="inventory_auto_refresh"
)

# ============================================================
# KONSTANTEN
# ============================================================

EMPLOYEES = {
    "NA": 10,
    "NB": 39,
    "ND": 30,
    "PCBA": 13,
}

BLUE = "#004696"
GREEN = "#98ED4B"
YELLOW = "#FFC455"
RED = "#FF5964"

WHITE = "#F7FBFF"
MUTED = "#B9CDDC"
ICON = "#D8EAF8"

CARD_BG = "rgba(5, 61, 101, 0.72)"
CARD_BORDER = "rgba(126, 190, 232, 0.27)"


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def progress_info(progress):
    """
    progress ist ein Wert zwischen 0 und 1.
    """

    if progress >= 1.0:
        return GREEN, "Abgeschlossen"

    elif progress >= 0.50:
        return YELLOW, "Im Plan"

    else:
        return RED, "Kritisch"


def clean_location(value):

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def sort_location(value):

    try:
        return (0, float(value))

    except (ValueError, TypeError):
        return (1, str(value))


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
<style>
[data-testid="stStatusWidget"],
[data-testid="stToolbar"],
.viewerBadge_container__1QSob,
.viewerBadge_link__1S137 {{
    display: none !important;
}}
/* ==========================================================
   STREAMLIT GRUNDLAYOUT
========================================================== */

html,
body,
[class*="css"] {{
    font-family:
        Inter,
        "Segoe UI",
        Arial,
        sans-serif;
}}

.stApp {{
    background:
        radial-gradient(
            circle at 45% -10%,
            rgba(0, 100, 175, 0.42),
            transparent 42%
        ),
        radial-gradient(
            circle at 90% 80%,
            rgba(0, 70, 150, 0.18),
            transparent 38%
        ),
        linear-gradient(
            145deg,
            #00365F 0%,
            #002B4D 42%,
            #001F38 100%
        );

    color: {WHITE};
}}

.block-container {{
    max-width: 100%;
    padding:
        1.0rem
        1.55rem
        0.45rem
        1.55rem;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

div[data-testid="stToolbar"] {{
    visibility: hidden;
    height: 0;
}}

div[data-testid="stDecoration"] {{
    visibility: hidden;
}}

div[data-testid="stStatusWidget"] {{
    visibility: hidden;
}}

div[data-testid="stVerticalBlock"] {{
    gap: 0.42rem;
}}


/* ==========================================================
   UPLOADER
========================================================== */

[data-testid="stFileUploader"] {{
    max-width: 380px;
}}

[data-testid="stFileUploader"] section {{
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
}}


/* ==========================================================
   HEADER
========================================================== */

.hero-title {{
    height: 168px;

    display: flex;
    flex-direction: column;
    justify-content: center;

    padding-left: 12px;
}}

.hero-inner {{
    display: flex;
    align-items: center;
    gap: 22px;
}}

.hero-cube {{
    font-size: 63px;
    color: {ICON};
    line-height: 1;
}}

.hero-text {{
    display: flex;
    flex-direction: column;
}}

.eyebrow {{
    color: #BBD5E8;

    font-size: 15px;
    font-weight: 700;

    letter-spacing: 0.25em;

    margin-bottom: 5px;
}}

.main-title {{
    color: {WHITE};

    font-size: 37px;
    line-height: 1.03;

    font-weight: 850;

    letter-spacing: -0.035em;
}}

.subtitle {{
    color: {MUTED};

    font-size: 17px;

    margin-top: 10px;
}}


/* ==========================================================
   STANDARD TOP CARD
========================================================== */

.top-card {{    height: 115px;

    background:
        linear-gradient(
            145deg,
            rgba(6, 77, 126, 0.76),
            rgba(3, 48, 82, 0.84)
        );

    border: 1px solid rgba(126, 190, 232, 0.27);
    border-radius: 11px;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.035),
        0 6px 18px rgba(0,0,0,0.07);

    padding: 9px 14px;
    box-sizing: border-box;
}}

.top-heading {{
    color: #F7FBFF;
    font-size: 16px;
    font-weight: 900;

    display: flex;
    align-items: center;
    gap: 7px;

    margin-bottom: 7px;
}}
.top-icon {{
    color: {ICON};
    font-size: 20px;
    width: 20px;
    line-height: 1;
}}

/* ==========================================================
   MITARBEITER
========================================================== */

.employee-grid {{
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);
        transform: translateY(-4px);
}}

.employee-item {{
    text-align: center;

    border-right:
        1px solid
        rgba(190, 220, 240, 0.34);
}}

.employee-item:last-child {{
    border-right: none;
}}

.employee-label {{
    color: #F7FBFF;
    font-size: 12px;
    font-weight: 500;
}}


.employee-value {{
    color: #F7FBFF;
    font-size: 25px;
    font-weight: 850;
    line-height: 1;
    margin-top: 4px;
}}


/* ==========================================================
   AUF KURS
========================================================== */

.course-card {{
    height: 115px;

    background:
        linear-gradient(
            145deg,
            rgba(6, 77, 126, 0.76),
            rgba(3, 48, 82, 0.84)
        );

    border: 1px solid {CARD_BORDER};
    border-radius: 11px;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.035),
        0 6px 18px rgba(0,0,0,0.07);

    padding: 9px 14px;
    box-sizing: border-box;
}}

.course-heading-row {{
    display: flex;
    align-items: center;
    gap: 7px;
}}

.course-icon {{
    color: {ICON};

    font-size: 20px;

    line-height: 1;
}}

.course-heading {{
    color: {WHITE};

    font-size: 15px;

    font-weight: 800;

    line-height: 1;
}}

.course-subtitle {{
    color: {MUTED};

    font-size: 9px;

    margin-top: 2px;
}}


/* ==========================================================
   GAUGE
========================================================== */

.gauge-area {{
    display: flex;

    justify-content: center;

    align-items: flex-end;

    gap: 10px;

    margin-top: 2px;
}}

.gauge {{
    position: relative;

    width: 120px;

    height: 58px;

    overflow: hidden;
}}

.gauge-outer {{
    position: absolute;

    width: 120px;

    height: 120px;

    border-radius: 50%;

    background:
        conic-gradient(
            from 270deg,

            {RED} 0deg 30deg,

            {YELLOW} 30deg 64deg,

            {GREEN} 64deg 90deg,

            rgba(35, 110, 150, 0.46)
            90deg 360deg
        );
}}

.gauge-inner {{
    position: absolute;

    width: 86px;

    height: 86px;

    left: 17px;

    top: 17px;

    border-radius: 50%;

    background: #05375E;
}}

.gauge-needle {{
    position: absolute;

    left: 58px;

    bottom: 0;

    width: 4px;

    height: 46px;

    background: {WHITE};

    border-radius: 99px;

    transform-origin: 50% 100%;
}}

.gauge-center {{
    position: absolute;

    left: 54px;

    bottom: -5px;

    width: 12px;

    height: 12px;

    background: {WHITE};

    border-radius: 50%;
}}

.gauge-value {{
    position: absolute;

    left: 0;

    right: 0;

    bottom: 3px;

    text-align: center;

    color: {WHITE};

    font-size: 19px;

    font-weight: 900;
}}

.gauge-status {{
    border: 2px solid;

    border-radius: 999px;

    padding: 3px 14px;

    font-size: 13px;

    font-weight: 800;

    white-space: nowrap;

    margin-bottom: 3px;
}}


/* ==========================================================
   DATUM UND UHR
========================================================== */

.date-header {{
    display: flex;

    align-items: center;

    gap: 11px;

    color: {WHITE};

    font-size: 18px;

    font-weight: 800;
}}

.calendar-icon {{
    color: {ICON};

    font-size: 29px;
}}

.date-value {{
    color: {WHITE};

    font-size: 17px;

    font-weight: 700;

    margin-left: 40px;

    margin-top: -3px;
}}

.clock-row {{
    display: flex;

    align-items: center;

    gap: 12px;

    margin-top: 7px;
}}

.clock-icon {{
    color: {ICON};

    font-size: 35px;
}}

.live-clock {{
    color: {WHITE};

    font-size: 37px;

    font-weight: 900;

    line-height: 1;
}}

.last-update {{
    color: {MUTED};

    font-size: 10px;

    margin-left: 47px;

    margin-top: 5px;

    line-height: 1.35;
}}


/* ==========================================================
   SECTION CONTAINER
========================================================== */

.overview-container {{
    border:
        1px solid
        rgba(126, 190, 232, 0.24);

    border-radius: 13px;

    padding:
        9px
        12px
        12px
        12px;

    background:
        rgba(0, 52, 88, 0.18);
}}

.section-heading {{
    display: flex;

    align-items: center;

    gap: 11px;

    color: {WHITE};

    font-size: 24px;

    font-weight: 850;

    margin:
        1px
        0
        9px
        2px;
}}

.section-heading-icon {{
    color: {ICON};

    font-size: 27px;
}}


/* ==========================================================
   KPI KARTEN
========================================================== */

.kpi-card {{
    height: 104px;

    background:
        linear-gradient(
            145deg,
            rgba(6, 79, 130, 0.78),
            rgba(3, 49, 83, 0.88)
        );

    border:
        1px solid
        rgba(126, 190, 232, 0.26);

    border-radius: 11px;

    padding: 14px 18px;

    display: flex;

    align-items: center;

    gap: 19px;

    box-sizing: border-box;
}}

.kpi-icon {{
    width: 53px;

    color: {ICON};

    font-size: 43px;

    text-align: center;

    line-height: 1;
}}

.kpi-content {{
    flex: 1;
}}

.kpi-label {{
    color: {WHITE};

    font-size: 17px;

    font-weight: 500;
}}

.kpi-value {{
    color: {WHITE};

    font-size: 37px;

    font-weight: 900;

    line-height: 1;

    margin-top: 5px;
}}


/* ==========================================================
   FORTSCHRITT KPI
========================================================== */

.progress-kpi {{
    height: 104px;

    background:
        linear-gradient(
            145deg,
            rgba(6, 79, 130, 0.78),
            rgba(3, 49, 83, 0.88)
        );

    border:
        1px solid
        rgba(126, 190, 232, 0.26);

    border-radius: 11px;

    padding: 14px 18px;

    display: flex;

    align-items: center;

    gap: 18px;

    box-sizing: border-box;
}}

.progress-kpi-icon {{
    width: 53px;

    color: {ICON};

    font-size: 42px;

    text-align: center;
}}

.progress-kpi-content {{
    flex: 1;
}}

.progress-kpi-label {{
    color: {WHITE};

    font-size: 17px;
}}

.progress-kpi-bottom {{
    display: flex;

    align-items: center;

    gap: 12px;

    margin-top: 12px;
}}

.progress-kpi-track {{
    flex: 1;

    height: 16px;

    background:
        rgba(55, 126, 171, 0.45);

    border-radius: 999px;

    overflow: hidden;
}}

.progress-kpi-fill {{
    height: 100%;

    border-radius: 999px;
}}

.progress-kpi-number {{
    color: {WHITE};

    font-size: 27px;

    font-weight: 900;

    min-width: 60px;

    text-align: right;
}}


/* ==========================================================
   STORAGE HEADER
========================================================== */

.storage-header {{
    display: flex;

    align-items: center;

    justify-content: space-between;

    margin:
        10px
        5px
        7px
        5px;
}}

.storage-title {{
    display: flex;

    align-items: center;

    gap: 12px;

    color: {WHITE};

    font-size: 26px;

    font-weight: 900;
}}

.storage-title-icon {{
    color: {ICON};

    font-size: 32px;
}}

.storage-count {{
    color: {MUTED};

    font-size: 14px;
}}


/* ==========================================================
   STORAGE LOCATION CARD
========================================================== */

.location-card {{
    height: 112px;
    min-height: 112px;

    background:
        linear-gradient(
            145deg,
            rgba(5, 76, 126, 0.84),
            rgba(2, 46, 79, 0.93)
        );

    border:
        1px solid
        rgba(126, 190, 232, 0.29);

    border-radius: 11px;

    padding:
        8px
        12px
        8px
        12px;

    box-sizing: border-box;

    margin-bottom: 30px;
}}

.location-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 5px;
}}

.location-name {{
    color: {WHITE};
    font-size: 18px;
    font-weight: 900;

    display: flex;
    align-items: center;
    gap: 6px;
}}

.location-pin {{
    color: {ICON};
    font-size: 18px;
}}

.status-badge {{
    border: 2px solid;
    border-radius: 999px;

    padding: 2px 6px;

    font-size: 14px;
    font-weight: 850;
    line-height: 1;
    hight: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.status-content {{
    display: inline-block;
    transform: translateY(7px);
}}
.location-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;

    margin-bottom: 5px;

    position: relative;
    top: -10px;
}}

.location-label {{
    color: {MUTED};

    font-size: 11px;

    font-weight: 500;
}}

.location-value {{
    color: {WHITE};

    font-size: 18px;

    font-weight: 900;

    line-height: 1;

    margin-top: 2px;
}}

.location-progress-row {{
    display: flex;

    align-items: center;

    gap: 8px;
    position: relative;
    top: -12px;
}}

.location-progress-track {{
    flex: 1;

    height: 16px;

    background:
        rgba(49, 117, 163, 0.48);

    border-radius: 999px;

    overflow: hidden;
}}

.location-progress-fill {{
    height: 100%;

    border-radius: 999px;
}}

.location-progress-value {{
    color: {WHITE};

    font-size: 16px;

    font-weight: 900;

    min-width: 46px;

    text-align: right;
}}


/* ==========================================================
   FOOTER
========================================================== */

.dashboard-footer {{
    display: flex;

    justify-content: space-between;

    align-items: center;

    color: #A7C1D3;

    font-size: 11px;

    padding:
        3px
        6px
        0
        6px;
}}


/* ==========================================================
   TV / KLEINERE BILDSCHIRME
========================================================== */

@media (max-width: 1500px) {{

    .main-title {{
        font-size: 31px;
    }}

    .employee-value {{
        font-size: 32px;
    }}

    .location-name {{
        font-size: 21px;
    }}

    .location-value {{
        font-size: 20px;
    }}

    .location-label {{
        font-size: 12px;
    }}

}}

</style>
""",
    unsafe_allow_html=True,
)





# ============================================================
# EXCEL EINLESEN
# ============================================================

EXCEL_FILE = "data/inventory.xlsx"

try:
    df = pd.read_excel(EXCEL_FILE)

except FileNotFoundError:
    st.error("Die Datei data/inventory.xlsx wurde nicht gefunden.")
    st.stop()

except Exception as e:
    st.error(
        f"Excel-Datei konnte nicht gelesen werden: {e}"
    )
    st.stop()


df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


# ============================================================
# SPALTEN PRÜFEN
# ============================================================

required_columns = [
    "Phys. Inventory Doc.",
    "Storage Location",
    "Physical inventory status",
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    st.error(
        "Folgende Spalten fehlen: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# DATEN BEREINIGEN
# ============================================================

df = df[
    df["Storage Location"].notna()
].copy()


df["_status"] = (
    df["Physical inventory status"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ============================================================
# GESAMTWERTE
# ============================================================

total_documents = (
    df["Phys. Inventory Doc."]
    .nunique()
)


total_positions = len(df)


total_counted = (
    df["_status"]
    .eq("counted, adjusted")
    .sum()
)
total_in_progress = (
    df["_status"]
    .eq("counted")
    .sum()
)

total_open = (
    total_positions
    - total_counted
    - total_in_progress
)


if total_positions > 0:

    total_progress = (
        total_counted
        / total_positions
    )

else:

    total_progress = 0


total_color, total_status = (
    progress_info(
        total_progress
    )
)


total_percent = total_progress * 100

if total_progress < 1.0:
    total_percent_text = f"{total_percent:.1f}%"
else:
    total_percent_text = "100%"


# ============================================================
# ZEIGERPOSITION
# ============================================================

# Halbkreis:
# -90° = ganz links
#  0°  = Mitte
# +90° = ganz rechts

needle_angle = (
    -90
    + (180 * total_progress)
)


# ============================================================
# DATUM
# ============================================================

now = datetime.now()


weekdays = {
    0: "Montag",
    1: "Dienstag",
    2: "Mittwoch",
    3: "Donnerstag",
    4: "Freitag",
    5: "Samstag",
    6: "Sonntag",
}


months = {
    1: "Januar",
    2: "Februar",
    3: "März",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Dezember",
}


weekday = weekdays[
    now.weekday()
]


date_text = (
    f"{now.day}. "
    f"{months[now.month]} "
    f"{now.year}"
)






# ============================================================
# HEADER
# ============================================================

title_col, employee_col, course_col, date_col = st.columns(
    [1.52, 1.40, 0.93, 1.10],
    gap="small",
)


# ============================================================
# TITEL
# ============================================================

with title_col:

    st.markdown(
        """
<div class="hero-title">

<div class="hero-inner">

<div class="hero-cube">
◇
</div>

<div class="hero-text">

<div class="eyebrow">
LAGER
</div>

<div class="main-title">
Inventur<br>
Fortschrittskontrolle
</div>

<div class="subtitle">
Live-Übersicht der physischen Inventur
</div>

</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# MITARBEITER
# ============================================================

with employee_col:

    st.markdown(
        f"""
<div class="top-card">

<div class="top-heading">

<span class="top-icon">
♟
</span>

Mitarbeiter pro Bereich

</div>


<div class="employee-grid">


<div class="employee-item">

<div class="employee-label">
NA
</div>

<div class="employee-value">
{EMPLOYEES["NA"]}
</div>

</div>


<div class="employee-item">

<div class="employee-label">
NB
</div>

<div class="employee-value">
{EMPLOYEES["NB"]}
</div>

</div>


<div class="employee-item">

<div class="employee-label">
ND
</div>

<div class="employee-value">
{EMPLOYEES["ND"]}
</div>

</div>


<div class="employee-item">

<div class="employee-label">
PCBA
</div>

<div class="employee-value">
{EMPLOYEES["PCBA"]}
</div>

</div>


</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# AUF KURS
# ============================================================

with course_col:

    st.markdown(
        f"""
<div class="course-card">

<div class="course-heading-row">

<div class="course-icon">
◎
</div>

<div>

<div class="course-heading">
Auf Kurs
</div>

<div class="course-subtitle">
Gesamtfortschritt
</div>

</div>

</div>


<div class="gauge-area">


<div class="gauge">

<div class="gauge-outer">
</div>

<div class="gauge-inner">
</div>

<div
    class="gauge-needle"
    style="
        transform:
        rotate({needle_angle}deg);
    "
>
</div>

<div class="gauge-center">
</div>

<div class="gauge-value">
{total_percent_text}
</div>

</div>


<div
    class="gauge-status"
    style="
        color:{total_color};
        border-color:{total_color};
    "
>
{total_status}
</div>


</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# DATUM + LIVE UHR
# ============================================================

with date_col:

    clock_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>

    * {{
        box-sizing: border-box;
    }}

    html, body {{
        margin: 0;
        padding: 0;
        background: transparent;
        overflow: hidden;

        font-family:
            Inter,
            "Segoe UI",
            Arial,
            sans-serif;
    }}

    .date-card {{
    width: 100%;
    height: 115px;

    background:
        linear-gradient(
            145deg,
            rgba(6, 77, 126, 0.76),
            rgba(3, 48, 82, 0.84)
        );

    border:
        1px solid rgba(126, 190, 232, 0.27);

    border-radius: 11px;

    padding: 10px 16px;

    color: #F7FBFF;
}}

    .date-header {{
        display: flex;
        align-items: center;
        gap: 7px;

        font-size: 15px;
        font-weight: 800;
    }}

    .calendar-icon {{
        color: #D8EAF8;
        font-size: 20px;
        width: 23px;
        text-align: center;
    }}

    .date-value {{
        margin-left: 30px;
        margin-top: 2px;

        font-size: 13px;
        font-weight: 700;
    }}

    .clock-row {{
        display: flex;
        align-items: center;
        gap: 12px;

        margin-top: 8px;
    }}

    .clock-icon {{
        color: #D8EAF8;

        width: 29px;

        font-size: 30px;
        font-weight: 400;

        text-align: center;
    }}

    #live-clock {{
        font-size: 35px;
        line-height: 1;

        font-weight: 900;

        letter-spacing: 0.02em;
    }}

    .last-update {{
        margin-left: 30px;
        margin-top: 6px;

        color: #B9CDDC;

        font-size: 9px;
        line-height: 1.35;
    }}

    .last-update-title {{
        font-weight: 800;
        letter-spacing: 0.04em;
    }}

    </style>
    </head>

    <body>

        <div class="date-card">

            <div class="date-header">

                <div class="calendar-icon">
                    ▣
                </div>

                <div>
                    {weekday}
                </div>

            </div>


            <div class="date-value">
                {date_text}
            </div>


           

            <div class="last-update">

                <span class="last-update-title">
                    LETZTE AKTUALISIERUNG
                </span>
                {now.strftime("%H:%M Uhr")}

                <br>

                

            </div>

        </div>


        

    </body>
    </html>
    """

    components.html(
        clock_html,
        height=115,
        scrolling=False,
    )


# ============================================================
# GESAMTÜBERSICHT
# ============================================================

st.markdown(
    """
<div class="section-heading">

<span class="section-heading-icon">
▥
</span>

Gesamtübersicht

</div>
""",
    unsafe_allow_html=True,
)


k1, k2, k3, k4, k5 = st.columns(
    5,
    gap="small",
)


# ============================================================
# KPI FUNKTION
# ============================================================

def render_kpi(
    column,
    icon,
    label,
    value,
):

    with column:

        st.markdown(
            f"""
<div class="kpi-card">

<div class="kpi-icon">
{icon}
</div>

<div class="kpi-content">

<div class="kpi-label">
{label}
</div>

<div class="kpi-value">
{value}
</div>

</div>

</div>
""",
            unsafe_allow_html=True,
        )


# ============================================================
# KPIs
# ============================================================

render_kpi(
    k1,
    "▤",
    "Inventurdokumente",
    total_documents,
)


render_kpi(
    k2,
    "◇",
    "Positionen",
    total_positions,
)


render_kpi(
    k3,
    "✓",
    "Abgeschlossen",
    total_counted,
)


# Sanduhr bewusst als neutrales Textsymbol,
# damit sie NICHT gelb als Emoji dargestellt wird.

render_kpi(
    k4,
    "↻",
    "In Arbeit",
    total_in_progress,
)
render_kpi(
    k5,
   "◷",
    "Offen",
    total_open,
)

# ============================================================
# FORTSCHRITT-KACHEL
# Balken ist NUR HIER.
# ============================================================

st.markdown(
    f'<div style="margin-top:8px;margin-bottom:14px;padding:10px 16px;">'
    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
    f'<span style="font-size:13px;font-weight:600;">Gesamtfortschritt</span>'
    f'<span style="font-size:16px;font-weight:700;">{total_percent:.1f}%</span>'
    f'</div>'
    f'<div style="width:100%;height:8px;background:rgba(255,255,255,0.12);border-radius:999px;overflow:hidden;">'
    f'<div style="width:{total_percent}%;height:100%;background:{total_color};border-radius:999px;"></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)


# ============================================================
# STORAGE LOCATIONS
# ============================================================

storage_locations = sorted(
    df["Storage Location"]
    .dropna()
    .unique(),
    key=sort_location,
)


number_locations = len(
    storage_locations
)


st.markdown(
    f"""
<div class="storage-header">

<div class="storage-title">

<span class="storage-title-icon">
⌖
</span>

Storage Locations

</div>


<div class="storage-count">
{number_locations} Storage Locations
</div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# STORAGE LOCATION CARDS
# ============================================================

COLUMNS_PER_ROW = 3


for start in range(
    0,
    number_locations,
    COLUMNS_PER_ROW,
):

    cols = st.columns(
        COLUMNS_PER_ROW,
        gap="small",
    )


    locations_in_row = (
        storage_locations[
            start:
            start + COLUMNS_PER_ROW
        ]
    )


    for column, location in zip(
        cols,
        locations_in_row,
    ):

        location_df = df[
            df["Storage Location"]
            == location
        ]


        documents = (
            location_df[
                "Phys. Inventory Doc."
            ]
            .nunique()
        )


        positions = len(
            location_df
        )


        counted = (
            location_df["_status"]
            .eq("counted, adjusted")
            .sum()
        )
        in_progress = (
            location_df["_status"]
            .eq("counted")
            .sum()
        )

        open_items = (
            positions
            - counted
            - in_progress
        )


        if positions > 0:
            progress = (
                counted
                / positions
            )
        else:
            progress = 0

        percent = progress * 100

        if progress < 1.0:
            percent_text = f"{percent:.1f}%"
        else:
            percent_text = "100%"

        color, status = (
            progress_info(
                progress
            )
        )

        location_name = html.escape(
            clean_location(
                location
            )
        )


        # Status-Symbol

        if progress >= 0.90:

            status_symbol = "✓"

        elif progress >= 0.50:

            status_symbol = "≈"

        else:

            status_symbol = "!"


        card_html = f"""
<div class="location-card">


<div class="location-header">


<div class="location-name">

<span class="location-pin">
⌖
</span>

{location_name}

</div>


<div
    class="status-badge"
    style="
        color:{color};
        border-color:{color};
    "
>

<span class="status-content">{status_symbol} {status}</span>

</div>


</div>


<div class="location-grid">


<div>

<div class="location-label">
Dokumente
</div>

<div class="location-value">
{documents}
</div>

</div>


<div>

<div class="location-label">
Positionen
</div>

<div class="location-value">
{positions}
</div>

</div>


<div>

<div class="location-label">
Abgeschlossen
</div>

<div class="location-value">
{counted}
</div>

</div>

<div>

<div class="location-label">
In Arbeit
</div>

<div class="location-value">
{in_progress}
</div>

</div>
<div>

<div class="location-label">
Offen
</div>

<div class="location-value">
{open_items}
</div>

</div>


</div>


<div class="location-progress-row">


<div class="location-progress-track">

<div
    class="location-progress-fill"
    style="
        width:{percent}%;
        background:{color};
    "
>
</div>

</div>


<div class="location-progress-value">
{percent_text}
</div>


</div>


</div>
"""


        with column:

            st.markdown(
                card_html,
                unsafe_allow_html=True,
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="dashboard-footer">

<div>
◇ &nbsp;
&nbsp;&nbsp;
Inventur Fortschrittskontrolle
</div>


</div>
""",
    unsafe_allow_html=True,
)