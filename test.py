# COMMAND ----------

# AUTO-REFRESH DASHBOARD SOLUTION
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

if analysis_action == "Analyze" and selected_mitre:
    
    # Run analysis
    print(f"🤖 Analyzing {selected_mitre}...")
    analysis_result = analyze_technique_with_llm(selected_mitre)
    
    # Display results with auto-refresh trigger
    displayHTML(f"""
    <div id="analysis-results-{int(time.time())}" style="background: #f8f9fa; border: 2px solid #28a745; border-radius: 10px; padding: 20px; margin: 15px 0;">
        <h2 style="color: #28a745;">🎯 LLM Analysis Results</h2>
        <div style="background: white; padding: 15px; border-radius: 5px;">
            <pre style="white-space: pre-wrap; font-family: monospace; line-height: 1.4;">{analysis_result}</pre>
        </div>
        <div style="margin-top: 15px; padding: 10px; background: #d4edda; border-radius: 5px;">
            <strong>✅ Analysis completed:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    
    <script>
    // Auto-refresh dashboard after analysis
    setTimeout(function() {{
        if (parent.location) {{
            parent.location.reload();
        }} else {{
            location.reload();
        }}
    }}, 2000);
    </script>
    """)
    
    # Reset widget to Ready
    dbutils.widgets.remove("analyze_action")
    dbutils.widgets.dropdown("analyze_action", "Ready", 
                             ["Ready", "Analyze", "Clear"], 
                             "🚀 Analysis Action")

else:
    # Show current status
    if selected_mitre:
        technique_data = get_technique_data(selected_mitre)
        if technique_data:
            displayHTML(f"""
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px;">
                <h3>📋 Ready: {selected_mitre}</h3>
                <p><strong>Name:</strong> {technique_data['technique_name']}</p>
                <p><strong>Status:</strong> Set action to 'Analyze' to start</p>
            </div>
            """)
