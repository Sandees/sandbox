def display_formatted_spl_query(query, title="SPL Query"):
    """Display an SPL query with proper pipe formatting"""
    if not query:
        return
    
    # Format the query
    import re
    clean_query = re.sub(r'\s+', ' ', query.strip())
    parts = clean_query.split('|')
    
    formatted = ''
    for i, part in enumerate(parts):
        trimmed_part = part.strip()
        if i == 0:
            formatted += trimmed_part
        elif trimmed_part:
            formatted += '\n| ' + trimmed_part
    
    # Display with proper styling
    displayHTML(f"""
    <div style="margin: 20px 0;">
        <h4 style="color: #2c3e50; margin-bottom: 10px; border-bottom: 2px solid #3498db; padding-bottom: 5px;">
            📊 {title}
        </h4>
        <div style="
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-y: auto;
            max-height: 300px;
            border: 1px solid #4a5568;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
{formatted}
        </div>
    </div>
    """)



# NEW CODE - Use this instead
display_formatted_spl_query(technique_data['spl_query'], "SPL Query")


# NEW CODE - Use this instead
display_formatted_spl_query(technique_data['drill_down_spl'], "Drill-Down SPL Query")
