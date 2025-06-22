# COMMAND ----------

# WIDGET-AWARE AUTO-UPDATE SOLUTION
import time
import uuid

# Force widget value refresh
try:
    dbutils.widgets.get("mitre_technique")
    dbutils.widgets.get("analyze_action")
except:
    # Recreate widgets if they don't exist
    dbutils.widgets.dropdown("mitre_technique", "", 
                             [""] + mitre_id_list, 
                             "🎯 Select MITRE Technique")
    dbutils.widgets.dropdown("analyze_action", "Ready", 
                             ["Ready", "Analyze", "Clear"], 
                             "🚀 Analysis Action")
    dbutils.widgets.text("custom_spl", "", 
                         "📝 Custom SPL Query (Optional)")

# Get current widget values
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

print(f"🔄 Current State - Technique: {selected_mitre}, Action: {analysis_action}")

# Always show current status first
if selected_mitre and selected_mitre != "":
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        # Always display technique info
        displayHTML(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 2px solid #dee2e6; border-radius: 10px; padding: 20px; margin: 10px 0;">
            <h2 style="color: #2c3e50; margin-bottom: 15px;">📋 {selected_mitre}: {technique_data['technique_name']}</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
                <div style="background: white; padding: 12px; border-radius: 5px; border-left: 3px solid #3498db;">
                    <strong style="color: #2c3e50;">Tactic:</strong><br>
                    <span style="color: #34495e;">{technique_data['tactics']}</span>
                </div>
                <div style="background: white; padding: 12px; border-radius: 5px; border-left: 3px solid #e74c3c;">
                    <strong style="color: #2c3e50;">Platform:</strong><br>
                    <span style="color: #34495e;">{technique_data['platforms']}</span>
                </div>
            </div>
            
            <div style="background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <strong style="color: #3498db;">🔍 SPL Query:</strong><br>
                <pre style="margin-top: 10px; font-size: 13px; line-height: 1.4; overflow-x: auto; background: #34495e; padding: 10px; border-radius: 3px;">{technique_data['spl_query']}</pre>
            </div>
        </div>
        """)
        
        # Handle different actions
        if analysis_action == "Analyze":
            
            execution_id = str(uuid.uuid4())[:8]
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Show analysis starting
            displayHTML(f"""
            <div style="background: #3498db; color: white; padding: 15px; border-radius: 8px; text-align: center; margin: 10px 0;">
                <h3>🤖 Running Analysis for {selected_mitre}</h3>
                <p>Started at: {timestamp}</p>
                <p>Execution ID: {execution_id}</p>
            </div>
            """)
            
            print(f"🔍 Starting LLM analysis for {selected_mitre}...")
            
            # Run analysis
            analysis_result = analyze_technique_with_llm(selected_mitre)
            
            completion_time = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Display results
            displayHTML(f"""
            <div style="background: #ffffff; border: 2px solid #28a745; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h2 style="color: #28a745; margin-bottom: 15px;">
                    🎯 Analysis Results - {completion_time}
                </h2>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745;">
                    <pre style="white-space: pre-wrap; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.5; margin: 0; font-size: 14px;">{analysis_result}</pre>
                </div>
                <div style="margin-top: 15px; padding: 10px; background: #d4edda; border-radius: 5px; text-align: center;">
                    <strong>✅ Analysis completed successfully!</strong><br>
                    <small>Execution ID: {execution_id}</small>
                </div>
            </div>
            """)
            
            print(f"✅ Analysis completed for {selected_mitre}")
            print("🔄 Resetting action to 'Ready'...")
            
            # Force reset the widget
            time.sleep(1)  # Brief delay
            dbutils.widgets.remove("analyze_action")
            dbutils.widgets.dropdown("analyze_action", "Ready", 
                                     ["Ready", "Analyze", "Clear"], 
                                     "🚀 Analysis Action")
            
        elif analysis_action == "Ready":
            displayHTML("""
            <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 15px; border-radius: 8px; text-align: center; margin: 10px 0;">
                <h3>🚀 Ready for Analysis!</h3>
                <p>Set Analysis Action to 'Analyze' to start LLM analysis</p>
            </div>
            """)
            
        elif analysis_action == "Clear":
            print("🧹 Clearing dashboard...")
            
            # Clear everything
            dbutils.widgets.removeAll()
            
            # Recreate fresh widgets
            dbutils.widgets.dropdown("mitre_technique", "", 
                                     [""] + mitre_id_list, 
                                     "🎯 Select MITRE Technique")
            dbutils.widgets.dropdown("analyze_action", "Ready", 
                                     ["Ready", "Analyze", "Clear"], 
                                     "🚀 Analysis Action")
            dbutils.widgets.text("custom_spl", "", 
                                 "📝 Custom SPL Query (Optional)")
            
            displayHTML("""
            <div style="background: #ffc107; color: #212529; padding: 15px; border-radius: 8px; text-align: center;">
                <h3>✅ Dashboard Cleared!</h3>
                <p>Select a new MITRE technique to start fresh.</p>
            </div>
            """)
    
    else:
        print(f"❌ No data found for technique: {selected_mitre}")

else:
    # No technique selected
    displayHTML("""
    <div style="background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 20px; border-radius: 8px; text-align: center;">
        <h3>👆 Please select a MITRE technique from the dropdown above</h3>
        <p>Choose a technique to view its details and run SPL analysis.</p>
    </div>
    """)

print(f"🔄 Cell execution completed at {time.strftime('%H:%M:%S')}")
