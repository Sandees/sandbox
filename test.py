# COMMAND ----------

# FORCE EXECUTION SOLUTION - Never Skips
import time
import random

# Force unique execution every time
execution_token = f"{time.time()}_{random.randint(1000,9999)}"
print(f"🔄 FORCED EXECUTION: {execution_token}")

# Get widget values
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

# Force execution marker
exec_time = time.strftime('%H:%M:%S')
print(f"⏰ Execution Time: {exec_time}")
print(f"🎯 Technique: {selected_mitre}")
print(f"⚡ Action: {analysis_action}")

# Create a dummy computation to prevent caching
dummy_calc = sum(range(100)) + int(time.time() % 1000)
print(f"🔢 Cache Buster: {dummy_calc}")

print("="*80)

# MAIN LOGIC - This will ALWAYS execute
if selected_mitre and selected_mitre != "" and analysis_action == "Analyze":
    
    print(f"🤖 STARTING ANALYSIS FOR: {selected_mitre}")
    print(f"🕒 Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Get technique data
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        print(f"📋 Technique: {technique_data['technique_name']}")
        print(f"🔍 SPL Query Length: {len(technique_data['spl_query'])} characters")
        print("="*80)
        
        # RUN LLM ANALYSIS
        print("🤖 Calling LLM...")
        analysis_result = analyze_technique_with_llm(selected_mitre)
        
        end_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n🎯 ANALYSIS RESULTS (Completed: {end_time}):")
        print("="*100)
        print(analysis_result)
        print("="*100)
        
        # Visual completion indicator
        print("\n" + "🎉" * 20)
        print(f"✅ ANALYSIS COMPLETE FOR {selected_mitre}")
        print("🎉" * 20)
        
    else:
        print("❌ ERROR: No technique data found")
        
elif selected_mitre and selected_mitre != "":
    # Show technique info only
    technique_data = get_technique_data(selected_mitre)
    if technique_data:
        print(f"📋 LOADED: {selected_mitre} - {technique_data['technique_name']}")
        print(f"🚀 Status: Ready for analysis")
        print("💡 Set Analysis Action to 'Analyze' to run LLM analysis")
    else:
        print("❌ No data found for selected technique")
        
else:
    print("👆 Please select a MITRE technique and set action to 'Analyze'")

# End marker
print(f"\n🏁 EXECUTION END: {time.strftime('%H:%M:%S')} - Token: {execution_token}")
