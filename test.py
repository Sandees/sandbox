# COMMAND ----------

# AUTO-UPDATE SOLUTION WITHOUT JAVASCRIPT
import time
import uuid

selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

# Generate unique ID for this execution
execution_id = str(uuid.uuid4())[:8]

if analysis_action == "Analyze" and selected_mitre:
    
    # Show immediate feedback
    displayHTML(f"""
    <div style="background: #3498db; color: white; padding: 15px; border-radius: 8px; text-align: center;">
        <h3>🤖 Starting Analysis for {selected_mitre}</h3>
        <p>Execution ID: {execution_id}</p>
    </div>
    """)
    
    # Run analysis
    analysis_result = analyze_technique_with_llm(selected_mitre)
    
    # Display results with unique timestamp
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    displayHTML(f"""
    <div style="background: #ffffff; border: 2px solid #28a745; border-radius: 10px; padding: 20px; margin: 15px 0;">
        <h2 style="color: #28a745; margin-bottom: 15px;">
            🎯 Analysis Results - {timestamp}
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
    
    # Auto-reset widget to Ready state
    dbutils.widgets.remove("analyze_action")
    dbutils.widgets.dropdown("analyze_action", "Ready", 
                             ["Ready", "Analyze", "Clear"], 
                             "🚀 Analysis Action")
    
    print(f"✅ Analysis completed for {selected_mitre} at {timestamp}")

elif selected_mitre and selected_mitre != "":
    # Show technique information
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
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
            
            <div style="background: white; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <strong style="color: #2c3e50;">Description:</strong><br>
                <span style="color: #34495e; line-height: 1.5;">{technique_data['description']}</span>
            </div>
            
            <div style="background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <strong style="color: #3498db;">🔍 SPL Query:</strong><br>
                <pre style="margin-top: 10px; font-size: 13px; line-height: 1.4; overflow-x: auto; background: #34495e; padding: 10px; border-radius: 3px;">{technique_data['spl_query']}</pre>
            </div>
        </div>
        """)
        
        # Show ready status
        if analysis_action == "Ready":
            displayHTML("""
            <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 15px; border-radius: 8px; text-align: center; margin: 10px 0;">
                <h3>🚀 Ready for Analysis!</h3>
                <p>Set Analysis Action to 'Analyze' to start LLM analysis</p>
            </div>
            """)
        elif analysis_action == "Clear":
            # Handle clear action
            displayHTML("""
            <div style="background: #ffc107; color: #212529; padding: 15px; border-radius: 8px; text-align: center;">
                <h3>🧹 Clearing Dashboard...</h3>
            </div>
            """)
            
            # Reset all widgets
            dbutils.widgets.removeAll()
            dbutils.widgets.dropdown("mitre_technique", "", 
                                     [""] + mitre_id_list, 
                                     "🎯 Select MITRE Technique")
            dbutils.widgets.dropdown("analyze_action", "Ready", 
                                     ["Ready", "Analyze", "Clear"], 
                                     "🚀 Analysis Action")
            dbutils.widgets.text("custom_spl", "", 
                                 "📝 Custom SPL Query (Optional)")

else:
    # No technique selected
    displayHTML("""
    <div style="background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 20px; border-radius: 8px; text-align: center;">
        <h3>👆 Please select a MITRE technique from the dropdown above</h3>
        <p>Choose a technique to view its details and run SPL analysis.</p>
    </div>
    """)
