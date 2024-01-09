
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec as gsp
import matplotlib.pyplot as plt


def read_data(file_path):
    # Read data from CSV file
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        # Return the entire data
        return list(csv_reader)
    

def create_line_plot(data, indicator_to_plot, start_year, end_year, countries_to_plot, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots()

    # Create a dictionary to store data for each country
    country_data = {country: {'years': [], 'data': []} for country in countries_to_plot}

    # Extract years and data for the chosen indicator within the specified range
    for row in data:
        if row['Indicator Name'] == indicator_to_plot and start_year <= int(row['Year']) <= end_year:
            for country in countries_to_plot:
                country_data[country]['years'].append(int(row['Year']))
                # Assuming the column for the country is the same as the country name
                data_value = float(row[country])
                country_data[country]['data'].append(data_value)

                # Print statement to display the data used for plotting

    # Plot the data for each country
    for country in countries_to_plot:
        ax.plot(country_data[country]['years'], country_data[country]['data'], label=country)

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')
    ax.set_title('Line Plot for {}'.format(indicator_to_plot))

    # Add legend
    ax.legend()

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax

def create_donut_chart(data, indicator_to_plot, year, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots()

    # Create a dictionary to store data for each country
    country_data = {}

    # Extract data for the chosen indicator and year
    for row in data:
        if row['Indicator Name'] == indicator_to_plot and int(row['Year']) == year:
            for country in row.keys():
                if country != 'Year' and country != 'Indicator Name':
                    country_data[country] = float(row[country])

    # Print statement to display the data used for plotting

    # Define colors for each slice of the pie chart
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red']

    # Extract values and labels from the dictionary
    labels = list(country_data.keys())
    values = list(country_data.values())

    # Plot the data as a donut chart with customized wedge properties
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
           wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2))  # Adjust width, edge color, and linewidth

    # Add a circle at the center to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.6, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that the pie chart is circular
    ax.axis('equal')

    # Add title
    ax.set_title('Donut Chart for {} in {}'.format(indicator_to_plot, year))

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax

