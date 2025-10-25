"""
Business Logic Extractor - MVP Frontend
Sistema de análisis de código legacy mainframe con interfaz web profesional.
"""

import streamlit as st
import requests
import json
import markdown
import base64
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
    """Run analysis and get JSON response with markdown content."""
    payload = {"process_name": process_name} if process_name else None
    
    response = requests.post(
        f"{API_BASE_URL}/analysis/run",
        json=payload
    )
    response.raise_for_status()
    return response.json()


def markdown_to_pdf_html(markdown_content, process_name):
    """Convert markdown to HTML with ICBC styling for PDF generation."""
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['tables', 'fenced_code', 'codehilite']
    )
    
    # ICBC CSS styling
    css_styles = """
    <style>
        @media print {
            @page {
                size: A4;
                margin: 2.5cm 2cm 3cm 2cm;
            }
        }
        
        body {
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #222;
            margin: 0;
            padding: 20px;
            background: white;
        }
        
        .document-header {
            text-align: center;
            margin-bottom: 2cm;
            padding-bottom: 1cm;
            border-bottom: 3px solid #C0161C;
        }
        
        .document-title {
            font-family: 'Arial', sans-serif;
            font-size: 22pt;
            font-weight: bold;
            color: #C0161C;
            text-transform: uppercase;
            margin: 0 0 0.5cm 0;
            letter-spacing: 1px;
        }
        
        .document-subtitle {
            font-family: 'Calibri', sans-serif;
            font-size: 14pt;
            color: #444;
            margin-bottom: 0.3cm;
        }
        
        h1 {
            font-family: 'Arial', sans-serif;
            font-size: 16pt;
            font-weight: bold;
            color: #C0161C;
            text-transform: uppercase;
            margin: 1.5cm 0 0.8cm 0;
            padding-bottom: 0.3cm;
            border-bottom: 2px solid #C0161C;
            page-break-after: avoid;
        }
        
        h2 {
            font-family: 'Arial', sans-serif;
            font-size: 14pt;
            font-weight: bold;
            color: #C0161C;
            text-transform: uppercase;
            margin: 1.2cm 0 0.6cm 0;
            page-break-after: avoid;
        }
        
        h3 {
            font-family: 'Calibri', sans-serif;
            font-size: 12pt;
            font-weight: bold;
            color: #444;
            margin: 1cm 0 0.5cm 0;
            page-break-after: avoid;
        }
        
        p {
            margin: 0 0 0.6cm 0;
            text-align: justify;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            border: 2px solid #C0161C;
            margin: 0.8cm 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }
        
        table th {
            background-color: #C0161C;
            color: white;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            text-transform: uppercase;
            padding: 0.4cm;
            border: 1px solid #A0141A;
            text-align: center;
        }
        
        table td {
            padding: 0.3cm 0.4cm;
            border: 1px solid #ddd;
            vertical-align: top;
            line-height: 1.3;
        }
        
        table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        pre {
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-left: 4px solid #C0161C;
            padding: 0.8cm;
            margin: 0.8cm 0;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.3;
            overflow-x: auto;
            page-break-inside: avoid;
        }
        
        code {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background-color: #f1f1f1;
            padding: 0.1cm 0.2cm;
            border-radius: 2px;
        }
        
        blockquote {
            border-left: 4px solid #C0161C;
            margin: 0.8cm 0;
            padding: 0.5cm 0.8cm;
            background-color: #fafafa;
            font-style: italic;
            page-break-inside: avoid;
        }
        
        ul, ol {
            margin: 0.5cm 0;
            padding-left: 1.2cm;
        }
        
        li {
            margin-bottom: 0.3cm;
            line-height: 1.4;
        }
    </style>
    """
    
    # Complete HTML document
    html_document = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{process_name}</title>
        {css_styles}
    </head>
    <body>
        <div class="document-header">
            <h1 class="document-title">{process_name}</h1>
            <div class="document-subtitle">Business Logic Extractor - Análisis de Código Legacy</div>
        </div>
        
        <div class="document-content">
            {html_content}
        </div>
    </body>
    </html>
    """
    
    return html_document


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
    if 'report_format' not in st.session_state:
        st.session_state.report_format = None

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
    
    # Process name and format selection
    col_name, col_format = st.columns([2, 1])
    with col_name:
        process_name = st.text_input(
            "Nombre del Proceso (Opcional)",
            placeholder="Ej: Mantenimiento_VSAM, Proceso_Batch_Cuentas, etc.",
            help="Si no se especifica, se usará 'Business_Requirements' por defecto"
        )
    
    with col_format:
        st.markdown("#### 📄 Formato de Salida")
        output_format = st.selectbox(
            "Seleccionar formato",
            options=["markdown", "pdf"],
            format_func=lambda x: "📝 Markdown (.md)" if x == "markdown" else "📄 PDF (.pdf)",
            help="PDF incluye diagramas renderizados, tablas formateadas y diseño profesional ICBC"
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
    
    format_icon = "📄" if output_format == "pdf" else "📝"
    format_text = "PDF PROFESIONAL" if output_format == "pdf" else "MARKDOWN"
    
    analyze_button = st.button(
        f"🚀 ANALIZAR Y DESCARGAR {format_text}",
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
            analysis_result = run_analysis(final_process_name)
            
            # Step 5: Process the report based on format
            status_text.markdown("**Fase 5/5:** Procesando reporte...")
            progress_bar.progress(80)
            
            # Extract content from the JSON response
            markdown_content_es = analysis_result.get('markdown_report', '')
            markdown_content_en = analysis_result.get('markdown_report_en', '')
            result_process_name = analysis_result.get('process_name', final_process_name)
            
            if output_format == "pdf":
                # Generate PDF HTML for both languages
                html_content_es = markdown_to_pdf_html(markdown_content_es, result_process_name)
                html_content_en = markdown_to_pdf_html(markdown_content_en, result_process_name)
                
                # Store HTML for PDF generation via browser
                st.session_state.report_data_es = html_content_es
                st.session_state.report_data_en = html_content_en
                st.session_state.report_filename_es = f"{result_process_name}_ES.html"
                st.session_state.report_filename_en = f"{result_process_name}_EN.html"
                st.session_state.report_format = "pdf"
                st.session_state.markdown_content_es = markdown_content_es
                st.session_state.markdown_content_en = markdown_content_en
                st.session_state.process_name = result_process_name
            else:
                # Store markdown content for both languages
                st.session_state.report_data_es = markdown_content_es
                st.session_state.report_data_en = markdown_content_en
                st.session_state.report_filename_es = f"{result_process_name}_ES.md"
                st.session_state.report_filename_en = f"{result_process_name}_EN.md"
                st.session_state.report_format = "markdown"
                st.session_state.process_name = result_process_name
                
            st.session_state.analysis_complete = True
            
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            # Success message
            format_desc = "PDF profesional con diagramas renderizados y formato ICBC" if output_format == "pdf" else "archivo Markdown"
            st.markdown(f"""
            <div class="success-box">
                ✅ <strong>¡Análisis completado exitosamente!</strong><br>
                El {format_desc} está listo para descargar en ESPAÑOL e INGLÉS. Los archivos temporales han sido limpiados automáticamente.
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
            st.error("Por favor, verifique que el servidor backend esté ejecutándose en https://business-logic-extractor.onrender.com")

    # Download section
    if st.session_state.analysis_complete and st.session_state.get('report_data_es'):
        st.markdown("---")
        st.markdown('<h2 class="section-header">📥 Descargar Reporte</h2>', unsafe_allow_html=True)
        
        # Info box about bilingual reports
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title">🌐 Reportes Bilingües Disponibles</div>
            <p>El sistema ha generado automáticamente el reporte completo en <strong>español</strong> e <strong>inglés</strong>. 
            Ambas versiones contienen exactamente el mismo contenido y estructura, solo difieren en el idioma.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for Spanish and English downloads
        col_spanish, col_english = st.columns(2)
        
        with col_spanish:
            st.markdown("#### 🇪🇸 Versión en Español")
            if st.session_state.get('report_format') == 'pdf':
                # For PDF, provide HTML for browser-based PDF generation
                st.download_button(
                    label="📄 DESCARGAR HTML ESPAÑOL",
                    data=st.session_state.report_data_es,
                    file_name=st.session_state.report_filename_es,
                    mime="text/html",
                    use_container_width=True,
                    key="download_html_es"
                )
                
                # Also provide markdown option
                if 'markdown_content_es' in st.session_state:
                    st.download_button(
                        label="📝 MARKDOWN ESPAÑOL",
                        data=st.session_state.markdown_content_es,
                        file_name=f"{st.session_state.get('process_name', 'Business_Requirements')}_ES.md",
                        mime="text/markdown",
                        use_container_width=True,
                        key="download_md_es"
                    )
            else:
                st.download_button(
                    label="📝 DESCARGAR MARKDOWN ESPAÑOL",
                    data=st.session_state.report_data_es,
                    file_name=st.session_state.report_filename_es,
                    mime="text/markdown",
                    use_container_width=True,
                    key="download_md_only_es"
                )
        
        with col_english:
            st.markdown("#### 🇬🇧 English Version")
            if st.session_state.get('report_format') == 'pdf':
                # For PDF, provide HTML for browser-based PDF generation
                st.download_button(
                    label="📄 DOWNLOAD ENGLISH HTML",
                    data=st.session_state.report_data_en,
                    file_name=st.session_state.report_filename_en,
                    mime="text/html",
                    use_container_width=True,
                    key="download_html_en"
                )
                
                # Also provide markdown option
                if 'markdown_content_en' in st.session_state:
                    st.download_button(
                        label="📝 ENGLISH MARKDOWN",
                        data=st.session_state.markdown_content_en,
                        file_name=f"{st.session_state.get('process_name', 'Business_Requirements')}_EN.md",
                        mime="text/markdown",
                        use_container_width=True,
                        key="download_md_en"
                    )
            else:
                st.download_button(
                    label="📝 DOWNLOAD ENGLISH MARKDOWN",
                    data=st.session_state.report_data_en,
                    file_name=st.session_state.report_filename_en,
                    mime="text/markdown",
                    use_container_width=True,
                    key="download_md_only_en"
                )
        
        # Single info box below both columns
        st.markdown("---")
        if st.session_state.get('report_format') == 'pdf':
            st.info("""**📄 Instrucciones para generar PDF:**
            
1. Descarga el archivo HTML en el idioma deseado (Español o English)
2. Ábrelo en tu navegador web (Chrome, Edge, Firefox)
3. Presiona **Ctrl+P** (o Cmd+P en Mac) para abrir el diálogo de impresión
4. En "Destino" o "Destination", selecciona **"Guardar como PDF"**
5. Ajusta los márgenes si es necesario y haz clic en Guardar
6. ¡Listo! Tendrás tu reporte en formato PDF profesional con el diseño ICBC

**Nota:** También puedes descargar la versión Markdown si prefieres editar o procesar el contenido.""")
        else:
            st.info("""**📝 Formato Markdown:**
            
Los reportes están disponibles en formato Markdown (.md) en ambos idiomas.
Puedes abrirlos con cualquier editor de texto o visualizador de Markdown.

**Uso recomendado:** Importar en herramientas de documentación, wikis, o editores como VSCode, Obsidian, Notion.""")
        
        # Reset button
        if st.button("🔄 Realizar Nuevo Análisis", use_container_width=True):
            st.session_state.analysis_complete = False
            st.session_state.report_data_es = None
            st.session_state.report_data_en = None
            st.session_state.report_filename_es = None
            st.session_state.report_filename_en = None
            st.session_state.report_format = None
            st.session_state.markdown_content_es = None
            st.session_state.markdown_content_en = None
            st.session_state.process_name = None
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
