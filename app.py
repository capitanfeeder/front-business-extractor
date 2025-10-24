"""
Business Logic Extractor - MVP Frontend
Sistema de análisis de código legacy mainframe con interfaz web profesional.
"""

import streamlit as st
import requests
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Business Logic Extractor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional banking look
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1a365d;
        --secondary-color: #2c5282;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Section headers */
    .section-header {
        color: #1a365d;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #e2e8f0;
    }
    
    /* Info boxes */
    .info-box {
        background: #ebf8ff;
        border-left: 4px solid #3182ce;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    .info-box-title {
        color: #1a365d;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Success box */
    .success-box {
        background: #c6f6d5;
        border-left: 4px solid #38a169;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    /* Warning box */
    .warning-box {
        background: #feebc8;
        border-left: 4px solid #d69e2e;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    /* Error box */
    .error-box {
        background: #fed7d7;
        border-left: 4px solid #e53e3e;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border-left: 4px solid #38a169 !important;
        background: #f0fff4 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 6px;
        border: none;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f7fafc;
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "https://business-logic-extractor.onrender.com"


def upload_files(file_type, files):
    """Upload files to the API."""
    files_data = [('files', (file.name, file.getvalue(), 'text/plain')) for file in files]
    response = requests.post(f"{API_BASE_URL}/documents/{file_type}", files=files_data)
    response.raise_for_status()
    return response.json()


def run_analysis(process_name):
    """Run analysis and download report."""
    payload = {"process_name": process_name}
    response = requests.post(
        f"{API_BASE_URL}/analysis/run?download=true",
        json=payload,
        stream=True
    )
    response.raise_for_status()
    return response.content


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Business Logic Extractor</h1>
        <p>Sistema Profesional de Análisis de Código Legacy Mainframe</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'report_data' not in st.session_state:
        st.session_state.report_data = None
    if 'report_filename' not in st.session_state:
        st.session_state.report_filename = None

    # Sidebar with information
    with st.sidebar:
        st.markdown("### 📋 Información del Sistema")
        st.markdown("""
        Este sistema analiza código legacy mainframe y genera documentación técnica exhaustiva.
        
        **Arquitectura:**
        - 🔹 Fase 1: Análisis específico
        - 🔹 Fase 2: Correlación maestra
        - 🔹 Fase 3: Generación de docs
        
        **Tecnologías soportadas:**
        - COBOL
        - DB2
        - JCL
        - VSAM
        - CICS
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Requisitos")
        st.info("**Obligatorio:** Al menos 1 archivo COBOL\n\n**Opcional:** DB2, JCL/CICS")

    # Main content
    st.markdown('<h2 class="section-header">📁 Carga de Archivos</h2>', unsafe_allow_html=True)
    
    # Create three columns for file uploads
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💼 Archivos COBOL")
        st.markdown("*Programas fuente COBOL (.txt)*")
        cobol_files = st.file_uploader(
            "Seleccionar archivos COBOL",
            type=['txt'],
            accept_multiple_files=True,
            key="cobol",
            label_visibility="collapsed"
        )
        if cobol_files:
            st.success(f"✓ {len(cobol_files)} archivo(s) COBOL cargado(s)")
            with st.expander("Ver archivos"):
                for f in cobol_files:
                    st.text(f"• {f.name}")
    
    with col2:
        st.markdown("#### 🗄️ Scripts DB2")
        st.markdown("*DDL y scripts de BD (.txt)*")
        db2_files = st.file_uploader(
            "Seleccionar scripts DB2",
            type=['txt'],
            accept_multiple_files=True,
            key="db2",
            label_visibility="collapsed"
        )
        if db2_files:
            st.success(f"✓ {len(db2_files)} archivo(s) DB2 cargado(s)")
            with st.expander("Ver archivos"):
                for f in db2_files:
                    st.text(f"• {f.name}")
    
    with col3:
        st.markdown("#### ⚙️ Contexto JCL/CICS")
        st.markdown("*Jobs, transacciones (.txt)*")
        context_files = st.file_uploader(
            "Seleccionar archivos de contexto",
            type=['txt'],
            accept_multiple_files=True,
            key="context",
            label_visibility="collapsed"
        )
        if context_files:
            st.success(f"✓ {len(context_files)} archivo(s) de contexto cargado(s)")
            with st.expander("Ver archivos"):
                for f in context_files:
                    st.text(f"• {f.name}")

    # Information box
    st.markdown("""
    <div class="info-box">
        <div class="info-box-title">ℹ️ Requisitos de Archivos</div>
        <p><strong>Obligatorio:</strong> Al menos un archivo COBOL.<br>
        <strong>Opcional:</strong> DB2 (si no se incluye, se asume sistema VSAM puro).<br>
        <strong>Recomendado:</strong> Archivos JCL para análisis completo del flujo batch.<br>
        <strong>Formato:</strong> Todos los archivos deben ser .txt en formato texto plano.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Analysis section
    st.markdown('<h2 class="section-header">🔍 Configuración y Análisis</h2>', unsafe_allow_html=True)
    
    # Process name input
    col_name, col_space = st.columns([3, 1])
    with col_name:
        process_name = st.text_input(
            "Nombre del Proceso (Opcional)",
            placeholder="Ej: Mantenimiento_VSAM, Proceso_Batch_Cuentas, etc.",
            help="Si no se especifica, se usará 'Business_Requirements' por defecto"
        )

    # Analysis button
    st.markdown("<br>", unsafe_allow_html=True)
    
    can_analyze = len(cobol_files) > 0 if cobol_files else False
    
    if not can_analyze:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Se requiere al menos un archivo COBOL para iniciar el análisis.</strong>
        </div>
        """, unsafe_allow_html=True)
    
    analyze_button = st.button(
        "🚀 ANALIZAR Y DESCARGAR REPORTE",
        disabled=not can_analyze,
        use_container_width=True
    )

    if analyze_button:
        try:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Upload COBOL files
            status_text.markdown("**Fase 1/5:** Cargando archivos COBOL...")
            progress_bar.progress(10)
            upload_files('cobol', cobol_files)
            
            # Step 2: Upload DB2 files (if any)
            if db2_files:
                status_text.markdown("**Fase 2/5:** Cargando scripts DB2...")
                progress_bar.progress(25)
                upload_files('db2', db2_files)
            else:
                progress_bar.progress(25)
            
            # Step 3: Upload context files (if any)
            if context_files:
                status_text.markdown("**Fase 3/5:** Cargando archivos de contexto...")
                progress_bar.progress(40)
                upload_files('context', context_files)
            else:
                progress_bar.progress(40)
            
            # Step 4: Run analysis
            status_text.markdown("**Fase 4/5:** Ejecutando análisis multiagente (esto puede tardar varios minutos)...")
            progress_bar.progress(60)
            
            final_process_name = process_name.strip() if process_name.strip() else "Business_Requirements"
            report_content = run_analysis(final_process_name)
            
            # Step 5: Prepare download
            status_text.markdown("**Fase 5/5:** Generando reporte para descarga...")
            progress_bar.progress(90)
            
            st.session_state.report_data = report_content
            st.session_state.report_filename = f"{final_process_name}.md"
            st.session_state.analysis_complete = True
            
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            # Success message
            st.markdown("""
            <div class="success-box">
                ✅ <strong>¡Análisis completado exitosamente!</strong><br>
                El reporte está listo para descargar. Los archivos temporales han sido limpiados automáticamente.
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
        except Exception as e:
            st.markdown(f"""
            <div class="error-box">
                ❌ <strong>Error durante el análisis:</strong><br>
                {str(e)}
            </div>
            """, unsafe_allow_html=True)
            st.error("Por favor, verifique que el servidor backend esté ejecutándose en http://localhost:8000")

    # Download section
    if st.session_state.analysis_complete and st.session_state.report_data:
        st.markdown("---")
        st.markdown('<h2 class="section-header">📥 Descargar Reporte</h2>', unsafe_allow_html=True)
        
        col_download, col_info = st.columns([2, 2])
        
        with col_download:
            st.download_button(
                label="📄 DESCARGAR REPORTE MARKDOWN",
                data=st.session_state.report_data,
                file_name=st.session_state.report_filename,
                mime="text/markdown",
                use_container_width=True
            )
        
        with col_info:
            st.info(f"**Archivo:** {st.session_state.report_filename}\n\n**Formato:** Markdown (.md)")
        
        # Reset button
        if st.button("🔄 Realizar Nuevo Análisis", use_container_width=True):
            st.session_state.analysis_complete = False
            st.session_state.report_data = None
            st.session_state.report_filename = None
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #718096; padding: 2rem;">
        <p>© 2025 Business Logic Extractor | Sistema de Análisis de Código Legacy Mainframe</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=2)
        main()
    except requests.exceptions.RequestException:
        st.error("""
        ⚠️ **Error de Conexión**
        
        No se puede conectar con el servidor backend.
        
        Por favor, asegúrese de que el servidor FastAPI esté ejecutándose:
        
        ```bash
        python main.py
        ```
        
        El servidor debe estar disponible en: https://business-logic-extractor.onrender.com
        """)
