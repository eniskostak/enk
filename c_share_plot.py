import pandas as pd
import altair as alt

# Load data
file_path = r'C:\Users\eko067\Desktop\My Paper - Presentation etc\Paper\meso_sel_study\DATA\sup files\plot_data\c_share\C_Share_lantern_14_ext_21.xlsx'
data = pd.read_excel(file_path, header=1)
data = data.apply(pd.to_numeric, errors='coerce')


# combine line (catch share rate) and circle (catch share points) for left axis

left_axis_chart = alt.Chart(data).mark_line(color='black',                  # color line
                                            clip = True).encode(            # clip and fit the line   
    # X AXIS - split line                            
    x=alt.X('X1:Q',                                                         # X axis data column
            scale=alt.Scale(domain=[15, 85]),                               # data range axis
            title='Length (mm)',                                            # title (x-axis)
            axis=alt.Axis(values=[15, 25, 35, 45, 55, 65, 75, 85],          # values (x-axis))
                          grid = False,                                     
                          titleFontSize=20,                                 # title font size
                          labelFontSize=15)),                               # label font size
    # Y AXIS (left 1) - catch share rate
    y=alt.Y('Y1:Q',                                                         # column
            scale=alt.Scale(domain=[0, 1]),                                 # range
            title='Catch share rate',                                       # title (left y-axis)
            axis=alt.Axis(values=[0, 0.25, 0.50, 0.75, 1.00],               # values
                          labelFontSize=15,                                 # label font size
                          titleFontSize=20,                                 # title font size
                          format='.2f',                                     # 2decimal
                          grid = False))                                    # vertical guideline
    # Y AXIS (left 2) - catch share points
) + alt.Chart(data).mark_point(shape='circle',                              # shape, size, color etc.
                               filled=False,                
                               size=50, 
                               color='black').encode(
    x=alt.X('X0:Q',                                                         # column x
            scale=alt.Scale(domain=[15, 85])),                              # range
    y='Y0:Q'
)                                                                           # column y

# combine dotted population struct (pop+test) with right y axis

right_axis_chart = alt.Chart(data).mark_line(strokeDash=[5, 5],             # size distribution (control)
                                             color='black').encode(
    x='X2:Q',                                                               
    y=alt.Y('Y2:Q', 
            scale=alt.Scale(domain=[0, 300]),                               # range
            title='Number captured',                                        # title name
            axis=alt.Axis(orient='right', 
                          labelFontSize=15,                                 #label size
                          titleFontSize=20,                                 # title size
                          grid = False, 
                          values=[0, 100, 200, 300]))                       # label values (right y-axis)
) + alt.Chart(data).mark_line(strokeDash=[5, 5],                            # size distribution (test)
                              color='darkgrey').encode(
    x='X2:Q',
    y=alt.Y('Y3:Q', 
            scale=alt.Scale(domain=[0, 300]))
)

# specify right y axis for combined pop 
right_axis_chart = right_axis_chart.encode(
    y=alt.Y('Y2:Q', 
            axis=alt.Axis(orient='right', 
                          grid = False,))
)

# combine all charts
final_chart = alt.layer(left_axis_chart, right_axis_chart).resolve_scale(
    y='independent'
).properties(
    width=400,                                                              # plot size
    height=250,
    title='MB14',                                                           # plot title
)
final_chart = final_chart.configure_title(fontSize=30)                      # plot title font size
# Show the chart
final_chart.save('chart.html')
import webbrowser
webbrowser.open('chart.html')