def create_stacked_area_plot(data, indicator_to_plot, start_year, end_year, countries_to_plot, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    # Filter data for the chosen indicator and years
    filtered_data = [row for row in data if row['Indicator Name'] == indicator_to_plot and start_year <= int(row['Year']) <= end_year]

    # Create a dictionary to store data for each source
    sources_data = {source: {'years': [], 'data': []} for source in data[0].keys() if source not in ['Year', 'Indicator Name'] and source in countries_to_plot}

    # Extract years and data for each source
    for row in filtered_data:
        for source in sources_data.keys():
            sources_data[source]['years'].append(int(row['Year']))
            sources_data[source]['data'].append(float(row[source]))

    # Create a list of years
    years = list(set(year for source_data in sources_data.values() for year in source_data['years']))

    # Plot the data as a stacked area plot
    ax.stackplot(years,
                 *[sources_data[c]['data'] for c in countries_to_plot],
                 labels=countries_to_plot)

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage of Total')
    ax.set_title(f'Stacked Area Plot for {indicator_to_plot} ({start_year} to {end_year})')

    # Add legend
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax

    
def create_bar_plot(data, indicator_to_plot, selected_years, countries_to_plot, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots()

    # Create a dictionary to store data for each country and year
    country_year_data = {country: {year: [] for year in selected_years} for country in countries_to_plot}

    # Extract data for the chosen indicator and years
    for row in data:
        if row['Indicator Name'] == indicator_to_plot and int(row['Year']) in selected_years:
            year = int(row['Year'])
            for country in countries_to_plot:
                country_year_data[country][year].append(float(row[country]))

    # Plot the data as a grouped bar chart
    bar_width = 0.2  # Adjust the width of the bars

    # Define the positions for each group of bars
    positions = np.arange(len(countries_to_plot)) + 0.5 * (len(selected_years) - 1) * bar_width

    for i, year in enumerate(selected_years):
        # Adjust the positions for each year
        year_positions = positions - 0.5 * (len(selected_years) - 1 - i) * bar_width
        values = np.array([country_year_data[country][year] for country in countries_to_plot])
        ax.bar(year_positions, np.sum(values, axis=1), width=bar_width, label=str(year))

    # Add labels and title
    ax.set_xlabel('Country')
    ax.set_ylabel('Value')
    ax.set_title('Grouped Bar Plot for {} (Selected Years)'.format(indicator_to_plot))

    # Set x-axis ticks and labels
    ax.set_xticks(positions)
    ax.set_xticklabels(countries_to_plot)

    # Add legend
    ax.legend(title='Year')

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax


def create_dashboard(data, indicator_to_plot_line, start_year_line, end_year_line, countries_to_plot_line,
                      indicator_to_plot_donut, year_donut,
                      indicator_to_plot_bar, selected_years_bar, countries_to_plot_bar,
                      indicator_to_plot_area, start_year_area, end_year_area, countries_to_plot_area):
    # set the size for dashboard visualization

    fig = plt.figure(figsize=(20, 20), facecolor='lightgray')  # Set facecolor to light gray
    fig.text(0.5, 0.9, "Name: Swethadevi Ravipati     StudentId: 22082165",
             ha="center", fontweight='bold', fontsize=15)

    # set grid size rows and columns to 2x2
    gs = gsp(2, 2, hspace=0.4, wspace=0.4)

    # set first grid point - Line Plot
    ax1 = fig.add_subplot(gs[0, 0])
    create_line_plot(data, indicator_to_plot_line, start_year_line, end_year_line, countries_to_plot_line, ax=ax1)
    ax1.set_title('Line Plot')
    ax1.text(0.5, -0.18,"""From 2000 to 2010, the United States, China, India, Brazil, and Germany 
             experienced significant growth in renewable energy production. 
             The U.S. increased from 1.92% to 4.10%, China surged from 0.23% to 1.67%,
             India rose from 0.52% to 3.48%, Brazil climbed from 2.25% to 6.53%, and Germany soared from 2.40% to 13.38%""",
             size=10, ha="center", fontweight='bold', transform=ax1.transAxes)
    ax1.set_xlabel('')
    ax1.set_ylabel('')

    # set second grid point - Donut Chart
    ax2 = fig.add_subplot(gs[0, 1])
    create_donut_chart(data, indicator_to_plot_donut, year_donut, ax=ax2)
    ax2.set_title('Donut Chart')
    ax2.text(0.5, -0.18, """       Electricity production from hydroelectric sources (% of total) in the 2005 , Brazil has the highest value (42.3%),
                              and uk has the lowest (0.6%). """,
             size=10, ha="center", fontweight='bold', transform=ax2.transAxes)
    ax2.set_xlabel('')
    ax2.set_ylabel('')

    # set third grid point - Grouped Bar Plot
    ax3 = fig.add_subplot(gs[1, 0])
    create_bar_plot(data, indicator_to_plot_bar, selected_years_bar, countries_to_plot_bar, ax=ax3)
    ax3.set_title('Grouped Bar Plot')
    ax3.text(0.5, -0.25, """ the years 2002, 2004, 2006, 2008, and 2010. Brazil consistently leads in hydroelectric production, 
                             ranging from 78.2% to 83.2%, while the United States shows a slight decrease from 6.6% to 6.0%. 
                             China and India maintain relatively stable percentages, with Germany contributing the least at around 3.3%.""",
             size=10, ha="center", fontweight='bold', transform=ax3.transAxes)
    ax3.set_xlabel('')
    ax3.set_ylabel('')

    # set fourth grid point - Stacked Area Plot
    ax4 = fig.add_subplot(gs[1, 1])
    create_stacked_area_plot(data, indicator_to_plot_area, start_year_area, end_year_area, countries_to_plot_area, ax=ax4)
    ax4.set_title('Stacked Area Plot')
    ax4.text(0.5, -0.25, """the evolution of coal's share in electricity production (2000-2010) for the United States (52.9% to 45.8%), 
                            China (fluctuating, ending at 80.3%), India (fluctuating, around 67.2%), Brazil (maintaining around 2.2%), 
                            and Germany (consistently decreasing to 43.6%).""",
             size=10, ha="center", fontweight='bold', transform=ax4.transAxes)
    ax4.set_xlabel('')
    ax4.set_ylabel('')

    # Conclusion Statement
    # Conclusion Statement
    conclusion_text = """
\n\n In summary, From 2000 to 2010, the Line Plot illustrates substantial growth in renewable energy production for the United States,
 China, India, Brazil, and Germany. The Donut Chart emphasizes Brazil's dominance in hydroelectric production (42.3%), while 
 the Grouped Bar Plot highlights Brazil consistently leading (78.2% to 83.2%).
 The Stacked Area Plot shows shifts in coal's share, with the United States decreasing (52.9% to 45.8%)
 and China fluctuating (ending at 80.3%). These visualizations capture the evolving energy landscape among these nations
"""


    # Conclusion Text Box
    conclusion_box = fig.add_axes([0.1, 0.05, 0.8, 0.1], frameon=False, facecolor='lightgray')  # Set facecolor for the text box
    conclusion_box.get_xaxis().set_visible(False)
    conclusion_box.get_yaxis().set_visible(False)
    conclusion_box.text(0.3, 0, conclusion_text, size=12, ha="left", va="top", fontweight='bold', wrap=True)
    
    # Super Title
    fig.suptitle('Decade in Power: Visualizing Trends in Global Energy Production (2000-2010) Dashboard',
                 fontweight='bold', fontsize=20)

    # Save and show the visualization
    plt.savefig("22082165.png", dpi=300)
    plt.show()


def main():
    file_path = r"C:\Users\ACER\Desktop\ADS-3\uday\filtered_data.csv"
    indicator_to_plot_line = 'Electricity production from renewable sources, excluding hydroelectric (% of total)'
    start_year_line = 2000
    end_year_line = 2010
    countries = ['United States', 'China', 'India', 'Brazil', 'Germany']

    indicator_to_plot_donut = 'Electricity production from hydroelectric sources (% of total)'
    year_donut = 2005

    indicator_to_plot_bar = 'Electricity production from hydroelectric sources (% of total)'
    selected_years_bar = [2002, 2004, 2006, 2008, 2010]

    indicator_to_plot_area = 'Electricity production from coal sources (% of total)'
    start_year_area = 2000
    end_year_area = 2010

    # Read data from CSV file
    data = read_data(file_path)

    # Create individual plots
    create_line_plot(data, indicator_to_plot_line, start_year_line, end_year_line, countries)
    create_donut_chart(data, indicator_to_plot_donut, year_donut)
    create_bar_plot(data, indicator_to_plot_bar, selected_years_bar, countries)
    create_stacked_area_plot(data, indicator_to_plot_area, start_year_area, end_year_area, countries)

    # Create the dashboard
    create_dashboard(data, indicator_to_plot_line, start_year_line, end_year_line, countries,
                      indicator_to_plot_donut, year_donut,
                      indicator_to_plot_bar, selected_years_bar, countries,
                      indicator_to_plot_area, start_year_area, end_year_area, countries)


if __name__ == "__main__":
    main()

