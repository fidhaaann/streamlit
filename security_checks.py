import streamlit as st
import requests
import builtwith
from bs4 import BeautifulSoup
import re

# Streamlit Page Config
st.set_page_config(page_title="WebTech Analyzer", page_icon="🌐", layout="wide")

# Custom CSS for improved UI
st.markdown("""
    <style>
        /* Centered Headings */
        .title, .subheader { text-align: center !important; }

        /* Rounded Corner Boxes */
        .result-box {
            background-color: #1e1e2f;
            padding: 15px;
            border-radius: 12px;
            margin: 10px 0;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }

        /* Font Styling */
        html, body, [class*="st-"] { font-family: 'Poppins', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Centered Page Title
st.markdown("<h1 class='title'>🌐 WebTech Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subheader'>Analyze website technologies & frameworks</h3>", unsafe_allow_html=True)

# User Input Section
url = st.text_input("🔗 Enter Website URL (e.g., https://example.com)", "")

if url:
    try:
        # Fetch HTTP Headers
        response = requests.get(url, timeout=5)
        headers = response.headers

        # Rounded Box for HTTP Headers
        st.markdown("<h4 class='subheader'>🔍 HTTP Headers</h4>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            for key, value in headers.items():
                st.markdown(f"**{key}**: {value}")
            st.markdown("</div>", unsafe_allow_html=True)

        # Detect Server & Backend
        if 'Server' in headers or 'X-Powered-By' in headers:
            st.markdown("<h4 class='subheader'>🖥️ Server & Backend</h4>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                if 'Server' in headers:
                    st.success(f"**Server Technology**: {headers['Server']}")
                if 'X-Powered-By' in headers:
                    st.success(f"**Backend Technology**: {headers['X-Powered-By']}")
                st.markdown("</div>", unsafe_allow_html=True)

        # JavaScript Library Detection
        st.markdown("<h4 class='subheader'>📜 JavaScript Libraries & Frameworks</h4>", unsafe_allow_html=True)
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = [script['src'] for script in soup.find_all('script', src=True)]

        js_frameworks = {
            "React.js": "react",
            "Vue.js": "vue",
            "Angular": "angular",
            "jQuery": "jquery"
        }

        detected_js = []
        for script in scripts:
            for framework, keyword in js_frameworks.items():
                if keyword in script:
                    detected_js.append(f"**{framework}** → `{script}`")

        with st.container():
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            if detected_js:
                st.info("\n".join(detected_js))
            else:
                st.warning("No common JS frameworks detected!")
            st.markdown("</div>", unsafe_allow_html=True)

        # CMS Detection
        st.markdown("<h4 class='subheader'>🏗️ CMS Detection</h4>", unsafe_allow_html=True)
        cms_patterns = {
            "WordPress": r"wp-content|wp-includes",
            "Joomla": r"\/templates\/",
            "Drupal": r"\/sites\/default\/"
        }

        detected_cms = [cms for cms, pattern in cms_patterns.items() if re.search(pattern, response.text, re.IGNORECASE)]

        with st.container():
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            if detected_cms:
                st.success(f"Detected CMS: **{', '.join(detected_cms)}**")
            else:
                st.warning("No CMS detected!")
            st.markdown("</div>", unsafe_allow_html=True)

        # BuiltWith API (Optional)
        st.markdown("<h4 class='subheader'>🛠️ BuiltWith Analysis (Optional)</h4>", unsafe_allow_html=True)
        try:
            techs = builtwith.parse(url)
            with st.container():
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                for category, technologies in techs.items():
                    st.write(f"**{category}**: {', '.join(technologies)}")
                st.markdown("</div>", unsafe_allow_html=True)
        except:
            st.error("BuiltWith API failed or unavailable!")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching website data: {e}")

