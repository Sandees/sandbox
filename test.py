# COMMAND ----------

# RELIABLE ANALYSIS SOLUTION - Always Runs
import time
import datetime

# Force get widget values every time
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

# Always print current state for debugging
print(f"🔄 Execution Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
print(f"📊 Technique: {selected_mitre}")
print(f"⚡ Action: {analysis_action}")
print("="*60)

# ALWAYS show technique info if selected
if selected_mitre and selected_mitre != "":
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        print(f"📋 TECHNIQUE INFORMATION:")
        print(f"ID: {selected_mitre}")
        print(f"Name: {technique_data['technique_name']}")
        print(f"Tactic: {technique_data['tactics']}")
        print(f"Platform: {technique_data['platforms']}")
        print("="*60)
        print("🔍 SPL QUERY:")
        print("="*60)
        print(technique_data['spl_query'])
        print("="*60)
        
        # Check if we should run analysis
        if analysis_action == "Analyze":
            print("\n🤖 RUNNING LLM ANALYSIS...")
            print("="*80)
            
            # Run the analysis
            analysis_result = analyze_technique_with_llm(selected_mitre)
            
            print("\n🎯 LLM ANALYSIS RESULTS:")
            print("="*80)
            print(analysis_result)
            print("="*80)
            print(f"✅ Analysis completed at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Create a completion display
            displayHTML(f"""
            <div style="background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;">
                <h2>✅ Analysis Complete!</h2>
                <p><strong>Technique:</strong> {selected_mitre}</p>
                <p><strong>Time:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><em>Scroll up to see full results</em></p>
            </div>
            """)
            
        elif analysis_action == "Ready":
            print("\n🚀 READY FOR ANALYSIS")
            print("Set Analysis Action to 'Analyze' to start LLM analysis")
            
        elif analysis_action == "Clear":
            print("\n🧹 CLEARING DASHBOARD...")
            # Don't actually clear here, just show message
            
    else:
        print("❌ No data found for selected technique")
        
else:
    print("👆 Please select a MITRE technique from the dropdown")

print(f"\n🔄 Cell completed at: {datetime.datetime.now().strftime('%H:%M:%S')}")
