import plotly.graph_objects as go
import numpy as np

# Function to compute the start and end angles of the segments for each digit
def get_digit_angles(digit, total_digits=10, offset=0):
    digit_angle = 360 / total_digits
    start_angle = (digit * digit_angle + offset) % 360
    end_angle = ((digit + 1) * digit_angle + offset) % 360
    return start_angle, end_angle

# Function to compute the position on the circle given an angle
def get_position_on_circle(angle, radius=1):
    radian_angle = np.radians(angle)
    x = radius * np.cos(radian_angle)
    y = radius * np.sin(radian_angle)
    return x, y

# Function to interpolate between two colors
# def interpolate_colors(color1, color2, t):
#     return tuple((np.array(color1) * (1 - t) + np.array(color2) * t).astype(int))

# Define the base colors for each digit segment
base_colors = [
    (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0),
    (0, 0, 255), (75, 0, 130), (238, 130, 238), (255, 192, 203),
    (255, 69, 0), (127, 255, 212)
]
# 计算π的数字
def compute_pi_digits(digits):
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    decimal = 0
    counter = 0
    pi_digits = ""
    while counter < digits:
        if 4 * q + r - t < n * t:
            pi_digits += str(n)
            if counter == 0:
                pi_digits += "."
            counter += 1
            nr = 10 * (r - n * t)
            n = ((10 * (3 * q + r)) // t) - 10 * n
            q *= 10
            r = nr
        else:
            nr = (2 * q + r) * l
            nn = (q * (7 * k + 2) + r * l) // (t * l)
            q *= k
            t *= l
            l += 2
            k += 1
            n = nn
            r = nr
    return pi_digits
# Function to interpolate between two colors, with clamping between 0 and 255
def interpolate_colors(color1, color2, t):
    # Clamp the result between 0 and 255
    return tuple(min(255, max(0, int((1 - t) * c1 + t * c2))) for c1, c2 in zip(color1, color2))

# The rest of the code would remain the same...

# 生成π的1000个数字
pi_digits = compute_pi_digits(10000)
# Initialize figure
fig = go.Figure()

# Compute the digits of Pi (here we use a constant for simplicity)
# pi_digits = '3141592653589793238462643383279502884197169399375105820974944592'  # Extend this string as needed

# We will use a counter to evenly distribute the start and end points on the segment
counter = np.zeros(10, dtype=int)
control_point_radius = 2
# Plot the links between successive digits
for i in range(len(pi_digits) - 1):
    if pi_digits[i] == '.' or pi_digits[i + 1] == '.':
        continue

    digit_from = int(pi_digits[i])
    digit_to = int(pi_digits[i + 1])

    # Get the angles for the starting and ending segments
    start_angle_from, end_angle_from = get_digit_angles(digit_from)
    start_angle_to, end_angle_to = get_digit_angles(digit_to)

    # Calculate the angle offset based on the counter for the digits
    angle_from = start_angle_from + (end_angle_from - start_angle_from) * counter[digit_from] / 1000
    angle_to = start_angle_to + (end_angle_to - start_angle_to) * counter[digit_to] / 1000

    # Increment the counters for the digits
    counter[digit_from] += 1
    counter[digit_to] += 1

    # Get the positions on the circle
    x_from, y_from = get_position_on_circle(angle_from)
    x_to, y_to = get_position_on_circle(angle_to)

    # Interpolate the color for the link based on its position within the segment
    color_from = interpolate_colors(base_colors[digit_from], base_colors[(digit_from + 1) % 10], counter[digit_from] / 1000)
    color_to = interpolate_colors(base_colors[digit_to], base_colors[(digit_to + 1) % 10], counter[digit_to] / 1000)

    # Add a line trace for the link with gradient color
    # fig.add_trace(go.Scatter(x=[x_from, x_to], y=[y_from, y_to], mode='lines',
    #                          line=dict(color='rgba({}, {}, {}, {})'.format(*color_from, 0.5), width=1)))
    mid_angle = (angle_from + angle_to) / 2
    ctrl_x, ctrl_y = get_position_on_circle(mid_angle, control_point_radius)

    # 创建曲线路径
    path = f'M{x_from},{y_from} Q{ctrl_x},{ctrl_y} {x_to},{y_to}'

    # 在 figure 中添加曲线
    fig.add_trace(go.Scatter(
        x=[x_from, ctrl_x, x_to],
        y=[y_from, ctrl_y, y_to],
        mode='lines',
        line=dict(color='rgba({}, {}, {}, {})'.format(*color_from, 0.5), width=1),
        hoverinfo='none',
        line_shape='spline'  # 设置为 'spline' 使线条平滑
    ))
# Update layout to have a circular look
fig.update_layout(
    autosize=False,
    width=2000,
    height=2000,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        visible=False,
        scaleanchor="y",  # this enforces the aspect ratio
        scaleratio=1,
        range=[-1.2, 1.2]  # setting the same range for x and y
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        visible=False,
        range=[-1.2, 1.2]  # setting the same range for x and y
    )
)

# Update the figure to have equal axis and a circle shape
fig.update_shapes(
    # This adds a circle shape to the layout to reinforce the circular aspect of the plot
    [dict(
        type="circle",
        xref="x", yref="y",
        x0=-1, y0=-1, x1=1, y1=1,
        # line_color="black",
    )]
)

# Update the figure to have equal axis and a circle shape
fig.update_layout(hovermode=False,showlegend=False,plot_bgcolor='white',shapes=[

    go.layout.Shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-1,
        y0=-1,
        x1=1,
        y1=1,
        # line_color="black",
    )
])

# Note: To display the figure, run this script in a local environment with Plotly installed
fig.show()  # Uncomment this line when running locally
