# COMMAND ----------

# CELL 1: Status and Info Display
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

print(f"Current selection: {selected_mitre}")
print(f"Current action: {analysis_action}")

if selected_mitre and selected_mitre != "":
    technique_data = get_technique_data(selected_mitre)
    if technique_data:
        print(f"📋 Ready to analyze: {technique_data['technique_name']}")
        print("SPL Query loaded successfully")
    else:
        print("❌ No data found")
else:
    print("👆 Select a MITRE technique")




# COMMAND ----------

# CELL 2: Analysis Executor
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

if analysis_action == "Analyze" and selected_mitre:
    print(f"🤖 ANALYZING: {selected_mitre}")
    print("="*60)
    
    analysis_result = analyze_technique_with_llm(selected_mitre)
    
    print("🎯 RESULTS:")
    print("="*60)
    print(analysis_result)
    print("="*60)
    print("✅ Analysis complete!")
    
    # Reset action
    dbutils.widgets.remove("analyze_action")
    dbutils.widgets.dropdown("analyze_action", "Ready", 
                             ["Ready", "Analyze", "Clear"], 
                             "🚀 Analysis Action")
else:
    print("Set action to 'Analyze' to run analysis")
