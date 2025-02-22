import streamlit as st
import requests
import builtwith
from bs4 import BeautifulSoup
import re

# Streamlit Page Config
st.set_page_config(page_title="WebTech Analyzer", page_icon="🌐", layout="wide")

# Header
st.title("🌐 WebTech Analyzer")
st.subheader("Analyze website technologies and frameworks")

# User Input
url = st.text_input("🔗 Enter Website URL (e.g., https://example.com)", "")

if url:
    try:
        # Fetch HTTP Headers
        st.write("### 🔍 HTTP Headers")
        response = requests.get(url, timeout=5)
        headers = response.headers

        for key, value in headers.items():
            st.write(f"**{key}**: {value}")

        # Detect Server & Backend
        if 'Server' in headers:
            st.success(f"**Server Technology**: {headers['Server']}")
        if 'X-Powered-By' in headers:
            st.success(f"**Backend Technology**: {headers['X-Powered-By']}")

        # JavaScript Library Detection
        st.write("### 📜 JavaScript Libraries & Frameworks")
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

        if detected_js:
            st.info("\n".join(detected_js))
        else:
            st.warning("No common JS frameworks detected!")

        # CMS Detection
        st.write("### 🏗️ CMS Detection")
        cms_patterns = {
            "WordPress": r"wp-content|wp-includes",
            "Joomla": r"\/templates\/",
            "Drupal": r"\/sites\/default\/"
        }

        detected_cms = [cms for cms, pattern in cms_patterns.items() if re.search(pattern, response.text, re.IGNORECASE)]
        
        if detected_cms:
            st.success(f"Detected CMS: **{', '.join(detected_cms)}**")
        else:
            st.warning("No CMS detected!")

        # BuiltWith API (Optional)
        st.write("### 🛠️ BuiltWith Analysis (Optional)")
        try:
            techs = builtwith.parse(url)
            for category, technologies in techs.items():
                st.write(f"**{category}**: {', '.join(technologies)}")
        except:
            st.error("BuiltWith API failed or unavailable!")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching website data: {e}")
