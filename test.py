# COMMAND ----------

# Dashboard Auto-Refresh for Analysis Results
selected_mitre = dbutils.widgets.get("mitre_technique")
analysis_action = dbutils.widgets.get("analyze_action")

if analysis_action == "Analyze" and selected_mitre and selected_mitre != "":
    
    # Show progress in dashboard-friendly way
    print("🤖 LLM Analysis in Progress...")
    print(f"Analyzing: {selected_mitre}")
    print("=" * 50)
    
    # Run analysis
    analysis_result = analyze_technique_with_llm(selected_mitre)
    
    # Display results in dashboard
    print("\n🎯 LLM ANALYSIS RESULTS")
    print("=" * 80)
    print(analysis_result)
    print("=" * 80)
    print("\n✅ Analysis Complete!")
    
    # Force widget refresh to show "Ready" state
    dbutils.widgets.remove("analyze_action")
    dbutils.widgets.dropdown("analyze_action", "Ready", 
                             ["Ready", "Analyze", "Clear"], 
                             "🚀 Analysis Action")
    
    # Create a results summary table for dashboard
    results_summary = [
        ("Technique", selected_mitre),
        ("Status", "Analysis Complete"),
        ("Result Length", f"{len(analysis_result)} characters"),
        ("Timestamp", str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    ]
    
    df_results = spark.createDataFrame(results_summary, ["Field", "Value"])
    display(df_results)

elif selected_mitre and selected_mitre != "":
    print(f"🚀 Ready to analyze: {selected_mitre}")
    print("Set Analysis Action to 'Analyze' to start")
else:
    print("👆 Select a MITRE technique first")
