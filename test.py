# COMMAND ----------

# DASHBOARD RESULTS VIEWER - Import this cell to dashboard
import time

selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

# Create a simple status check
if selected_mitre and selected_mitre != "":
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        print("="*80)
        print(f"📋 TECHNIQUE: {selected_mitre}")
        print("="*80)
        print(f"Name: {technique_data['technique_name']}")
        print(f"Tactic: {technique_data['tactics']}")
        print(f"Platform: {technique_data['platforms']}")
        print("="*80)
        print("🔍 SPL QUERY:")
        print("="*80)
        print(technique_data['spl_query'])
        print("="*80)
        
        # Show analysis results if analyze was clicked
        if analysis_action == "Analyze":
            print("\n🤖 STARTING LLM ANALYSIS...")
            print("="*80)
            
            analysis_result = analyze_technique_with_llm(selected_mitre)
            
            print("\n🎯 LLM ANALYSIS RESULTS:")
            print("="*100)
            print(analysis_result)
            print("="*100)
            print(f"\n✅ Analysis completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
        else:
            print("\n🚀 Ready for analysis!")
            print("Set Analysis Action to 'Analyze' to run LLM analysis")
            
    else:
        print("❌ No data found for selected technique")
else:
    print("👆 Please select a MITRE technique from the dropdown")
