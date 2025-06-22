# COMMAND ----------

# MAGIC %md
# MAGIC ## Dashboard Display Components

# COMMAND ----------

# Get current widget values
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")
custom_spl = dbutils.widgets.get("custom_spl")

# Only show content if a technique is selected
if selected_mitre and selected_mitre != "":
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        # Display technique information
        print("=" * 80)
        print(f"📋 TECHNIQUE INFORMATION: {selected_mitre}")
        print("=" * 80)
        print(f"Name: {technique_data['technique_name']}")
        print(f"Tactic: {technique_data['tactics']}")
        print(f"Platform: {technique_data['platforms']}")
        print(f"Domain: {technique_data['domain']}")
        print(f"Description: {technique_data['description']}")
        
        # Display SPL Query in a formatted way
        print("\n" + "=" * 80)
        print("🔍 SPL QUERY")
        print("=" * 80)
        print(technique_data['spl_query'])
        
        # Display drill-down SPL if available
        if technique_data.get('drill_down_spl'):
            print("\n" + "=" * 80)
            print("🔬 DRILL-DOWN SPL QUERY")
            print("=" * 80)
            print(technique_data['drill_down_spl'])
        
        # Display detection notes if available
        if technique_data.get('detection'):
            print("\n" + "=" * 80)
            print("📝 DETECTION NOTES")
            print("=" * 80)
            print(technique_data['detection'])
            
    else:
        print("❌ No data found for the selected MITRE technique.")
else:
    print("👆 Please select a MITRE technique from the dropdown above to view its details.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## LLM Analysis Results

# COMMAND ----------

# Handle LLM analysis when action is set to "Analyze"
if analysis_action == "Analyze" and selected_mitre and selected_mitre != "":
    
    print("🤖 STARTING LLM ANALYSIS...")
    print("=" * 80)
    print(f"Analyzing MITRE technique: {selected_mitre}")
    print("This may take a few moments...")
    print("=" * 80)
    
    # Perform LLM analysis
    analysis_result = analyze_technique_with_llm(selected_mitre)
    
    print("\n" + "🎯 LLM ANALYSIS RESULTS")
    print("=" * 100)
    print(analysis_result)
    print("=" * 100)
    
    # Show completion message
    print("\n✅ Analysis completed successfully!")
    print("💡 Review the recommendations above to improve your SPL query coverage.")
    
elif analysis_action == "Analyze" and (not selected_mitre or selected_mitre == ""):
    print("⚠️ Please select a MITRE technique before running analysis.")
    
elif analysis_action == "Clear":
    print("🧹 Dashboard cleared. Select a new technique to start fresh.")
    
else:
    if selected_mitre and selected_mitre != "":
        print("🚀 Ready for analysis!")
        print(f"Selected technique: {selected_mitre}")
        print("Set the Analysis Action to 'Analyze' to run LLM analysis.")
    else:
        print("👆 Select a MITRE technique and set action to 'Analyze' to see LLM analysis results here.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Dashboard Summary

# COMMAND ----------

# Display current dashboard state
print("📊 DASHBOARD STATUS")
print("=" * 50)
print(f"Selected Technique: {selected_mitre if selected_mitre else 'None'}")
print(f"Analysis Action: {analysis_action}")
print(f"Custom SPL: {'Yes' if custom_spl else 'No'}")

if selected_mitre:
    technique_data = get_technique_data(selected_mitre)
    if technique_data:
        print(f"Technique Name: {technique_data['technique_name']}")
        print(f"SPL Query Length: {len(technique_data['spl_query'])} characters")
        print("Status: ✅ Ready for analysis")
    else:
        print("Status: ❌ No data found")
else:
    print("Status: ⏳ Waiting for technique selection")

print("=" * 50)
