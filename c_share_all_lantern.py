import pandas as pd
import altair as alt
import webbrowser
import re  # Import regular expression library

def generate_chart(file_path):
    match = re.search(r'c_share_lantern_(MB\d+)_', file_path)
    title_suffix = match.group(1) if match else 'Unknown'
    data = pd.read_excel(file_path, header=1)
    data = data.apply(pd.to_numeric, errors='coerce')

    # combine line (catch share rate) and circle (catch share points) for left axis
    left_axis_chart = alt.Chart(data).mark_line(color='black', clip=True).encode(
        x=alt.X('X1:Q', scale=alt.Scale(domain=[15, 85]), title='Length (mm)',
            axis=alt.Axis(values=[15, 25, 35, 45, 55, 65, 75, 85], grid=False, titleFontSize=20, labelFontSize=15)),
        y=alt.Y('Y1:Q', scale=alt.Scale(domain=[0, 1]), title='Catch share rate',
            axis=alt.Axis(values=[0, 0.25, 0.50, 0.75, 1.00], labelFontSize=15, titleFontSize=20, format='.2f', grid=False))
    ) + alt.Chart(data).mark_point(shape='circle', clip=True, filled=False, size=50, color='black').encode(
        x=alt.X('X0:Q', scale=alt.Scale(domain=[15, 85])),
        y='Y0:Q'
    )

    # combine dotted population struct (pop+test) with right y axis
    right_axis_chart = alt.Chart(data).mark_line(strokeDash=[5, 5], color='black', clip=True).encode(
        x='X2:Q',
        y=alt.Y('Y2:Q', scale=alt.Scale(domain=[0, 400]), title='Number captured',
            axis=alt.Axis(orient='right', labelFontSize=15, titleFontSize=20, grid=False, values=[0, 100, 200, 300, 400]))
    ) + alt.Chart(data).mark_line(strokeDash=[5, 5], color='darkgrey', clip=True).encode(
        x='X2:Q',
        y=alt.Y('Y3:Q', scale=alt.Scale(domain=[0, 400]))
    )

    # specify right y axis for combined pop 
    right_axis_chart = right_axis_chart.encode(
        y=alt.Y('Y2:Q', axis=alt.Axis(orient='right', grid=False))
    )

    # combine all charts
    final_chart = alt.layer(left_axis_chart, right_axis_chart).resolve_scale(
        y='independent'
    ).properties(
        width=400, height=250, title= title_suffix
    ).configure_title(fontSize=30)
    
    chart_file = f"{file_path.split('.')[0]}.html"
    final_chart.save(chart_file)
    webbrowser.open(chart_file)

# List of file paths
file_paths = [
    r'C:\Users\eko067\Desktop\My Paper - Presentation etc\Paper\meso_sel_study\DATA\sup files\plot_data\c_share\c_share_lantern_MB14_21.xlsx',
    r'C:\Users\eko067\Desktop\My Paper - Presentation etc\Paper\meso_sel_study\DATA\sup files\plot_data\c_share\c_share_lantern_MB20_21.xlsx',
    r'C:\Users\eko067\Desktop\My Paper - Presentation etc\Paper\meso_sel_study\DATA\sup files\plot_data\c_share\c_share_lantern_MB30_21.xlsx',
]

# Generate charts for each file path
for path in file_paths:
    generate_chart(path)
