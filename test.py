# COMMAND ----------

# DASHBOARD HTML CARDS SOLUTION
import time
import datetime

selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

current_time = datetime.datetime.now().strftime('%H:%M:%S')

if selected_mitre and selected_mitre != "":
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        # Technique Information Card
        displayHTML(f"""
        <div style="border: 2px solid #007bff; border-radius: 10px; padding: 20px; margin: 10px; background: white;">
            <h2 style="color: #007bff; margin-bottom: 15px;">📋 Technique Information</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold;">ID:</td>
                    <td style="padding: 8px;">{selected_mitre}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold;">Name:</td>
                    <td style="padding: 8px;">{technique_data['technique_name']}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold;">Tactic:</td>
                    <td style="padding: 8px;">{technique_data['tactics']}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px; font-weight: bold;">Platform:</td>
                    <td style="padding: 8px;">{technique_data['platforms']}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Status:</td>
                    <td style="padding: 8px; color: #28a745;">{analysis_action} - {current_time}</td>
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
        </div>
        """)
        
        # Analysis Results Card
        if analysis_action == "Analyze":
            
            # Show processing card
            displayHTML(f"""
            <div style="border: 2px solid #ffc107; border-radius: 10px; padding: 20px; margin: 10px; background: #fff3cd;">
                <h2 style="color: #856404; margin-bottom: 15px;">🤖 Processing Analysis</h2>
                <p style="margin: 0;">Running LLM analysis for {selected_mitre}...</p>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Started: {current_time}</p>
            </div>
            """)
            
            # Run analysis
            analysis_result = analyze_technique_with_llm(selected_mitre)
            completion_time = datetime.datetime.now().strftime('%H:%M:%S')
            
            # Show results card
            displayHTML(f"""
            <div style="border: 2px solid #dc3545; border-radius: 10px; padding: 20px; margin: 10px; background: white;">
                <h2 style="color: #dc3545; margin-bottom: 15px;">🎯 Analysis Results</h2>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; max-height: 400px; overflow-y: auto;">
                    <pre style="margin: 0; font-family: Arial, sans-serif; font-size: 13px; line-height: 1.5; white-space: pre-wrap;">{analysis_result}</pre>
                </div>
                <div style="margin-top: 15px; padding: 10px; background: #d4edda; border-radius: 5px;">
                    <strong>✅ Completed at: {completion_time}</strong>
                </div>
            </div>
            """)
            
            # Reset widget
            dbutils.widgets.remove("analyze_action")
            dbutils.widgets.dropdown("analyze_action", "Ready", 
                                     ["Ready", "Analyze", "Clear"], 
                                     "🚀 Analysis Action")
                                     
        elif analysis_action == "Ready":
            displayHTML(f"""
            <div style="border: 2px solid #17a2b8; border-radius: 10px; padding: 20px; margin: 10px; background: #d1ecf1;">
                <h2 style="color: #0c5460; margin-bottom: 15px;">🚀 Ready for Analysis</h2>
                <p style="margin: 0;">Set Analysis Action to 'Analyze' to start LLM analysis of {selected_mitre}</p>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Last updated: {current_time}</p>
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
        <h2 style="color: #383d41; margin-bottom: 15px;">👆 Select Technique</h2>
        <p style="margin: 0;">Please select a MITRE technique from the dropdown above</p>
        <p style="margin: 5px 0 0 0; font-size: 14px;">Time: {current_time}</p>
    </div>
    """)
