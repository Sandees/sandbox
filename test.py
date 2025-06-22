# COMMAND ----------

# AUTO-POLLING DASHBOARD (run this cell every 30 seconds)
import datetime

selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

print(f"🔄 Dashboard refresh: {datetime.datetime.now().strftime('%H:%M:%S')}")

if selected_mitre and analysis_action == "Analyze":
    print(f"🤖 AUTO-ANALYZING: {selected_mitre}")
    
    analysis_result = analyze_technique_with_llm(selected_mitre)
    
    print("🎯 RESULTS:")
    print("="*80)
    print(analysis_result)
    print("="*80)
    
    # Auto-reset
    dbutils.widgets.remove("analyze_action")
    dbutils.widgets.dropdown("analyze_action", "Ready", 
                             ["Ready", "Analyze", "Clear"], 
                             "🚀 Analysis Action")

elif selected_mitre:
    technique_data = get_technique_data(selected_mitre)
    if technique_data:
        print(f"📋 READY: {selected_mitre} - {technique_data['technique_name']}")
        print("Set action to 'Analyze' to run analysis")
