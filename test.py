# COMMAND ----------

# BUTTON-BASED ANALYSIS TRIGGER
import time

# Create a run counter widget
try:
    current_count = int(dbutils.widgets.get("run_counter"))
except:
    current_count = 0

# Increment counter
new_count = current_count + 1

# Remove and recreate the counter widget to force update
try:
    dbutils.widgets.remove("run_counter")
except:
    pass

dbutils.widgets.text("run_counter", str(new_count), "🔄 Run Counter (click to analyze)")

# Get other widgets
selected_mitre = dbutils.widgets.get("mitre_technique")

print(f"🔄 RUN #{new_count} - {time.strftime('%H:%M:%S')}")
print(f"🎯 Selected Technique: {selected_mitre}")

if selected_mitre and selected_mitre != "":
    
    print(f"\n🤖 RUNNING ANALYSIS #{new_count} FOR: {selected_mitre}")
    print("="*80)
    
    # Run analysis
    analysis_result = analyze_technique_with_llm(selected_mitre)
    
    print(f"\n🎯 ANALYSIS RESULTS (Run #{new_count}):")
    print("="*100)
    print(analysis_result)
    print("="*100)
    print(f"✅ Analysis #{new_count} completed at {time.strftime('%H:%M:%S')}")
    
else:
    print("👆 Select a MITRE technique first, then update the Run Counter to analyze")
