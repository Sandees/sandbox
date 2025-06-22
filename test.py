# COMMAND ----------

# Dashboard-Optimized Analysis Display
import datetime

selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

if analysis_action == "Analyze" and selected_mitre:
    
    # Clear previous results
    print("Starting fresh analysis...")
    
    # Get technique info
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        
        # Display technique summary for dashboard
        displayHTML(f"""
        <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h3>📋 Analyzing: {selected_mitre}</h3>
            <p><strong>Name:</strong> {technique_data['technique_name']}</p>
            <p><strong>Status:</strong> 🤖 Running LLM Analysis...</p>
        </div>
        """)
        
        # Run analysis
        analysis_result = analyze_technique_with_llm(selected_mitre)
        
        # Display results in dashboard-friendly format
        displayHTML(f"""
        <div style="background: #f8f9fa; border: 2px solid #28a745; border-radius: 10px; padding: 20px; margin: 15px 0;">
            <h2 style="color: #28a745; margin-bottom: 15px;">🎯 LLM Analysis Results</h2>
            <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745;">
                <pre style="white-space: pre-wrap; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.5;">{analysis_result}</pre>
            </div>
            <div style="margin-top: 15px; padding: 10px; background: #d4edda; border-radius: 5px;">
                <strong>✅ Analysis completed at:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </div>
        </div>
        """)
        
        # Reset action to Ready
        dbutils.widgets.remove("analyze_action")
        dbutils.widgets.dropdown("analyze_action", "Ready", 
                                 ["Ready", "Analyze", "Clear"], 
                                 "🚀 Analysis Action")
        
    else:
        print("❌ No data found for selected technique")

else:
    if analysis_action == "Clear":
        print("🧹 Dashboard cleared")
    elif selected_mitre:
        print(f"🚀 Ready to analyze: {selected_mitre}")
    else:
        print("👆 Select technique and set action to 'Analyze'")
