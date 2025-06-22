# COMMAND ----------

# CELL 1: Technique Display (Always Shows Current Selection)
import datetime

selected_mitre = dbutils.widgets.get("mitre_technique")
current_time = datetime.datetime.now().strftime('%H:%M:%S')

if selected_mitre and selected_mitre != "":
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        # Technique Information Card
        displayHTML(f"""
        <div style="border: 2px solid #007bff; border-radius: 10px; padding: 20px; margin: 10px; background: white;">
            <h2 style="color: #007bff; margin-bottom: 15px;">📋 {selected_mitre}: {technique_data['technique_name']}</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold; width: 150px;">Tactic:</td>
                    <td style="padding: 8px;">{technique_data['tactics']}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold;">Platform:</td>
                    <td style="padding: 8px;">{technique_data['platforms']}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold;">Domain:</td>
                    <td style="padding: 8px;">{technique_data['domain']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Last Updated:</td>
                    <td style="padding: 8px; color: #28a745;">{current_time}</td>
                </tr>
            </table>
        </div>
        """)
        
        # SPL Query Card
        displayHTML(f"""
        <div style="border: 2px solid #28a745; border-radius: 10px; padding: 20px; margin: 10px; background: white;">
            <h2 style="color: #28a745; margin-bottom: 15px;">🔍 SPL Query</h2>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">
                <pre style="margin: 0; font-family: monospace; font-size: 12px; line-height: 1.4;">{technique_data['spl_query']}</pre>
            </div>
            <div style="margin-top: 10px; padding: 10px; background: #d1ecf1; border-radius: 5px;">
                <strong>📏 Query Length:</strong> {len(technique_data['spl_query'])} characters
            </div>
        </div>
        """)
        
        # Ready for Analysis Card
        displayHTML(f"""
        <div style="border: 2px solid #17a2b8; border-radius: 10px; padding: 20px; margin: 10px; background: #d1ecf1;">
            <h2 style="color: #0c5460; margin-bottom: 15px;">🚀 Ready for Analysis</h2>
            <p style="margin: 0; font-size: 16px;">To run LLM analysis:</p>
            <ol style="margin: 10px 0; padding-left: 20px;">
                <li>Set Analysis Action to "Analyze"</li>
                <li>Run the "Analysis Runner" cell below</li>
            </ol>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #6c757d;">Current time: {current_time}</p>
        </div>
        """)
        
    else:
        displayHTML("""
        <div style="border: 2px solid #dc3545; border-radius: 10px; padding: 20px; margin: 10px; background: #f8d7da;">
            <h2 style="color: #721c24;">❌ Error</h2>
            <p style="margin: 0;">No data found for selected technique</p>
        </div>
        """)
        
else:
    displayHTML(f"""
    <div style="border: 2px solid #6c757d; border-radius: 10px; padding: 20px; margin: 10px; background: #e2e3e5;">
        <h2 style="color: #383d41; margin-bottom: 15px;">👆 Select MITRE Technique</h2>
        <p style="margin: 0;">Please select a MITRE technique from the dropdown above to view details</p>
        <p style="margin: 5px 0 0 0; font-size: 14px;">Time: {current_time}</p>
    </div>
    """)







# COMMAND ----------

# CELL 2: Analysis Runner (Run this cell manually to analyze)
import datetime
import uuid

# Generate unique execution ID
execution_id = str(uuid.uuid4())[:8]
start_time = datetime.datetime.now()

selected_mitre = dbutils.widgets.get("mitre_technique")

# Always show execution info
displayHTML(f"""
<div style="border: 2px solid #ffc107; border-radius: 10px; padding: 15px; margin: 10px; background: #fff3cd;">
    <h3 style="color: #856404; margin: 0;">🤖 Analysis Execution</h3>
    <p style="margin: 5px 0;"><strong>Execution ID:</strong> {execution_id}</p>
    <p style="margin: 5px 0;"><strong>Started:</strong> {start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p style="margin: 5px 0;"><strong>Technique:</strong> {selected_mitre if selected_mitre else 'None selected'}</p>
</div>
""")

if selected_mitre and selected_mitre != "":
    
    # Show analysis in progress
    displayHTML(f"""
    <div style="border: 2px solid #007bff; border-radius: 10px; padding: 20px; margin: 10px; background: #cce5ff;">
        <h2 style="color: #004085; margin-bottom: 15px;">🔄 Running Analysis for {selected_mitre}</h2>
        <p style="margin: 0;">Please wait while the LLM analyzes the SPL query...</p>
        <div style="margin: 15px 0; padding: 10px; background: white; border-radius: 5px;">
            <small>Execution ID: {execution_id} | Started: {start_time.strftime('%H:%M:%S')}</small>
        </div>
    </div>
    """)
    
    # Run the analysis
    analysis_result = analyze_technique_with_llm(selected_mitre)
    
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Show results
    displayHTML(f"""
    <div style="border: 2px solid #dc3545; border-radius: 10px; padding: 20px; margin: 10px; background: white;">
        <h2 style="color: #dc3545; margin-bottom: 15px;">🎯 Analysis Results</h2>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; max-height: 500px; overflow-y: auto;">
            <pre style="margin: 0; font-family: Arial, sans-serif; font-size: 13px; line-height: 1.5; white-space: pre-wrap;">{analysis_result}</pre>
        </div>
        <div style="margin-top: 15px; padding: 15px; background: #d4edda; border-radius: 5px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <strong>✅ Status:</strong> Complete<br>
                    <strong>🎯 Technique:</strong> {selected_mitre}
                </div>
                <div>
                    <strong>⏰ Duration:</strong> {duration:.1f} seconds<br>
                    <strong>🔗 Execution ID:</strong> {execution_id}
                </div>
            </div>
        </div>
    </div>
    """)
    
else:
    displayHTML("""
    <div style="border: 2px solid #dc3545; border-radius: 10px; padding: 20px; margin: 10px; background: #f8d7da;">
        <h2 style="color: #721c24;">❌ Cannot Run Analysis</h2>
        <p style="margin: 0;">Please select a MITRE technique first, then run this cell again.</p>
    </div>
    """)
