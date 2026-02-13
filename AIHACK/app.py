import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv('AIzaSyDbGcPr1EiJdjFWMhxcRJOv2sNq44ERWnk'))
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(
    page_title="AI Skill Roadmap Generator",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🎓 AI Skill Roadmap Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Personalized Learning Journey Starts Here</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📝 Your Details")
    
    qualification = st.selectbox(
        "Current Qualification",
        ["10th Grade", "12th Grade", "Undergraduate", "Graduate", "Post Graduate", "Other"]
    )
    
    area_of_interest = st.text_input(
        "Area of Interest",
        placeholder="e.g., Web Development, Data Science, AI/ML"
    )
    
    time_available = st.slider(
        "Hours Available Per Day",
        min_value=0.5,
        max_value=8.0,
        value=2.0,
        step=0.5
    )
    
    duration_preference = st.radio(
        "Roadmap Duration",
        ["1 Month", "3 Months", "6 Months", "1 Year"]
    )
    
    experience_level = st.selectbox(
        "Current Experience Level",
        ["Complete Beginner", "Some Knowledge", "Intermediate", "Advanced"]
    )
    
    generate_button = st.button("🚀 Generate Roadmap", use_container_width=True)

if generate_button:
    if not area_of_interest:
        st.error("⚠️ Please enter your area of interest!")
    else:
        with st.spinner("🤖 Creating your personalized roadmap..."):
            prompt = f"""
            You are an expert educational counselor and career guide. Create a comprehensive, personalized learning roadmap for a student with the following details:

            - Current Qualification: {qualification}
            - Area of Interest: {area_of_interest}
            - Daily Available Time: {time_available} hours
            - Duration: {duration_preference}
            - Experience Level: {experience_level}

            Please provide:

            1. **Course Overview**: Brief introduction to {area_of_interest} and why it's valuable
            
            2. **Prerequisites**: What basic knowledge they need before starting
            
            3. **Learning Path**: Break down the journey into clear phases
            
            4. **Detailed Roadmap**: Week-by-week or month-by-month plan with:
               - Specific topics to learn
               - Recommended free resources (courses, tutorials, documentation)
               - Practical projects for each phase
               - Estimated time for each topic
            
            5. **Free Resources**: List of best free platforms, courses, YouTube channels, and documentation
            
            6. **Project Ideas**: 5-7 hands-on projects from beginner to advanced
            
            7. **Career Opportunities**: Potential career paths and job roles
            
            8. **Tips for Success**: Practical advice for staying motivated and learning effectively
            
            Make it encouraging, practical, and suitable for someone from a rural background with limited resources. Focus on completely free resources.
            """
            
            try:
                response = model.generate_content(prompt)
                roadmap = response.text
                
                st.success("✅ Your personalized roadmap is ready!")
                
                tab1, tab2, tab3 = st.tabs(["📚 Complete Roadmap", "💡 Quick Summary", "📥 Download"])
                
                with tab1:
                    st.markdown(roadmap)
                
                with tab2:
                    st.info(f"""
                    **Your Learning Plan Summary:**
                    - **Field:** {area_of_interest}
                    - **Duration:** {duration_preference}
                    - **Daily Commitment:** {time_available} hours
                    - **Level:** {experience_level}
                    
                    Scroll down to see your complete personalized roadmap! 🎯
                    """)
                
                with tab3:
                    download_content = f"""
                    AI SKILL ROADMAP GENERATOR
                    ==========================
                    
                    Student Profile:
                    - Qualification: {qualification}
                    - Interest: {area_of_interest}
                    - Daily Time: {time_available} hours
                    - Duration: {duration_preference}
                    - Level: {experience_level}
                    
                    {roadmap}
                    """
                    
                    st.download_button(
                        label="📥 Download Roadmap as Text File",
                        data=download_content,
                        file_name=f"{area_of_interest.replace(' ', '_')}_roadmap.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                st.session_state.last_roadmap = roadmap
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Please check your API key and internet connection.")

else:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 For Everyone
        Whether you're from a city or rural area, this tool helps you learn any skill with a clear path.
        """)
    
    with col2:
        st.markdown("""
        ### 💰 100% Free
        All recommended resources are completely free. No hidden costs or premium requirements.
        """)
    
    with col3:
        st.markdown("""
        ### 🚀 Personalized
        Get a roadmap tailored to your time, level, and goals.
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📖 How to Use:
    1. Fill in your details in the sidebar (left panel)
    2. Enter what you want to learn
    3. Click "Generate Roadmap"
    4. Get your personalized learning plan!
    
    ### 💡 Popular Topics to Try:
    - Web Development
    - Python Programming
    - Data Science
    - Digital Marketing
    - Graphic Design
    - Mobile App Development
    - Machine Learning
    - Cybersecurity
    """)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        Made with ❤️ for empowering learners everywhere | Powered by Google Gemini AI
    </div>
""", unsafe_allow_html=True)