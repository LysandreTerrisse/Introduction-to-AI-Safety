import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


def ordinary_least_squares(x, y, precision=2):
    x_mean, y_mean = sum(x)/len(x), sum(y)/len(y)
    
    beta_1 = sum((x[i] - x_mean)*(y[i] - y_mean) for i in range(len(x))) / sum((x[i] - x_mean)**2 for i in range(len(x)))
    beta_0 = y_mean - beta_1 * x_mean
    
    return round(beta_0, precision), round(beta_1, precision)

#https://factsonclimate.org/infographics/concentration-warming-relationship
#https://docs.google.com/spreadsheets/d/1aVn3Uz1wLUtmATagtZHEpeayiee6uy_BRAivZPwfb2s/edit?gid=469212572
df = pd.read_csv('https://docs.google.com/spreadsheets/d/1aVn3Uz1wLUtmATagtZHEpeayiee6uy_BRAivZPwfb2s/export?gid=1318999242&format=csv')
df.drop(df.columns[0], axis=1, inplace=True)
df.set_axis(["CO2 concentration (ppm)", "Global warming relative to 1800-1900 (°C)"], axis=1, inplace=True)
x, y = df[df.columns[0]], df[df.columns[1]]

beta_0, beta_1 = ordinary_least_squares(x, y)
print(beta_0, beta_1)

extension = "pgf"

if extension!="png":
    mpl.use(extension)

mpl.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

"""Create picture of climate change"""
plt.plot(x, y, "o")
plt.xlabel(df.columns[0])
plt.ylabel(df.columns[1])
plt.savefig('climate_change.' + extension)

"""Create picture of climate change with a line through the points"""
plt.plot([min(x), max(x)], [beta_0 + beta_1 * min(x), beta_0 + beta_1 * max(x)], "k")
plt.savefig('OLS_climate_change.' + extension)

"""Create picture of climate change with a line through the points and the residuals in red"""
for i in range(len(x)):
    plt.plot([x[i], x[i]], [y[i], beta_0 + beta_1 * x[i]], "r")
plt.savefig('OLS_climate_change_with_residuals.' + extension)