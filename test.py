# COMMAND ----------

# MANUAL ANALYSIS TRIGGER - Run this cell to analyze
selected_mitre = dbutils.widgets.get("mitre_technique")

if selected_mitre and selected_mitre != "":
    print(f"🤖 MANUAL ANALYSIS FOR: {selected_mitre}")
    print("="*80)
    
    # Get technique data
    technique_data = get_technique_data(selected_mitre)
    
    if technique_data:
        print(f"Technique: {technique_data['technique_name']}")
        print(f"SPL Query: {technique_data['spl_query'][:100]}...")
        print("="*80)
        
        # Run analysis
        analysis_result = analyze_technique_with_llm(selected_mitre)
        
        print("\n🎯 ANALYSIS RESULTS:")
        print("="*100)
        print(analysis_result)
        print("="*100)
        
        # Show completion
        displayHTML(f"""
        <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h2>🎯 Analysis Complete for {selected_mitre}</h2>
            <p>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """)
        
    else:
        print("❌ No technique data found")
else:
    print("❌ Please select a MITRE technique first")
