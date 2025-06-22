# COMMAND ----------

# REACTIVE DASHBOARD SOLUTION
import time
import hashlib

# Get widget values
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

# Create unique state ID for cache busting
state_id = hashlib.md5(f"{selected_mitre}_{analysis_action}_{int(time.time())}".encode()).hexdigest()[:8]

if selected_mitre and selected_mitre != "":
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        # Always show technique info
        displayHTML(f"""
        <div id="technique-info-{state_id}" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 2px solid #dee2e6; border-radius: 10px; padding: 20px; margin: 10px 0;">
            <h2 style="color: #2c3e50;">📋 {selected_mitre}: {technique_data['technique_name']}</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
                <div style="background: white; padding: 10px; border-radius: 5px;">
                    <strong>Tactic:</strong> {technique_data['tactics']}
                </div>
                <div style="background: white; padding: 10px; border-radius: 5px;">
                    <strong>Platform:</strong> {technique_data['platforms']}
                </div>
            </div>
            
            <div style="background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <strong>🔍 SPL Query:</strong><br>
                <pre style="margin-top: 10px; font-size: 0.9em; line-height: 1.3; overflow-x: auto;">{technique_data['spl_query']}</pre>
            </div>
        </div>
        """)
        
        # Handle analysis
        if analysis_action == "Analyze":
            # Show loading with auto-refresh
            displayHTML(f"""
            <div id="analysis-{state_id}" style="background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
                <h3>🤖 Running Analysis...</h3>
                <div style="width: 30px; height: 30px; border: 3px solid rgba(255,255,255,0.3); border-top: 3px solid white; border-radius: 50%; animation: spin 1s linear infinite; margin: 10px auto;"></div>
            </div>
            <style>
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            </style>
            <script>
            setTimeout(function() {{
                document.getElementById('analysis-{state_id}').innerHTML = '<h3>🔄 Processing...</h3>';
            }}, 1000);
            </script>
            """)
            
            # Run analysis
            analysis_result = analyze_technique_with_llm(selected_mitre)
            
            # Show results with timestamp for uniqueness
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            displayHTML(f"""
            <div id="results-{state_id}" style="background: #ffffff; border: 2px solid #28a745; border-radius: 10px; padding: 20px; margin: 10px 0;">
                <h2 style="color: #28a745; margin-bottom: 15px;">🎯 Analysis Results - {current_time}</h2>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745;">
                    <pre style="white-space: pre-wrap; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.5; margin: 0;">{analysis_result}</pre>
                </div>
                <div style="margin-top: 15px; padding: 10px; background: #d4edda; border-radius: 5px; text-align: center;">
                    <strong>✅ Analysis completed successfully!</strong>
                </div>
            </div>
            """)
            
            # Auto-reset to Ready
            dbutils.widgets.remove("analyze_action")
            dbutils.widgets.dropdown("analyze_action", "Ready", 
                                     ["Ready", "Analyze", "Clear"], 
                                     "🚀 Analysis Action")
                                     
        elif analysis_action == "Ready":
            displayHTML(f"""
            <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 15px; border-radius: 8px; text-align: center; margin: 10px 0;">
                <h3>🚀 Ready for Analysis!</h3>
                <p>Set Analysis Action to 'Analyze' to start LLM analysis</p>
            </div>
            """)
            
        elif analysis_action == "Clear":
            # Clear all selections
            dbutils.widgets.removeAll()
            # Recreate widgets
            dbutils.widgets.dropdown("mitre_technique", "", 
                                     [""] + mitre_id_list, 
                                     "🎯 Select MITRE Technique")
            dbutils.widgets.dropdown("analyze_action", "Ready", 
                                     ["Ready", "Analyze", "Clear"], 
                                     "🚀 Analysis Action")
            dbutils.widgets.text("custom_spl", "", 
                                 "📝 Custom SPL Query (Optional)")
            
            displayHTML("""
            <div style="background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; text-align: center;">
                ✅ Dashboard cleared! Select a new MITRE technique to start fresh.
            </div>
            """)

else:
    displayHTML("""
    <div style="background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 20px; border-radius: 8px; text-align: center;">
        <h3>👆 Please select a MITRE technique from the dropdown above</h3>
        <p>Choose a technique to view its details and run SPL analysis.</p>
    </div>
    """)
